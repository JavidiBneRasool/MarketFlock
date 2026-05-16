import os
import urllib.request
import urllib.error
import json
import time

GROQ_KEY = os.environ.get("GROQ_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
UA = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"

def ask(prompt, system="You are a professional financial news editor. Be concise and factual."):
    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512
    }).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                GROQ_URL,
                data=payload,
                headers={
                    "Authorization": "Bearer " + GROQ_KEY,
                    "Content-Type": "application/json",
                    "User-Agent": UA
                }
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read())
                return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 5 * (attempt + 1)
                print(f"[AI] Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"[AI] Failed: {e}")
                return None
        except Exception as e:
            print(f"[AI] Failed: {e}")
            return None
    return None

def ask_with_delay(prompt, system="You are a professional financial news editor. Be concise and factual.", delay=1):
    time.sleep(delay)
    return ask(prompt, system)
