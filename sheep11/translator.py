# SHEEP 11 - Real Urdu Translation Generator with History
import json, os, shutil, requests, time

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"
TRANS_HISTORY = f"{PROJECT}/trans_history.json"

def translate_google(text, target_lang):
    """Translate using free Google Translate API"""
    try:
        import urllib.parse
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={encoded}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            result = r.json()
            translated = ''.join([s[0] for s in result[0] if s[0]])
            return translated
    except:
        pass
    return text

def run():
    print("🐑 SHEEP 11: Generating Urdu translations...")
    os.makedirs(OUTPUT, exist_ok=True)
    
    # Load translations history
    trans_db = {"en": {}, "ur": {}}
    if os.path.exists(TRANS_HISTORY):
        try:
            with open(TRANS_HISTORY, "r", encoding="utf-8") as f:
                trans_db = json.load(f)
        except: pass

    # 1. Static UI elements
    ui_texts = {
        "site_title": "Auto Flock - AI & Terminal Intelligence",
        "latest_stories": "Latest Stories",
        "past_editions": "Past Editions",
        "show_more": "Show More Articles",
        "breaking": "BREAKING",
        "live": "LIVE",
        "back_home": "Back to Auto Flock Home",
        "ai_flock": "AI Flock",
        "politics": "Politics",
        "business": "Business",
        "technology": "Technology",
        "world": "World",
    }
    
    for key, text in ui_texts.items():
        if key not in trans_db["ur"]:
            trans_db["en"][key] = text
            trans_db["ur"][key] = translate_google(text, "ur")
            time.sleep(0.1)
    
    # 2. Translate current run (Headlines + Summaries)
    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            current = json.load(f)
    except:
        current = []

    print("   Translating intelligence signals...")
    for a in current:
        h = a.get("headline", "")
        s = a.get("body", "").split('\n')[0] # Get the first paragraph as summary
        
        if h and h not in trans_db["ur"]:
            trans_db["en"][h] = h
            trans_db["ur"][h] = translate_google(h, "ur")
            time.sleep(0.1)
        
        if s and s not in trans_db["ur"]:
            trans_db["en"][s] = s
            trans_db["ur"][s] = translate_google(s, "ur")
            time.sleep(0.1)

    # Export for site
    with open(f"{OUTPUT}/translations.json", "w", encoding="utf-8") as f:
        json.dump(trans_db, f, ensure_ascii=False, indent=2)
    
    print(f"🐑 SHEEP 11: {len(trans_db['ur'])} Urdu strings ready ✓")

if __name__ == "__main__":
    run()
