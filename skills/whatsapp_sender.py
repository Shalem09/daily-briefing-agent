import os
import httpx

_BASE = "https://api.green-api.com"


def _chat_id(raw: str) -> str:
    if "@" in raw:
        return raw
    digits = "".join(c for c in raw if c.isdigit())
    if digits.startswith("0"):
        digits = "972" + digits[1:]
    elif not digits.startswith("972"):
        digits = "972" + digits
    return f"{digits}@c.us"


def send_whatsapp(text: str, chat_id: str | None = None) -> dict:
    instance = os.environ["GREEN_API_INSTANCE"]
    token = os.environ["GREEN_API_TOKEN"]
    chat_id = _chat_id(chat_id or os.environ["WHATSAPP_CHAT_ID"])

    url = f"{_BASE}/waInstance{instance}/sendMessage/{token}"
    resp = httpx.post(url, json={"chatId": chat_id, "message": text}, timeout=15)
    resp.raise_for_status()
    return resp.json()
