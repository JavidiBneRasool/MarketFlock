# SHEEP 13 - The Monetizer (Financial Services Comparison)
import json, os, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

OFFERS = [
    {
        "name": "High-Yield Savings Accounts",
        "description": "Earn up to 5.25% APY on your liquid cash with top-tier FDIC-insured banks.",
        "link": "https://cutbar.in/finance-recommends/savings",
        "cta": "Compare APYs"
    },
    {
        "name": "Institutional-Grade Trading Platforms",
        "description": "Access global markets with 0% commission and advanced technical indicators.",
        "link": "https://cutbar.in/finance-recommends/trading",
        "cta": "Open Account"
    },
    {
        "name": "Business Credit & Capital",
        "description": "Unlock up to $250k in business credit lines with 0% introductory APR for 12 months.",
        "link": "https://cutbar.in/finance-recommends/capital",
        "cta": "Check Eligibility"
    }
]

def run():
    print("🐑 SHEEP 13: Generating Financial Comparison Tables...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 13: No input!"); return None

    # We augment the top article with a comparison table
    if articles:
        top_article = articles[0]
        
        comparison_table = """
| Financial Service | Advantage | Action |
| :--- | :--- | :--- |
"""
        for offer in OFFERS:
            comparison_table += f"| **{offer['name']}** | {offer['description']} | [{offer['cta']}]({offer['link']}) |\n"

        top_article["body"] += f"\n\n## 📊 Comparative Intelligence: Financial Solutions\n{comparison_table}\n"
        
        with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
            json.dump(articles, f, indent=2)
            
    print("🐑 SHEEP 13: Financial tables injected into core articles ✓")

if __name__ == "__main__":
    run()
