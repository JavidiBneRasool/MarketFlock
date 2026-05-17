# SHEEP 10 - Multi-Platform Social Poster (Telegram + Facebook)
import json, os, requests, time, random, re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"
POSTED_FILE = f"{OUTPUT}/social_posted.json"
BASE_URL = "https://market.cutbar.in"
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid", "ref"}


def load_config():
    with open(f"{PROJECT}/config/social.json") as f:
        return json.load(f)


def _canonical_url(url):
    if not url:
        return ""
    parts = urlsplit(url.strip())
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS])
    path = parts.path.rstrip('/') or '/'
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ''))


def _title_key(title):
    title = re.sub(r"[^a-z0-9 ]+", " ", (title or "").lower())
    return re.sub(r"\s+", " ", title).strip()


def _article_url(article):
    filename = article.get("filename", "")
    if filename:
        return f"{BASE_URL}/{filename.replace('.html', '')}"
    # If publishing did not run, prefer the original source over repeatedly posting the homepage.
    return article.get("source_url") or article.get("url") or BASE_URL


def _load_posted():
    if not os.path.exists(POSTED_FILE):
        return []
    try:
        with open(POSTED_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def _load_published_articles():
    # Sheep 8 runs before Sheep 10, so history.json has filenames. This avoids homepage-only posts.
    try:
        with open(HISTORY_FILE) as f:
            history = json.load(f)
            if history:
                return history
    except Exception:
        pass
    try:
        with open(f"{OUTPUT}/sheep7_audited.json") as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            with open(f"{OUTPUT}/sheep1_basket.json") as f:
                articles = json.load(f)
                for article in articles:
                    article.setdefault("headline", article.get("title", ""))
                return articles
        except FileNotFoundError:
            return []


def post_to_telegram(bot_token, channel_id, headline, article_url, category, source):
    post_text = f"""
🤖 <b>{category} Update</b>

<b>{headline}</b>

Source: {source}
🔗 {article_url}

#MarketFlock #Crypto #Markets #Finance
"""
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel_id, "text": post_text, "parse_mode": "HTML", "disable_web_page_preview": False}
    try:
        response = requests.post(api_url, json=payload)
        return response.json().get("ok"), response.json().get("description", "unknown")
    except Exception as e:
        return False, str(e)


def post_to_whatsapp(instance_id, access_token, phone_number, headline, article_url):
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    message = f"*🤖 {headline}*\n\nRead more: {article_url}\n\n#MarketFlock #Crypto #Markets"
    payload = {"token": access_token, "to": phone_number, "body": message}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)


def post_to_facebook(page_id, access_token, headline, article_url, category):
    triggers = [
        f"🚀 {category} signal: {headline}",
        f"🤖 New MarketFlock signal: {headline}",
        f"⚡ Developer and automation watch: {headline}",
        f"🔧 📊 MarketFlock signal: {headline}"
    ]
    message = f"🤖 {headline}\n\n{random.choice(triggers)}\n\nRead more: {article_url}\n\n#MarketFlock #Crypto #Markets #Finance"
    api_url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "link": article_url, "access_token": access_token}
    try:
        response = requests.post(api_url, data=payload)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)


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

    articles = _load_published_articles()
    if not articles:
        print("🐑 SHEEP 10: No articles!")
        return None

    posted = _load_posted()
    posted_urls = {_canonical_url(item.get("source_url", "")) for item in posted if item.get("source_url")}
    posted_titles = {_title_key(item.get("headline", "")) for item in posted if item.get("headline")}

    results = []
    selected = []
    for article in articles:
        headline = article.get("headline") or article.get("title") or ""
        source_url = _canonical_url(article.get("source_url") or article.get("url") or "")
        title_key = _title_key(headline)
        if source_url in posted_urls or title_key in posted_titles:
            continue
        if not article.get("filename") and not source_url:
            continue
        selected.append(article)
        posted_urls.add(source_url)
        posted_titles.add(title_key)
        if len(selected) == 3:
            break

    if not selected:
        print("🐑 SHEEP 10: No new social posts to send ✓")
        return []

    for article in selected:
        headline = article.get("headline") or article.get("title")
        article_url = _article_url(article)
        category = article.get("category", "Tech")
        source = article.get("source", "MarketFlock")
        source_url = article.get("source_url") or article.get("url") or ""
        print(f"   Social Post: {headline[:50]}...")

        sent_any = False
        if bot_token and channel_id:
            ok, err = post_to_telegram(bot_token, channel_id, headline, article_url, category, source)
            sent_any = sent_any or bool(ok)
            print("      ✓ Posted to Telegram" if ok else f"      ✗ Telegram Failed: {err}")
        if fb_page_id and fb_access_token:
            ok, err = post_to_facebook(fb_page_id, fb_access_token, headline, article_url, category)
            sent_any = sent_any or bool(ok)
            print("      ✓ Posted to Facebook" if ok else f"      ✗ Facebook Failed: {err}")
        if wa_instance and wa_token:
            ok, err = post_to_whatsapp(wa_instance, wa_token, wa_number, headline, article_url)
            sent_any = sent_any or bool(ok)
            print("      ✓ Posted to WhatsApp" if ok else f"      ✗ WhatsApp Failed: {err}")

        result = {"headline": headline, "url": article_url, "source_url": source_url, "success": sent_any}
        results.append(result)
        posted.insert(0, result)
        time.sleep(3)

    posted = posted[:300]
    with open(POSTED_FILE, "w") as f:
        json.dump(posted, f, indent=2)
    with open(f"{OUTPUT}/sheep10_social.json", "w") as f:
        json.dump(results, f, indent=2)

    print("🐑 SHEEP 10: Social updates completed ✓")
    return results

if __name__ == "__main__":
    run()
