import re
import feedparser
import httpx

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}


def fetch_feed(url: str, max_items: int = 3) -> list[dict]:
    """Fetch an RSS feed and return up to max_items normalized articles."""
    resp = httpx.get(url, headers=_HEADERS, timeout=15, follow_redirects=True)
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)
    articles = []
    for entry in feed.entries[:max_items]:
        articles.append({
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", ""),
            "description": _clean(entry.get("summary", entry.get("description", ""))),
            "date": entry.get("published", entry.get("updated", "")),
            "source": feed.feed.get("title", url),
        })
    return articles


def _clean(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()
