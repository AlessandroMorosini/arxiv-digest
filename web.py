"""Flask web UI for browsing arxiv-digest outputs."""

import json
import re
from pathlib import Path

from flask import Flask, abort, render_template, request, send_from_directory

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
LEGACY_DIGESTS_DIR = BASE_DIR / "digests"
LEGACY_PODCASTS_DIR = BASE_DIR / "podcasts"


def slugify(text: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def strip_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", arxiv_id)


def get_dates() -> list[str]:
    dates = set()
    for directory in (OUTPUT_DIR, LEGACY_DIGESTS_DIR):
        if directory.exists():
            for d in directory.iterdir():
                if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name):
                    dates.add(d.name)
    return sorted(dates, reverse=True)


def resolve_date_dir(date: str) -> Path | None:
    """Resolve date directory, preferring output/ over legacy digests/."""
    primary = OUTPUT_DIR / date
    if primary.is_dir():
        return primary
    legacy = LEGACY_DIGESTS_DIR / date
    if legacy.is_dir():
        return legacy
    return None


def load_papers_json(date: str) -> dict:
    date_dir = resolve_date_dir(date)
    if not date_dir:
        return {}
    path = date_dir / "papers.json"
    if not path.exists():
        return {}
    with open(path) as f:
        papers = json.load(f)
    return {strip_version(p["arxiv_id"]): p for p in papers}


def parse_digest(date: str) -> tuple[list[dict], dict]:
    date_dir = resolve_date_dir(date)
    if not date_dir:
        return [], {}
    path = date_dir / "digest.md"
    if not path.exists():
        return [], {}

    text = path.read_text()

    header = {}
    ctx = re.search(r"\*\*Research context:\*\*\s*(.+)", text)
    if ctx:
        header["context"] = ctx.group(1)
    else:
        ctx = re.search(r"## Context:\s*(.+)", text)
        if ctx:
            header["context"] = ctx.group(1)

    m = re.search(r"(\d+)\s*papers?\s*fetched", text) or re.search(
        r"\*\*Papers fetched:\*\*\s*(\d+)", text
    )
    if m:
        header["fetched"] = int(m.group(1))

    m = re.search(r"(\d+)\s*analyzed\s*in\s*depth", text) or re.search(
        r"\*\*Analyzed in depth:\*\*\s*(\d+)", text
    )
    if m:
        header["analyzed"] = int(m.group(1))

    paper_re = re.compile(r"###\s+\[(.+?)\]\((.+?)\)\s*.*?(\d+)/10")
    matches = list(paper_re.finditer(text))
    papers = []

    for i, match in enumerate(matches):
        title = match.group(1)
        url = match.group(2)
        score = int(match.group(3))

        aid = re.search(r"abs/(.+?)(?:\s|$)", url)
        arxiv_id = aid.group(1) if aid else ""

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        bullets = re.findall(r"^- (.+)$", block, re.MULTILINE)
        summary_lines = []
        paper_card = None
        podcast = None

        for bullet in bullets:
            cm = re.match(r"Paper card:\s*`(.+?)`", bullet)
            pm = re.match(r"Podcast:\s*`(.+?)`", bullet)
            if cm:
                paper_card = cm.group(1)
            elif pm:
                podcast = pm.group(1)
            else:
                summary_lines.append(bullet)

        papers.append(
            {
                "title": title,
                "arxiv_url": url,
                "arxiv_id": arxiv_id,
                "base_id": strip_version(arxiv_id),
                "score": score,
                "summary": summary_lines,
                "paper_card": paper_card,
                "podcast": podcast,
            }
        )

    return papers, header


@app.route("/")
def index():
    dates = get_dates()
    summaries = []
    for date in dates:
        papers, header = parse_digest(date)
        top = sum(1 for p in papers if p["score"] >= 8)
        mid = sum(1 for p in papers if 5 <= p["score"] <= 7)
        has_podcasts = any(p.get("podcast") for p in papers)
        has_cards = any(p.get("paper_card") for p in papers)
        summaries.append(
            {
                "date": date,
                "context": header.get("context", ""),
                "fetched": header.get("fetched", len(papers)),
                "analyzed": header.get("analyzed", 0),
                "top_count": top,
                "mid_count": mid,
                "total_scored": len(papers),
                "has_podcasts": has_podcasts,
                "has_cards": has_cards,
            }
        )
    return render_template("index.html", summaries=summaries)


@app.route("/digest/<date>")
def digest(date):
    if not re.match(r"\d{4}-\d{2}-\d{2}$", date):
        abort(404)
    if not resolve_date_dir(date):
        abort(404)

    papers_scored, header = parse_digest(date)
    papers_json = load_papers_json(date)

    for p in papers_scored:
        full = papers_json.get(p["base_id"], {})
        p["authors"] = full.get("authors", [])
        p["abstract"] = full.get("abstract", "")
        p["primary_category"] = full.get("primary_category", "")

    top = [p for p in papers_scored if p["score"] >= 8]
    mid = [p for p in papers_scored if 5 <= p["score"] <= 7]
    low_count = max(header.get("fetched", 0) - len(papers_scored), 0)

    return render_template(
        "digest.html", date=date, header=header, top=top, mid=mid, low_count=low_count
    )


@app.route("/paper/<date>/<arxiv_id>")
def paper(date, arxiv_id):
    if not re.match(r"\d{4}-\d{2}-\d{2}$", date):
        abort(404)

    papers_scored, _ = parse_digest(date)
    papers_json = load_papers_json(date)
    base_id = strip_version(arxiv_id)

    scored = next((p for p in papers_scored if p["base_id"] == base_id), None)
    full = papers_json.get(base_id)

    if not scored and not full:
        abort(404)

    paper_data = {
        "arxiv_id": arxiv_id,
        "base_id": base_id,
        "title": scored["title"] if scored else full.get("title", ""),
        "score": scored["score"] if scored else None,
        "summary": scored.get("summary", []) if scored else [],
        "paper_card": scored.get("paper_card") if scored else None,
        "podcast": scored.get("podcast") if scored else None,
        "arxiv_url": scored["arxiv_url"] if scored else full.get("arxiv_url", ""),
        "authors": full.get("authors", []) if full else [],
        "abstract": full.get("abstract", "") if full else "",
        "categories": full.get("categories", []) if full else [],
        "primary_category": full.get("primary_category", "") if full else "",
        "published": full.get("published", "") if full else "",
        "pdf_url": full.get("pdf_url", "") if full else "",
        "comment": full.get("comment") if full else None,
    }

    return render_template("paper.html", date=date, paper=paper_data)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = []
    if query:
        q_lower = query.lower()
        for date in get_dates():
            papers_scored, _ = parse_digest(date)
            papers_json = load_papers_json(date)

            score_map = {p["base_id"]: p for p in papers_scored}

            for base_id, full in papers_json.items():
                title = full.get("title", "")
                abstract = full.get("abstract", "")
                if q_lower in title.lower() or q_lower in abstract.lower():
                    scored = score_map.get(base_id)
                    results.append(
                        {
                            "date": date,
                            "title": title,
                            "arxiv_id": full.get("arxiv_id", ""),
                            "base_id": base_id,
                            "score": scored["score"] if scored else None,
                            "primary_category": full.get("primary_category", ""),
                            "abstract_snippet": (
                                abstract[:200] + "..."
                                if len(abstract) > 200
                                else abstract
                            ),
                        }
                    )
    return render_template("search.html", query=query, results=results)


@app.route("/files/output/<path:filepath>")
def serve_output_file(filepath):
    return send_from_directory(OUTPUT_DIR, filepath)


@app.route("/files/digests/<path:filepath>")
def serve_legacy_digest_file(filepath):
    """Serve files from legacy digests/ directory for old digest.md references."""
    return send_from_directory(LEGACY_DIGESTS_DIR, filepath)


@app.route("/files/podcasts/<path:filepath>")
def serve_legacy_podcast_file(filepath):
    """Serve files from legacy podcasts/ directory for old digest.md references."""
    return send_from_directory(LEGACY_PODCASTS_DIR, filepath)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
