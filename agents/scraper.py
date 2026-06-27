from skills.rss_fetcher import fetch_feed

SOURCES = {
    "N12": "https://www.mako.co.il/rss/news.xml",
    "כלכליסט": "https://www.calcalist.co.il/rss/AAABVpbHMkE.xml",
    "ערוץ 13": "https://13news.co.il/feed/",
    "ערוץ 14": "https://www.now14.co.il/feed/",
}


def run() -> list[dict]:
    """Fetch up to 3 articles from each source. Failed sources are skipped."""
    all_articles = []
    for source_name, url in SOURCES.items():
        try:
            articles = fetch_feed(url, max_items=3)
            for article in articles:
                article["source"] = source_name
            all_articles.extend(articles)
            print(f"[scraper] {source_name}: {len(articles)} articles")
        except Exception as exc:
            print(f"[scraper] {source_name} failed: {exc}")
    return all_articles
