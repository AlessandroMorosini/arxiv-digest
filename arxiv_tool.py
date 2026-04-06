#!/usr/bin/env python3
"""arXiv Daily Digest Tool — fetch, cache, and manage arXiv papers."""

import argparse
import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import arxiv
import yaml

BASE_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = BASE_DIR / "config.yaml"
CACHE_DIR = BASE_DIR / "cache"
HISTORY_FILE = BASE_DIR / ".history.jsonl"


def load_config():
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)


def load_history():
    seen = set()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    aid = json.loads(line)["arxiv_id"]
                    seen.add(aid.split("v")[0])
    return seen


def append_history(papers):
    with open(HISTORY_FILE, "a") as f:
        for p in papers:
            record = {
                "arxiv_id": p["arxiv_id"],
                "date": date.today().isoformat(),
                "title": p["title"],
            }
            f.write(json.dumps(record) + "\n")


def paper_to_dict(result):
    return {
        "arxiv_id": result.get_short_id(),
        "title": result.title,
        "authors": [a.name for a in result.authors],
        "abstract": result.summary.replace("\n", " "),
        "categories": result.categories,
        "primary_category": result.primary_category,
        "pdf_url": result.pdf_url,
        "published": result.published.strftime("%Y-%m-%d"),
        "updated": result.updated.strftime("%Y-%m-%d") if result.updated else None,
        "comment": result.comment,
        "arxiv_url": result.entry_id,
    }


def extract_pdf_text(path):
    """Extract text from a PDF file using pymupdf if available, else pdfminer."""
    try:
        import fitz  # pymupdf
        doc = fitz.open(str(path))
        text = "\n\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except ImportError:
        pass
    try:
        from pdfminer.high_level import extract_text
        return extract_text(str(path))
    except ImportError:
        pass
    print("Error: PDF context requires pymupdf or pdfminer. Install with: pip3 install pymupdf", file=sys.stderr)
    sys.exit(1)


def resolve_context(args, config):
    """Read context from --context file or fall back to config interests."""
    if args.context:
        context_path = Path(args.context).expanduser().resolve()
        if not context_path.exists():
            print(f"Error: context file not found: {context_path}", file=sys.stderr)
            sys.exit(1)
        if context_path.suffix.lower() == ".pdf":
            return extract_pdf_text(context_path), str(args.context)
        return context_path.read_text(), str(args.context)
    interests = config.get("interests", "")
    return interests if interests else None, "config.yaml"


def resolve_output_dir(args, config):
    """Resolve the base output directory from --output, config, or default."""
    if getattr(args, "output", None):
        return Path(args.output).expanduser().resolve()
    save_dir = config.get("output", {}).get("save_dir", "digests")
    return BASE_DIR / save_dir


def cmd_daily(args):
    config = load_config()
    categories = args.categories.split(",") if args.categories else config["categories"]
    max_papers = args.max or config.get("max_papers", 50)
    threshold = args.threshold or config.get("relevance_threshold", 8)
    context_text, context_source = resolve_context(args, config)
    output_dir = resolve_output_dir(args, config)

    lookback = config.get("lookback_days", 1)
    # Weekends and Mondays: arXiv doesn't publish Sat/Sun, so look back further
    weekday = date.today().weekday()
    if weekday == 0:    # Monday — cover Fri+Sat+Sun
        lookback = max(lookback, 3)
    elif weekday == 5:  # Saturday — cover Thu+Fri
        lookback = max(lookback, 2)
    elif weekday == 6:  # Sunday — cover Fri+Sat
        lookback = max(lookback, 3)

    cutoff_date = (datetime.utcnow() - timedelta(days=lookback)).date()

    seen_ids = load_history()

    if getattr(args, "from_file", None):
        # Read pre-fetched papers (e.g. from WebFetch + parse_arxiv_feed.py)
        with open(args.from_file) as f:
            raw = json.load(f)
        papers = []
        local_seen = set()
        for p in raw:
            base_id = p["arxiv_id"].split("v")[0]
            if base_id in seen_ids or base_id in local_seen:
                continue
            if p.get("published", "") < cutoff_date.isoformat():
                continue
            local_seen.add(base_id)
            papers.append(p)
    else:
        # Query by category only — arXiv's submittedDate query filter is
        # unreliable. Instead, fetch recent papers sorted by date and
        # filter client-side by the lookback window.
        cat_query = " OR ".join(f"cat:{cat}" for cat in categories)
        full_query = cat_query

        client = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=3)
        search = arxiv.Search(
            query=full_query,
            max_results=max_papers,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        papers = []
        local_seen = set()

        for result in client.results(search):
            short_id = result.get_short_id()
            base_id = short_id.split("v")[0]  # strip version
            if base_id in seen_ids or base_id in local_seen:
                continue
            if result.published.date() < cutoff_date:
                continue
            local_seen.add(base_id)
            papers.append(paper_to_dict(result))

    # Cache results
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{date.today().isoformat()}.json"
    with open(cache_file, "w") as f:
        json.dump(papers, f, indent=2)

    # Update history
    append_history(papers)

    # If no new papers found, fall back to the most recent non-empty cache
    if not papers:
        cache_files = sorted(CACHE_DIR.glob("*.json"), reverse=True)
        for cf in cache_files:
            if cf == cache_file:
                continue
            with open(cf) as f:
                cached = json.load(f)
            if cached:
                papers = cached
                cache_file = cf
                print(f"# No new papers today — using most recent cache: {cf.name} ({len(papers)} papers)", file=sys.stderr)
                break

    # Ensure output directory for today exists
    today_str = date.today().isoformat()
    today_output = output_dir / today_str
    today_output.mkdir(parents=True, exist_ok=True)

    # Compute podcast directory as sibling of base output dir
    podcast_dir = output_dir.parent / "podcasts" / today_str

    # Pre-compute tier boundaries
    tiers = {
        "top": threshold,
        "mid": threshold - 3,
    }

    # Output
    output = {
        "context": context_text,
        "context_source": context_source,
        "output_dir": str(today_output),
        "podcast_dir": str(podcast_dir),
        "date": today_str,
        "relevance_threshold": threshold,
        "tiers": tiers,
        "papers": papers,
    }
    print(json.dumps(output, indent=2))
    print(f"\n# Fetched {len(papers)} new papers (cached to {cache_file})", file=sys.stderr)
    print(f"# Output directory: {today_output}", file=sys.stderr)


def cmd_search(args):
    config = load_config()
    context_text, context_source = resolve_context(args, config)
    max_results = args.max or 20

    client = arxiv.Client(page_size=50, delay_seconds=3.0, num_retries=3)
    search = arxiv.Search(
        query=args.query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    seen = set()
    for result in client.results(search):
        short_id = result.get_short_id()
        base_id = short_id.split("v")[0]
        if base_id in seen:
            continue
        seen.add(base_id)
        papers.append(paper_to_dict(result))

    output = {
        "context": context_text,
        "context_source": context_source,
        "papers": papers,
    }
    print(json.dumps(output, indent=2))
    print(f"\n# Found {len(papers)} papers for query: {args.query}", file=sys.stderr)


def cmd_config(args):
    if args.show:
        with open(CONFIG_FILE) as f:
            print(f.read())
    elif args.set:
        key, _, value = args.set.partition("=")
        config = load_config()
        # Handle nested keys with dot notation
        keys = key.strip().split(".")
        target = config
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        # Try to parse value as YAML for proper typing
        parsed = yaml.safe_load(value.strip())
        target[keys[-1]] = parsed
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"Updated {key} = {parsed}")
    else:
        print("Use --show to display config or --set key=value to update it")


def cmd_history(args):
    config = load_config()
    output_dir = resolve_output_dir(args, config)
    last_n = args.last or 7
    if not HISTORY_FILE.exists():
        print(json.dumps({"digests": [], "total_papers": 0}))
        return

    by_date = {}
    with open(HISTORY_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            d = record["date"]
            if d not in by_date:
                by_date[d] = {"date": d, "count": 0, "papers": []}
            by_date[d]["count"] += 1
            by_date[d]["papers"].append(record["title"])

    # Sort by date descending, take last N
    digests = sorted(by_date.values(), key=lambda x: x["date"], reverse=True)[:last_n]

    # Also check for saved digest files
    for d in digests:
        digest_dir = output_dir / d["date"]
        d["has_digest"] = (digest_dir / "digest.md").exists()

    result = {
        "digests": digests,
        "total_papers": sum(d["count"] for d in digests),
    }
    print(json.dumps(result, indent=2))


def cmd_save(args):
    config = load_config()
    output_dir = resolve_output_dir(args, config)
    target_date = args.date or date.today().isoformat()
    digest_dir = output_dir / target_date
    digest_dir.mkdir(parents=True, exist_ok=True)

    if args.file and args.file != "/dev/stdin":
        with open(args.file) as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    output_path = digest_dir / "digest.md"
    with open(output_path, "w") as f:
        f.write(content)

    # Also copy cached papers.json if available
    cache_file = CACHE_DIR / f"{target_date}.json"
    if cache_file.exists():
        papers_path = digest_dir / "papers.json"
        if not papers_path.exists():
            import shutil
            shutil.copy2(cache_file, papers_path)

    print(f"Digest saved to {output_path}", file=sys.stderr)
    print(str(output_path))


def main():
    parser = argparse.ArgumentParser(
        description="arXiv Daily Digest Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # daily
    p_daily = subparsers.add_parser("daily", help="Fetch today's papers")
    p_daily.add_argument("--categories", type=str, help="Comma-separated arXiv categories")
    p_daily.add_argument("--max", type=int, help="Max papers to fetch")
    p_daily.add_argument("--context", type=str, help="Path to context file (README, spec, etc.)")
    p_daily.add_argument("--output", type=str, help="Base output directory (default: digests/)")
    p_daily.add_argument("--threshold", type=int, help="Relevance threshold for deep analysis (default: from config)")
    p_daily.add_argument("--from-file", type=str, dest="from_file", help="Read pre-fetched papers from JSON file instead of querying the API")
    p_daily.set_defaults(func=cmd_daily)

    # search
    p_search = subparsers.add_parser("search", help="Search arXiv for papers")
    p_search.add_argument("query", type=str, help="Search query")
    p_search.add_argument("--max", type=int, help="Max results")
    p_search.add_argument("--context", type=str, help="Path to context file (README, spec, etc.)")
    p_search.set_defaults(func=cmd_search)

    # config
    p_config = subparsers.add_parser("config", help="Show or edit configuration")
    p_config.add_argument("--show", action="store_true", help="Display current config")
    p_config.add_argument("--set", type=str, help="Set a config value (key=value)")
    p_config.set_defaults(func=cmd_config)

    # history
    p_history = subparsers.add_parser("history", help="Show digest history")
    p_history.add_argument("--last", type=int, default=7, help="Number of days to show")
    p_history.add_argument("--output", type=str, help="Base output directory (default: digests/)")
    p_history.set_defaults(func=cmd_history)

    # save
    p_save = subparsers.add_parser("save", help="Save digest content")
    p_save.add_argument("--date", type=str, help="Date for this digest (YYYY-MM-DD)")
    p_save.add_argument("--file", type=str, default="/dev/stdin", help="File to read content from")
    p_save.add_argument("--output", type=str, help="Base output directory (default: digests/)")
    p_save.set_defaults(func=cmd_save)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
