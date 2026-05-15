import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

TRUSTED = ["bbc", "reuters", "al jazeera", "associated press", "ap news", "fox"]
UNTRUSTED = ["infowars", "naturalnews", "theonion"]

def run():
    print("🐑 SHEEP 2: Verifying...")
    try:
        with open(f"{OUTPUT}/sheep1_basket.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 2: No articles!"); return None
    
    verified = []
    for article in articles:
        source_lower = article["source"].lower()
        level, score = "UNKNOWN", 5
        for t in TRUSTED:
            if t in source_lower:
                level, score = "TRUSTED", 10
                break
        for u in UNTRUSTED:
            if u in source_lower:
                level, score = "UNTRUSTED", 0
                break
        article["credibility"] = level
        article["score"] = score
        article["verdict"] = "PASS" if level == "TRUSTED" else "WARNING"
        verified.append(article)
    
    with open(f"{OUTPUT}/sheep2_verified.json", "w") as f:
        json.dump(verified, f, indent=2)
    
    passed = sum(1 for a in verified if a["verdict"] == "PASS")
    print(f"🐑 SHEEP 2: {passed}/{len(verified)} passed ✓")
    return verified

if __name__ == "__main__":
    run()
