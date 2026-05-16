# SHEEP 1 - MarketFlock Scout: Finance, Crypto, Commodity, Markets
import feedparser, json, os, re, time
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"

MAX_ARTICLES = 12
MAX_PER_SOURCE = 2
MIN_TITLE_WORDS = 4

MARKET_FEEDS = [
    {"name": "CoinDesk", "category": "Crypto", "tier": 10, "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
    {"name": "CoinTelegraph", "category": "Crypto", "tier": 10, "url": "https://cointelegraph.com/rss"},
    {"name": "Bitcoin Magazine", "category": "Crypto", "tier": 9, "url": "https://bitcoinmagazine.com/feed"},
    {"name": "Decrypt", "category": "Crypto", "tier": 9, "url": "https://decrypt.co/feed"},
    {"name": "The Block", "category": "Crypto", "tier": 9, "url": "https://www.theblock.co/rss.xml"},
    {"name": "Reuters Finance", "category": "Markets", "tier": 10, "url": "https://feeds.reuters.com/reuters/businessNews"},
    {"name": "Bloomberg Markets", "category": "Markets", "tier": 10, "url": "https://feeds.bloomberg.com/markets/news.rss"},
    {"name": "Financial Times", "category": "Markets", "tier": 9, "url": "https://www.ft.com/rss/home"},
    {"name": "MarketWatch", "category": "Stocks", "tier": 9, "url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
    {"name": "Investing.com", "category": "Markets", "tier": 8, "url": "https://www.investing.com/rss/news.rss"},
    {"name": "Yahoo Finance", "category": "Stocks", "tier": 8, "url": "https://finance.yahoo.com/news/rssindex"},
    {"name": "Seeking Alpha", "category": "Stocks", "tier": 8, "url": "https://seekingalpha.com/feed.xml"},
    {"name": "Oil Price", "category": "Commodity", "tier": 8, "url": "https://oilprice.com/rss/main"},
    {"name": "Gold Price", "category": "Commodity", "tier": 8, "url": "https://www.kitco.com/rss/kitco-news.xml"},
    {"name": "Forex Live", "category": "Forex", "tier": 8, "url": "https://www.forexlive.com/feed/news"},
    {"name": "FXStreet", "category": "Forex", "tier": 7, "url": "https://www.fxstreet.com/rss/news"},
    {"name": "Economic Times Markets", "category": "India Markets", "tier": 9, "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"},
    {"name": "Moneycontrol", "category": "India Markets", "tier": 9, "url": "https://www.moneycontrol.com/rss/MCtopnews.xml"},
    {"name": "BSE India", "category": "Stocks", "tier": 8, "url": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms"},
    {"name": "Whale Alert Blog", "category": "Crypto", "tier": 7, "url": "https://blog.whale-alert.io/rss/"},
    {"name": "CryptoSlate", "category": "Crypto", "tier": 7, "url": "https://cryptoslate.com/feed/"},
    {"name": "NewsBTC", "category": "Crypto", "tier": 7, "url": "https://www.newsbtc.com/feed/"},
]

LOW_SIGNAL_PATTERNS = [
    r"\bdiscount codes?\b", r"\bcoupon\b", r"\bpromo code\b",
    r"\bgiveaway\b", r"\bsponsored\b", r"\badvertisement\b",
]
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid", "ref"}


def _canonical_url(url):
    if not url:
        return ""
    parts = urlsplit(url.strip())
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS])
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))


def _title_key(title):
    title = re.sub(r"[^a-z0-9 ]+", " ", (title or "").lower())
    return re.sub(r"\s+", " ", title).strip()


def run():
    print("🐑 SHEEP 1: Scouting market, crypto, and finance sources...")
    os.makedirs(OUTPUT, exist_ok=True)

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    seen_urls = {_canonical_url(a.get("url", "")) for a in history}
    seen_titles = {_title_key(a.get("title", "")) for a in history}

    candidates = []
    for feed in MARKET_FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])
            count = 0
            for entry in parsed.entries:
                if count >= MAX_PER_SOURCE:
                    break
                title = (entry.get("title") or "").strip()
                url = _canonical_url(entry.get("link") or entry.get("id") or "")
                summary = (entry.get("summary") or entry.get("description") or "").strip()
                summary = re.sub(r"<[^>]+>", "", summary)[:300]

                if len(title.split()) < MIN_TITLE_WORDS:
                    continue
                if url in seen_urls or _title_key(title) in seen_titles:
                    continue
                if any(re.search(p, title, re.I) for p in LOW_SIGNAL_PATTERNS):
                    continue

                candidates.append({
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "source": feed["name"],
                    "category": feed["category"],
                    "tier": feed["tier"],
                    "fetched_at": datetime.now(timezone.utc).isoformat()
                })
                seen_urls.add(url)
                seen_titles.add(_title_key(title))
                count += 1
        except Exception as e:
            pass

    candidates.sort(key=lambda x: x["tier"], reverse=True)
    basket = candidates[:MAX_ARTICLES]

    for a in basket:
        print(f"   [{a['category']}] {a['title'][:60]}...")

    with open(f"{OUTPUT}/sheep1_basket.json", "w") as f:
        json.dump(basket, f, indent=2)

    print(f"🐑 SHEEP 1: {len(basket)} articles from {len(MARKET_FEEDS)} sources ✓")
    return basket


if __name__ == "__main__":
    run()
