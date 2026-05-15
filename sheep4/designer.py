# SHEEP 4 - Designer (handles multiple articles)
import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

def run():
    print("🐑 SHEEP 4: Designing...")
    os.makedirs(OUTPUT, exist_ok=True)
    try:
        with open(f"{OUTPUT}/sheep3_compliance.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 4: No input!"); return None
    
    # Filter passed articles
    passed = [a for a in articles if a.get("decision") == "PASS"]
    
    designs = []
    for a in passed:
        designs.append({
            "template": "suspense",
            "layout": "HOOK→SCENE→TENSION→REVEAL→AFTERMATH",
            "category": a["category"],
            "ai_tag": "🤖 AI-GENERATED IMAGE"
        })
    
    with open(f"{OUTPUT}/sheep4_design.json", "w") as f:
        json.dump(designs, f, indent=2)
    
    print(f"🐑 SHEEP 4: {len(designs)} templates ready ✓")
    return designs

if __name__ == "__main__":
    run()
