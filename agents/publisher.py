import os
from datetime import datetime
from skills.telegram_sender import escape, send_message
from skills.whatsapp_sender import send_whatsapp


def _format_telegram(articles: list[dict]) -> str:
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
            lines.append(f"[קישור]({link})")

    return "\n".join(lines)


def _format_whatsapp(articles: list[dict]) -> str:
    today = datetime.now().strftime("%d/%m/%Y")
    lines = [f"📰 *תדריך חדשות יומי — {today}*"]

    current_source = None
    for article in articles:
        source = article.get("source", "")
        if source != current_source:
            current_source = source
            lines.append(f"\n*{source}*")

        title = article.get("title", "")
        summary = article.get("summary", "")
        link = article.get("link", "")

        lines.append(f"\n• *{title}*")
        if summary:
            lines.append(summary)
        if link:
            lines.append(link)

    return "\n".join(lines)


def run(articles: list[dict]) -> bool:
    """Format and publish the briefing to all configured channels. Returns True if at least one succeeded."""
    if not articles:
        print("[publisher] No articles — nothing to send.")
        return False

    success = False

    # Telegram
    try:
        send_message(_format_telegram(articles))
        print("[publisher] Telegram: sent.")
        success = True
    except Exception as exc:
        print(f"[publisher] Telegram failed: {exc}")

    # WhatsApp (only if credentials are configured)
    if os.environ.get("GREEN_API_INSTANCE") and os.environ.get("WHATSAPP_CHAT_ID"):
        try:
            send_whatsapp(_format_whatsapp(articles))
            print("[publisher] WhatsApp: sent.")
            success = True
        except Exception as exc:
            print(f"[publisher] WhatsApp failed: {exc}")
    else:
        print("[publisher] WhatsApp: skipped (no credentials).")

    return success
