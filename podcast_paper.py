#!/usr/bin/env python3
"""Generate a podcast episode for an arXiv paper via NotebookLM.

Usage:
    python3 podcast_paper.py <arxiv_url> <title> [--output-dir DIR] [--date YYYY-MM-DD]

Produces an MP3 file in the output directory (default: current directory).
"""

import argparse
import asyncio
import re
import sys
from datetime import date
from pathlib import Path

from notebooklm import NotebookLMClient


def slugify(text: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


async def generate_podcast(arxiv_url: str, title: str, output_dir: Path, date_str: str | None = None, context: str | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    if date_str is None:
        date_str = date.today().isoformat()
    output_path = output_dir / f"podcast-{slug}-{date_str}.mp3"

    async with await NotebookLMClient.from_storage() as client:
        # Create a notebook for this paper
        nb = await client.notebooks.create(f"arXiv: {title[:80]}")

        # Add the arXiv URL as a source and wait for processing
        await client.sources.add_url(nb.id, arxiv_url, wait=True)

        # Build instructions with optional listener context
        parts = [
            "Create a focused podcast episode about this research paper. "
            "HARD LIMIT: 12 minutes maximum. "
            "Be dense and direct: skip filler, small talk, and lengthy introductions.",
        ]
        if context:
            parts.append(
                f"\nThe listener is a researcher. Infer their background from this context: {context}. "
                "Avoid over-explaining or re-explaining concepts they likely already know. "
                "Background that falls outside their expertise is welcome — just don't rehash the basics of their own field."
            )
        parts.append(
            "\nFocus on: (1) the core contribution and what's novel, "
            "(2) key methodology choices, (3) main results, "
            "(4) why this matters and open questions."
        )
        instructions = " ".join(parts)

        # Generate the audio overview
        status = await client.artifacts.generate_audio(
            nb.id,
            instructions=instructions,
        )
        await client.artifacts.wait_for_completion(nb.id, status.task_id, timeout=900)

        # Download the generated audio (retry with backoff — artifact may
        # not be immediately available after wait_for_completion returns)
        for attempt in range(12):
            try:
                await client.artifacts.download_audio(nb.id, str(output_path))
                break
            except Exception:
                if attempt == 11:
                    raise
                wait = 15 * (attempt + 1)  # 15s, 30s, 45s, ...
                print(f"Audio not ready yet, retrying in {wait}s (attempt {attempt + 1}/12)...", file=sys.stderr)
                await asyncio.sleep(wait)

    print(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate a podcast for an arXiv paper")
    parser.add_argument("url", help="arXiv paper URL")
    parser.add_argument("title", help="Paper title")
    parser.add_argument("--output-dir", default=".", help="Output directory for the MP3")
    parser.add_argument("--date", default=None, help="Date string (YYYY-MM-DD) for filename; defaults to today")
    parser.add_argument("--context", default=None, help="Short description of the listener's expertise (concepts to skip)")
    args = parser.parse_args()

    try:
        path = asyncio.run(generate_podcast(args.url, args.title, Path(args.output_dir), args.date, args.context))
    except Exception as e:
        error_msg = str(e).lower()
        if "auth" in error_msg or "credential" in error_msg or "login" in error_msg or "token" in error_msg:
            print(
                "ERROR: NotebookLM authentication failed.\n"
                "Please re-authenticate by running:\n"
                "  notebooklm login\n"
                "Then retry.",
                file=sys.stderr,
            )
            sys.exit(2)
        raise
    return path


if __name__ == "__main__":
    main()
