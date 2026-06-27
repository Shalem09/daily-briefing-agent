from datetime import datetime
from skills.telegram_sender import escape, send_message


def _format(articles: list[dict]) -> str:
    today = escape(datetime.now().strftime("%d/%m/%Y"))
    lines = [f"*📰 תדריך חדשות יומי — {today}*"]

    current_source = None
    for article in articles:
        source = article.get("source", "")
        if source != current_source:
            current_source = source
            lines.append(f"\n*{escape(source)}*")

        title = escape(article.get("title", ""))
        summary = escape(article.get("summary", ""))
        link = article.get("link", "")

        lines.append(f"\n• *{title}*")
        if summary:
            lines.append(summary)
        if link:
            # URL itself needs only ) and \ escaped; standard URLs are safe as-is
            lines.append(f"[קישור]({link})")

    return "\n".join(lines)


def run(articles: list[dict]) -> bool:
    """Format and publish the briefing. Returns True on success."""
    if not articles:
        print("[publisher] No articles — nothing to send.")
        return False

    text = _format(articles)
    try:
        send_message(text)
        print(f"[publisher] Sent ({len(text)} chars).")
        return True
    except Exception as exc:
        print(f"[publisher] Send failed: {exc}")
        return False
