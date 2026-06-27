from agents import scraper, summarizer, publisher


def run() -> bool:
    """Run the full pipeline: scrape → summarize → publish. Returns True on success."""
    print("[orchestrator] Starting daily briefing pipeline…")

    articles = scraper.run()
    print(f"[orchestrator] Scraped {len(articles)} articles total.")

    if not articles:
        print("[orchestrator] No articles fetched — aborting.")
        return False

    summarized = summarizer.run(articles)
    print(f"[orchestrator] Summarized {len(summarized)} articles.")

    success = publisher.run(summarized)
    status = "complete" if success else "finished with errors"
    print(f"[orchestrator] Pipeline {status}.")
    return success
