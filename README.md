# AI-Based Legal Assistance System

## Run
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Where to add the Gemini API key
Open `app.py` and replace the placeholder near the top:

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
                                                       

Or, without editing code, set an environment variable:
- Windows PowerShell: `$env:GEMINI_API_KEY="your-key"`
- Linux / macOS: `export GEMINI_API_KEY="your-key"`

The model can be changed with `GEMINI_MODEL` (default `gemini-3.8-flash`; if a model is retired the app tries newer fallback models automatically).

## How answers work
1. Gemini answers the question (with the user's last few chats as context).
2. If the key is missing/invalid or Gemini fails, the predefined data set in
   `legal_data.py` is used instead.

To add more predefined questions, append an entry to `KNOWLEDGE_BASE` in `legal_data.py`.

## Check your key
    python test_gemini.py
Prints SUCCESS, or the exact reason Gemini failed.
