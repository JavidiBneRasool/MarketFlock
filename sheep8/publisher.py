import json, os, hashlib, zipfile, time, subprocess, shutil, urllib.parse, random, re, html
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
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
            .ai-header {
                position: sticky; top: 0; z-index: 9999; width: 100%;
                background: rgba(5, 5, 5, 0.8); backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--border);
                font-family: 'Space Grotesk', sans-serif;
                padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center;
            }
            .brand { font-size: 1.5rem; font-weight: 800; color: var(--text-main); text-transform: uppercase; letter-spacing: -0.5px; }
            .brand span { color: var(--accent-blue); }
            .nav-controls { display: flex; gap: 0.75rem; align-items: center; }
            .theme-btn, .lang-btn {
                background: var(--panel-bg); color: var(--text-main);
                border: 1px solid var(--border); padding: 0.5rem 0.8rem; border-radius: 8px; cursor: pointer; font-size: 0.8rem;
            }
            .lang-btn.active { border-color: var(--accent-blue); color: var(--accent-blue); }
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
            document.body.classList.toggle('ur', lang === 'ur');
            const btnEn = document.getElementById('btn-en');
            const btnUr = document.getElementById('btn-ur');
            if(btnEn) btnEn.classList.toggle('active', lang === 'en');
            if(btnUr) btnUr.classList.toggle('active', lang === 'ur');
            
            // Basic RTL toggle
            if(lang === 'ur') {
                document.documentElement.dir = 'rtl';
            } else {
                document.documentElement.dir = 'ltr';
            }
        }
        window.onload = function() {
            if (localStorage.getItem('theme') === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('themeToggle').innerText = '☀️';
            }
            const savedLang = localStorage.getItem('lang') || 'en';
            setLang(savedLang);
        }
    </script>
"""

FOOTER_HTML = """
    <footer class="ai-footer">
        <style>
            .ai-footer {
                padding: 4rem 1.5rem; background: var(--bg-primary); border-top: 1px solid var(--border);
                font-family: 'Space Grotesk', sans-serif; text-align: center;
            }
            .ai-footer-logo { font-size: 1.1rem; font-weight: 700; color: var(--text-main); text-transform: uppercase; margin-bottom: 0.5rem; }
            .ai-footer-logo span { color: #0ff; }
            .ai-footer-text { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.6; }
            .ai-footer-bottom { font-size: 0.65rem; color: var(--text-muted); opacity: 0.5; text-transform: uppercase; letter-spacing: 2px; }
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

def _slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return slug[:100] or hashlib.md5(str(value).encode()).hexdigest()[:12]

def _markdown_to_html(value):
    if not value: return ""
    # Ensure headers have a space after # for reliable parsing
    value = re.sub(r'^(#+)([A-Za-z0-9])', r'\1 \2', str(value), flags=re.MULTILINE)
    try:
        import markdown
        return markdown.markdown(value, extensions=['extra'])
    except Exception:
        paragraphs = [p.strip() for p in str(value).split("\n\n") if p.strip()]
        return "\n".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)

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

    for a in history:
        slug = _slugify(a.get("headline", "article"))
        a["filename"] = f"{slug}.html"
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{a['filename']}", "w", encoding="utf-8") as f:
            f.write(content)

    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"🐑 SHEEP 8: {len(history)} articles regenerated with new design ✓")
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
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; color: var(--text-main);">{a['headline']}</h3>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">{excerpt}</p>
                    <div class="card-foot">
                        <span style="color: var(--text-muted);">{a['source']}</span>
                    </div>
                </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketFlock | Intelligence</title>
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-theme">
{HEADER_HTML}
<div class="dashboard">
    <aside class="sidebar"></aside>
    <main>
        <div class="pro-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
            {articles_html}
        </div>
    </main>
    <aside class="sidebar"></aside>
</div>
{FOOTER_HTML}
{COMMON_JS}
</body>
</html>"""

def _get_affiliate_block(category):
    c = category.lower()
    if 'crypto' in c or 'market' in c:
        branding = "Institutional-Grade Trading Infrastructure"
        links = [
            ("Binance", "https://accounts.binance.com/register?ref=V7G8123A", "fa-solid fa-chart-line"),
            ("Bybit", "https://partner.bybit.com/b/marketflock", "fa-solid fa-bolt"),
            ("TradingView", "https://www.tradingview.com/?aff_id=125672", "fa-solid fa-area-chart"),
            ("CoinGlass", "https://coinglass.com/", "fa-solid fa-glass-water"),
            ("Ledger", "https://shop.ledger.com/?r=marketflock", "fa-solid fa-shield-halved"),
            ("CWallet", "https://cwallet.com/", "fa-solid fa-wallet"),
            ("KuCoin", "https://www.kucoin.com/r/af/rBDP123", "fa-solid fa-coins")
        ]
    else:
        branding = "Market Intelligence: Optimize Your Stack"
        links = [("Market Intelligence", "#", "fa-solid fa-brain")]
    
    links_html = "".join([f'''
        <a href="{url}" class="affiliate-card">
            <i class="{icon}"></i>
            <span>{name}</span>
        </a>''' for name, url, icon in links])
    
    return f'''
    <div class="affiliate-container">
        <h4 class="affiliate-title">{branding}</h4>
        <div class="affiliate-grid">
            {links_html}
        </div>
    </div>
    '''

def _build_article_page(a):
    body_html = _markdown_to_html(a.get('body', ''))
    affiliate_block = _get_affiliate_block(a.get('category', 'Default'))
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a.get('headline', 'MarketFlock Intelligence')}</title>
    {a.get('meta', '')}
    <link rel="stylesheet" href="style.css">
    <style>
@font-face{{font-family:'JameelNoori';src:url('/fonts/JameelNooriNastaleeq.ttf') format('truetype')}}
        .article-content {{ max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }}
        .article-body {{ 
            font-size: 1.1rem; 
            line-height: 1.7; 
            color: var(--text-main); 
        }}
        .article-body h1, .article-body h2, .article-body h3 {{ 
            font-family: 'Space Grotesk', sans-serif; 
            color: var(--text-main); 
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            text-align: left;
            font-weight: 700;
        }}
        .article-body p {{ margin-bottom: 1.2rem; text-align: left; }}
        .article-body ul, .article-body ol {{ margin-bottom: 1.2rem; padding-left: 1.5rem; text-align: left; }}
        .article-body li {{ margin-bottom: 0.4rem; }}
        
        .article-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: rgba(255,255,255,0.02);
            border-radius: 8px;
            overflow: hidden;
            font-size: 0.95rem;
        }}
        .article-body th, .article-body td {{
            padding: 0.75rem;
            border: 1px solid var(--border);
            text-align: left;
            color: var(--text-main);
        }}
        .article-body th {{
            background: rgba(255,255,255,0.05);
            font-weight: 700;
        }}
        
        /* Affiliate Grid Styles */
        .affiliate-container {{
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin: 3.5rem 0;
            backdrop-filter: blur(10px);
        }}
        .affiliate-title {{
            color: var(--text-main);
            margin-bottom: 1.8rem;
            font-size: 1.2rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.5px;
            font-family: 'Space Grotesk', sans-serif;
        }}
        .affiliate-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 1.2rem;
        }}
        .affiliate-card {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        .affiliate-card:hover {{
            background: rgba(59, 130, 246, 0.1);
            border-color: var(--accent-blue);
            transform: translateY(-3px);
        }}
        .affiliate-card i {{
            font-size: 1.8rem;
            color: var(--accent-blue);
        }}
        .affiliate-card span {{
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-align: center;
        }}
        
        .hero-img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .source-link {{
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            font-size: 0.85rem;
            color: var(--text-muted);
            text-align: center;
        }}
        .source-link a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        
        @media (max-width: 768px) {{
            .hero-img {{ height: 220px; }}
            .affiliate-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .article-body {{ font-size: 1.05rem; }}
        }}
    </style>
</head>
<body class="article-page dark-theme">
    {HEADER_HTML}
    <main class="article-content">
        <article>
            <img src="{a['image_url']}" class="hero-img" alt="{a['headline']}">
            <div class="article-body">
                {body_html}
                {affiliate_block}
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
