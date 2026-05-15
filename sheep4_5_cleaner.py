# SHEEP 4.5 - Removes old/mock data from index.html
import json, os

PROJECT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(os.path.dirname(PROJECT), "newshour-site")

MOCK_PATTERNS = [
    "Markets Rally as Economic Indicators",
    "Revolutionary AI System Transforms Healthcare",
    "Championship Finals: Underdog Team",
    "Cybersecurity Alert: New Protection",
    "Award-Winning Director Announces",
    "Senate Passes Landmark Infrastructure",
    "New Policy Reforms Announced",
    "The Morning Brief",
    "CUTBAR Investigates",
    "Tech Today",
    "Global Perspective",
    "Latest Stories",
]

def clean_index(html):
    """Remove all mock data cards from index.html"""
    import re
    for pattern in MOCK_PATTERNS:
        # Remove entire article cards containing mock data
        html = re.sub(r'<article[^>]*>.*?' + re.escape(pattern) + r'.*?</article>', '', html, flags=re.DOTALL)
    return html

def run():
    print("🐑 SHEEP 4.5: Cleaning old mock data...")
    os.makedirs(OUTPUT, exist_ok=True)
    
    index_path = os.path.join(SITE_DIR, "index.html")
    
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            content = f.read()
        
        cleaned = clean_index(content)
        
        with open(f"{OUTPUT}/index_cleaned.html", "w") as f:
            f.write(cleaned)
        
        print("🐑 SHEEP 4.5: Mock data removed ✓")
    else:
        print("🐑 SHEEP 4.5: No index.html found")

if __name__ == "__main__":
    run()
