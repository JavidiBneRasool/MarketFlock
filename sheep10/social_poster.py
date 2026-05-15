# SHEEP 10 - Multi-Platform Social Poster (Telegram + Facebook)
import json, os, requests, time, random
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

def load_config():
    with open(f"{PROJECT}/config/social.json") as f:
        return json.load(f)
def post_to_telegram(bot_token, channel_id, headline, article_url, category, source):
    post_text = f"""
🤖 <b>{category} Update</b>

<b>{headline}</b>

🔗 {article_url}

#Autoflock #AI #Terminal #Automation
"""
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": channel_id,
        "text": post_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(api_url, json=payload)
        return response.json().get("ok"), response.json().get("description", "unknown")
    except Exception as e:
        return False, str(e)

def post_to_whatsapp(instance_id, access_token, phone_number, headline, article_url):
    """WhatsApp API Implementation (UltraMsg format)"""
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    message = f"*🤖 {headline}*\n\nRead more: {article_url}\n\n#Autoflock #AI"
    
    payload = {
        "token": access_token,
        "to": phone_number,
        "body": message
    }
    
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)

def post_to_facebook(page_id, access_token, headline, article_url, category):
    # 2. Build the 'Engagement Trigger' message
    triggers = [
        f"🚀 Check out this {category} trick: {headline}",
        f"🤖 New AI Tool Alert: {headline}. Total game changer.",
        f"⚡ Terminal Tip: {headline}. Boost your productivity.",
        f"🔧 Automation Build: {headline}. Ready to deploy."
    ]
    message = f"🤖 {headline}\n\n{random.choice(triggers)}\n\nRead more: {article_url}\n\n#Autoflock #AI #Automation"
    
    api_url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {
        "message": message,
        "link": article_url,
        "access_token": access_token
    }
    try:
        response = requests.post(api_url, data=payload)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)

def post_to_x(api_key, api_secret, access_token, access_token_secret, headline, article_url):
    """Placeholder for X (Twitter) API v2 Integration"""
    # Note: Requires 'tweepy' or direct oauth1.0a signing. 
    # For now, we simulate the hook for the user to add credentials.
    print(f"      [X/Twitter Simulator] Posting: {headline[:50]}...")
    return True, "Simulated"

def run():
    print("🐑 SHEEP 10: Posting to Multi-Channel Social Hub...")
    
    config = load_config()
    bot_token = config.get("telegram_bot_token")
    channel_id = config.get("telegram_channel_id")
    fb_page_id = config.get("facebook_page_id")
    fb_access_token = config.get("facebook_access_token")
    wa_instance = config.get("whatsapp_instance")
    wa_token = config.get("whatsapp_token")
    wa_number = config.get("whatsapp_number")
    
    # Load published articles
    try:
        # For now, fallback to sheep1 if audited doesn't exist yet
        try:
            with open(f"{OUTPUT}/sheep7_audited.json") as f:
                articles = json.load(f)
        except:
            with open(f"{OUTPUT}/sheep1_basket.json") as f:
                articles = json.load(f)
                # Map titles to headlines if using sheep1 output
                for a in articles:
                    if "headline" not in a: a["headline"] = a["title"]
    except FileNotFoundError:
        print("🐑 SHEEP 10: No articles!"); return None
    
    base_url = "https://autoflock.cutbar.in"
    results = []

    # Post top 3 articles
    for article in articles[:3]:
        headline = article["headline"]
        article_url = article.get("url", f"{base_url}/{article.get('filename', '')}")
        category = article.get("category", "Tech")
        source = article.get('source', 'Autoflock')
        
        print(f"   Social Post: {headline[:50]}...")
        
        # Telegram
        if bot_token and channel_id:
            ok, err = post_to_telegram(bot_token, channel_id, headline, article_url, category, source)
            if ok: print(f"      ✓ Posted to Telegram")
            else: print(f"      ✗ Telegram Failed: {err}")

        # Facebook
        if fb_page_id and fb_access_token:
            ok, err = post_to_facebook(fb_page_id, fb_access_token, headline, article_url, category)
            if ok: print(f"      ✓ Posted to Facebook")
            else: print(f"      ✗ Facebook Failed: {err}")

        # WhatsApp
        if wa_instance and wa_token:
            ok, err = post_to_whatsapp(wa_instance, wa_token, wa_number, headline, article_url)
            if ok: print(f"      ✓ Posted to WhatsApp")
            else: print(f"      ✗ WhatsApp Failed: {err}")
        
        results.append({"headline": headline, "success": True})
        time.sleep(3)  # Polite delay
    
    with open(f"{OUTPUT}/sheep10_social.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"🐑 SHEEP 10: Social updates completed ✓")
    return results

if __name__ == "__main__":
    run()
