import json, os, urllib.parse, uuid, time, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai import ask_with_delay

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

MARKET_IMAGES = {
    "Crypto": ["bitcoin,cryptocurrency", "ethereum,blockchain", "crypto,trading", "bitcoin,gold,coin"],
    "Markets": ["stock,market,chart", "wall,street,trading", "financial,market", "stock,exchange"],
    "Stocks": ["stock,market", "trading,floor", "financial,chart", "investment"],
    "Commodity": ["gold,bullion", "oil,rig,platform", "commodity,trading", "silver,gold"],
    "Forex": ["forex,trading", "currency,exchange", "dollar,euro", "forex,chart"],
    "India Markets": ["mumbai,stock,exchange", "bse,india", "nse,trading", "sensex"],
}

def get_image_url(category, index):
    keywords = MARKET_IMAGES.get(category, ["finance,market,trading"])
    kw = keywords[index % len(keywords)]
    seed = int(time.time()) + index
    return {
        "unsplash": f"https://loremflickr.com/1200/630/{urllib.parse.quote(kw)}?lock={seed}",
        "pollinations": f"https://image.pollinations.ai/prompt/{urllib.parse.quote(kw+' professional photo')}?width=800&height=600&nologo=true&seed={seed}"
    }

def generate_headline(title, category):
    prompt = f"""Write a punchy financial news headline for: '{title}'
Category: {category}
Rules: max 10 words, no quotes, use financial language, make it urgent and specific, include numbers if relevant."""
    result = ask_with_delay(prompt, system="You are a Bloomberg financial news editor. Write precise market headlines.", delay=2)
    if result:
        if "</think>" in result:
            result = result.split("</think>")[-1].strip()
        return result[:100].strip()
    return title[:80]

def run():
    print("🐑 SHEEP 5: Headlines & Images (AI-powered)...")
    try:
        with open(f"{OUTPUT}/sheep3_compliance.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 5: No input!"); return None

    passed = [a for a in articles if a["decision"] == "PASS"]
    results = []
    seen = set()

    for i, article in enumerate(passed):
        print(f"  → Headline {i+1}/{len(passed)}...")
        headline = generate_headline(article["title"], article["category"])
        if headline in seen:
            headline = generate_headline(article["title"] + " update", article["category"])
        seen.add(headline)
        images = get_image_url(article["category"], i)
        results.append({
            "category": article["category"],
            "headline": headline,
            "image_url": images["unsplash"],
            "image_fallback": images["pollinations"],
            "article": article
        })

    with open(f"{OUTPUT}/sheep5_headlines.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"🐑 SHEEP 5: {len(results)} AI headlines ready ✓")
    return results

if __name__ == "__main__":
    run()
