import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

BLOCKED = ["kill all", "must be killed", "exterminate", "death to", "hope they die"]

def run():
    print("🐑 SHEEP 3: Checking...")
    os.makedirs(OUTPUT, exist_ok=True)
    try:
        with open(f"{OUTPUT}/sheep2_verified.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 3: No input!"); return None
    
    checked = []
    for article in articles:
        text = (article["title"] + " " + article.get("summary","")).lower()
        flags = [p for p in BLOCKED if p in text]
        article["decision"] = "BLOCK" if flags else "PASS"
        article["flags"] = flags
        checked.append(article)
    
    with open(f"{OUTPUT}/sheep3_compliance.json", "w") as f:
        json.dump(checked, f, indent=2)
    
    blocked = sum(1 for a in checked if a["decision"] == "BLOCK")
    print(f"🐑 SHEEP 3: {len(checked)-blocked} passed, {blocked} blocked")
    return checked

if __name__ == "__main__":
    run()
