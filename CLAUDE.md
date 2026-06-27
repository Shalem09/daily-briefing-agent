# Daily Briefing Agent — CLAUDE.md

## Project overview
Multi-agent system that scrapes Israeli news sources (N12, Calcalist, Channel 13, Channel 14),
summarizes the top stories in Hebrew, and sends a formatted daily briefing to Telegram.

## Architecture
This project uses Claude Code native multi-agent pattern (subagents via Task tool).

### Agents
| Agent | File | Role |
|-------|------|------|
| Orchestrator | agents/orchestrator.py | Coordinates the full pipeline |
| Scraper | agents/scraper.py | Fetches RSS feeds from all sources |
| Summarizer | agents/summarizer.py | Summarizes articles using Claude API |
| Publisher | agents/publisher.py | Formats and sends to Telegram |

## Skills
- `skills/rss_fetcher.py` — Fetch and normalize RSS feeds → returns list of {title, link, description, date}
- `skills/telegram_sender.py` — Send MarkdownV2-formatted message to Telegram Bot API

## Project structure
daily-briefing-agent/

├── CLAUDE.md

├── plans/

│   └── project_plan.md

├── skills/

│   ├── rss_fetcher.py

│   └── telegram_sender.py

├── agents/

│   ├── orchestrator.py

│   ├── scraper.py

│   ├── summarizer.py

│   └── publisher.py

├── main.py

├── .env.example

└── requirements.txt
## News sources (RSS)
- N12: https://www.mako.co.il/rss/news.xml
- כלכליסט: https://www.calcalist.co.il/rss/AAABVpbHMkE.xml
- ערוץ 13: https://13news.co.il/feed/
- ערוץ 14: https://www.now14.co.il/feed/

## Environment variables
- `ANTHROPIC_API_KEY` — for Summarizer agent
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `TELEGRAM_CHAT_ID` — target chat/channel ID

## Run
```bash
python main.py
```

## Constraints
- Max 3 stories per source (12 total)
- Output language: Hebrew
- Telegram message max 4096 chars — truncate if needed