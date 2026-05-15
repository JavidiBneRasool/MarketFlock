import json, os
from urllib.parse import urlsplit

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

TRUSTED_SOURCES = {
    "openai news", "google deepmind", "google ai blog", "anthropic news", "hugging face blog",
    "github blog ai", "github engineering", "cloudflare blog ai", "cloudflare security",
    "microsoft ai blog", "aws machine learning", "nvidia technical blog", "meta ai blog",
    "arxiv ai", "wired security", "techcrunch ai", "the verge ai", "the hacker news ai",
    "hacker news", "lobsters programming", "lobsters security",
}
TRUSTED_DOMAINS = (
    "openai.com", "deepmind.google", "blog.google", "anthropic.com", "huggingface.co",
    "github.blog", "blog.cloudflare.com", "microsoft.com", "aws.amazon.com", "developer.nvidia.com",
    "ai.meta.com", "arxiv.org", "wired.com", "techcrunch.com", "theverge.com",
    "thehackernews.com", "news.ycombinator.com", "lobste.rs",
)
UNTRUSTED_TERMS = ("infowars", "naturalnews", "theonion", "coupon", "discount code", "promo code")


def _domain(url):
    return urlsplit(url or "").netloc.lower().removeprefix("www.")


def run():
    print("🐑 SHEEP 2: Verifying source authenticity...")
    try:
        with open(f"{OUTPUT}/sheep1_basket.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 2: No articles!")
        return None

    verified = []
    for article in articles:
        source_lower = article.get("source", "").lower()
        url_domain = _domain(article.get("url", ""))
        text = f"{source_lower} {article.get('title', '')} {article.get('summary', '')}".lower()
        if any(term in text for term in UNTRUSTED_TERMS):
            level, score, verdict = "UNTRUSTED", 0, "BLOCK"
        elif source_lower in TRUSTED_SOURCES or any(url_domain.endswith(domain) for domain in TRUSTED_DOMAINS):
            level, score, verdict = "TRUSTED", 10, "PASS"
        else:
            level, score, verdict = "REVIEW", 6, "WARNING"
        article["credibility"] = level
        article["score"] = score
        article["verdict"] = verdict
        if verdict != "BLOCK":
            verified.append(article)

    with open(f"{OUTPUT}/sheep2_verified.json", "w") as f:
        json.dump(verified, f, indent=2)

    passed = sum(1 for a in verified if a["verdict"] == "PASS")
    print(f"🐑 SHEEP 2: {passed}/{len(verified)} trusted, {len(articles) - len(verified)} blocked ✓")
    return verified

if __name__ == "__main__":
    run()
