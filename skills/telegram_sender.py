import os
import httpx

_SPECIAL = r"\_*[]()~`>#+-=|{}.!"
MAX_LEN = 4096


def escape(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    for ch in _SPECIAL:
        text = text.replace(ch, f"\\{ch}")
    return text


def send_message(text: str, token: str | None = None, chat_id: str | None = None) -> dict:
    """Send a MarkdownV2-formatted message to a Telegram chat."""
    token = token or os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = chat_id or os.environ["TELEGRAM_CHAT_ID"]

    if len(text) > MAX_LEN:
        text = text[: MAX_LEN - 3] + "\\.\\.\\."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = httpx.post(
        url,
        json={"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()
