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

def _normalize_autoflock_article(article):
    replacements = {
        "NewsHour Intelligence": "Auto Flock Intelligence",
        "NewsHour Signal Engine": "Auto Flock Signal Engine",
        "NewsHour Flock": "Auto Flock",
        "News Hour Flock": "Auto Flock",
        "https://newshour.cutbar.in": "https://autoflock.cutbar.in",
        "https://www.newshour.cutbar.in": "https://autoflock.cutbar.in",
        "https://cutbar.in/": "https://autoflock.cutbar.in/",
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
    
    current_articles = [_normalize_autoflock_article(a) for a in current_articles]
    history = [_normalize_autoflock_article(a) for a in history]
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
        f.write("User-agent: *\nAllow: /\nSitemap: https://autoflock.cutbar.in/sitemap.xml")

    for a in history:
        content = _build_article_page(a, ads_config)
        with open(f"{SITE_DIR}/{a['filename']}", "w", encoding="utf-8") as f: f.write(content)

    print(f"🐑 SHEEP 8: Files generated in {SITE_DIR}. Ready for Git Sync.")
    return {"published": True}

def _load_config(path):
    with open(path) as f: return json.load(f)

COMMON_CSS = """
<link rel="stylesheet" href="style.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
"""

COMMON_JS = """
<script>
    function toggleMode() {
        const body = document.body;
        const btn = document.getElementById('mode-btn');
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');
        localStorage.setItem('flock-theme', isLight ? 'light' : 'dark');
        btn.innerText = isLight ? '☀️' : '🌙';
    }

    function initMode() {
        const theme = localStorage.getItem('flock-theme') || 'dark';
        if (theme === 'light') {
            document.body.classList.add('light-mode');
            document.getElementById('mode-btn').innerText = '☀️';
        }
    }
    window.onload = initMode;
</script>
"""

def _build_index(latest, archive, flock_name, date_str, ads_config=None):
    articles_html = ""
    for a in latest:
        excerpt = a.get("body", "").replace('#','').replace('*','').replace('\n',' ').strip()[:120] + "..."
        articles_html += f"""
            <div class="pro-card" onclick="window.location.href='{a['filename']}'">
                <div class="tag">{a['category']}</div>
                <h3>{a['headline']}</h3>
                <p>{excerpt}</p>
                <div class="card-foot">
                    <span>{a['source']}</span>
                    <span>{a['date_display']}</span>
                </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Flock | AI & Terminal Intelligence</title>
    {COMMON_CSS}
</head>
<body>
    <div id="bg-canvas">
        <div class="orb" style="top: 10%; left: 10%; width: 400px; height: 400px; background: var(--accent-primary);"></div>
        <div class="orb" style="bottom: 10%; right: 10%; width: 300px; height: 300px; background: var(--accent-secondary);"></div>
    </div>

    <header>
        <a href="/" class="logo-wrap">
            <div class="logo-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
            </div>
            <div class="logo-text">Auto <span>Flock</span></div>
        </a>
        <div class="nav-actions">
            <button class="mode-toggle" id="mode-btn" onclick="toggleMode()">🌙</button>
        </div>
    </header>

    <div class="container">
        <div style="text-align: center; margin-bottom: 5rem;">
            <div class="tag" style="margin-bottom: 1rem; color: var(--accent-primary)">System Operational</div>
            <h1 style="font-size: clamp(2.5rem, 8vw, 4.5rem); font-weight: 900; letter-spacing: -2px; line-height: 0.9;">
                Autonomous <br><span style="color: var(--accent-primary)">AI Signals</span>
            </h1>
        </div>

        <div class="pro-grid">
            {articles_html}
        </div>
    </div>

    <footer>
        <div class="logo-text f-logo">Auto <span>Flock</span></div>
        <p style="color: var(--text-dim)">Autonomous Journalism for the Agentic Era</p>
        <div class="legal">
            🤖 Engine: Auto Flock Agent • Domain: <a href="https://autoflock.cutbar.in" style="color: var(--accent-secondary); text-decoration: none; font-weight: 700;">autoflock.cutbar.in</a> • &copy; 2026
        </div>
        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-glow);">
            <p style="font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 1rem;">Autoflock Network</p>
            <a href="https://autoflock.cutbar.in" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px 20px; border-radius: 12px; border: 1px solid rgba(255,51,68,0.2); transition: var(--transition);">
                <div style="width: 30px; height: 30px; background: #00ff88; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 0.8rem;">AF</div>
                <div style="text-align: left;">
                    <div style="color: white; font-weight: 800; font-size: 0.9rem;">Auto <span>Flock</span></div>
                    <div style="color: #666; font-size: 0.6rem;">AI & Terminal Intelligence Hub</div>
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
    <title>{a['headline']} | Auto Flock</title>
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
            <div class="logo-text">Auto <span>Flock</span></div>
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
        <div class="logo-text f-logo">Auto <span>Flock</span></div>
        <div class="legal">
            🤖 Engine: Auto Flock Agent • Domain: <a href="https://autoflock.cutbar.in" style="color: var(--accent-secondary); text-decoration: none; font-weight: 700;">autoflock.cutbar.in</a>
        </div>
        <div style="margin-top: 2rem;">
            <a href="https://autoflock.cutbar.in" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px 20px; border-radius: 12px; border: 1px solid rgba(255,51,68,0.2); transition: var(--transition);">
                <div style="width: 25px; height: 25px; background: #00ff88; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 0.7rem;">AF</div>
                <div style="color: white; font-weight: 800; font-size: 0.8rem;">Auto <span>Flock</span></div>
            </a>
        </div>
    </footer>
    {COMMON_JS}
</body>
</html>"""



def _generate_sitemap(history, site_dir):
    # 1. Standard Sitemap
    urls = ['https://autoflock.cutbar.in/']
    for a in history:
        urls.append(f"https://autoflock.cutbar.in/{a['filename']}")

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
        news_sitemap += f'    <loc>https://autoflock.cutbar.in/{a["filename"]}</loc>\n'
        news_sitemap += '    <news:news>\n'
        news_sitemap += '      <news:publication>\n'
        news_sitemap += '        <news:name>Auto Flock Intelligence</news:name>\n'
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
