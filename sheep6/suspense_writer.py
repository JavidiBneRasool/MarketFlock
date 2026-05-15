import json, os, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

HOOKS = ["It started quietly.", "Nobody saw it coming.", "The signs were there.", "What happened next stunned everyone."]
REVEALS = ["Here is what happened:", "The truth emerged:", "Sources confirmed:"]
ENDINGS = ["What happens next?", "This story is far from over.", "The world watches and waits."]

def run():
    print("🐑 SHEEP 6: Writing articles...")
    try:
        with open(f"{OUTPUT}/sheep5_headlines.json") as f:
            headlines = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 6: No input!"); return None
    
    articles = []
    for item in headlines:
        h = item["headline"]
        a = item["article"]
        iu = item["image_url"]
        fb = item.get("image_fallback", "")
        
        summary_text = a.get('summary', 'Details are unfolding. Stay tuned for updates on this developing story.')
        
        # Heuristic "Deepening"
        takeaways = [f"• {line.strip()}" for line in summary_text.split('.') if len(line.strip()) > 10][:3]
        if not takeaways: takeaways = ["• Significant developments reported in this sector.", "• Strategic implications for global stakeholders.", "• Ongoing monitoring required by analysts."]
        
        takeaways_html = "\n".join(takeaways)
        
        # Financial Niche Monetization Logic
        adsense_code = '<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-1473583694933213" data-ad-slot="3952378980"></ins>\n<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'

        # Dynamic Amazon Recommendations (cutbar-21)
        cat = a.get('category', '').lower()
        amazon_block = ""
        if 'tech' in cat or 'gadget' in cat:
            amazon_block = """
• **Tech Optimization:** Protect your digital infrastructure with top-rated security hardware.
"View Recommended Security Gear" (https://www.amazon.in/s?k=security+camera+wifi+outdoor&tag=cutbar-21)
"""
        elif 'business' in cat or 'market' in cat:
            amazon_block = """
• **Executive Productivity:** Upgrade your workspace with ergonomic high-performance tools.
"View Professional Office Gear" (https://www.amazon.in/s?k=mechanical+keyboard+for+coding&tag=cutbar-21)
"""
        elif 'health' in cat or 'science' in cat:
            amazon_block = """
• **Bio-Optimization:** Track your vitals with precision health monitoring technology.
"View Health Monitoring Tools" (https://www.amazon.in/s?k=smart+watch+with+ecg&tag=cutbar-21)
"""
        else:
            amazon_block = """
• **Daily Intelligence:** Stay prepared with the latest high-utility EDC (Everyday Carry) tools.
"View Essential Utility Gear" (https://www.amazon.in/s?k=leatherman+multitool&tag=cutbar-21)
"""

        affiliate_block = f"""
• **High-Yield Savings:** Don't let your capital sit idle.
"Compare Top Savings Rates" (https://cutbar.in/finance-recommends/savings)

• **Precision Trading:** Execute on these signals with low-fee institutional-grade platforms.
"View Trading Platforms" (https://cutbar.in/finance-recommends/trading)
{amazon_block}
• **Debt Restructuring:** If interest rates are affecting your overhead, consider a strategic refinance.
"Check Refinance Options" (https://cutbar.in/finance-recommends/refi)
"""

        body = f"""# {h}

*NewsHour Intelligence | {datetime.now().strftime('%B %d, %Y')}*

---

## 🔮 The Intelligence Signal
{summary_text}

{adsense_code}

## 💡 Why This Matters (The Deep Dive)
This story is critical because it highlights shifting dynamics in {a.get('category', 'this sector')}. Our analysis suggests this development could serve as a precursor to even larger structural changes in the coming weeks.

{affiliate_block}

## 🛠️ Actionable Strategy Checklist
If you are affected by this news, here are your next steps:
• **Assess Risk:** Evaluate how this development impacts your current portfolio or career path.
• **Stay Informed:** Monitor real-time updates on {a.get('source', 'original sources')} to catch shifts before they go mainstream.
• **Pivot Fast:** Prepare a contingency plan for the next 48 hours as the situation stabilizes.

{adsense_code}

## 🧠 Expert Prediction
Industry veterans suggest that the timing of this event is no coincidence. "We are seeing a convergence of factors that point towards a new normal," noted one senior analyst. **The Signal:** Watch for regional power shifts in the next quarter.

---
🤖 Published by NewsHour Signal Engine | Category: {a['category']} | Source: {a['source']}"""
        
        articles.append({
            "category": item["category"],
            "headline": h,
            "image_url": iu,
            "image_fallback": fb,
            "body": body,
            "source": a["source"],
            "source_url": a["url"],
            "written_at": datetime.now().isoformat()
        })
    
    with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
        json.dump(articles, f, indent=2)
    
    print(f"🐑 SHEEP 6: {len(articles)} articles written ✓")
    return articles

if __name__ == "__main__":
    run()
