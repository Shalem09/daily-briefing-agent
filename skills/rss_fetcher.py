import feedparser


def fetch_feed(url: str, max_items: int = 3) -> list[dict]:
    """Fetch an RSS feed and return up to max_items normalized articles."""
    feed = feedparser.parse(url)
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
    """Strip HTML tags from a string."""
    import re
    return re.sub(r"<[^>]+>", "", text).strip()
