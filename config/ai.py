import os
import urllib.request
import urllib.error
import json
import time

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load_env():
    env_file = os.path.join(PROJECT, ".env")
    if not os.path.exists(env_file):
        return
    with open(env_file, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

_load_env()

GROQ_KEY = os.environ.get("GROQ_KEY") or os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
UA = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
AUTH_DISABLED = False

def ask(prompt, system="You are a professional financial news editor. Be concise and factual."):
    global AUTH_DISABLED
    if AUTH_DISABLED:
        return None
    if not GROQ_KEY:
        print("[AI] GROQ_KEY missing. Using deterministic fallback.")
        AUTH_DISABLED = True
        return None
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
            elif e.code in (401, 403):
                print("[AI] Groq auth failed. Check GROQ_KEY/GROQ_API_KEY in .env; using fallback for this run.")
                AUTH_DISABLED = True
                return None
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
