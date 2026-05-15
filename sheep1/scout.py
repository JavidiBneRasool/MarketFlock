# SHEEP 1 - AI & Terminal Scout
import feedparser, json, os
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"

# AI, Terminal, and Automation Sources
TECH_FEEDS = [
    {"name": "Hacker News", "category": "Terminal/Dev", "url": "https://news.ycombinator.com/rss"},
    {"name": "Product Hunt", "category": "AI Tools", "url": "https://www.producthunt.com/feed"},
    {"name": "The Verge AI", "category": "AI News", "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"},
    {"name": "Wired Security", "category": "Automation/Sec", "url": "https://www.wired.com/feed/category/security/latest/rss"},
    {"name": "ArXiv AI", "category": "AI Research", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortby=submittedDate&sortorder=descending"},
    {"name": "OpenAI Blog", "category": "Agents/AI", "url": "https://openai.com/news/rss.xml"},
    {"name": "Google AI Blog", "category": "AI Research", "url": "https://blog.google/technology/ai/rss/"},
    {"name": "TechCrunch AI", "category": "AI Business", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "Reddit SelfHosted", "category": "Automation", "url": "https://www.reddit.com/r/selfhosted/.rss"},
    {"name": "Reddit Commandline", "category": "Terminal", "url": "https://www.reddit.com/r/commandline/.rss"},
]

def run():
    print("🐑 SHEEP 1: Scouting AI & Terminal tools...")
    os.makedirs(OUTPUT, exist_ok=True)
    
    published_urls = set()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                published_urls = {a.get("source_url") for a in history if a.get("source_url")}
        except:
            pass

    articles = []
    
    for source in TECH_FEEDS:
        try:
            feed = feedparser.parse(source["url"])
            if feed.entries:
                # Find the first entry not in history
                new_entry = None
                for entry in feed.entries:
                    if entry.link not in published_urls:
                        new_entry = entry
                        break
                
                if new_entry:
                    articles.append({
                        "title": new_entry.title,
                        "url": new_entry.link,
                        "source": source["name"],
                        "category": source["category"],
                        "summary": new_entry.get("summary", ""),
                        "found_at": datetime.now().isoformat()
                    })
                    print(f"   [{source['category']}] {new_entry.title[:55]}...")
                else:
                    print(f"   [{source['category']}] No new articles.")
        except Exception as e:
            print(f"   [{source['name']}] Skipped: {e}")
    
    if articles:
        with open(f"{OUTPUT}/sheep1_basket.json", "w") as f:
            json.dump(articles, f, indent=2)
        print(f"🐑 SHEEP 1: {len(articles)} articles ✓")
        return articles
    
    print("🐑 SHEEP 1: Nothing found!")
    return None

if __name__ == "__main__":
    run()
