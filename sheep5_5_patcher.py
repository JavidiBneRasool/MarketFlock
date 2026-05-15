# SHEEP 5.5 - Patches new articles into index.html
import json, os

PROJECT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(os.path.dirname(PROJECT), "newshour-site")

def run():
    print("🐑 SHEEP 5.5: Patching new articles...")
    os.makedirs(OUTPUT, exist_ok=True)
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 5.5: No articles!"); return None
    
    # Build new article cards
    cards_html = ""
    for i, a in enumerate(articles):
        excerpt = a["body"].replace('#','').replace('*','').replace('\n',' ').strip()[:150] + "..."
        cards_html += f"""
<article class="news-card">
<div class="news-card-category">{a['category'].upper()}</div>
<h3><a href="/{a['filename']}">{a['headline']}</a></h3>
<p>{excerpt}</p>
<div class="news-card-meta">
<span><i class="far fa-clock"></i> Just now</span>
<span><i class="fas fa-robot"></i> AI Flock</span>
</div>
</article>"""
    
    # Insert into news grid
    index_path = os.path.join(SITE_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            html = f.read()
        
        # Replace everything between news-grid divs
        import re
        html = re.sub(
            r'(<div class="news-grid">).*?(</div>)',
            r'\1' + cards_html + r'\2',
            html,
            flags=re.DOTALL
        )
        
        with open(index_path, "w") as f:
            f.write(html)
        
        print(f"🐑 SHEEP 5.5: {len(articles)} articles patched ✓")
    else:
        print("🐑 SHEEP 5.5: No index.html found")

if __name__ == "__main__":
    run()
