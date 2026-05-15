# SHEEP 13 - The Monetizer (Financial Services Comparison)
import json, os, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

OFFERS = [
    {
        "name": "Cloud GPU Cluster Access",
        "description": "Deploy A100/H100 clusters for heavy AI training with per-second billing and zero egress fees.",
        "link": "https://autoflock.cutbar.in/recommend/gpu-cloud",
        "cta": "Scale Compute"
    },
    {
        "name": "Agentic API Endpoints",
        "description": "Unified access to frontier models (Claude 3.5, GPT-4o, Gemini 1.5) with built-in agentic reasoning.",
        "link": "https://autoflock.cutbar.in/recommend/ai-api",
        "cta": "Get API Key"
    },
    {
        "name": "Custom Automation Builds",
        "description": "Unlock efficiency with custom-coded Python/Node agents for scraping, data mining, and social media.",
        "link": "https://autoflock.cutbar.in/recommend/automation",
        "cta": "Build Agent"
    }
]

def run():
    print("🐑 SHEEP 13: Generating AI Stack Comparison Tables...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 13: No input!"); return None

    # We augment the top article with a comparison table
    if articles:
        top_article = articles[0]
        
        comparison_table = """
| AI Professional Stack | Core Advantage | Strategic Action |
| :--- | :--- | :--- |
"""
        for offer in OFFERS:
            comparison_table += f"| **{offer['name']}** | {offer['description']} | [{offer['cta']}]({offer['link']}) |\n"

        top_article["body"] += f"\n\n## 📊 Comparative Intelligence: AI Stack Solutions\n{comparison_table}\n"
        
        with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
            json.dump(articles, f, indent=2)
            
    print("🐑 SHEEP 13: AI comparison tables injected into core articles ✓")

if __name__ == "__main__":
    run()
