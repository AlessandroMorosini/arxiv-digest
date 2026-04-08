# arxiv-digest

A Claude Code-powered research assistant that fetches daily arXiv papers, scores them against your project, and generates standardized 1-page LaTeX summary cards + short podcast episodes.

You tell it what you're working on. It tells you what came out today that matters — and why.

## How it works

There are three commands you can run inside Claude Code. Each one is a multi-phase workflow that orchestrates Python scripts and parallel subagents.

```
/arxiv-daily [context_file] [--output path]     Fetch today's papers, score, analyze the best ones
/arxiv-search [context] "query"                 Search arXiv for a specific topic
/paper-analysis <paper> [--output path]         Deep-dive on one or more specific papers
```

The daily workflow is the main one. Here's what happens when you run it:

```
┌─────────────────────────────────────────────────────────────────────┐
│  /arxiv-daily ./my-project/README.md                                │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  1. Fetch papers    │  arxiv_tool.py daily --context ...
                │     from arXiv API  │  → cache/2026-03-02.json
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │  2. Read your       │  Understand your research project
                │     context file    │  so scoring is project-specific
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │  3. Score & rank    │  Each paper gets 1-10
                │     every paper     │  based on relevance to your work
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │  4. Show you the    │  Top Picks (≥ threshold)
                │     digest          │  Worth a Look (threshold-3 .. threshold)
                └─────────┬───────────┘  Quick Scan (rest)
                          │
                          ▼
          ┌───────────────┴──────────────────────┐
          │  For each Top Pick, launch in        │
          │  parallel:                           │
          │  • paper-analyst subagent            │
          │  • podcast-generator subagent        │
          └───────────────┬──────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  Analysis       │     │  Podcast        │
    │  subagent       │     │  subagent       │
    │                 │     │                 │
    │  • Fetch full   │     │  • NotebookLM   │
    │    text         │     │    audio gen    │
    │  • Deep analyze │     │  • Context-     │
    │  • Write .tex   │     │    aware: skips │
    │  • Compile PDF  │     │    basics you   │
    └────────┬────────┘     │    already know │
             │              └────────┬────────┘
             ▼                       ▼
      paper-card-*.pdf      podcast-*.mp3
                          │
                          ▼
                ┌─────────────────────┐
                │  6. Save digest     │  digests/2026-03-02/
                │     + PDF report    │  ├── digest.md
                └─────────────────────┘  ├── paper-card-*.tex/.pdf
                                         └── digest-report.pdf
                                         podcasts/2026-03-02/
                                         └── podcast-*.mp3
```

## Setup

**Install dependencies:**

```bash
cd arxiv-digest
pip install -r requirements.txt
```

**Configure your interests:**

Edit `config.yaml` to set your arXiv categories, keywords, and a description of what you're working on:

```yaml
categories:
  - cs.AI
  - cs.CL
  - cs.LG
  - stat.ML

max_papers: 100
lookback_days: 1

interests: |
  I work on efficient attention mechanisms and transformer architectures.
  Interested in: sparse attention, linear attention, long-context models...

keywords:
  - attention mechanism
  - transformer efficiency
  - long context
```

`interests` and `keywords` are your **default scoring context** — they're used when you run `/arxiv-daily` or `/arxiv-search` with no context file. If you pass one (e.g., `/arxiv-daily ./my-project/README.md`), that file takes over and these fields are ignored.

## Usage

The recommended way to use this is through Claude Code slash commands. Open Claude Code in the `arxiv-digest` directory. The main command is:

```
/arxiv-daily
```

This fetches today's papers, scores each one 1-10 against your config interests, shows you a ranked digest, and for every Top Pick generates a 1-page LaTeX summary card + a short podcast episode. Cards land in `digests/YYYY-MM-DD/`, podcasts in `podcasts/YYYY-MM-DD/`. The relevance threshold is configurable via `config.yaml` or `--threshold`.

To score against a specific project instead of your general interests:

```
/arxiv-daily ./path/to/your/project/details
```

To send output to a custom directory (paper cards and digests will go into `<path>/YYYY-MM-DD/`):

```
/arxiv-daily --output ~/research/paper-cards
/arxiv-daily ./my-project/README.md --output ~/Dropbox/papers
```

For example:

```
/arxiv-daily ~/Desktop/my-thesis/notes.tek
```

You can also search arXiv for a specific topic with `/arxiv-search`:

```
/arxiv-search "transformer scaling laws"
```

## The LaTeX summary cards

Every paper card follows an identical template, defined in [`.claude/commands/paper-analysis.md`](.claude/commands/paper-analysis.md). This makes them scannable and easy to collect over time.

The current template follows the structure:

1. **Header** — title, authors, year, venue, URL, code repo
2. **Contribution** — 2-3 sentences on what's novel and what gap it fills
3. **Method** — 2-4 sentences on the approach
4. **Core Equation(s)** — 1-3 key equations with variable annotations (or "N/A" for empirical papers)
5. **Relevance to My Project** — 2-3 bullets, specific and actionable
6. **Limitations** — 2-3 bullets, both acknowledged and apparent

Hard 1-page limit. Cards are compiled to PDF with `xelatex` (falls back to `pdflatex`).

## The Python CLI

`arxiv_tool.py` can also be used standalone. It outputs JSON — the Claude commands are what add scoring, analysis, and LaTeX generation on top.

```bash
python3 arxiv_tool.py daily                                        # fetch today's papers from your configured categories
python3 arxiv_tool.py daily --context ./README.md                  # use this file as scoring context instead of config interests
python3 arxiv_tool.py daily --output ~/research/cards              # store results in ~/research/cards/YYYY-MM-DD/
python3 arxiv_tool.py search "attention" --max 20                  # search arXiv by query, return up to 20 results
python3 arxiv_tool.py history --last 7                             # show papers fetched in the last 7 days
python3 arxiv_tool.py save --date 2026-03-02 --output ~/papers     # save digest to a custom directory
```

## Project files

| File | Description |
|------|-------------|
| `arxiv_tool.py` | Main CLI — fetches, caches, scores, and manages arXiv papers via the `arxiv` Python library |
| `podcast_paper.py` | Generates a short podcast episode for a paper using NotebookLM |
| `config.yaml` | Your arXiv categories, keywords, and research interests |
| `daily_arxiv.sh` | Shell wrapper that runs the daily digest headlessly via `claude -p` |

## Notes

- **Deduplication**: Papers are tracked in `.history.jsonl` by arxiv ID. You won't see the same paper twice across daily runs.
- **Weekend handling**: Monday fetches look back 3 days automatically (arXiv doesn't publish on weekends).
- **LaTeX is required for cards**: You need `xelatex` or `pdflatex` installed. On macOS: `brew install --cask mactex-no-gui`. The `.tex` files are always saved even if compilation fails.
- **Podcasts require NotebookLM**: First-time setup needs a browser for Google auth:
  ```bash
  playwright install chromium
  notebooklm login
  ```
  This opens a browser window to authenticate with your Google account. Credentials are stored locally. When a research context is provided, podcasts adapt to your expertise.

## Automation

The daily digest can run fully unattended. `daily_arxiv.sh` wraps the entire pipeline into a single headless `claude -p` call — no human interaction needed.

### Quick start

```bash
# One-off run with a research context:
./daily_arxiv.sh contexts/forward_lm.md

# Run with default interests from config.yaml:
./daily_arxiv.sh
```

The script checks prerequisites (Claude CLI, `arxiv` package, context file), runs the `/arxiv-daily` slash command headlessly, and writes everything to `digests/YYYY-MM-DD/` and `podcasts/YYYY-MM-DD/`. Logs go to `~/logs/arxiv-digest-YYYY-MM-DD.log`.

If NotebookLM auth fails (common in headless mode), podcast generation is skipped gracefully — paper cards and the digest are still produced.

### Scheduling with cron

To run every day at 1am:

```bash
crontab -e
# Add this line:
0 1 * * * /path/to/arxiv-digest/daily_arxiv.sh contexts/forward_lm.md
```

You can run multiple cron jobs with different context files to track separate research threads.

### Auto-wake (macOS)

If your Mac sleeps overnight, schedule a wake 5 minutes before the cron job:

```bash
sudo pmset repeat wakeorpoweron MTWRFSU 00:55:00
```

The Mac will sleep again on its own after the job finishes.

### Managing

```bash
crontab -l                    # view cron jobs
crontab -e                    # edit cron jobs
pmset -g sched                # view wake schedule
sudo pmset repeat cancel      # remove auto-wake
```
