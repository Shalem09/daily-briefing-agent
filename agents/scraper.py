from skills.rss_fetcher import fetch_feed

SOURCES = {
    "ynet": "https://www.ynet.co.il/Integration/StoryRss2.xml",
    "וואלה חדשות": "https://rss.walla.co.il/feed/22",
    "וואלה כלכלה": "https://rss.walla.co.il/feed/2",
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
