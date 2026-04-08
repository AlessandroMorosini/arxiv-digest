#!/bin/bash
# daily_arxiv.sh — Headless arXiv digest via Claude Code
# Usage:
#   ./daily_arxiv.sh                              # default interests from config.yaml
#   ./daily_arxiv.sh contexts/forward_lm.md       # filtered by research context
#   ./daily_arxiv.sh contexts/self_consistency.md  # filtered by different context
#
# Cron example (every weekday at 9am):
#   0 9 * * 1-5 /Users/alessandromorosini/Desktop/arxiv-digest/daily_arxiv.sh contexts/forward_lm.md

set -euo pipefail

PROJECT_DIR="/Users/alessandromorosini/Desktop/arxiv-digest"
LOG_DIR="$HOME/logs"
DATE=$(date +%Y-%m-%d)
LOGFILE="$LOG_DIR/arxiv-digest-${DATE}.log"
CONTEXT="${1:-}"

mkdir -p "$LOG_DIR"
cd "$PROJECT_DIR"

# ── Pre-flight checks ──────────────────────────────────────────────
echo "[$DATE] Starting arXiv digest pipeline" | tee "$LOGFILE"

if ! command -v claude &>/dev/null; then
  echo "ERROR: claude CLI not found in PATH" | tee -a "$LOGFILE"
  exit 1
fi

if ! python3 -c "import arxiv" &>/dev/null; then
  echo "ERROR: arxiv Python package not installed" | tee -a "$LOGFILE"
  exit 1
fi

if [[ -n "$CONTEXT" && ! -f "$CONTEXT" ]]; then
  echo "ERROR: Context file not found: $CONTEXT" | tee -a "$LOGFILE"
  exit 1
fi

# ── Build prompt ────────────────────────────────────────────────────
PROMPT="Run the /arxiv-daily slash command"

if [[ -n "$CONTEXT" ]]; then
  PROMPT="$PROMPT with context file: $CONTEXT"
fi

PROMPT="$PROMPT

Additional instructions for this headless run:
- If NotebookLM authentication fails or podcast generation errors out, skip ALL podcast generation and continue with paper cards and digest only.
- Do NOT use AskUserQuestion — this is a non-interactive run. Make reasonable decisions autonomously.
- Write a brief summary of what was produced to stdout when done."

# ── Run ─────────────────────────────────────────────────────────────
claude -p "$PROMPT" \
  --allowedTools "Bash(python3:*),Bash(xelatex:*),Bash(pdflatex:*),Bash(mkdir:*),Bash(cat:*),Read,Write,WebSearch,WebFetch,Agent" \
  --max-turns 80 \
  2>&1 | tee -a "$LOGFILE"

EXIT_CODE=${PIPESTATUS[0]}

# ── Post-run summary ───────────────────────────────────────────────
echo "" | tee -a "$LOGFILE"
if [[ $EXIT_CODE -eq 0 ]]; then
  echo "[$DATE] Pipeline completed successfully" | tee -a "$LOGFILE"
  # List what was produced
  if [[ -d "output/$DATE" ]]; then
    echo "Output files:" | tee -a "$LOGFILE"
    ls -lh "output/$DATE/" 2>/dev/null | tee -a "$LOGFILE"
  fi
  if [[ -d "digests/$DATE" ]]; then
    echo "Digest files:" | tee -a "$LOGFILE"
    ls -lh "digests/$DATE/" 2>/dev/null | tee -a "$LOGFILE"
  fi
  if [[ -d "podcasts/$DATE" ]]; then
    echo "Podcast files:" | tee -a "$LOGFILE"
    ls -lh "podcasts/$DATE/" 2>/dev/null | tee -a "$LOGFILE"
  fi
else
  echo "[$DATE] Pipeline failed with exit code $EXIT_CODE" | tee -a "$LOGFILE"
fi

exit $EXIT_CODE
