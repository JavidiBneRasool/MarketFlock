# SHEEP 1 - AI & Terminal Scout
import feedparser, json, os, re, time
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"

MAX_ARTICLES = 12
MAX_PER_SOURCE = 2
MIN_TITLE_WORDS = 4

# Higher-signal AI, terminal, developer, security, and automation sources.
TECH_FEEDS = [
    {"name": "OpenAI News", "category": "Agents/AI", "tier": 10, "url": "https://openai.com/news/rss.xml"},
    {"name": "Google DeepMind", "category": "AI Research", "tier": 10, "url": "https://deepmind.google/discover/blog/rss.xml"},
    {"name": "Google AI Blog", "category": "AI Research", "tier": 9, "url": "https://blog.google/technology/ai/rss/"},
    {"name": "Anthropic News", "category": "Agents/AI", "tier": 9, "url": "https://www.anthropic.com/news/rss.xml"},
    {"name": "Hugging Face Blog", "category": "AI Tools", "tier": 8, "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "GitHub Blog AI", "category": "Terminal/Dev", "tier": 8, "url": "https://github.blog/ai-and-ml/feed/"},
    {"name": "GitHub Engineering", "category": "Terminal/Dev", "tier": 8, "url": "https://github.blog/engineering/feed/"},
    {"name": "Cloudflare Blog AI", "category": "Automation/Sec", "tier": 8, "url": "https://blog.cloudflare.com/tag/ai/rss/"},
    {"name": "Cloudflare Security", "category": "Automation/Sec", "tier": 8, "url": "https://blog.cloudflare.com/tag/security/rss/"},
    {"name": "Microsoft AI Blog", "category": "AI Business", "tier": 8, "url": "https://blogs.microsoft.com/ai/feed/"},
    {"name": "AWS Machine Learning", "category": "AI Business", "tier": 8, "url": "https://aws.amazon.com/blogs/machine-learning/feed/"},
    {"name": "NVIDIA Technical Blog", "category": "AI Research", "tier": 8, "url": "https://developer.nvidia.com/blog/feed/"},
    {"name": "Meta AI Blog", "category": "AI Research", "tier": 8, "url": "https://ai.meta.com/blog/rss/"},
    {"name": "ArXiv AI", "category": "AI Research", "tier": 7, "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortby=submittedDate&sortorder=descending&max_results=20"},
    {"name": "The Hacker News AI", "category": "Automation/Sec", "tier": 7, "url": "https://feeds.feedburner.com/TheHackersNews"},
    {"name": "Wired Security", "category": "Automation/Sec", "tier": 7, "url": "https://www.wired.com/feed/category/security/latest/rss"},
    {"name": "TechCrunch AI", "category": "AI Business", "tier": 7, "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "The Verge AI", "category": "AI News", "tier": 7, "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"},
    {"name": "Hacker News", "category": "Terminal/Dev", "tier": 6, "url": "https://news.ycombinator.com/rss"},
    {"name": "Lobsters Programming", "category": "Terminal/Dev", "tier": 6, "url": "https://lobste.rs/t/programming.rss"},
    {"name": "Lobsters Security", "category": "Automation/Sec", "tier": 6, "url": "https://lobste.rs/t/security.rss"},
    {"name": "Product Hunt AI", "category": "AI Tools", "tier": 4, "url": "https://www.producthunt.com/feed"},
]

LOW_SIGNAL_PATTERNS = [
    r"\bdiscount codes?\b", r"\bcoupon\b", r"\bpromo code\b", r"\bworkshop\b",
    r"\blaunching today\b", r"\bdeal\b", r"\bgiveaway\b",
]
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid", "ref"}


def _canonical_url(url):
    if not url:
        return ""
    parts = urlsplit(url.strip())
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS])
    path = parts.path.rstrip('/') or '/'
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ''))


def _title_key(title):
    title = re.sub(r"[^a-z0-9 ]+", " ", (title or "").lower())
    title = re.sub(r"\s+", " ", title).strip()
    return title


def _is_low_signal(title, summary, source_name):
    text = f"{title} {summary}".lower()
    if len(_title_key(title).split()) < MIN_TITLE_WORDS:
        return True
    if any(re.search(pattern, text) for pattern in LOW_SIGNAL_PATTERNS):
        return True
    # Product Hunt is useful, but only keep entries that clearly fit Autoflock.
    if source_name == "Product Hunt AI":
        ai_terms = ("ai", "agent", "llm", "automation", "developer", "code", "api", "workflow", "browser", "terminal")
        return not any(term in text for term in ai_terms)
    return False


def _entry_time(entry):
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return int(time.mktime(parsed))
    return 0


def _load_seen():
    seen_urls, seen_titles = set(), set()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                for item in json.load(f):
                    seen_urls.add(_canonical_url(item.get("source_url", "")))
                    seen_titles.add(_title_key(item.get("headline") or item.get("title", "")))
        except Exception:
            pass
    posted_file = f"{OUTPUT}/social_posted.json"
    if os.path.exists(posted_file):
        try:
            with open(posted_file, "r") as f:
                for item in json.load(f):
                    seen_urls.add(_canonical_url(item.get("source_url", "")))
                    seen_titles.add(_title_key(item.get("headline", "")))
        except Exception:
            pass
    return seen_urls, seen_titles


def run():
    print("🐑 SHEEP 1: Scouting top-tier AI, terminal, and automation sources...")
    os.makedirs(OUTPUT, exist_ok=True)
    seen_urls, seen_titles = _load_seen()

    candidates = []
    per_source = {}
    for source in TECH_FEEDS:
        try:
            feed = feedparser.parse(source["url"])
            source_count = 0
            for entry in feed.entries[:12]:
                title = entry.get("title", "").strip()
                url = _canonical_url(entry.get("link", ""))
                summary = entry.get("summary", "") or entry.get("description", "") or ""
                title_key = _title_key(title)
                if not url or url in seen_urls or title_key in seen_titles:
                    continue
                if _is_low_signal(title, summary, source["name"]):
                    continue
                candidates.append({
                    "title": title,
                    "url": url,
                    "source": source["name"],
                    "category": source["category"],
                    "summary": summary,
                    "tier": source["tier"],
                    "published_ts": _entry_time(entry),
                    "found_at": datetime.now(timezone.utc).isoformat()
                })
                seen_urls.add(url)
                seen_titles.add(title_key)
                source_count += 1
                if source_count >= MAX_PER_SOURCE:
                    break
            if source_count:
                per_source[source["name"]] = source_count
        except Exception as e:
            print(f"   [{source['name']}] Skipped: {e}")

    candidates.sort(key=lambda a: (a["tier"], a["published_ts"]), reverse=True)
    articles = candidates[:MAX_ARTICLES]

    for article in articles:
        print(f"   [{article['source']} / {article['category']}] {article['title'][:65]}...")

    if articles:
        with open(f"{OUTPUT}/sheep1_basket.json", "w") as f:
            json.dump(articles, f, indent=2)
        print(f"🐑 SHEEP 1: {len(articles)} articles from {len(per_source)} sources ✓")
        return articles

    print("🐑 SHEEP 1: Nothing found!")
    return None

if __name__ == "__main__":
    run()
