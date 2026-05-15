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
            
    cf = _load_config(f"{PROJECT}/config/cloudflare.json")
    env = os.environ.copy()
    env["CLOUDFLARE_API_TOKEN"] = cf["api_token"]
    env["CLOUDFLARE_ACCOUNT_ID"] = cf["account_id"]
    env["WRANGLER_SKIP_WORKERD_INSTALL"] = "1"
    
    wrangler_cmd = "wrangler" if shutil.which("wrangler") else "npx -y wrangler@2"
    cmd = f"{wrangler_cmd} pages publish {SITE_DIR} --project-name newshour --branch main --commit-dirty=true"
    
    print(f"🐑 SHEEP 8: Uploading assets...")
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True, timeout=120)
        if result.returncode == 0:
            print(f"🐑 SHEEP 8: Success! {flock_name} is LIVE.")
            return {"published": True}
        else:
            print(f"🐑 SHEEP 8: Wrangler Error: {result.stderr or result.stdout}")
            return {"published": False}
    except Exception as e:
        print(f"🐑 SHEEP 8: Failed: {e}")
        return {"published": False}

def _load_config(path):
    with open(path) as f: return json.load(f)

COMMON_CSS = """
<link rel="stylesheet" href="style.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
"""

COMMON_JS = """
<script>
    let TRANSLATIONS = {};
    fetch('/translations.json').then(r => r.json()).catch(()=>{}).then(data => { if(data) TRANSLATIONS = data; applyLang(); });

    function toggleTheme() {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        document.getElementById('themeToggle').innerText = isLight ? '☀️' : '🌙';
    }

    function applyTheme() {
        const theme = localStorage.getItem('theme') || 'dark';
        if (theme === 'light') {
            document.body.classList.add('light-mode');
            const toggle = document.getElementById('themeToggle');
            if(toggle) toggle.innerText = '☀️';
        }
    }
    applyTheme();

    async function applyLang() {
        const lang = localStorage.getItem('lang') || 'en';
        document.body.classList.toggle('ur', lang === 'ur');
        const btnEn = document.getElementById('btn-en');
        const btnUr = document.getElementById('btn-ur');
        if(btnEn) btnEn.classList.toggle('active', lang === 'en');
        if(btnUr) btnUr.classList.toggle('active', lang === 'ur');
        
        const nodes = document.querySelectorAll('[data-trans]');
        
        if (lang === 'en') {
            nodes.forEach(el => {
                if (el.hasAttribute('data-original')) {
                    el.innerHTML = el.getAttribute('data-original');
                } else {
                    const key = el.getAttribute('data-trans');
                    if (TRANSLATIONS['en'] && TRANSLATIONS['en'][key]) el.innerHTML = TRANSLATIONS['en'][key];
                }
            });
            return;
        }

        for(let el of nodes) {
            const key = el.getAttribute('data-trans');
            const originalText = el.getAttribute('data-original') || key;
            
            if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                el.innerHTML = TRANSLATIONS[lang][key];
            } else if (originalText && originalText.length > 1 && originalText !== 'AI Flock' && (!TRANSLATIONS[lang] || !TRANSLATIONS[lang][key])) {
                try {
                    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${lang}&dt=t&q=${encodeURIComponent(originalText)}`;
                    const res = await fetch(url);
                    const data = await res.json();
                    let translated = '';
                    if(data && data[0]) {
                        data[0].forEach(part => {
                            if(part[0]) translated += part[0];
                        });
                    }
                    if(translated) {
                        if(!TRANSLATIONS[lang]) TRANSLATIONS[lang] = {};
                        TRANSLATIONS[lang][key] = translated;
                        el.innerHTML = translated;
                    }
                } catch(e) {
                    console.error('Translation failed for', originalText);
                    el.innerHTML = originalText;
                }
            }
        }
    }

    function setLang(lang) {
        localStorage.setItem('lang', lang);
        applyLang();
    }

    // Admin Button Logic
    (function() {
        const API_URL = 'http://localhost:8765';
        const adminBtn = document.getElementById('adminBtn');
        if (!adminBtn) return;

        // Check if local API is running
        fetch(API_URL)
            .then(r => r.json())
            .then(data => {
                if (data.name === 'NewsHour Flock API') {
                    adminBtn.style.display = 'block';
                }
            })
            .catch(() => {
                // API not reachable, keep button hidden
            });

        window.triggerFlock = function() {
            if (adminBtn.classList.contains('running')) return;
            
            adminBtn.classList.add('running');
            adminBtn.innerText = 'RUNNING FLOCK...';

            fetch(API_URL + '/api/run-flock')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ Flock Cycle Complete!');
                        location.reload();
                    } else {
                        alert('❌ Error: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(err => {
                    alert('❌ Connection failed to local API');
                })
                .finally(() => {
                    adminBtn.classList.remove('running');
                    adminBtn.innerText = 'TRIGGER FLOCK';
                });
        };
    })();
</script>
"""

def _build_index(latest, archive, flock_name, date_str, ads_config=None):
    articles_html = ""
    for a in latest:
        articles_html += f"""
            <div class="card" onclick="window.location.href='{a['filename']}'">
                <div class="card-tag">{a['category']}</div>
                <h3>{a['headline']}</h3>
                <div class="card-meta">
                    <span>Source: {a['source']}</span>
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
        <div class="glow-orb" style="top: 10%; left: 20%;"></div>
        <div class="glow-orb" style="top: 60%; left: 70%; background: radial-gradient(circle, rgba(180, 143, 255, 0.05) 0%, transparent 70%);"></div>
    </div>

    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
            </div>
            <div class="logo-text">Auto <span>Flock</span></div>
        </div>
        <nav>
            <a href="index.html">Intelligence</a>
            <a href="about.html">Architecture</a>
            <a href="contact.html">Terminal</a>
        </nav>
    </header>

    <section class="hero">
        <div class="badge">System Operational</div>
        <h1>Autonomous AI <span>Signals</span></h1>
        <p>Real-time intelligence on AI tools, agentic workflows, and terminal mastery. Curated by 9 autonomous journalist bots.</p>
    </section>

    <div class="container">
        <div class="grid" id="article-grid">
            {articles_html}
        </div>
    </div>

    <footer>
        <div class="logo-text" style="font-size: 1.2rem;">Auto <span>Flock</span></div>
        <p style="margin-top: 10px; color: #666;">Autonomous Journalism for the Modern Developer</p>
        <div class="footer-info">
            🤖 Generated by Auto Flock Agent • Running on Termux + Cloudflare Pages<br>
            &copy; 2026 Auto Flock. All signals encrypted.
        </div>
    </footer>
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
            bh_html += f'<h2 class="subheading">{clean_p[2:]}</h2>'
        elif clean_p.startswith('## '):
            bh_html += f'<h3 class="subheading">{clean_p[3:]}</h3>'
        else:
            bh_html += f'<p>{clean_p}</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a['headline']} | Auto Flock</title>
    {COMMON_CSS}
    <style>
        .article-body {{ max-width: 800px; margin: 0 auto; padding: 4rem 5%; }}
        .article-body h1 {{ font-size: 3rem; margin-bottom: 2rem; color: #fff; }}
        .article-body p {{ margin-bottom: 1.5rem; color: #aaa; font-size: 1.2rem; }}
        .article-body .subheading {{ color: var(--accent-primary); margin-top: 2rem; margin-bottom: 1rem; }}
        .back-btn {{ display: inline-block; margin-bottom: 2rem; color: var(--accent-secondary); text-decoration: none; font-weight: 700; }}
    </style>
</head>
<body>
    <div id="bg-canvas">
        <div class="glow-orb" style="top: -10%; left: -10%;"></div>
    </div>
    
    <div class="article-body">
        <a href="index.html" class="back-btn">&larr; Back to Intelligence</a>
        <div class="card-tag">{a['category']}</div>
        <h1>{a['headline']}</h1>
        <div class="card-meta" style="margin-bottom: 3rem;">
            <span>Source: {a['source']}</span> | <span>{a['date_display']}</span>
        </div>
        {bh_html}
    </div>

    <footer>
        <div class="logo-text" style="font-size: 1.2rem;">Auto <span>Flock</span></div>
        <div class="footer-info">
            🤖 Generated by Auto Flock Agent
        </div>
    </footer>
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
        news_sitemap += '        <news:name>NewsHour Intelligence</news:name>\n'
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
