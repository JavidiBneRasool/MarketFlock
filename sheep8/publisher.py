import json, os, hashlib, requests, zipfile, time, subprocess, shutil, urllib.parse, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(os.path.dirname(PROJECT), "newshour-site")
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
        f.write("User-agent: *\nAllow: /\nSitemap: https://cutbar.in/sitemap.xml")

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
<style>
@font-face{font-family:'JameelNoori';src:url('/fonts/JameelNooriNastaleeq.ttf') format('truetype')}
:root{
  --bg-base: #0b0b0c;
  --bg-surface: #141416;
  --bg-panel: rgba(255, 255, 255, 0.03);
  --accent-red: #ff3344;
  --accent-blue: #3399ff;
  --accent-green: #00e676;
  --accent-yellow: #ffea00;
  --text-main: #eaeaea;
  --text-muted: #8a8a8e;
  --border-color: rgba(255,255,255,0.04);
  --font-editorial: 'Inter', sans-serif;
}
body.light-mode {
  --bg-base: #ffffff;
  --bg-surface: #f8f9fa;
  --bg-panel: #ffffff;
  --text-main: #111111;
  --text-muted: #666666;
  --border-color: rgba(0,0,0,0.08);
}
body{
  background-color: var(--bg-base);
  color: var(--text-main);
  font-family: var(--font-editorial);
  line-height: 1.6;
  overflow-x: hidden;
  transition: background-color 0.3s ease, color 0.3s ease;
  margin: 0; padding: 0;
}
body.ur{font-family:'JameelNoori','Inter',sans-serif;direction:rtl;line-height:1.9;}
body.ur h1, body.ur h2, body.ur h3 { line-height: 1.6; }
body.ur .meta-info { flex-direction: row-reverse; }

.navbar{position:fixed;top:0;width:100%;height:60px;padding:0 5%;background:var(--bg-surface);border-bottom:1px solid var(--border-color);z-index:1000;display:flex;justify-content:space-between;align-items:center;transition:background 0.3s;box-sizing:border-box;}
.logo{display:flex;align-items:center;gap:.6rem;text-decoration:none}
.logo-icon{width:34px;height:34px;background:var(--accent-red);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:.95rem;box-shadow:0 4px 12px rgba(255,51,68,0.3);flex-shrink:0;}
.brand-name{font-size:1.05rem;font-weight:800;color:var(--text-main);letter-spacing:-0.3px;}
.lang-toggle{display:flex;gap:.75rem;font-weight:700;font-size:0.82rem}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.5}}
.lang-btn{cursor:pointer;color:var(--text-muted);text-decoration:none;transition:color .3s}
.lang-btn:hover, .lang-btn.active{color:var(--accent-red)}
footer{padding:4rem 5%;border-top:1px solid var(--border-color);text-align:center;color:var(--text-muted);font-size:14px;background:var(--bg-base);transition:background 0.3s;}
.bg-glow{
  position:fixed;top:-20vh;left:-10vw;width:60vw;height:60vh;
  background:radial-gradient(circle, rgba(255,51,68,0.04) 0%, rgba(11,11,12,0) 70%);
  z-index:-1;pointer-events:none;
}
.admin-btn {
  display: none;
  background: var(--accent-blue);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(51, 153, 255, 0.3);
}
.admin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(51, 153, 255, 0.4);
}
.admin-btn.running {
  background: var(--text-muted);
  cursor: not-allowed;
  animation: pulse 1.5s infinite;
}
</style>
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
    ticker = " • ".join([a['headline'] for a in latest]) + " • "
    ads_tag = ads_config["script_tag"] if ads_config else ""
    
    def get_accent(cat):
        c = cat.lower()
        if 'tech' in c or 'sci' in c: return 'var(--accent-blue)'
        if 'market' in c or 'econ' in c or 'biz' in c or 'india' in c: return 'var(--accent-green)'
        if 'politic' in c or 'world' in c or 'analysis' in c: return 'var(--accent-yellow)'
        return 'var(--accent-red)'

    hero_html = ""
    if latest:
        a = latest[0]
        excerpt = a["body"].replace('#','').replace('*','').replace('\n',' ').strip()[:180] + "..."
        accent = get_accent(a['category'])
        attr_hl = a['headline'].replace('"', '&quot;')
        hero_html = f"""
            <article class="hero-card fade-in">
                <a href="/{a['filename']}" class="card-link"></a>
                <div class="card-image-wrapper">
                    <img src="{a['image_url']}" alt="{attr_hl}" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80';">
                    <div class="gradient-overlay"></div>
                </div>
                <div class="hero-content">
                    <div class="meta-row">
                        <span class="category-badge" style="--cat-color: {accent}">{a['category']}</span>
                        <span class="breaking-pulse">BREAKING</span>
                    </div>
                    <h2 data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</h2>
                    <p>{excerpt}</p>
                    <div class="card-footer">
                        <span class="date">{a['date_display']}</span>
                        <span class="flock-tag"><i class="fas fa-robot"></i> <span data-trans="AI Flock" data-original="AI Flock">AI Flock</span></span>
                    </div>
                </div>
            </article>
        """

    secondary_html = ""
    for i, a in enumerate(latest[1:5]):
        excerpt = a["body"].replace('#','').replace('*','').replace('\n',' ').strip()[:100] + "..."
        accent = get_accent(a['category'])
        attr_hl = a['headline'].replace('"', '&quot;')
        delay = i * 0.1
        secondary_html += f"""
            <article class="standard-card fade-in" style="animation-delay: {delay}s;">
                <a href="/{a['filename']}" class="card-link"></a>
                <div class="card-image-wrapper">
                    <img src="{a['image_url']}" alt="{attr_hl}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80';">
                    <div class="gradient-overlay"></div>
                    <span class="category-badge" style="--cat-color: {accent}">{a['category']}</span>
                </div>
                <div class="standard-content">
                    <h3 data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</h3>
                    <div class="card-footer">
                        <span class="date">{a['date_display']}</span>
                    </div>
                </div>
            </article>
        """

    sidebar_html = ""
    for i, a in enumerate(latest[5:]):
        accent = get_accent(a['category'])
        attr_hl = a['headline'].replace('"', '&quot;')
        delay = i * 0.1
        sidebar_html += f"""
            <article class="compact-card fade-in" style="animation-delay: {delay}s;">
                <a href="/{a['filename']}" class="card-link"></a>
                <div class="compact-content">
                    <div class="meta-row">
                        <span class="category-dot" style="background: {accent}"></span>
                        <span class="category-text" style="color: {accent}">{a['category']}</span>
                    </div>
                    <h4 data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</h4>
                    <div class="date">{a['date_display']}</div>
                </div>
            </article>
        """

    ARCHIVE_PAGE_SIZE = 12
    archive_html = ""
    if archive:
        archive_html = '<div class="archive-section fade-in" id="archive"><h2 class="section-title" data-trans="past_editions" data-original="Intelligence Archive">Intelligence Archive</h2><div class="archive-grid" id="archive-items">'
        for i, a in enumerate(archive):
            page_num = (i // ARCHIVE_PAGE_SIZE) + 1
            attr_hl = a['headline'].replace('"', '&quot;')
            archive_html += f"""
                <div class="archive-item" data-page="{page_num}">
                    <div class="archive-meta">{a['date_display']} • {a['flock']}</div>
                    <a href="/{a['filename']}" class="archive-link" data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</a>
                </div>"""
        archive_html += '<div class="archive-pagination" id="archive-pagination"></div>'
        archive_html += '</div></div>'
        archive_html += f"""
<script>
(function(){{
  var ITEMS_PER_PAGE = {ARCHIVE_PAGE_SIZE};
  var items = document.querySelectorAll('#archive-items .archive-item[data-page]');
  if(!items.length) return;
  var totalPages = 0;
  items.forEach(function(el){{ var p = parseInt(el.dataset.page); if(p > totalPages) totalPages = p; }});
  var cur = 1;
  function show(n){{
    cur = n;
    items.forEach(function(el){{ el.style.display = parseInt(el.dataset.page) === n ? '' : 'none'; }});
    renderNav();
    var arch = document.getElementById('archive');
    if(arch) arch.scrollIntoView({{behavior:'smooth', block:'start'}});
  }}
  function renderNav(){{
    var c = document.getElementById('archive-pagination');
    if(!c) return;
    var h = '';
    if(cur > 1) h += '<button class="page-btn" onclick="window._archivePage(' + (cur-1) + ')">&#8592; Prev</button>';
    for(var i=1; i<=totalPages; i++){{
      if(i===1 || i===totalPages || (i>=cur-2 && i<=cur+2)){{
        h += '<button class="page-btn' + (i===cur?' active':'') + '" onclick="window._archivePage(' + i + ')">' + i + '</button>';
      }} else if(i===cur-3 || i===cur+3){{
        h += '<span class="page-ellipsis">…</span>';
      }}
    }}
    if(cur < totalPages) h += '<button class="page-btn" onclick="window._archivePage(' + (cur+1) + ')">Next &#8594;</button>';
    c.innerHTML = h;
  }}
  window._archivePage = show;
  show(1);
}})();
</script>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NewsHour - Intelligence Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{ads_tag}
{COMMON_CSS}
<style>
.container{{max-width:1440px;margin:76px auto 40px;padding:0 32px}}
.dashboard-grid {{display: grid; grid-template-columns: repeat(12, 1fr); gap: 32px; margin-top: 2rem;}}
.main-column {{grid-column: span 8; display: flex; flex-direction: column; gap: 32px;}}
.sidebar-column {{grid-column: span 4;}}
.sticky-sidebar {{position: sticky; top: 100px; display: flex; flex-direction: column; gap: 24px;}}
article {{
  position: relative; background: var(--bg-surface);
  border: 1px solid var(--border-color); border-radius: 16px;
  overflow: hidden; transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
}}
article:hover {{transform: translateY(-4px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: rgba(255,255,255,0.1);}}
body.light-mode article:hover {{box-shadow: 0 20px 40px rgba(0,0,0,0.05); border-color: rgba(0,0,0,0.1);}}
.card-link {{position: absolute; top:0; left:0; width:100%; height:100%; z-index: 10;}}
.card-image-wrapper {{position: relative; overflow: hidden; background: #111;}}
.card-image-wrapper img {{width: 100%; height: 100%; object-fit: cover; transition: transform 0.7s ease;}}
article:hover .card-image-wrapper img {{transform: scale(1.05);}}
.gradient-overlay {{position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, rgba(0,0,0,0) 20%, rgba(0,0,0,0.85) 100%); pointer-events: none;}}

.hero-card {{min-height: 440px; max-height: 440px; display: flex; flex-direction: column; justify-content: flex-end;}}
.hero-card .card-image-wrapper {{position: absolute; top:0; left:0; width:100%; height:100%; z-index: 0;}}
.hero-card .hero-content {{position: relative; z-index: 2; padding: 32px;}}
.hero-card h2 {{font-size: 26px; font-weight: 700; line-height: 1.65; margin-bottom: 12px; letter-spacing: -0.5px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.8);}}
.hero-card p {{font-size: 14px; color: #ddd; max-width: 80%; margin-bottom: 20px; line-height: 1.7; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-shadow: 0 1px 5px rgba(0,0,0,0.8);}}

.meta-row {{display: flex; align-items: center; gap: 12px; margin-bottom: 12px;}}
.category-badge {{background: rgba(255,255,255,0.05); color: var(--cat-color, #fff); padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);}}
.breaking-pulse {{color: var(--accent-red); font-size: 12px; font-weight: 800; letter-spacing: 1px; display: flex; align-items: center; gap: 6px;}}
.breaking-pulse::before {{content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--accent-red); box-shadow: 0 0 10px var(--accent-red); animation: pulse-dot 1.5s infinite;}}
@keyframes pulse-dot {{0% {{opacity: 1; transform: scale(1);}} 50% {{opacity: 0.4; transform: scale(1.2);}} 100% {{opacity: 1; transform: scale(1);}}}}

.secondary-grid {{display: grid; grid-template-columns: 1fr 1fr; gap: 24px;}}
.standard-card .card-image-wrapper {{aspect-ratio: 16/9; height: auto;}}
.standard-card .category-badge {{position: absolute; top: 12px; left: 12px; z-index: 2;}}
.standard-card .standard-content {{padding: 20px;}}
.standard-card h3 {{font-size: 16px; font-weight: 600; margin-bottom: 12px; line-height: 1.6; color: var(--text-main);}}

.compact-list {{display: flex; flex-direction: column; gap: 16px;}}
.compact-card {{padding: 16px; border-radius: 12px; background: var(--bg-surface); border: 1px solid var(--border-color); transition: background 0.3s;}}
.compact-card:hover {{background: var(--bg-panel); transform: translateX(4px);}}
.compact-card h4 {{font-size: 14px; font-weight: 500; line-height: 1.65; margin-bottom: 10px; color: var(--text-main);}}
.category-dot {{width: 8px; height: 8px; border-radius: 50%; display: inline-block;}}
.category-text {{font-size: 12px; font-weight: 700; text-transform: uppercase;}}
.date {{font-size: 13px; color: var(--text-muted);}}
.card-footer {{display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: var(--text-muted); margin-top: auto;}}

.fade-in {{animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; opacity: 0;}}
@keyframes fadeInUp {{from {{opacity: 0; transform: translateY(20px);}} to {{opacity: 1; transform: translateY(0);}}}}

.section-title {{font-size: 13px; font-weight: 800; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted);}}

.breaking-news{{position:fixed;bottom:0;width:100%;background:var(--bg-surface);backdrop-filter:blur(15px);border-top:1px solid rgba(255,51,68,0.3);padding:.75rem 2rem;z-index:999;display:flex;align-items:center;overflow:hidden;}}
.breaking-label{{background:var(--accent-red);color:#fff;padding:.2rem .8rem;font-weight:800;font-size:.8rem;border-radius:4px;margin-right:1.5rem;animation:pulse 2s infinite; letter-spacing: 1px;}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.7}}}}
.ticker-wrapper {{flex:1; overflow:hidden;}}
.ticker-text{{display:inline-block;padding-left:100%;animation:ticker 30s linear infinite;white-space:nowrap;color:var(--text-main); font-weight: 500; font-size: 14px;}}
@keyframes ticker{{0%{{transform:translate3d(0,0,0)}}100%{{transform:translate3d(-100%,0,0)}}}}

.archive-grid{{display:flex;flex-direction:column;gap:1.25rem;background:var(--bg-panel);padding:2rem;border-radius:20px;border:1px solid var(--border-color); margin-top: 40px;}}
.archive-item{{padding-bottom:1.25rem;border-bottom:1px solid var(--border-color)}}
.archive-item.hidden-article{{display:none}}
.archive-meta{{font-size:.75rem;color:var(--text-muted);font-weight:700;margin-bottom:.4rem;text-transform:uppercase;letter-spacing:1px}}
.archive-link{{font-size:15px;color:var(--text-main);text-decoration:none;font-weight:500; line-height:1.65; display:block;}}
.archive-link:hover{{color:var(--accent-blue);}}
.archive-pagination{{display:flex;gap:6px;align-items:center;justify-content:center;margin-top:1.5rem;flex-wrap:wrap;}}
.page-btn{{background:var(--bg-surface);border:1px solid var(--border-color);color:var(--text-muted);padding:8px 14px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600;transition:all .2s;min-width:40px;}}
.page-btn:hover{{border-color:var(--accent-blue);color:var(--accent-blue);}}
.page-btn.active{{background:var(--accent-red);border-color:var(--accent-red);color:#fff;}}
.page-ellipsis{{color:var(--text-muted);font-size:13px;padding:0 4px;}}

@media (max-width: 1024px) {{
  .dashboard-grid {{grid-template-columns: 1fr;}}
  .main-column, .sidebar-column {{grid-column: span 1;}}
}}
@media (max-width: 768px) {{
  .container {{padding: 0 14px; margin-top: 68px;}}
  .hero-card h2 {{font-size: 20px; line-height: 1.6;}}
  .hero-card p {{display: none;}}
  .hero-card {{min-height: 300px; max-height: 320px;}}
  .hero-card .hero-content {{padding: 20px;}}
  .standard-card h3 {{font-size: 15px;}}
  .secondary-grid {{grid-template-columns: 1fr;}}
  .archive-grid {{padding: 1.25rem;}}
}}
</style>
</head>
<body>
    <div class="bg-glow"></div>
    <nav class="navbar">
        <a href="/" class="logo"><div class="logo-icon">NH</div><div class="logo-text"><span class="brand-name">NewsHour</span></div></a>
        <div style="display:flex; align-items:center; gap: 1rem;">
            <button id="adminBtn" class="admin-btn" onclick="triggerFlock()">TRIGGER FLOCK</button>
            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" aria-label="Toggle Theme" style="background:transparent; border:none; font-size:1.2rem; cursor:pointer;">🌙</button>
            <div class="lang-toggle">
                <span class="lang-btn" id="btn-en" onclick="setLang('en')">EN</span>
                <span style="color:var(--text-muted)">|</span>
                <span class="lang-btn" id="btn-ur" onclick="setLang('ur')">اردو</span>
            </div>
            <div class="live-indicator" style="display:inline-flex;align-items:center;gap:.5rem;background:rgba(255,51,68,0.1);padding:.4rem 1rem;border-radius:20px;color:var(--accent-red);font-size:.75rem;font-weight:800; letter-spacing: 0.5px; border: 1px solid rgba(255,51,68,0.2);">
                <span class="live-dot" style="width:8px;height:8px;background-color:var(--accent-red);border-radius:50%;box-shadow:0 0 10px var(--accent-red);animation:blink 1.5s infinite;"></span> {flock_name.upper()}
            </div>
        </div>
    </nav>
    
    <div class="container">
        <header style="margin-bottom: 24px; margin-top: 24px;">
            <h2 class="section-title" style="border:none; padding:0; margin:0;" data-trans="latest_stories" data-original="Intelligence Feed">Intelligence Feed</h2>
        </header>
        
        <div class="dashboard-grid">
            <div class="main-column">
                {hero_html}
                <div class="secondary-grid">
                    {secondary_html}
                </div>
            </div>
            
            <div class="sidebar-column">
                <div class="sticky-sidebar">
                    <h3 class="section-title" data-trans="Trending Now" data-original="Trending Now">Trending Now</h3>
                    <div class="compact-list">
                        {sidebar_html}
                    </div>
                </div>
            </div>
        </div>
        
        {archive_html}
    </div>
    
    <div class="breaking-news">
        <span class="breaking-label" data-trans="breaking" data-original="BREAKING">BREAKING</span>
        <div class="ticker-wrapper"><span class="ticker-text">{ticker}</span></div>
    </div>
    
    <footer><p>© 2026 NewsHour Premium Intelligence — <span data-trans="ai_flock" data-original="Autonomous Journalism by AI Flock">Autonomous Journalism by AI Flock</span></p></footer>
    
    {COMMON_JS}
</body>
</html>"""

def _build_article_page(a, ads_config=None):
    ads_tag = ads_config["script_tag"] if ads_config else ""
    ad_unit = ""
    if ads_config and ads_config.get("in_article_slots"):
        slot = ads_config["in_article_slots"][0]
        ad_unit = f"""
        <div class="ad-container" style="margin: 30px 0; text-align: center;">
            <ins class="adsbygoogle"
                 style="display:block; text-align:center;"
                 data-ad-layout="in-article"
                 data-ad-format="fluid"
                 data-ad-client="{ads_config['client']}"
                 data-ad-slot="{slot}"
                 data-adtest="on"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>
        """

    bh_html = ""
    content_parts = a["body"].split('\n')
    for i, p in enumerate(content_parts):
        p = p.strip()
        if not p: continue
        
        # Check if line is raw HTML (AdSense or similar)
        if p.startswith('<ins') or p.startswith('<script') or p.startswith('</script>') or p.startswith('<div'):
            bh_html += p + "\n"
            continue

        clean_p = p.replace('*', '')
        
        if clean_p.startswith('# '):
            clean_p = clean_p[2:]
            attr = clean_p.replace('"', '&quot;')
            bh_html += f'<h2 class="subheading" data-trans="{attr}" data-original="{attr}">{clean_p}</h2>'
        elif clean_p.startswith('## '):
            clean_p = clean_p[3:]
            attr = clean_p.replace('"', '&quot;')
            bh_html += f'<h3 class="subheading" data-trans="{attr}" data-original="{attr}">{clean_p}</h3>'
        else:
            attr = clean_p.replace('"', '&quot;')
            
            # Special handling for "Anchor Text" (URL) format
            if clean_p.startswith('"') and ') ' not in clean_p and '(' in clean_p and ')' in clean_p:
                import re
                match = re.search(r'"([^"]+)"\s*\(([^)]+)\)', clean_p)
                if match:
                    anchor, url = match.groups()
                    bh_html += f'<p style="margin-top: -5px; margin-bottom: 20px; padding-left: 20px;"><a href="{url}" style="color: var(--accent-blue); font-weight: 700; text-decoration: none;">{anchor} &rarr;</a></p>'
                    continue

            if clean_p.startswith('•'):
                bh_html += f'<p class="list-item" data-trans="{attr}" data-original="{attr}" style="margin-bottom: 8px; padding-left: 20px;">{clean_p}</p>'
            else:
                bh_html += f'<p data-trans="{attr}" data-original="{attr}">{clean_p}</p>'
        
        # Inject ad after 3rd paragraph (or similar)
        if i == len(content_parts) // 2 and ad_unit:
            bh_html += ad_unit

    def get_accent(cat):
        c = cat.lower()
        if 'tech' in c or 'sci' in c: return 'var(--accent-blue)'
        if 'market' in c or 'econ' in c or 'biz' in c or 'india' in c: return 'var(--accent-green)'
        if 'politic' in c or 'world' in c or 'analysis' in c: return 'var(--accent-yellow)'
        return 'var(--accent-red)'
        
    accent = get_accent(a['category'])
    attr_hl = a['headline'].replace('"', '&quot;')
    description = a["body"].replace('#','').replace('*','').replace('\n',' ').strip()[:160] + "..."
    description = description.replace('"', '&quot;')

    # Lead Generation: Intelligence Circle Signup
    signup_form = """
    <div class="signup-section" style="background: var(--bg-surface); border: 2px solid var(--accent-blue); padding: 40px; border-radius: 20px; margin-top: 60px; text-align: center;">
        <h3 style="color: var(--accent-blue); margin-bottom: 10px;" data-trans="Join the Intelligence Circle" data-original="Join the Intelligence Circle">Join the Intelligence Circle</h3>
        <p style="color: var(--text-muted); margin-bottom: 24px;" data-trans="circle_desc" data-original="Get the weekly Alpha Signal report and automated financial insights delivered to your inbox.">Get the weekly Alpha Signal report and automated financial insights delivered to your inbox.</p>
        <form onsubmit="event.preventDefault(); alert('Subscribed to NewsHour Intelligence!');" style="display: flex; gap: 10px; max-width: 500px; margin: 0 auto;">
            <input type="email" placeholder="Enter your best email..." required style="flex: 1; padding: 12px 20px; border-radius: 10px; border: 1px solid var(--border-color); background: var(--bg-base); color: var(--text-main);">
            <button type="submit" style="background: var(--accent-blue); color: #fff; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 700; cursor: pointer;">JOIN ALPHA</button>
        </form>
    </div>
    """

    return f"""<!DOCTYPE html>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{attr_hl}",
  "image": ["{a['image_url']}"],
  "datePublished": "{a['published_at']}",
  "author": [{{
    "@type": "Organization",
    "name": "NewsHour Flock",
    "url": "https://cutbar.in"
  }}]
}}
</script>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{a['headline']} | NewsHour Intelligence</title>
<meta name="description" content="{description}">
<!-- Open Graph -->
<meta property="og:title" content="{attr_hl}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{a['image_url']}">
<meta property="og:url" content="https://cutbar.in/{a['filename']}">
<meta property="og:type" content="article">
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr_hl}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{a['image_url']}">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{ads_tag}
{COMMON_CSS}
<style>
.article-container {{ max-width: 1000px; margin: 76px auto 0; padding: 0 32px; }}
.hero-img-container {{ width: 100%; height: 50vh; max-height: 480px; border-radius: 16px; overflow: hidden; position: relative; margin-bottom: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
.hero-img-container img {{ width: 100%; height: 100%; object-fit: cover; }}
.gradient-overlay {{position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,0.8) 100%); pointer-events: none;}}

.article-header {{ text-align: center; max-width: 800px; margin: -140px auto 40px; position: relative; z-index: 10; }}
.category-badge {{ display: inline-block; background: rgba(11,11,12,0.8); color: {accent}; padding: 6px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
h1 {{ font-size: 26px; font-weight: 700; line-height: 1.65; margin-bottom: 20px; letter-spacing: -0.3px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }}
.meta-info {{ display: flex; justify-content: center; gap: 24px; font-size: 13px; font-weight: 500; color: var(--text-muted); opacity: 0.8; border-bottom: 1px solid var(--border-color); padding-bottom: 24px; margin-bottom: 32px; }}
.meta-item {{ display: flex; align-items: center; gap: 8px; }}

.article-body {{ max-width: 720px; margin: 0 auto 80px; font-size: 16px; line-height: 1.75; color: var(--text-main); }}
.article-body p {{ margin-bottom: 20px; }}
.article-body::first-letter {{ font-size: 2.6rem; font-weight: 800; float: left; margin-right: 10px; line-height: 1; color: {accent}; }}

.subheading {{ font-size: 17px; font-weight: 600; margin-top: 28px; margin-bottom: 14px; color: var(--text-main); }}

.back-link {{ display: inline-flex; align-items: center; gap: 8px; color: var(--text-main); font-weight: 600; padding: 14px 28px; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 12px; transition: all 0.3s ease; text-decoration: none; }}
.back-link:hover {{ transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-color: var(--accent-blue); }}

@media (max-width: 768px) {{
  .article-container {{ padding: 0 14px; margin-top: 68px; }}
  .hero-img-container {{ height: 30vh; max-height: 300px; border-radius: 10px; margin-bottom: 20px; }}
  .article-header {{ margin-top: -80px; }}
  h1 {{ font-size: 20px; line-height: 1.6; }}
  .subheading {{ font-size: 15px; }}
  .article-body {{ font-size: 15px; line-height: 1.75; }}
  .meta-info {{ flex-direction: column; gap: 12px; align-items: center; }}
}}
</style>
</head>
<body>
    <div class="bg-glow"></div>
    <nav class="navbar">
        <a href="/" class="logo"><div class="logo-icon">NH</div><div class="logo-text"><span class="brand-name">NewsHour</span></div></a>
        <div style="display:flex; align-items:center; gap: 1rem;">
            <button id="adminBtn" class="admin-btn" onclick="triggerFlock()">TRIGGER FLOCK</button>
            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" aria-label="Toggle Theme" style="background:transparent; border:none; font-size:1.2rem; cursor:pointer;">🌙</button>
            <div class="lang-toggle">
                <span class="lang-btn" id="btn-en" onclick="setLang('en')">EN</span>
                <span style="color:var(--text-muted)">|</span>
                <span class="lang-btn" id="btn-ur" onclick="setLang('ur')">اردو</span>
            </div>
        </div>
    </nav>
    
    <div class="article-container">
        <div class="hero-img-container">
            <img src="{a['image_url']}" alt="{attr_hl}" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80';">
            <div class="gradient-overlay"></div>
        </div>
        
        <div class="article-header">
            <div class="category-badge">{a['category']} | {a['flock']}</div>
            <h1 data-trans="{attr_hl}" data-original="{attr_hl}">{a['headline']}</h1>
            <div class="meta-info">
                <span class="meta-item"><i class="far fa-calendar-alt"></i> {a['date_display']}</span>
                <span class="meta-item"><i class="fas fa-satellite-dish"></i> <span data-trans="Source:" data-original="Source:">Source:</span> {a['source']}</span>
                <span class="meta-item"><i class="fas fa-robot"></i> <span data-trans="AI Flock" data-original="AI Flock">AI Flock</span></span>
            </div>
        </div>
        
        <div class="article-body">
            {bh_html}
            <div style="margin-top: 60px; padding: 20px; background: var(--bg-surface); border-radius: 12px; border: 1px solid var(--border-color); color: var(--text-muted); font-size: 0.9rem;">
                <p style="margin: 0;"><strong>Editorial Note:</strong> This article was summarized by AI and reviewed for accuracy and editorial integrity by <strong>KhAn</strong> and the <strong>Flock+</strong> editorial team.</p>
            </div>
        </div>

        {signup_form}
        
        <div style="text-align: center; margin-bottom: 60px; margin-top: 40px;">
            <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> <span data-trans="back_home" data-original="Return to Intelligence Dashboard">Return to Intelligence Dashboard</span></a>
        </div>
    </div>

    <footer><p>© 2026 NewsHour Premium Intelligence — <span data-trans="ai_flock" data-original="Autonomous Journalism by AI Flock">Autonomous Journalism by AI Flock</span></p></footer>

    {COMMON_JS}
</body>
</html>"""

def _generate_sitemap(history, site_dir):
    # 1. Standard Sitemap
    urls = ['https://cutbar.in/']
    for a in history:
        urls.append(f"https://cutbar.in/{a['filename']}")

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
        news_sitemap += f'    <loc>https://cutbar.in/{a["filename"]}</loc>\n'
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
