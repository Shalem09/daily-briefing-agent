# Project Plan — Daily Briefing Agent

## Goal
Build a multi-agent pipeline that delivers a daily Hebrew news briefing via Telegram,
sourcing content from N12, Calcalist, Channel 13, and Channel 14.

## Phases

### Phase 1 — Scaffold
- [ ] Create project structure
- [ ] Write CLAUDE.md
- [ ] Create .env.example and requirements.txt

### Phase 2 — Skills
- [ ] Implement rss_fetcher skill (feedparser based)
- [ ] Implement telegram_sender skill (httpx based)
- [ ] Unit test both skills independently

### Phase 3 — Agents
- [ ] Scraper agent — calls rss_fetcher for all 4 sources
- [ ] Summarizer agent — Claude API call per article
- [ ] Publisher agent — format + send via telegram_sender
- [ ] Orchestrator — chains all agents, handles errors

### Phase 4 — Integration
- [ ] main.py wires everything together
- [ ] End-to-end test run
- [ ] README with setup instructions

## Success criteria
- [ ] Runs with `python main.py`
- [ ] Sends formatted Hebrew message to Telegram
- [ ] Handles source failures gracefully (partial results still sent)
- [ ] CLAUDE.md present and accurate