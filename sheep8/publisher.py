import os
import json, os, hashlib, zipfile, time, subprocess, shutil, urllib.parse, random, re, html
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(PROJECT, "publish")
HISTORY_FILE = f"{PROJECT}/history.json"
BASE_URL = "https://market.cutbar.in"

# CSS moved to a central variable to ensure consistency
MARKETFLOCK_STYLE = """
:root {
  --bg-primary: #050505;
  --bg-secondary: #0a0a0c;
  --panel-bg: #111114;
  --accent-blue: #3b82f6;
  --accent-green: #10b981;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --border: #2d2d34;
}
body.light-mode { 
  --bg-primary: #ffffff; 
  --bg-secondary: #f8fafc; 
  --panel-bg: #ffffff; 
  --text-main: #0f172a; 
  --text-muted: #475569; 
  --border: #e2e8f0; 
}

@font-face {
  font-family: 'JameelNoori';
  src: url('/fonts/JameelNooriNastaleeq.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

* { box-sizing: border-box; }
body { 
  background-color: var(--bg-primary); 
  color: var(--text-main); 
  font-family: 'Inter', system-ui, sans-serif;
  margin: 0; line-height: 1.6;
  font-size: 18px;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* Force Nastaleeq for Urdu */
[dir="rtl"], body.ur, body.ur * { 
  font-family: 'JameelNoori', serif !important; 
  line-height: 2 !important;
  text-align: right !important;
}

h1, h2, h3, h4 { color: var(--text-main); font-weight: 800; }
p { color: var(--text-muted); }

.ai-header {
  background: rgba(10, 10, 12, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  padding: 1rem 5%;
  position: sticky; top: 0; z-index: 9999;
  display: flex; justify-content: space-between; align-items: center;
}
.brand { font-size: 1.5rem; font-weight: 800; color: var(--text-main); text-transform: uppercase; letter-spacing: -0.5px; }
.brand span { color: var(--accent-blue); }
.nav-controls { display: flex; gap: 0.75rem; align-items: center; }
.theme-btn, .lang-btn {
  background: var(--panel-bg); color: var(--text-main);
  border: 1px solid var(--border); padding: 0.5rem 0.8rem; border-radius: 8px; cursor: pointer; font-size: 0.8rem;
}
.lang-btn.active { border-color: var(--accent-blue); color: var(--accent-blue); }

.dashboard {
  display: grid;
  grid-template-columns: 1fr;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.pro-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
}

.pro-card {
  background: var(--panel-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid var(--border);
}
.card-content { padding: 1.5rem; flex: 1; }
.pro-card:hover { border-color: var(--accent-blue); transform: translateY(-3px); }
.tag { font-size: 0.7rem; color: var(--accent-blue); text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
h3 { font-size: 1.25rem; font-weight: 800; margin: 0.5rem 0; line-height: 1.4; color: var(--text-main); }
.card-foot { font-size: 0.8rem; color: var(--text-muted); display: flex; justify-content: space-between; margin-top: 1rem;}

.article-content { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }
.article-body { font-size: 1.1rem; line-height: 1.7; color: var(--text-main); }
.article-body h1, .article-body h2, .article-body h3 { 
    font-family: inherit; 
    color: var(--text-main); 
    margin-top: 2.5rem;
    margin-bottom: 1.2rem;
    font-weight: 700;
}
.article-body p { margin-bottom: 1.2rem; }

.affiliate-container {
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin: 3.5rem 0;
    backdrop-filter: blur(10px);
    text-align: center;
}
.affiliate-title {
    color: var(--text-main);
    margin-bottom: 1.8rem;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.affiliate-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 1.2rem;
}
.affiliate-card {
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
}
.affiliate-card:hover {
    background: rgba(59, 130, 246, 0.1);
    border-color: var(--accent-blue);
    transform: translateY(-3px);
}
.affiliate-card i { font-size: 1.8rem; color: var(--accent-blue); }
.affiliate-card span { color: var(--text-main); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }

.hero-img {
    width: 100%;
    height: 400px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
.source-link {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    font-size: 0.85rem;
    color: var(--text-muted);
    text-align: center;
}
.source-link a { color: var(--accent-blue); text-decoration: none; font-weight: 600; }

.ai-footer {
    padding: 4rem 1.5rem; background: var(--bg-primary); border-top: 1px solid var(--border);
    text-align: center;
}
.ai-footer-logo { font-size: 1.1rem; font-weight: 700; color: var(--text-main); text-transform: uppercase; margin-bottom: 0.5rem; }
.ai-footer-logo span { color: #0ff; }
.ai-footer-text { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.6; }
.ai-footer-bottom { font-size: 0.65rem; color: var(--text-muted); opacity: 0.5; text-transform: uppercase; letter-spacing: 2px; }

@media (max-width: 768px) {
    .hero-img { height: 220px; }
    .affiliate-grid { grid-template-columns: repeat(2, 1fr); }
    .article-body { font-size: 1.05rem; }
    .ai-header { padding: 1rem; }
    .brand { font-size: 1.2rem; }
}
"""

HEADER_HTML = """
    <header class="ai-header">
        <div class="brand">Market<span>Flock</span></div>
        <div class="nav-controls">
            <a href="/about.html" class="lang-btn" style="text-decoration:none; display:flex; align-items:center;">About</a>
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
        let TRANSLATIONS = {};
        fetch('/translations.json').then(r => r.json()).catch(()=>{ }).then(data => { if(data) TRANSLATIONS = data; applyLang(); });

        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            document.getElementById('themeToggle').innerText = isLight ? '☀️' : '🌙';
        }

        async function applyLang() {
            const lang = localStorage.getItem('lang') || 'en';
            document.documentElement.lang = lang;
            document.body.classList.toggle('ur', lang === 'ur');
            const btnEn = document.getElementById('btn-en');
            const btnUr = document.getElementById('btn-ur');
            if(btnEn) btnEn.classList.toggle('active', lang === 'en');
            if(btnUr) btnUr.classList.toggle('active', lang === 'ur');
            
            if(lang === 'ur') {
                document.documentElement.dir = 'rtl';
            } else {
                document.documentElement.dir = 'ltr';
            }

            const nodes = document.querySelectorAll('[data-trans]');
            if (lang === 'en') {
                nodes.forEach(el => {
                    if (el.hasAttribute('data-original')) {
                        el.innerHTML = el.getAttribute('data-original');
                    }
                });
                return;
            }

            for(let el of nodes) {
                const key = el.getAttribute('data-trans');
                const originalText = el.getAttribute('data-original') || el.innerText;
                if (!originalText || originalText.length < 2) continue;
                
                if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                    el.innerHTML = TRANSLATIONS[lang][key];
                } else {
                    try {
                        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${lang}&dt=t`;
                        const res = await fetch(url, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: `q=${encodeURIComponent(originalText)}`
                        });
                        const data = await res.json();
                        let translated = '';
                        if(data && data[0]) {
                            data[0].forEach(part => { if(part[0]) translated += part[0]; });
                        }
                        if(translated) {
                            if(!TRANSLATIONS[lang]) TRANSLATIONS[lang] = {};
                            TRANSLATIONS[lang][key] = translated;
                            el.innerHTML = translated;
                        }
                    } catch(e) {
                        console.error('Translation failed:', e);
                        el.innerHTML = originalText;
                    }
                }
            }
        }

        function setLang(lang) {
            localStorage.setItem('lang', lang);
            applyLang();
        }

        window.onload = function() {
            if (localStorage.getItem('theme') === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('themeToggle').innerText = '☀️';
            }
            applyLang();
        }
    </script>
"""

FOOTER_HTML = """
    <footer class="ai-footer">
        <div class="ai-footer-logo">Market <span>Flock</span></div>
        <p class="ai-footer-text" data-trans="footer_copy">© 2026 AI Flock Empire — MarketFlock Network | On-Chain Analytics</p>
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
    
    # Ensure font exists
    font_dir = f"{SITE_DIR}/fonts"
    os.makedirs(font_dir, exist_ok=True)
    font_src = os.path.expanduser("~/storage/downloads/Jameel Noori Nastaleeq Regular.ttf")
    if os.path.exists(font_src):
        shutil.copy(font_src, f"{font_dir}/JameelNooriNastaleeq.ttf")

    # Sync translations
    trans_src = f"{OUTPUT}/translations.json"
    if os.path.exists(trans_src):
        shutil.copy(trans_src, f"{SITE_DIR}/translations.json")
    
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

    # Write Style
    shutil.copy("/data/data/com.termux/files/home/projects/media/shared/styles/global.css", f"{SITE_DIR}/style.css")

    for a in history:
        slug = _slugify(a.get("headline", "article"))
        a["filename"] = f"{slug}.html"
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{a['filename']}", "w", encoding="utf-8") as f:
            f.write(content)

    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate About Page
    try:
        manifesto_path = os.path.join(os.path.dirname(PROJECT), "FlockHub", "manifesto.md")
        if os.path.exists(manifesto_path):
            with open(manifesto_path, "r") as f:
                manifesto_md = f.read()
            about_page = _build_article_page({
                "headline": "About Our Intelligence Network",
                "body": manifesto_md,
                "category": "Manifesto",
                "source": "FlockHub Agent",
                "source_url": "/",
                "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80"
            })
            with open(f"{SITE_DIR}/about.html", "w", encoding="utf-8") as f:
                f.write(about_page)
    except Exception as e:
        print(f"⚠ About Page Error: {e}")

    print(f"🐑 SHEEP 8: {len(history)} articles regenerated with new design ✓")
    return {"published": True}

def _build_index(latest):
    articles_html = ""
    for a in latest:
        excerpt = a.get("body", "").split("---")[0].replace('#','').replace('*','').strip()[:100] + "..."
        filename = a.get("filename", "#")
        img_url = a.get("image_url", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80")
        
        attr_hl = a['headline'].replace('"', '&quot;')
        attr_ex = excerpt.replace('"', '&quot;')
        
        articles_html += f"""
            <div class="pro-card" onclick="window.location.href='{filename}'">
                <img src="{img_url}" class="card-image" alt="{attr_hl}">
                <div class="card-content">
                    <div class="tag">{a['category']}</div>
                    <h3 data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</h3>
                    <p data-trans="{attr_ex}" data-original="{attr_ex}">{excerpt}</p>
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
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-theme">
{HEADER_HTML}
<div class="dashboard">
    <main>
        <div class="pro-grid">
            {articles_html}
        </div>
    </main>
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
    
    def wrap_trans(m):
        tag, inner = m.group(1), m.group(2)
        if not inner.strip() or len(inner) < 2: return m.group(0)
        attr = inner.replace('"', '&quot;')
        return f'<{tag} data-trans="{attr}" data-original="{attr}">{inner}</{tag}>'
    
    translated_body = re.sub(r'<(p|h[1-6]|li|th|td|figcaption)\b[^>]*>(.*?)</\1>', wrap_trans, body_html, flags=re.DOTALL|re.IGNORECASE)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a.get('headline', 'MarketFlock Intelligence')}</title>
    {a.get('meta', '')}
    <link rel="stylesheet" href="style.css">
</head>
<body class="article-page dark-theme">
    {HEADER_HTML}
    <main class="article-content">
        <article>
            <img src="{a['image_url']}" class="hero-img" alt="{a['headline']}">
            <div class="article-body">
                {translated_body}
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
