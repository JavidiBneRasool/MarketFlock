import json, os, hashlib, requests, zipfile, time, subprocess, shutil, urllib.parse, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(PROJECT, "publish")
HISTORY_FILE = f"{PROJECT}/history.json"
BASE_URL = "https://market.cutbar.in"

HEADER_HTML = """
    <header class="ai-header">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');
            .ai-header {
                position: sticky; top: 0; z-index: 9999; width: 100%;
                background: rgba(5, 5, 5, 0.8); backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--border);
                font-family: 'Space Grotesk', sans-serif;
                padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center;
            }
            .brand { font-size: 1.5rem; font-weight: 800; color: #fff; text-transform: uppercase; letter-spacing: -0.5px; }
            .brand span { color: var(--accent-blue); }
            .nav-controls { display: flex; gap: 0.75rem; align-items: center; }
            .theme-btn, .lang-btn {
                background: var(--panel-bg); color: var(--text-main);
                border: 1px solid var(--border); padding: 0.5rem 0.8rem; border-radius: 8px; cursor: pointer; font-size: 0.8rem;
            }
            .lang-btn.active { border-color: var(--accent-blue); }
        </style>
        <div class="brand">Market<span>Flock</span></div>
        <div class="nav-controls">
            <button class="theme-btn" id="themeToggle" onclick="toggleTheme()">🌙</button>
            <div class="lang-toggle">
                <button class="lang-btn active" id="btn-en" onclick="setLang('en')">EN</button>
                <button class="lang-btn" id="btn-ur" onclick="setLang('ur')">UR</button>
            </div>
        </div>
    </header>
"""

COMMON_JS = """
    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            document.getElementById('themeToggle').innerText = isLight ? '☀️' : '🌙';
        }
        function setLang(lang) {
            localStorage.setItem('lang', lang);
            location.reload();
        }
        window.onload = function() {
            if (localStorage.getItem('theme') === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('themeToggle').innerText = '☀️';
            }
        }
    </script>
"""

FOOTER_HTML = """
    <footer class="ai-footer">
        <style>
            .ai-footer {
                padding: 4rem 1.5rem; background: #050505; border-top: 1px solid rgba(255, 255, 255, 0.05);
                font-family: 'Space Grotesk', sans-serif; text-align: center;
            }
            .ai-footer-logo { font-size: 1.1rem; font-weight: 700; color: #fff; text-transform: uppercase; margin-bottom: 0.5rem; }
            .ai-footer-logo span { color: #0ff; }
            .ai-footer-text { font-size: 0.8rem; color: rgba(255, 255, 255, 0.3); margin-bottom: 1.5rem; line-height: 1.6; }
            .ai-footer-bottom { font-size: 0.65rem; color: rgba(255, 255, 255, 0.15); text-transform: uppercase; letter-spacing: 2px; }
        </style>
        <div class="ai-footer-logo">Market <span>Flock</span></div>
        <p class="ai-footer-text">© 2026 AI Flock Empire — MarketFlock Network | On-Chain Analytics</p>
        <div class="ai-footer-bottom">System Status: Optimal • Protocol: X-7 Neural</div>
    </footer>
"""

def _pick_unique_image(headline, category, used_set):
    return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"

def _normalize_autoflock_article(article):
    replacements = {
        "Auto Flock Intelligence": "MarketFlock Intelligence",
        "Auto Flock Signal Engine": "MarketFlock Signal Engine",
        "Auto Flock": "MarketFlock",
        "https://autoflock.cutbar.in": "https://market.cutbar.in",
    }
    for key in ("body", "summary", "description"):
        value = article.get(key)
        if isinstance(value, str):
            for old, new in replacements.items():
                value = value.replace(old, new)
            article[key] = value
    return article

def run():
    print("🐑 SHEEP 8: Publishing Expert Signals...")
    os.makedirs(SITE_DIR, exist_ok=True)
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            current_articles = json.load(f)
    except:
        print("🐑 SHEEP 8: No articles!"); return None
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    current_articles = [_normalize_autoflock_article(a) for a in current_articles]
    history = current_articles + history
    history = history[:150]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    for a in current_articles:
        filename = a.get("filename", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.html")
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{filename}", "w", encoding="utf-8") as f:
            f.write(content)

    print(f"🐑 SHEEP 8: {len(current_articles)} SEO-optimized articles published ✓")
    return {"published": True}

def _build_index(latest):
    articles_html = ""
    for a in latest:
        excerpt = a.get("body", "").split("---")[0].replace('#','').replace('*','').strip()[:100] + "..."
        filename = a.get("filename", "#")
        img_url = a.get("image_url", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80")
        articles_html += f"""
            <div class="pro-card" onclick="window.location.href='{filename}'">
                <img src="{img_url}" class="card-image" alt="{a['headline']}">
                <div class="card-content">
                    <div class="tag">{a['category']}</div>
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem;">{a['headline']}</h3>
                    <p>{excerpt}</p>
                    <div class="card-foot">
                        <span>{a['source']}</span>
                    </div>
                </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketFlock | Intelligence</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-theme">
{HEADER_HTML}
<div class="dashboard">
    <aside class="sidebar"></aside>
    <main>
        <div class="pro-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem;">
            {articles_html}
        </div>
    </main>
    <aside class="sidebar"></aside>
</div>
{FOOTER_HTML}
{COMMON_JS}
</body>
</html>"""

def _build_article_page(a):
    import markdown
    body_html = markdown.markdown(a['body'])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {a.get('meta', '')}
    <link rel="stylesheet" href="style.css">
    <style>
        .article-body {{ font-size: 1.35rem; line-height: 1.9; color: rgba(255, 255, 255, 0.8); }}
        .article-body h1, .article-body h2, .article-body h3 {{ font-family: 'Space Grotesk', sans-serif; color: #fff; margin-top: 2.5rem; }}
    </style>
</head>
<body class="article-page dark-theme">
    {HEADER_HTML}
    <main class="container">
        <article class="pro-card-expanded">
            <img src="{a['image_url']}" class="hero-img">
            <div class="article-body">
                {body_html}
            </div>
            <div class="source-link">
                Source: <a href="{a['source_url']}" target="_blank">{a['source']}</a>
            </div>
        </article>
    </main>
    {FOOTER_HTML}
    {COMMON_JS}
</body>
</html>"""

if __name__ == "__main__":
    run()
