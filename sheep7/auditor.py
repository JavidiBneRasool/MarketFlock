import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

PLACEHOLDERS = ["TODO", "[HOOK]", "[REVEAL]", "fact one"]

def run():
    print("🐑 SHEEP 7: Auditing...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 7: No draft!"); return None
    
    clean = []
    for article in articles:
        body = article["body"]
        errors = [p for p in PLACEHOLDERS if p.lower() in body.lower()]
        if len(body) < 300: errors.append("TOO_SHORT")
        if "AI-Generated" not in body and "Auto Flock" not in body and "Auto Flock Signal" not in body:
            errors.append("MISSING_TAG")
        
        article["errors"] = len(errors)
        article["error_list"] = errors
        article["clean"] = len(errors) == 0
        if article["clean"]:
            clean.append(article)
    
    with open(f"{OUTPUT}/sheep7_audited.json", "w") as f:
        json.dump(clean, f, indent=2)
    
    print(f"🐑 SHEEP 7: {len(clean)} clean, {len(articles)-len(clean)} with errors ✓")
    return clean

if __name__ == "__main__":
    run()
