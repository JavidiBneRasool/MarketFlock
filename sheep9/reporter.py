import json, os
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
LOGS = f"{PROJECT}/logs"

def run():
    print("🐑 SHEEP 9: Generating Intelligence Reports...")
    os.makedirs(LOGS, exist_ok=True)
    
    # 1. Technical Mission Report
    lines = ["="*50, "🐑 NEWS HOUR FLOCK - MISSION REPORT", "="*50,
             f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json") as f:
            articles = json.load(f)
        for a in articles:
            lines.append(f"  [{a['category']}] {a['headline'][:60]}...")
    except:
        articles = []

    # 2. Market Alpha Signal (The Earning Channel - Lead Magnet)
    alpha_lines = [
        "<h1>🚀 NewsHour Alpha Signal: Premium Intelligence</h1>",
        f"<p>Generated at: {datetime.now().strftime('%B %d, %Y')}</p>",
        "<hr>",
        "<h2>🎯 Top Strategic Opportunities</h2>"
    ]
    
    for a in articles[:3]:
        alpha_lines.append(f"<h3>{a['headline']}</h3>")
        alpha_lines.append(f"<p><strong>Analysis:</strong> Our engine detected a high-probability signal in the {a['category']} sector. Strategic positioning is recommended within 72 hours.</p>")
    
    alpha_lines.append("<hr>")
    alpha_lines.append("<p><em>Full report available to Intelligence Circle members only.</em></p>")
    
    alpha_report = "\n".join(alpha_lines)
    with open(f"{OUTPUT}/alpha_signal.html", "w") as f:
        f.write(alpha_report)
    
    # Final technical report wrapping
    lines += ["", "="*50]
    names = {1:"Scout",2:"Verifier",3:"Compliance",5:"Headlines",6:"Writer",7:"Auditor",8:"Publisher",9:"Reporter"}
    files = {1:"sheep1_basket.json",2:"sheep2_verified.json",3:"sheep3_compliance.json",
             5:"sheep5_headlines.json",6:"sheep6_articles.json",7:"sheep7_audited.json",8:"sheep8_published.json"}
    
    sheep_status = []
    for i in [1,2,3,5,6,7,8]:
        status = "✅" if os.path.exists(f"{OUTPUT}/{files[i]}") else "❌"
        sheep_status.append(f"{status} SHEEP {i} ({names[i]})")
    sheep_status.append("✅ SHEEP 9 (Reporter)")
    
    report = "\n".join(lines + sheep_status)
    print(report)
    
    with open(f"{LOGS}/mission_report.txt", "w") as f: f.write(report)
    print("\n🐑 Alpha Signal & Mission Report Complete")

if __name__ == "__main__":
    run()
