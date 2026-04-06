#!/usr/bin/env python3
"""Parse arXiv Atom XML feed(s) into JSON compatible with arxiv_tool.py --from-file.

Usage:
    python3 parse_arxiv_feed.py feed1.xml [feed2.xml ...]
    cat feed.xml | python3 parse_arxiv_feed.py
"""

import json
import sys
import xml.etree.ElementTree as ET

ATOM = "http://www.w3.org/2005/Atom"
ARXIV = "http://arxiv.org/schemas/atom"


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall(f"{{{ATOM}}}entry"):
        id_text = entry.findtext(f"{{{ATOM}}}id", "")
        arxiv_id = id_text.split("/abs/")[-1] if "/abs/" in id_text else id_text
        title = (entry.findtext(f"{{{ATOM}}}title", "") or "").strip().replace("\n", " ")
        abstract = (entry.findtext(f"{{{ATOM}}}summary", "") or "").strip().replace("\n", " ")
        published = (entry.findtext(f"{{{ATOM}}}published", "") or "")[:10]
        updated_text = entry.findtext(f"{{{ATOM}}}updated", "")
        updated = updated_text[:10] if updated_text else None

        authors = [
            a.findtext(f"{{{ATOM}}}name", "")
            for a in entry.findall(f"{{{ATOM}}}author")
        ]

        primary_el = entry.find(f"{{{ARXIV}}}primary_category")
        primary_category = primary_el.get("term", "") if primary_el is not None else ""
        categories = [c.get("term", "") for c in entry.findall(f"{{{ATOM}}}category")]

        pdf_url = None
        for link in entry.findall(f"{{{ATOM}}}link"):
            if link.get("title") == "pdf":
                pdf_url = link.get("href")

        comment_el = entry.find(f"{{{ARXIV}}}comment")
        comment = comment_el.text if comment_el is not None else None

        papers.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "categories": categories,
            "primary_category": primary_category or (categories[0] if categories else ""),
            "pdf_url": pdf_url,
            "published": published,
            "updated": updated,
            "comment": comment,
            "arxiv_url": f"http://arxiv.org/abs/{arxiv_id}",
        })
    return papers


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        xml_text = sys.stdin.read()
        print(json.dumps(parse_feed(xml_text), indent=2))
        return

    all_papers = []
    seen = set()
    for path in files:
        with open(path) as f:
            xml_text = f.read()
        for paper in parse_feed(xml_text):
            base_id = paper["arxiv_id"].split("v")[0]
            if base_id not in seen:
                seen.add(base_id)
                all_papers.append(paper)

    print(json.dumps(all_papers, indent=2))


if __name__ == "__main__":
    main()
