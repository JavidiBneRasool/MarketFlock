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

        # AI & Terminal Niche Monetization Logic
        cat = a.get('category', '').lower()
        amazon_block = ""
        if 'tech' in cat or 'terminal' in cat:
            amazon_block = """
• **Terminal Mastery:** Enhance your CLI workflow with the ultimate developer hardware.
"View Pro Developer Gear" (https://www.amazon.in/s?k=mechanical+keyboard+coding&tag=cutbar-21)
"""
        elif 'ai' in cat or 'agent' in cat:
            amazon_block = """
• **Neural Hardware:** Run local LLMs with high-performance GPU-accelerated workstations.
"View AI Compute Hardware" (https://www.amazon.in/s?k=nvidia+rtx+gpu&tag=cutbar-21)
"""
        else:
            amazon_block = """
• **Agentic Tools:** Stay prepared with the latest high-utility automation and tech gear.
"View Essential Tech Tools" (https://www.amazon.in/s?k=leatherman+multitool&tag=cutbar-21)
"""

        affiliate_block = f"""
• **Frontier AI Models:** Deploy advanced agents with low-latency API access.
"Access AI Developer Portals" (https://autoflock.cutbar.in/recommend/ai-api)

• **GPU Cloud Compute:** Scale your training and inference on institutional-grade infrastructure.
"View Cloud GPU Platforms" (https://autoflock.cutbar.in/recommend/gpu-cloud)
{amazon_block}
• **Workflow Automation:** If overhead is high, consider a strategic automation build.
"Check Automation Services" (https://autoflock.cutbar.in/recommend/automation)
"""

        body = f"""# {h}

*Auto Flock Intelligence | {datetime.now().strftime('%B %d, %Y')}*

---

## 🔮 The Intelligence Signal
{summary_text}

{adsense_code}

## 💡 Why This Matters (The Deep Dive)
This story is critical because it highlights shifting dynamics in {a.get('category', 'this sector')}. Our analysis suggests this development could serve as a precursor to even larger structural changes in the coming weeks.

{affiliate_block}

## 🛠️ Actionable Strategy Checklist
If you are affected by this news, here are your next steps:
• **Assess Impact:** Evaluate how this development impacts your current technical stack or career path.
• **Stay Informed:** Monitor real-time updates on {a.get('source', 'original sources')} to catch shifts before they go mainstream.
• **Pivot Fast:** Prepare a contingency plan for the next 48 hours as the situation stabilizes.

{adsense_code}

## 🧠 Expert Prediction
Industry veterans suggest that the timing of this event is no coincidence. "We are seeing a convergence of factors that point towards a new normal," noted one senior analyst. **The Signal:** Watch for regional technical shifts in the next quarter.

---
🤖 Published by Auto Flock Signal Engine | Category: {a['category']} | Source: {a['source']}"""
        
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
