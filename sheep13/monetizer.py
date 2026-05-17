# SHEEP 13 - MarketFlock Monetizer (Financial Services)
import json, os
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

MARKET_OFFERS = {
    "Crypto": [
        {"name": "Binance", "description": "World's largest crypto exchange. Low fees, 350+ coins.", "link": "https://binance.com", "cta": "Trade Now"},
        {"name": "CoinDCX India", "description": "India's leading crypto platform. INR deposits supported.", "link": "https://coindcx.com", "cta": "Start Trading"},
        {"name": "Ledger Wallet", "description": "Industry-standard hardware wallet for cold storage.", "link": "https://www.amazon.in/s?k=ledger+nano+wallet&tag=cutbar-21", "cta": "Secure Assets"},
    ],
    "Stocks": [
        {"name": "Zerodha", "description": "India's #1 discount broker. Zero brokerage on delivery.", "link": "https://zerodha.com", "cta": "Open Account"},
        {"name": "Groww", "description": "Simple stock & mutual fund investing for beginners.", "link": "https://groww.in", "cta": "Start Investing"},
        {"name": "TradingView", "description": "Professional charting and market analysis platform.", "link": "https://tradingview.com", "cta": "View Charts"},
    ],
    "Commodity": [
        {"name": "Angel One", "description": "Trade gold, silver, crude oil on MCX with low brokerage.", "link": "https://angelone.in", "cta": "Trade Commodities"},
        {"name": "Gold ETF Guide", "description": "Learn how to invest in gold ETFs for portfolio hedging.", "link": "https://www.amazon.in/s?k=gold+etf+investing&tag=cutbar-21", "cta": "Learn More"},
        {"name": "ICICI Direct", "description": "Multi-asset trading platform for stocks, futures & options.", "link": "https://icicidirect.com", "cta": "Open Account"},
    ],
    "Forex": [
        {"name": "Forex.com", "description": "Trade 80+ currency pairs with tight spreads.", "link": "https://forex.com", "cta": "Trade Forex"},
        {"name": "HDFC Forex Card", "description": "Best forex rates for international transactions.", "link": "https://hdfcbank.com", "cta": "Get Forex Card"},
        {"name": "Forex Trading Books", "description": "Master forex trading with expert-recommended books.", "link": "https://www.amazon.in/s?k=forex+trading+books&tag=cutbar-21", "cta": "Shop Books"},
    ],
    "Markets": [
        {"name": "Zerodha Kite", "description": "India's best trading platform for stocks and F&O.", "link": "https://zerodha.com", "cta": "Start Trading"},
        {"name": "TradingView Pro", "description": "Advanced charts and real-time market data.", "link": "https://tradingview.com", "cta": "Try Free"},
        {"name": "Finance Books", "description": "Top-rated investing and market analysis books.", "link": "https://www.amazon.in/s?k=finance+investing+books&tag=cutbar-21", "cta": "Shop Now"},
    ],
}

DEFAULT_OFFERS = MARKET_OFFERS["Markets"]

def build_comparison_table(offers):
    table = "| Platform | What You Get | Action |\n"
    table += "| :--- | :--- | :--- |\n"
    for o in offers:
        table += f"| **{o['name']}** | {o['description']} | [{o['cta']}]({o['link']}) |\n"
    return table

def run():
    print("🐑 SHEEP 13: Generating Market Comparison Tables...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 13: No input!"); return None

    for article in articles:
        category = article.get("category", "Markets")
        offers = MARKET_OFFERS.get(category, DEFAULT_OFFERS)
        table = build_comparison_table(offers)
        section = f"\n\n## 📈 Market Platforms\n\n{table}"
        if "## 📊 Market Resources" in article["body"]:
            article["body"] = article["body"].replace("## 📊 Market Resources", f"## 📈 Market Platforms\n\n{table}\n\n## 📊 Market Resources")
        else:
            article["body"] += section

    with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
        json.dump(articles, f, indent=2)

    with open(f"{OUTPUT}/sheep7_audited.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"🐑 SHEEP 13: Market comparison tables injected into {len(articles)} articles ✓")
    return articles

if __name__ == "__main__":
    run()
