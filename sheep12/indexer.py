# SHEEP 12 - Google Indexing API Integration
import json, os, requests, time
from google.oauth2 import service_account
from google.auth.transport.requests import Request

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
KEY_FILE = f"{PROJECT}/config/google_indexing_key.json"

def ping_google_sitemap(sitemap_url):
    print(f"   Pinging Google Sitemap: {sitemap_url}")
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    print(f"      DEBUG: Sending GET to {ping_url}")
    try:
        response = requests.get(ping_url)
        if response.status_code == 200:
            print("      ✓ Sitemap Pinged successfully")
        else:
            print(f"      ! Ping response: {response.status_code}")
    except Exception as e:
        print(f"      ! Ping failed: {e}")

def run():
    print("🐑 SHEEP 12: Activating News Signal Engine...")
    
    # 1. Ping Sitemaps (Standard & News)
    ping_google_sitemap("https://market.cutbar.in/sitemap.xml")
    ping_google_sitemap("https://market.cutbar.in/news-sitemap.xml")

    # 2. Attempt Indexing API (Selective)
    if not os.path.exists(KEY_FILE):
        print("   ! Google Indexing key not found. Skipping API.")
    else:
        try:
            _run_api_indexing()
        except Exception as e:
            print(f"   ! Indexing API failed: {e} (Continuing with other signals)")

def _run_api_indexing():
    # Load recently published articles from history
    try:
        with open(f"{PROJECT}/history.json") as f:
            history = json.load(f)
            articles = history[:5] # Index only top 5 to keep trust high
    except: return

    scopes = ['https://www.googleapis.com/auth/indexing']
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=scopes)
    credentials.refresh(Request())
    access_token = credentials.token
    
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    for article in articles:
        # Use filename without .html as Cloudflare Pages/Wrangler likely redirects
        filename = article.get('filename', '').replace('.html', '')
        url = f"https://market.cutbar.in/{filename}"
        print(f"   API Indexing: {url}")
        payload = {"url": url, "type": "URL_UPDATED"}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        try:
            requests.post(endpoint, json=payload, headers=headers)
        except: pass

if __name__ == "__main__":
    run()
