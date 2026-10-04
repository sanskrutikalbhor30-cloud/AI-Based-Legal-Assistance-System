"""
Quick check that your Gemini key works.   Run:  python test_gemini.py
It prints the exact reason if something is wrong.
"""
import app

print("Model      :", app.GEMINI_MODEL)
print("Key set    :", app.gemini_is_configured())

text, error, detail = app.ask_gemini("What is a rental agreement in India? Answer in 2 lines.")

if text:
    print("\nSUCCESS - Gemini replied:\n")
    print(text)
else:
    print("\nFAILED  -", error)
    print("Reason  :", detail)
    print("\nWhat to try:")
    print(" * 'API has not been used / is disabled' -> enable the API named in the message for that Google project, or make a new key at aistudio.google.com/app/apikey")
    print(" * HTTP 400/401/403 -> the key is wrong/disabled: create a new one at https://aistudio.google.com/app/apikey")
    print(" * HTTP 404         -> set another model, e.g.  $env:GEMINI_MODEL='gemini-3.5-flash-lite'")
    print(" * HTTP 503 / high demand -> Google is busy, not your key. Wait a minute and retry")
    print(" * HTTP 429         -> free quota used up, wait a minute")
    print(" * timeout/network  -> check internet / VPN / firewall")
