import json, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai import ask_with_delay

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

ADSENSE = '''<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-1473583694933213" data-ad-slot="3952378980"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

def get_affiliate(category):
    cat = category.lower()
    if "crypto" in cat or "bitcoin" in cat:
        return """• **Trade Crypto:** [Start on Binance](https://www.binance.com) | [CoinDCX India](https://coindcx.com)
• **Cold Storage:** [Ledger Hardware Wallet](https://www.amazon.in/s?k=ledger+hardware+wallet&tag=cutbar-21)"""
    elif "stock" in cat or "nse" in cat or "bse" in cat or "india" in cat:
        return """• **Stock Trading:** [Zerodha](https://zerodha.com) | [Groww](https://groww.in)
• **Market Tools:** [View Trading Books](https://www.amazon.in/s?k=stock+market+books&tag=cutbar-21)"""
    elif "commodity" in cat or "gold" in cat or "oil" in cat:
        return """• **Commodity Trading:** [Angel One](https://angelone.in) | [ICICI Direct](https://icicidirect.com)
• **Gold Investment:** [View Gold ETF Guide](https://www.amazon.in/s?k=gold+etf+investing&tag=cutbar-21)"""
    elif "forex" in cat:
        return """• **Forex Trading:** [Forex.com](https://forex.com) | [HDFC Forex](https://hdfcbank.com)
• **Forex Books:** [View Forex Trading Books](https://www.amazon.in/s?k=forex+trading+books&tag=cutbar-21)"""
    else:
        return """• **Market Analysis:** [TradingView](https://tradingview.com) | [Investing.com](https://investing.com)
• **Finance Books:** [View Best Finance Books](https://www.amazon.in/s?k=finance+investing+books&tag=cutbar-21)"""

def write_article(headline, summary, category, source):
    prompt = f"""Write a professional market intelligence article.
Headline: {headline}
Category: {category}
Summary: {summary}
Source: {source}

Write in this structure:
1. Opening hook (2 sentences, data-driven)
2. Key market developments (3 bullet points with specific numbers/percentages where possible)
3. Market impact analysis (2-3 sentences)
4. Expert outlook (1 quote-style insight)

Rules: financial journalism tone, specific and factual, max 250 words, no generic filler."""

    result = ask_with_delay(
        prompt,
        system="You are a senior market analyst at a top financial news desk. Write precise, data-driven market intelligence. No fluff.",
        delay=2
    )
    if result:
        if "</think>" in result:
            result = result.split("</think>")[-1].strip()
        return result
    return f"{summary}\n\nThis market development is being closely monitored by analysts."

def run():
    print("🐑 SHEEP 6: Writing AI market articles...")
    try:
        with open(f"{OUTPUT}/sheep5_headlines.json") as f:
            headlines = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 6: No input!"); return None

    articles = []
    for i, item in enumerate(headlines):
        print(f"  → Writing article {i+1}/{len(headlines)}...")
        h = item["headline"]
        a = item["article"]
        summary = a.get("summary", "Market developments are unfolding.")
        category = a.get("category", "Markets")
        source = a.get("source", "MarketFlock")

        ai_body = write_article(h, summary, category, source)
        affiliate = get_affiliate(category)

        body = f"""# {h}

*MarketFlock Intelligence | {datetime.now().strftime("%B %d, %Y")}*

---

{ai_body}

{ADSENSE}

---

## 📊 Market Resources
{affiliate}

---
🤖 Published by MarketFlock Signal Engine | Category: {category} | Source: {source}"""

        articles.append({
            "category": category,
            "headline": h,
            "image_url": item.get("image_url", ""),
            "image_fallback": item.get("image_fallback", ""),
            "body": body,
            "source": source,
            "source_url": a.get("url", ""),
            "written_at": datetime.now().isoformat()
        })

    with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"🐑 SHEEP 6: {len(articles)} AI market articles written ✓")
    return articles

if __name__ == "__main__":
    run()
