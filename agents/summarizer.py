import os
import time
import anthropic
import httpx

_client: anthropic.Anthropic | None = None

_SYSTEM = (
    "אתה עוזר חדשות שמסכם כתבות בעברית בצורה תמציתית וברורה. "
    "סכם כל כתבה ב-2-3 משפטים קצרים בעברית. התמקד בעובדות המרכזיות בלבד."
)

_RETRYABLE = (httpx.ConnectError, httpx.TimeoutException, anthropic.APIConnectionError)


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _summarize_one(article: dict) -> str:
    content = f"כותרת: {article['title']}\n\n{article.get('description', '')}"
    for attempt in range(3):
        try:
            msg = _get_client().messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=_SYSTEM,
                messages=[{"role": "user", "content": content}],
            )
            return msg.content[0].text.strip()
        except _RETRYABLE as exc:
            if attempt == 2:
                raise
            wait = 2 ** attempt
            print(f"[summarizer] connection error, retrying in {wait}s: {exc}")
            time.sleep(wait)


def run(articles: list[dict]) -> list[dict]:
    """Summarize each article via Claude. Falls back to raw description on error."""
    results = []
    for article in articles:
        try:
            article["summary"] = _summarize_one(article)
            print(f"[summarizer] done: {article['title'][:60]}")
        except Exception as exc:
            print(f"[summarizer] failed '{article.get('title', '?')}': {exc}")
            article["summary"] = article.get("description", "")
        results.append(article)
    return results
