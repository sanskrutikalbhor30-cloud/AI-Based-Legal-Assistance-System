import os
import re
import json
import sqlite3
import time

import requests
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from legal_data import (
    KNOWLEDGE_BASE,
    DISCLAIMER,
    GREETING_RESPONSE,
    THANKS_RESPONSE,
    DEFAULT_RESPONSE,
    GREETING_KEYWORDS,
    THANKS_KEYWORDS,
)


APP_VERSION = "v8-json-gemini"

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "legal_assistance_secret_key"
)

DATABASE = "legal_assistance.db"


# =====================================================================
# GEMINI API CONFIGURATION
# =====================================================================

# DO NOT put your Gemini API key directly in this file.
#
# Windows PowerShell:
#
# $env:GEMINI_API_KEY="YOUR_NEW_API_KEY"
#
# Then run:
#
# py app.py

GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY",
    "YOUR_GEMINI_API_KEY_HERE"
).strip()


# Model to use first
GEMINI_MODEL = os.environ.get(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


# Fallback models
GEMINI_FALLBACK_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/{model}:generateContent"
)


# Maximum time for one HTTP request
GEMINI_TIMEOUT = 12

MAX_QUESTION_LENGTH = 1000


# =====================================================================
# SYSTEM PROMPT
# =====================================================================

SYSTEM_PROMPT = """
You are "AI Legal Assistance", a helpful legal information assistant
for people in India.

Your job:

- Answer questions about Indian law clearly and accurately in simple,
  plain English.
- If the user writes in Hindi or Marathi, reply in the language the
  user uses when appropriate.
- Cover family, property, tenancy, consumer, cyber crime, criminal
  procedure, employment, civil disputes, RTI, contracts, business,
  and other everyday legal matters.
- Refer to current Indian laws where relevant.
- The new criminal laws effective from 1 July 2024 include:
  Bharatiya Nyaya Sanhita 2023,
  Bharatiya Nagarik Suraksha Sanhita 2023,
  Bharatiya Sakshya Adhiniyam 2023.
- Mention older IPC/CrPC names in brackets when useful.
- Give practical step-by-step guidance.
- Mention useful documents to keep.
- Mention the relevant authority, forum or portal where appropriate.
- For urgent situations, put safety steps first.
- If important facts are missing, give a useful general answer first
  and explain what additional information would change the answer.
- Never invent section numbers, case names or statistics.
- If uncertain, say so and recommend verifying with a qualified lawyer
  or official source.
- Do not help with crimes, evading law enforcement, document forgery,
  or harassment.
- If the question is unrelated to law, politely say that you can only
  help with legal questions.

ANSWER FORMAT:

Return ONLY one valid JSON object.

The JSON MUST have exactly this structure:

{
    "answer": "Your complete legal answer here"
}

IMPORTANT JSON RULES:

- Return ONLY valid JSON.
- Do NOT return markdown code fences.
- Do NOT return ```json.
- Do NOT put any text before the JSON.
- Do NOT put any text after the JSON.
- Do NOT add any additional JSON fields.
- The "answer" field must always be a string.
- Escape quotation marks inside the answer correctly.
- Markdown such as **bold** and bullet points may be used INSIDE
  the answer string.
- Keep answers focused, normally around 120-300 words unless the
  question genuinely requires more detail.
- End the answer with one short line reminding the user that this is
  general legal information and not a substitute for a qualified lawyer.
"""


# =====================================================================
# DATABASE CONNECTION
# =====================================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================================
# USERS TABLE
# =====================================================================

def create_users_table():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =====================================================================
# CHAT HISTORY TABLE
# =====================================================================

def create_chat_table():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create tables
create_users_table()
create_chat_table()


# =====================================================================
# AI ANSWER LOGIC
# =====================================================================

def gemini_is_configured():

    key = (GEMINI_API_KEY or "").strip()

    return (
        bool(key)
        and key != "YOUR_GEMINI_API_KEY_HERE"
    )


# =====================================================================
# RECENT CHAT HISTORY
# =====================================================================

def get_recent_history(user_id, limit=4):

    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT question, response
        FROM chat_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()

    conn.close()

    return list(reversed(rows))


# =====================================================================
# GEMINI ENDPOINTS
# =====================================================================

def _gemini_endpoints(model):

    key = GEMINI_API_KEY.strip()

    endpoints = [
        (
            GEMINI_URL.format(model=model),
            {
                "Content-Type": "application/json",
                "x-goog-api-key": key
            },
            {}
        )
    ]

    return endpoints


# =====================================================================
# GOOGLE ERROR MESSAGE
# =====================================================================

def _google_error_message(response):

    try:

        data = response.json()

        return (
            data
            .get("error", {})
            .get("message", "")
        )[:260]

    except Exception:

        return response.text[:260]


# =====================================================================
# RETRY CONFIGURATION
# =====================================================================

RETRY_STATUS = (
    500,
    502,
    503,
    504
)

MAX_MODEL_ATTEMPTS = 2

RETRY_DELAYS = (
    1.5,
    0.0
)


# =====================================================================
# SINGLE GEMINI REQUEST
# =====================================================================

def _call_gemini_once(
    url,
    headers,
    params,
    payload,
    model
):

    last_error = "api_error"
    last_detail = ""

    for attempt in range(MAX_MODEL_ATTEMPTS):

        try:

            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=GEMINI_TIMEOUT
            )

        except requests.exceptions.Timeout:

            print(
                f"Gemini API timeout "
                f"({model}); moving to next model"
            )

            # Do NOT retry timeout.
            return (
                None,
                "timeout",
                "request timed out"
            )

        except requests.exceptions.RequestException as e:

            print(
                f"Gemini API network error "
                f"({model}): "
                f"{type(e).__name__}"
            )

            last_error = "network"
            last_detail = type(e).__name__

            if attempt + 1 < MAX_MODEL_ATTEMPTS:

                time.sleep(
                    RETRY_DELAYS[attempt]
                )

                continue

            return (
                None,
                last_error,
                last_detail
            )

        # =============================================================
        # SUCCESS
        # =============================================================

        if response.status_code == 200:

            return (
                response,
                None,
                ""
            )

        # =============================================================
        # ERROR
        # =============================================================

        message = _google_error_message(
            response
        )

        print(
            f"Gemini API Error "
            f"({model}, attempt "
            f"{attempt + 1}/"
            f"{MAX_MODEL_ATTEMPTS}): "
            f"{response.status_code} "
            f"{message}"
        )

        last_detail = (
            f"HTTP {response.status_code}: "
            f"{message}"
        )

        lowered = message.lower()

        # =============================================================
        # TEMPORARY GOOGLE SERVER ERROR
        # =============================================================

        if response.status_code in RETRY_STATUS:

            last_error = "overloaded"

            if attempt + 1 < MAX_MODEL_ATTEMPTS:

                time.sleep(
                    RETRY_DELAYS[attempt]
                )

                continue

        # =============================================================
        # API DISABLED
        # =============================================================

        elif response.status_code == 403 and (
            "has not been used" in lowered
            or "is disabled" in lowered
        ):

            last_error = "api_disabled"

        # =============================================================
        # INVALID API KEY
        # =============================================================

        elif response.status_code in (
            400,
            401,
            403
        ):

            last_error = "invalid_key"

        # =============================================================
        # MODEL NOT FOUND
        # =============================================================

        elif response.status_code == 404:

            last_error = "model_not_found"

            last_detail = (
                f"{model} - {message}"
            )

        # =============================================================
        # RATE LIMIT
        # =============================================================

        elif response.status_code == 429:

            last_error = "rate_limited"

        # =============================================================
        # OTHER ERROR
        # =============================================================

        else:

            last_error = "api_error"

        break

    return (
        None,
        last_error,
        last_detail
    )


# =====================================================================
# GEMINI RESPONSE JSON PARSER
# =====================================================================

def parse_gemini_response(response, model):

    try:

        data = response.json()

    except ValueError:

        return (
            None,
            "invalid_response",
            "Gemini returned invalid HTTP JSON."
        )

    try:

        candidates = data.get(
            "candidates"
        ) or []

        if not candidates:

            return (
                None,
                "blocked",
                str(
                    data.get(
                        "promptFeedback",
                        ""
                    )
                )[:200]
            )

        candidate = candidates[0]

        parts = (
            candidate
            .get("content", {})
            .get("parts", [])
        )

        text = "".join(
            part.get("text", "")
            for part in parts
            if isinstance(part, dict)
        ).strip()

        if not text:

            return (
                None,
                "empty",
                str(
                    candidate.get(
                        "finishReason",
                        ""
                    )
                )
            )

        # =============================================================
        # PARSE JSON
        # =============================================================

        try:

            parsed = json.loads(text)

        except json.JSONDecodeError as e:

            print(
                f"Gemini returned invalid JSON "
                f"({model}): {e}"
            )

            return (
                None,
                "invalid_json",
                text[:300]
            )

        # =============================================================
        # VALIDATE JSON OBJECT
        # =============================================================

        if not isinstance(parsed, dict):

            return (
                None,
                "invalid_json",
                "Response is not a JSON object."
            )

        # =============================================================
        # VALIDATE answer FIELD
        # =============================================================

        answer = parsed.get(
            "answer"
        )

        if not isinstance(
            answer,
            str
        ):

            return (
                None,
                "invalid_json",
                'Missing string field "answer".'
            )

        answer = answer.strip()

        if not answer:

            return (
                None,
                "empty",
                "Empty answer field."
            )

        # =============================================================
        # SUCCESS
        # =============================================================

        return (
            answer,
            None,
            ""
        )

    except Exception as e:

        print(
            "Gemini response parsing error:",
            type(e).__name__
        )

        return (
            None,
            "invalid_response",
            str(e)
        )


# =====================================================================
# ASK GEMINI
# =====================================================================

def ask_gemini(
    question,
    history=None
):

    if not gemini_is_configured():

        return (
            None,
            "not_configured",
            ""
        )

    # ================================================================
    # BUILD CONVERSATION
    # ================================================================

    contents = []

    for row in history or []:

        contents.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": row["question"][:500]
                    }
                ]
            }
        )

        contents.append(
            {
                "role": "model",
                "parts": [
                    {
                        "text": json.dumps(
                            {
                                "answer":
                                    row["response"][:1200]
                            },
                            ensure_ascii=False
                        )
                    }
                ]
            }
        )

    contents.append(
        {
            "role": "user",
            "parts": [
                {
                    "text": question
                }
            ]
        }
    )

    # ================================================================
    # GEMINI PAYLOAD
    # ================================================================

    payload = {

        "system_instruction": {
            "parts": [
                {
                    "text": SYSTEM_PROMPT
                }
            ]
        },

        "contents": contents,

        "generationConfig": {

            # ========================================================
            # FORCE JSON RESPONSE
            # ========================================================

            "responseMimeType": "application/json",

            "responseSchema": {
                "type": "OBJECT",

                "properties": {

                    "answer": {
                        "type": "STRING"
                    }

                },

                "required": [
                    "answer"
                ]
            },

            "maxOutputTokens": 2048
        }
    }

    # ================================================================
    # MODEL LIST
    # ================================================================

    models = [
        GEMINI_MODEL
    ]

    for model in GEMINI_FALLBACK_MODELS:

        if model not in models:

            models.append(model)

    last_error = "api_error"
    last_detail = ""

    # ================================================================
    # TRY EACH MODEL
    # ================================================================

    for model in models:

        print(
            f"Trying Gemini model: {model}"
        )

        model_failed = False

        for (
            url,
            headers,
            params
        ) in _gemini_endpoints(model):

            response, error, detail = (
                _call_gemini_once(
                    url,
                    headers,
                    params,
                    payload,
                    model
                )
            )

            last_error = error
            last_detail = detail

            # ========================================================
            # HTTP SUCCESS
            # ========================================================

            if response is not None:

                answer, parse_error, parse_detail = (
                    parse_gemini_response(
                        response,
                        model
                    )
                )

                if answer is not None:

                    print(
                        f"Gemini success using "
                        f"model: {model}"
                    )

                    return (
                        answer,
                        None,
                        ""
                    )

                print(
                    f"Gemini response problem "
                    f"({model}): "
                    f"{parse_detail}"
                )

                last_error = parse_error
                last_detail = parse_detail

                model_failed = True

                break

            # ========================================================
            # API KEY ERROR
            # ========================================================

            if error in (
                "invalid_key",
                "api_disabled"
            ):

                model_failed = True
                break

            # ========================================================
            # OTHER ERROR
            # ========================================================

            model_failed = True
            break

        print(
            f"Gemini model {model} unavailable "
            f"({last_error}); "
            f"trying next model if available."
        )

        # Continue to next model

    # ================================================================
    # ALL MODELS FAILED
    # ================================================================

    return (
        None,
        last_error,
        last_detail
    )


# =====================================================================
# RULE-BASED LEGAL SYSTEM
# =====================================================================

def _keyword_in(
    text,
    keyword
):

    return re.search(
        r"(?<![a-z0-9])"
        + re.escape(keyword)
        + r"(?![a-z0-9])",
        text
    ) is not None


def get_predefined_answer(question):

    text = re.sub(
        r"\s+",
        " ",
        question.lower()
    ).strip()

    # ================================================================
    # GREETING / THANKS
    # ================================================================

    if len(text.split()) <= 4:

        stripped = re.sub(
            r"[^a-z ]",
            "",
            text
        ).strip()

        squeezed = re.sub(
            r"(.)\1{2,}",
            r"\1\1",
            stripped
        )

        if (
            re.match(
                r"^(h+i+|h+e+l+o+|h+e+y+)( .*)?$",
                squeezed
            )
            or any(
                stripped == k
                or stripped.startswith(k + " ")
                for k in GREETING_KEYWORDS
            )
        ):

            return GREETING_RESPONSE

        if any(
            _keyword_in(
                stripped,
                k
            )
            for k in THANKS_KEYWORDS
        ):

            return THANKS_RESPONSE

    # ================================================================
    # KNOWLEDGE BASE
    # ================================================================

    best_entry = None
    best_score = 0

    for entry in KNOWLEDGE_BASE:

        score = 0

        for keyword in entry["keywords"]:

            if _keyword_in(
                text,
                keyword
            ):

                score += len(
                    keyword.split()
                )

        if score > best_score:

            best_score = score
            best_entry = entry

    if best_entry:

        return (
            best_entry["response"]
            + "\n\n"
            + DISCLAIMER
        )

    return (
        DEFAULT_RESPONSE
        + "\n\n"
        + DISCLAIMER
    )


# =====================================================================
# HOME
# =====================================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================================
# LEGAL CATEGORIES
# =====================================================================

@app.route("/categories")
def categories():

    return render_template(
        "categories.html"
    )


# =====================================================================
# AI CHAT
# =====================================================================

@app.route(
    "/ask-ai",
    methods=["POST"]
)
def ask_ai():

    # ================================================================
    # LOGIN CHECK
    # ================================================================

    if "user_id" not in session:

        return {
            "success": False,
            "message":
                "Please login first to use the AI chat.",
            "login_required": True
        }

    # ================================================================
    # GET QUESTION
    # ================================================================

    data = request.get_json(
        silent=True
    ) or {}

    question = str(
        data.get(
            "question",
            ""
        )
    ).strip()

    # ================================================================
    # EMPTY QUESTION
    # ================================================================

    if not question:

        return {
            "success": False,
            "message":
                "Please enter your legal question."
        }

    # ================================================================
    # QUESTION LENGTH
    # ================================================================

    if len(question) > MAX_QUESTION_LENGTH:

        return {
            "success": False,
            "message":
                "Your question is too long. "
                f"Please keep it under "
                f"{MAX_QUESTION_LENGTH} characters."
        }

    # ================================================================
    # HISTORY
    # ================================================================

    history = get_recent_history(
        session["user_id"]
    )

    # ================================================================
    # TRY GEMINI
    # ================================================================

    answer, error, detail = ask_gemini(
        question,
        history
    )

    source = "gemini"
    notice = None

    # ================================================================
    # RULE-BASED FALLBACK
    # ================================================================

    if answer is None:

        answer = get_predefined_answer(
            question
        )

        source = "knowledge_base"

        if error == "not_configured":

            notice = (
                "Gemini API key is not configured. "
                "Showing a built-in legal answer."
            )

        elif error == "overloaded":

            notice = (
                "Gemini is temporarily busy. "
                "Showing a built-in legal answer."
            )

        elif error == "timeout":

            notice = (
                "Gemini did not respond in time. "
                "Showing a built-in legal answer."
            )

        elif error == "invalid_key":

            notice = (
                "Gemini rejected the API key. "
                "Showing a built-in legal answer."
            )

        elif error == "api_disabled":

            notice = (
                "Gemini API is not enabled. "
                "Showing a built-in legal answer."
            )

        elif error == "model_not_found":

            notice = (
                "Gemini model is unavailable. "
                "Showing a built-in legal answer."
            )

        elif error == "rate_limited":

            notice = (
                "Gemini rate limit reached. "
                "Showing a built-in legal answer."
            )

        elif error == "invalid_json":

            notice = (
                "Gemini returned an invalid JSON response. "
                "Showing a built-in legal answer."
            )

        elif error == "blocked":

            notice = (
                "Gemini could not answer this question. "
                "Showing a built-in legal answer."
            )

        else:

            notice = (
                "Gemini is temporarily unavailable. "
                "Showing a built-in legal answer."
            )

    # ================================================================
    # SAVE CHAT HISTORY
    # ================================================================

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO chat_history
        (user_id, question, response)
        VALUES (?, ?, ?)
        """,
        (
            session["user_id"],
            question,
            answer
        )
    )

    conn.commit()
    conn.close()

    # ================================================================
    # RETURN TO FRONTEND
    # ================================================================

    return {
        "success": True,
        "question": question,
        "response": answer,
        "source": source,
        "notice": notice
    }


# =====================================================================
# CHAT HISTORY
# =====================================================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    chats = conn.execute(
        """
        SELECT *
        FROM chat_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (
            session["user_id"],
        )
    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        chats=chats
    )


@app.route(
    "/clear-history",
    methods=["POST"]
)
def clear_history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM chat_history
        WHERE user_id = ?
        """,
        (
            session["user_id"],
        )
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("history")
    )


# =====================================================================
# DOCUMENT CHECKLIST
# =====================================================================

@app.route("/checklist")
def checklist():

    return render_template(
        "checklist.html"
    )


# =====================================================================
# CONSUMER LAW
# =====================================================================

@app.route("/consumer-law")
def consumer_law():

    return render_template(
        "consumer-law.html"
    )

@app.route("/employment-law")
def employment_law():
    return render_template("employment-law.html")    


# =====================================================================
# CYBER CRIME
# =====================================================================

@app.route("/cyber-crime")
def cyber_crime():

    return render_template(
        "cyber-crime.html"
    )


# =====================================================================
# FAMILY LAW
# =====================================================================

@app.route("/family-law")
def family_law():

    return render_template(
        "family-law.html"
    )


# =====================================================================
# PROPERTY LAW
# =====================================================================

@app.route("/property-law")
def property_law():

    return render_template(
        "property-law.html"
    )


# =====================================================================
# FAQ
# =====================================================================

@app.route("/faq")
def faq():

    return render_template(
        "faq.html"
    )


# =====================================================================
# LOGIN
# =====================================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = (
            request.form.get(
                "email"
            )
            or ""
        ).strip().lower()

        password = (
            request.form.get(
                "password"
            )
            or ""
        )

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE lower(email) = ?
            """,
            (
                email,
            )
        ).fetchone()

        valid = False

        if user:

            stored = user["password"]

            if stored.startswith(
                (
                    "pbkdf2:",
                    "scrypt:"
                )
            ):

                valid = check_password_hash(
                    stored,
                    password
                )

            elif stored == password:

                valid = True

                conn.execute(
                    """
                    UPDATE users
                    SET password = ?
                    WHERE id = ?
                    """,
                    (
                        generate_password_hash(
                            password
                        ),
                        user["id"]
                    )
                )

                conn.commit()

        conn.close()

        if valid:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html",
            error="Invalid email or password.",
            email=email
        )

    return render_template(
        "login.html"
    )


# =====================================================================
# REGISTER
# =====================================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = (
            request.form.get(
                "name"
            )
            or ""
        ).strip()

        email = (
            request.form.get(
                "email"
            )
            or ""
        ).strip().lower()

        password = (
            request.form.get(
                "password"
            )
            or ""
        )

        if (
            not name
            or not email
            or not password
        ):

            return render_template(
                "register.html",
                error="Please fill all the fields.",
                name=name,
                email=email
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                error=(
                    "Password must be at least "
                    "6 characters."
                ),
                name=name,
                email=email
            )

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    generate_password_hash(
                        password
                    )
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "register.html",
                error=(
                    "This email is already registered. "
                    "Please use a different email or login."
                ),
                name=name
            )

    return render_template(
        "register.html"
    )


# =====================================================================
# AI RISK ANALYZER
# =====================================================================

@app.route("/risk-analyzer")
def risk_analyzer():

    return render_template(
        "risk-analyzer.html"
    )


# =====================================================================
# SAVE CHAT
# =====================================================================

@app.route(
    "/save-chat",
    methods=["POST"]
)
def save_chat():

    if "user_id" not in session:

        return {
            "success": False,
            "message":
                "Please login first"
        }

    data = request.get_json(
        silent=True
    ) or {}

    question = data.get(
        "question"
    )

    response = data.get(
        "response"
    )

    if not question or not response:

        return {
            "success": False,
            "message":
                "Nothing to save"
        }

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO chat_history
        (user_id, question, response)
        VALUES (?, ?, ?)
        """,
        (
            session["user_id"],
            question,
            response
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True
    }


# =====================================================================
# LOGOUT
# =====================================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =====================================================================
# CHAT PAGE
# =====================================================================

@app.route("/chat")
def chat():

    return render_template(
        "chat.html"
    )


# =====================================================================
# RUN APPLICATION
# =====================================================================

if __name__ == "__main__":

    if gemini_is_configured():

        print(
            f"[Legal Assistant {APP_VERSION}] "
            f"Gemini enabled "
            f"(model: {GEMINI_MODEL})"
        )

    else:

        print(
            "[Legal Assistant] "
            "Gemini key NOT set."
        )

        print(
            "Set GEMINI_API_KEY as an environment variable."
        )

    app.run(
        debug=True
    )