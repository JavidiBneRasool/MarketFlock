import json, os, hashlib, requests, zipfile, time, subprocess, shutil, urllib.parse, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(PROJECT, "publish")
HISTORY_FILE = f"{PROJECT}/history.json"

FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1557992260-ec58e38d363c?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1529107336181-e2c7a7df0744?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
]

TOPIC_IMAGES = {
    'tech': [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
    ],
    'market': [
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80",
    ],
    'health': [
        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?auto=format&fit=crop&w=1200&q=80",
    ],
    'politic': [
        "https://images.unsplash.com/photo-1529107336181-e2c7a7df0744?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1557992260-ec58e38d363c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1200&q=80",
    ],
    'sport': [
        "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
    ],
    'science': [
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
    ],
    'world': [
        "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    ],
}

def _pick_unique_image(headline, category, used_set):
    import hashlib
    h = int(hashlib.md5(headline.encode()).hexdigest(), 16)
    hl = headline.lower()
    cat = category.lower()
    pool = None
    for key, imgs in TOPIC_IMAGES.items():
        if key in hl or key in cat:
            pool = imgs[:]
            break
    seen = list(dict.fromkeys((pool or []) + FALLBACK_IMAGES))
    for i in range(len(seen)):
        candidate = seen[(h + i) % len(seen)]
        if candidate not in used_set:
            return candidate
    return seen[h % len(seen)]

def get_flock_name():
    hour = datetime.now().hour
    if 6 <= hour < 12: return "Morning Flock"
    elif 12 <= hour < 18: return "Afternoon Flock"
    elif 18 <= hour < 22: return "Evening Flock"
    else: return "Night Flock"

def _normalize_marketflock_article(article):
    replacements = {
        "NewsHour Intelligence": "MarketFlock Intelligence",
        "NewsHour Signal Engine": "MarketFlock Signal Engine",
        "NewsHour Flock": "MarketFlock",
        "News Hour Flock": "MarketFlock",
        "https://newshour.cutbar.in": "https://market.cutbar.in",
        "https://www.newshour.cutbar.in": "https://market.cutbar.in",
        "https://cutbar.in/": "https://market.cutbar.in/",
    }
    for key in ("body", "summary", "description"):
        value = article.get(key)
        if isinstance(value, str):
            for old, new in replacements.items():
                value = value.replace(old, new)
            article[key] = value
    return article

def run():
    print(f"🐑 SHEEP 8: Publishing {get_flock_name()}...")
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(SITE_DIR, exist_ok=True)
    
    trans_src = f"{OUTPUT}/translations.json"
    if os.path.exists(trans_src):
        shutil.copy(trans_src, f"{SITE_DIR}/translations.json")
    
    ads_txt_src = f"{PROJECT}/ads.txt"
    if os.path.exists(ads_txt_src):
        shutil.copy(ads_txt_src, f"{SITE_DIR}/ads.txt")
    
    font_dir = f"{SITE_DIR}/fonts"
    os.makedirs(font_dir, exist_ok=True)
    font_src = os.path.expanduser("~/storage/downloads/Jameel Noori Nastaleeq Regular.ttf")
    if os.path.exists(font_src):
        shutil.copy(font_src, f"{font_dir}/JameelNooriNastaleeq.ttf")

    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            current_articles = json.load(f)
    except:
        print("🐑 SHEEP 8: No articles!"); return None
    
    now = datetime.now()
    ts = now.strftime("%Y%m%d-%H%M%S")
    date_str = now.strftime("%B %d, %Y")
    flock_name = get_flock_name()
    
    used_images = set()
    for i, a in enumerate(current_articles):
        # Prefer the unique image from Sheep 5 if available
        if not a.get('image_url') or "unsplash.com" not in a.get('image_url'):
            img = _pick_unique_image(a.get('headline', ''), a.get('category', ''), used_images)
            a['image_url'] = img
        
        used_images.add(a['image_url'])

        a["filename"] = f"{ts}-{i+1}.html"
        a["published_at"] = now.isoformat()
        a["flock"] = flock_name
        a["date_display"] = date_str
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    current_articles = [_normalize_marketflock_article(a) for a in current_articles]
    history = [_normalize_marketflock_article(a) for a in history]
    history = current_articles + history
    history = history[:150]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    latest_9 = history[:9]
    past_articles = history[9:]
    
    ads_config = None
    try:
        with open(f"{PROJECT}/config/adsense.json", "r") as f:
            ads_config = json.load(f)
    except:
        pass

    index_html = _build_index(latest_9, past_articles, flock_name, date_str, ads_config)
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f: f.write(index_html)
    
    # Generate sitemap.xml
    _generate_sitemap(history, SITE_DIR)
    # Generate robots.txt
    with open(f"{SITE_DIR}/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://market.cutbar.in/sitemap.xml")

    for a in history:
        content = _build_article_page(a, ads_config)
        with open(f"{SITE_DIR}/{a['filename']}", "w", encoding="utf-8") as f: f.write(content)

    print(f"🐑 SHEEP 8: Files generated in {SITE_DIR}. Ready for Git Sync.")
    return {"published": True}

def _load_config(path):
    with open(path) as f: return json.load(f)

COMMON_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0a0e17;
  --surface: #111827;
  --card: #1a2235;
  --border: rgba(0,200,100,0.12);
  --accent: #00c864;
  --red: #ef4444;
  --gold: #f59e0b;
  --text: #e2e8f0;
  --muted: #64748b;
  --font: 'Inter', sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: var(--font); }
header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 5%; border-bottom: 1px solid var(--border); background: rgba(10,14,23,0.98); position: sticky; top: 0; z-index: 100; }
.logo-wrap { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo-icon { width: 34px; height: 34px; background: var(--accent); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.logo-icon svg { width: 18px; height: 18px; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: var(--text); }
.logo-text span { color: var(--accent); }
.ticker-wrap { background: #0d1420; border-bottom: 1px solid var(--border); padding: 0.35rem 0; overflow: hidden; white-space: nowrap; }
.ticker-inner { display: inline-block; animation: scroll 40s linear infinite; }
@keyframes scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.t-item { display: inline-block; margin: 0 1.5rem; font-size: 0.72rem; font-weight: 600; }
.t-up { color: var(--accent); }
.t-dn { color: var(--red); }
.t-na { color: var(--muted); }
.container { max-width: 1100px; margin: 0 auto; padding: 2rem 5%; }
.hero { text-align: center; padding: 2.5rem 0 2rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.live-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(0,200,100,0.08); border: 1px solid rgba(0,200,100,0.25); color: var(--accent); padding: 0.25rem 0.8rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1rem; }
.live-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
.hero h1 { font-size: clamp(1.8rem, 5vw, 3rem); font-weight: 900; line-height: 1.1; }
.hero h1 span { color: var(--accent); }
.stats-row { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; margin-top: 1.25rem; }
.s-pill { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 0.4rem 0.9rem; font-size: 0.75rem; display: flex; gap: 6px; align-items: center; }
.s-pill .val { color: var(--accent); font-weight: 700; }
.s-pill .dn { color: var(--red); font-weight: 700; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.25rem; cursor: pointer; transition: border-color 0.2s, transform 0.2s; }
.card:hover { border-color: var(--accent); transform: translateY(-2px); }
.cat-tag { display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.6rem; background: rgba(0,200,100,0.08); color: var(--accent); border: 1px solid rgba(0,200,100,0.2); }
.card h3 { font-size: 0.95rem; font-weight: 700; line-height: 1.4; margin-bottom: 0.5rem; }
.card p { font-size: 0.8rem; color: var(--muted); line-height: 1.6; margin-bottom: 0.75rem; }
.card-meta { display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--muted); border-top: 1px solid var(--border); padding-top: 0.6rem; }
.mode-toggle { background: var(--surface); border: 1px solid var(--border); color: var(--text); padding: 0.35rem 0.7rem; border-radius: 6px; cursor: pointer; font-size: 0.8rem; }
footer { border-top: 1px solid var(--border); padding: 2rem 5%; text-align: center; margin-top: 3rem; }
.f-brand { font-size: 1.1rem; font-weight: 800; margin-bottom: 0.4rem; }
.f-brand span { color: var(--accent); }
.f-legal { font-size: 0.7rem; color: var(--muted); margin-top: 0.5rem; }
.f-legal a { color: var(--accent); text-decoration: none; }
body.light-mode { --bg: #f1f5f9; --surface: #fff; --card: #fff; --text: #0f172a; --muted: #64748b; --border: rgba(0,150,80,0.15); }
</style>
"""
def _build_index(latest, archive, flock_name, date_str, ads_config=None):
    articles_html = ""
    for a in latest:
        excerpt = a.get("body", "").replace('#','').replace('*','').replace('\n',' ').strip()[:120] + "..."
        articles_html += f"""
            <div class="card" onclick="window.location.href='{a['filename']}'">
                <div class="cat-tag">{a['category']}</div>
                <h3>{a['headline']}</h3>
                <p>{excerpt}</p>
                <div class="card-meta">
                    <span>{a['source']}</span>
                    <span>{a['date_display']}</span>
                </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketFlock | Market & Crypto Intelligence</title>
    {COMMON_CSS}
</head>
<body>
    <header>
        <a href="/" class="logo-wrap">
            <div class="logo-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>
            </div>
            <div class="logo-text">Market<span>Flock</span></div>
        </a>
        <button class="mode-toggle" id="mode-btn" onclick="toggleMode()">🌙</button>
    </header>

    <div class="ticker-wrap">
        <div class="ticker-inner">
            <span class="t-item">BTC <span class="t-up">▲</span> Live</span>
            <span class="t-item">ETH <span class="t-up">▲</span> Live</span>
            <span class="t-item">BNB <span class="t-up">▲</span> Live</span>
            <span class="t-item">Gold <span class="t-na">◆</span> Spot</span>
            <span class="t-item">NSE <span class="t-up">▲</span> Live</span>
            <span class="t-item">BSE <span class="t-up">▲</span> Live</span>
            <span class="t-item">USD/INR <span class="t-na">◆</span> Forex</span>
            <span class="t-item">Crude Oil <span class="t-dn">▼</span> Live</span>
            <span class="t-item">S&P 500 <span class="t-up">▲</span> Live</span>
            <span class="t-item">BTC <span class="t-up">▲</span> Live</span>
            <span class="t-item">ETH <span class="t-up">▲</span> Live</span>
            <span class="t-item">BNB <span class="t-up">▲</span> Live</span>
            <span class="t-item">Gold <span class="t-na">◆</span> Spot</span>
            <span class="t-item">NSE <span class="t-up">▲</span> Live</span>
            <span class="t-item">BSE <span class="t-up">▲</span> Live</span>
            <span class="t-item">USD/INR <span class="t-na">◆</span> Forex</span>
            <span class="t-item">Crude Oil <span class="t-dn">▼</span> Live</span>
            <span class="t-item">S&P 500 <span class="t-up">▲</span> Live</span>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <div class="live-badge"><span class="live-dot"></span> MARKETS LIVE</div>
            <h1>Market <span>Intelligence</span><br>Powered by AI</h1>
            <div class="stats-row">
                <div class="s-pill">Crypto <span class="val">Live</span></div>
                <div class="s-pill">Stocks <span class="val">BSE/NSE</span></div>
                <div class="s-pill">Forex <span class="val">24/7</span></div>
                <div class="s-pill">Commodity <span class="val">Gold/Oil</span></div>
            </div>
        </div>

        <div class="grid">
            {articles_html}
        </div>
    </div>

    <footer>
        <div class="logo-text f-logo">Market<span>Flock</span></div>
        <p style="color: var(--text-dim)">AI-Powered Market & Crypto Intelligence</p>
        <div class="legal">
            🤖 Engine: MarketFlock Agent • Domain: <a href="https://market.cutbar.in" style="color: var(--accent-secondary); text-decoration: none; font-weight: 700;">market.cutbar.in</a> • &copy; 2026
        </div>
        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-glow);">
            <p style="font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 1rem;">MarketFlock Network</p>
            <a href="https://market.cutbar.in" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px 20px; border-radius: 12px; border: 1px solid rgba(255,51,68,0.2); transition: var(--transition);">
                <div style="width: 30px; height: 30px; background: #00b894; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 0.8rem;">AF</div>
                <div style="text-align: left;">
                    <div style="color: white; font-weight: 800; font-size: 0.9rem;">Market<span>Flock</span></div>
                    <div style="color: #666; font-size: 0.6rem;">Market & Crypto Intelligence Hub</div>
                </div>
            </a>
        </div>
    </footer>
    {COMMON_JS}
</body>
</html>"""

def _build_article_page(a, ads_config=None):
    bh_html = ""
    content_parts = a["body"].split('\n')
    for p in content_parts:
        p = p.strip()
        if not p: continue
        clean_p = p.replace('*', '')
        if clean_p.startswith('# '):
            bh_html += f'<h2 style="color: #fff; margin-top: 3rem; margin-bottom: 1.5rem;">{clean_p[2:]}</h2>'
        elif clean_p.startswith('## '):
            bh_html += f'<h3 style="color: var(--accent-primary); margin-top: 2rem; margin-bottom: 1rem;">{clean_p[3:]}</h3>'
        else:
            bh_html += f'<p style="color: var(--text-dim); font-size: 1.25rem; margin-bottom: 1.5rem; line-height: 1.8;">{clean_p}</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a['headline']} | MarketFlock</title>
    {COMMON_CSS}
    <style>
        .art-wrap {{ max-width: 900px; margin: 4rem auto; padding: 0 5%; }}
        .back-link {{ display: inline-block; margin-bottom: 3rem; color: var(--accent-secondary); text-decoration: none; font-weight: 700; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; }}
        h1 {{ font-size: clamp(2rem, 6vw, 3.5rem); font-weight: 900; line-height: 1.1; margin-bottom: 2rem; color: #fff; }}
    </style>
</head>
<body>
    <div id="bg-canvas">
        <div class="orb" style="top: -10%; right: -10%; width: 600px; height: 600px; background: var(--accent-glow);"></div>
    </div>

    <header>
        <a href="/" class="logo-wrap">
            <div class="logo-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
            </div>
            <div class="logo-text">Market<span>Flock</span></div>
        </a>
        <div class="nav-actions">
            <button class="mode-toggle" id="mode-btn" onclick="toggleMode()">🌙</button>
        </div>
    </header>
    
    <div class="art-wrap">
        <a href="index.html" class="back-link">&larr; Return to Signals</a>
        <div class="tag" style="margin-bottom: 1rem;">{a['category']}</div>
        <h1>{a['headline']}</h1>
        <div class="card-foot" style="margin-bottom: 4rem; border-top: none; padding-top: 0;">
            <span>Source: {a['source']}</span>
            <span>{a['date_display']}</span>
        </div>
        <div class="content">
            {bh_html}
        </div>
    </div>

    <footer>
        <div class="logo-text f-logo">Market<span>Flock</span></div>
        <div class="legal">
            🤖 Engine: MarketFlock Agent • Domain: <a href="https://market.cutbar.in" style="color: var(--accent-secondary); text-decoration: none; font-weight: 700;">market.cutbar.in</a>
        </div>
        <div style="margin-top: 2rem;">
            <a href="https://market.cutbar.in" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px 20px; border-radius: 12px; border: 1px solid rgba(255,51,68,0.2); transition: var(--transition);">
                <div style="width: 25px; height: 25px; background: #00b894; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 0.7rem;">AF</div>
                <div style="color: white; font-weight: 800; font-size: 0.8rem;">Market<span>Flock</span></div>
            </a>
        </div>
    </footer>
    {COMMON_JS}
</body>
</html>"""



def _generate_sitemap(history, site_dir):
    # 1. Standard Sitemap
    urls = ['https://market.cutbar.in/']
    for a in history:
        urls.append(f"https://market.cutbar.in/{a['filename']}")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f'  <url><loc>{url}</loc></url>\n'
    sitemap += '</urlset>'

    with open(f"{site_dir}/sitemap.xml", "w") as f:
        f.write(sitemap)

    # 2. Google News Sitemap (Last 2 days only)
    news_sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    news_sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n'
    
    # Google News only wants articles from the last 48 hours
    for a in history[:15]:
        pub_date = a.get('published_at', datetime.now().isoformat())
        news_sitemap += '  <url>\n'
        news_sitemap += f'    <loc>https://market.cutbar.in/{a["filename"]}</loc>\n'
        news_sitemap += '    <news:news>\n'
        news_sitemap += '      <news:publication>\n'
        news_sitemap += '        <news:name>MarketFlock Intelligence</news:name>\n'
        news_sitemap += '        <news:language>en</news:language>\n'
        news_sitemap += '      </news:publication>\n'
        news_sitemap += f'      <news:publication_date>{pub_date}</news:publication_date>\n'
        news_sitemap += f'      <news:title>{a["headline"].replace("&", "&amp;")}</news:title>\n'
        news_sitemap += '    </news:news>\n'
        news_sitemap += '  </url>\n'
    
    news_sitemap += '</urlset>'
    
    with open(f"{site_dir}/news-sitemap.xml", "w") as f:
        f.write(news_sitemap)

if __name__ == "__main__":
    run()
