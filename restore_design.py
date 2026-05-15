import re, os

# Get path relative to this script
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLISHER_FILE = os.path.join(PROJECT_DIR, "sheep8", "publisher.py")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsHour with CUTBAR - Breaking News & Latest Updates</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-red: #e63946;
            --dark-bg: #0a0a0a;
            --card-bg: rgba(255, 255, 255, 0.05);
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --gradient: linear-gradient(135deg, #e63946 0%, #ff6b6b 100%);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--dark-bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(circle at 20% 50%, rgba(230, 57, 70, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(230, 57, 70, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 107, 107, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }

        /* Navigation */
        .navbar {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 1.2rem 5%;
            background: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: var(--gradient);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 1.2rem;
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
        }

        .logo-text {
            display: flex;
            flex-direction: column;
        }

        .brand-name {
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }

        .brand-slogan {
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Main Grid */
        .container {
            max-width: 1300px;
            margin: 100px auto 40px;
            padding: 0 5%;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.05);
        }

        .section-title {
            font-size: 2.2rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .section-title::before {
            content: "";
            width: 6px;
            height: 35px;
            background: var(--gradient);
            border-radius: 3px;
        }

        /* News Grid */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 2.5rem;
        }

        .news-card {
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
        }

        .news-card:hover {
            transform: translateY(-10px);
            border-color: rgba(230, 57, 70, 0.4);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(230, 57, 70, 0.1);
        }

        .card-image {
            width: 100%;
            height: 220px;
            background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .card-image::after {
            content: "📰";
            font-size: 4rem;
            opacity: 0.15;
        }

        .category-badge {
            position: absolute;
            top: 1.5rem;
            left: 1.5rem;
            background: var(--gradient);
            padding: 0.4rem 1rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            z-index: 2;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        .news-card-content {
            padding: 2rem;
        }

        .news-card-category {
            color: var(--primary-red);
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 0.75rem;
            display: block;
        }

        .news-card h3 {
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 1rem;
            line-height: 1.3;
            color: var(--text-primary);
        }

        .news-card h3 a {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s;
        }

        .news-card h3 a:hover {
            color: var(--primary-red);
        }

        .news-card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .footer-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Breaking News Ticker */
        .breaking-news {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: rgba(10, 10, 10, 0.9);
            backdrop-filter: blur(15px);
            border-top: 1px solid var(--primary-red);
            padding: 0.75rem 2rem;
            z-index: 999;
            display: flex;
            align-items: center;
            overflow: hidden;
        }

        .breaking-label {
            background: var(--primary-red);
            color: white;
            padding: 0.2rem 0.8rem;
            font-weight: 800;
            font-size: 0.8rem;
            border-radius: 4px;
            margin-right: 1.5rem;
            flex-shrink: 0;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .ticker-wrapper {
            overflow: hidden;
            white-space: nowrap;
        }

        .ticker-text {
            display: inline-block;
            padding-left: 100%;
            animation: ticker 30s linear infinite;
            font-weight: 500;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }

        /* Footer */
        footer {
            background: #050505;
            padding: 5rem 5% 7rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 5rem;
        }

        .footer-grid {
            max-width: 1300px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 4rem;
        }

        .footer-brand p {
            margin: 1.5rem 0;
            color: var(--text-secondary);
            max-width: 400px;
        }

        .footer-section h3 {
            margin-bottom: 1.5rem;
            color: var(--text-primary);
        }

        .footer-links {
            list-style: none;
        }

        .footer-links li {
            margin-bottom: 0.75rem;
        }

        .footer-links a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer-links a:hover {
            color: var(--primary-red);
        }

        .copyright {
            max-width: 1300px;
            margin: 3rem auto 0;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            color: #555;
            font-size: 0.85rem;
        }

        /* Live Indicator */
        .live-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(230, 57, 70, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            color: var(--primary-red);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            background-color: var(--primary-red);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--primary-red);
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }

        @media (max-width: 768px) {
            .footer-grid {
                grid-template-columns: 1fr;
                gap: 2.5rem;
            }
            .news-grid {
                grid-template-columns: 1fr;
            }
            .navbar {
                padding: 1rem 5%;
            }
            .brand-name { font-size: 1.2rem; }
            .logo-icon { width: 35px; height: 35px; font-size: 1rem; }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>

    <nav class="navbar">
        <a href="/" class="logo">
            <div class="logo-icon">NH</div>
            <div class="logo-text">
                <span class="brand-name">NewsHour</span>
                <span class="brand-slogan">with CUTBAR</span>
            </div>
        </a>
        <div class="live-indicator">
            <span class="live-dot"></span>
            LIVE
        </div>
    </nav>

    <div class="container">
        <header class="section-header">
            <h2 class="section-title">Latest Headlines</h2>
        </header>

        <div class="news-grid">
            {cards}
        </div>
    </div>

    <!-- Breaking News Ticker -->
    <div class="breaking-news">
        <span class="breaking-label">BREAKING</span>
        <div class="ticker-wrapper">
            <span class="ticker-text">
                {ticker}
            </span>
        </div>
    </div>

    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="/" class="logo">
                    <div class="logo-icon">NH</div>
                    <div class="logo-text">
                        <span class="brand-name">NewsHour</span>
                    </div>
                </a>
                <p>Your trusted source for breaking news, in-depth analysis, and comprehensive coverage of the stories that matter most.</p>
            </div>
            <div class="footer-section">
                <h3>Categories</h3>
                <ul class="footer-links">
                    <li><a href="#">World News</a></li>
                    <li><a href="#">Politics</a></li>
                    <li><a href="#">Technology</a></li>
                    <li><a href="#">Business</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>Resources</h3>
                <ul class="footer-links">
                    <li><a href="#"><i class="fas fa-chevron-right"></i> About Us</a></li>
                    <li><a href="#"><i class="fas fa-chevron-right"></i> Live Coverage</a></li>
                    <li><a href="#"><i class="fas fa-chevron-right"></i> Archive</a></li>
                </ul>
            </div>
        </div>
        <div class="copyright">
            <p>© 2026 NewsHour with CUTBAR — Autonomous Journalism by AI Flock</p>
            <p style="margin-top: 5px;">Powered by Termux + Cloudflare Edge</p>
        </div>
    </footer>
</body>
</html>
"""

def get_cards(articles, date_str):
    cards = ""
    for a in articles:
        excerpt = a["body"].replace('#','').replace('*','').replace('\\n',' ').strip()[:150] + "..."
        cards += f'''
            <article class="news-card">
                <div class="card-image">
                    <span class="category-badge">{a['category']}</span>
                </div>
                <div class="news-card-content">
                    <span class="news-card-category">{a['category']}</span>
                    <h3><a href="/{a['filename']}">{a['headline']}</a></h3>
                    <p>{excerpt}</p>
                    <div class="card-footer">
                        <div class="footer-item">
                            <i class="far fa-calendar-alt"></i>
                            {date_str}
                        </div>
                        <div class="footer-item">
                            <i class="fas fa-robot"></i>
                            AI Flock
                        </div>
                    </div>
                </div>
            </article>'''
    return cards

def get_ticker(articles):
    return " • ".join([a['headline'] for a in articles]) + " • "

# Restore to publisher.py
with open(PUBLISHER_FILE, "r") as f:
    pub = f.read()

# Replace _build_index
new_build_index = f'''
def _build_index(articles, date_str):
    ticker = " • ".join([a['headline'] for a in articles]) + " • "
    cards = ""
    for a in articles:
        excerpt = a["body"].replace("#","").replace("*","").replace("\\n"," ").strip()[:150] + "..."
        cards += f"""
            <article class="news-card">
                <div class="card-image">
                    <span class="category-badge">{{a['category']}}</span>
                </div>
                <div class="news-card-content">
                    <span class="news-card-category">{{a['category']}}</span>
                    <h3><a href="/{{a['filename']}}">{{a['headline']}}</a></h3>
                    <p>{{excerpt}}</p>
                    <div class="card-footer">
                        <div class="footer-item">
                            <i class="far fa-calendar-alt"></i>
                            {{date_str}}
                        </div>
                        <div class="footer-item">
                            <i class="fas fa-robot"></i>
                            AI Flock
                        </div>
                    </div>
                </div>
            </article>"""
    return f"""{html_content}"""
'''

# Surgical replacement of _build_index
pub = re.sub(r'def _build_index\(articles, date_str\):.*?return f""".*?"""', new_build_index, pub, flags=re.DOTALL)

with open(PUBLISHER_FILE, "w") as f:
    f.write(pub)

print("Branded Design Restored!")
