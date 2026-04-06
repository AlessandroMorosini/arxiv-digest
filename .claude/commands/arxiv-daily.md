---
description: "Fetch and summarize today's arXiv papers, optionally filtered by a project context file"
allowed-tools:
  - Bash(python3 ./arxiv_tool.py:*)
  - Bash(cat:*)
  - Bash(xelatex:*)
  - Bash(pdflatex:*)
  - Bash(python3 -c:*)
  - Bash(python3 ./podcast_paper.py:*)
  - Bash(mkdir:*)
  - Read
  - Write
  - WebSearch
  - WebFetch
  - Agent
  - AskUserQuestion
---

You are a research paper discovery, analysis, and reporting agent.

**Input:** $ARGUMENTS

## Phase 1: Parse arguments and fetch papers

Determine what was passed in `$ARGUMENTS`:

- **If it contains a file path** (e.g., `./README.md`, `~/Desktop/CausalML/README.md`, `/path/to/spec.md`, `./paper.pdf`): use it as `--context` to tailor the paper search to that project.
- **If it contains `--output <path>`** (e.g., `--output ~/research/cards`): use it as the base output directory. Paper cards and digests will be stored in `<path>/YYYY-MM-DD/`.
- **If it contains `--threshold N`** (e.g., `--threshold 6`): pass it through to `arxiv_tool.py daily` to override the relevance threshold for deep analysis.
- **If empty or no file path**: fall back to the default config interests and default output directory (`digests/`).

Fetch papers:

```bash
# With context file, custom output, and threshold override:
python3 ./arxiv_tool.py daily --context <path> --output <output_path> --threshold <N>

# With context file (default output):
python3 ./arxiv_tool.py daily --context <path>

# With threshold override only:
python3 ./arxiv_tool.py daily --threshold <N>

# Without context (uses config.yaml interests):
python3 ./arxiv_tool.py daily
```

The CLI returns a JSON object with pre-computed fields:
- `output_dir` — date-specific directory for file writes (e.g., `digests/2026-03-02/`)
- `podcast_dir` — podcast output directory (e.g., `podcasts/2026-03-02/`)
- `date` — the YYYY-MM-DD date string
- `relevance_threshold` — the threshold value
- `tiers.top` — minimum score for Top Picks (= threshold)
- `tiers.mid` — minimum score for Worth a Look (= threshold - 3)
- `papers` — the fetched paper list

Use these fields directly. Do NOT compute tier boundaries or podcast paths yourself.

## Phase 2: Understand the research context

If a context file was provided, read it carefully (use the Read tool for text files, or read the PDF) to understand:
- What the research project is about
- What methods, frameworks, and techniques it uses
- What problems it's trying to solve
- What gaps or next steps are mentioned

Store this understanding — you will pass it to subagents.

If no context was provided, read the config:
```bash
python3 ./arxiv_tool.py config --show
```

## Phase 3: Score and filter papers

For each fetched paper, score its relevance **1-10** against the research context:

- **9-10**: Directly addresses the project's core problem or uses the same methods. Must-read.
- **7-8**: Closely related — same domain, complementary techniques, useful as baseline.
- **5-6**: Tangentially related — may contain reusable ideas or methods.
- **3-4**: Loosely connected — different problem but same general area.
- **1-2**: Not relevant to this specific project.

## Phase 4: Present the digest to the user

Use `tiers.top` and `tiers.mid` from the JSON output.

Present papers grouped by relevance tier:

### Top Picks (score >= tiers.top)
For each paper:
- **[Title](arxiv_url)** — score/10
- Authors | Category
- *One-line summary*
- **Key contribution**: What's novel
- **Why it matters for your project**: Specific connection to the context

### Worth a Look (score >= tiers.mid and < tiers.top)
- **[Title](arxiv_url)** (score/10) — One-line summary. *Category*

### Quick Scan (score < tiers.mid)
Compact table.

## Phase 5: Deep analysis + podcast generation — launch parallel subagents

For every paper that scored **>= tiers.top**, launch a **paper-analyst** subagent.
For every paper that scored **>= 9**, ALSO launch a **podcast-generator** subagent.

**Launch ALL subagents simultaneously in a single message with multiple Agent tool calls.**

### Paper analyst subagents

For each paper, use:
- `subagent_type: "paper-analyst"`
- `description: "Analyze paper: <short title>"`

Each subagent prompt should contain (replace `<output_dir>` with the `output_dir` value from Phase 1's JSON output):

```
Analyze this paper in the context of the user's research project.

## Paper to analyze
- Title: <title>
- arXiv URL: <url>
- Authors: <authors>
- Abstract: <abstract>

## User's research context
<paste the research context summary from Phase 2 here>

The user is evaluating this paper for: relevance as related work, methodological overlap, potential as a baseline, and positioning.

## Output directory
Write ALL output files to: <output_dir>
Create this directory if it doesn't exist (mkdir -p).
```

### Podcast generator subagents

For each paper, use:
- `subagent_type: "podcast-generator"`
- `description: "Generate podcast: <short title>"`

Use `podcast_dir` and `date` from the JSON output directly.

Each subagent prompt should contain (include the listener context section only when a research context was provided in Phase 2):

```
Generate a podcast episode for this arXiv paper.

## Paper details
- Title: <title>
- arXiv URL: <url>
- Date: <date>

## Output directory
<podcast_dir>

## Listener context
<1-2 sentence summary of the listener's expertise from Phase 2, describing concepts/techniques they already understand — e.g., "multi-turn LLM evaluation, reward modeling, RLHF pipelines". The podcast should NOT explain these basics.>
```

## Phase 6: Save digest and generate PDF report

After all subagents complete, use the `output_dir` from Phase 1 for all paths:

1. **Save the markdown digest** (include a "Podcasts" section listing generated MP3 file paths for papers that got podcast episodes):
```bash
# If --output was provided:
python3 ./arxiv_tool.py save --date $(date +%Y-%m-%d) --output <output_base_path> --file /dev/stdin

# Default:
python3 ./arxiv_tool.py save --date $(date +%Y-%m-%d) --file /dev/stdin
```

2. **Generate a PDF report** of the full digest. Launch one more subagent:
   - `subagent_type: "general-purpose"`
   - `description: "Generate digest PDF report"`
   - The prompt should instruct it to read the saved digest markdown file and convert it to a professional PDF using WeasyPrint (following the /create-pdf pattern: self-contained HTML with inline CSS, Helvetica Neue, dark/blue palette, cover page, then convert via `python3 -c "from weasyprint import HTML; HTML('report.html').write_pdf('report.pdf')"`).
   - **The report HTML and PDF must be written to `<output_dir>/`** (the date-specific directory).

3. **Report back** to the user with:
   - The digest summary (already shown in Phase 4)
   - Paths to all generated files: paper cards (.tex/.pdf), digest (.md), digest PDF, podcast MP3s
   - A count: "Analyzed X papers in depth, generated X LaTeX summary cards + X podcast episodes + 1 digest PDF"
   - The output directory path so the user knows where everything is

## Guidelines

- Be technically precise — this is for a researcher
- When a context file is provided, every "why it matters" must reference the specific project
- If no papers score >= the threshold, skip Phase 5 (no deep analysis needed) and just save the digest
- Always mention total counts: "X papers fetched, Y analyzed in depth"
- Pass the FULL research context to each subagent — they need it to produce relevant analysis
- All subagents for paper analysis should be launched IN PARALLEL in a single message
