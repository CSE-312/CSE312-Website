#!/usr/bin/env python3
"""Verify that rendered Quarto HTML has all of its local assets on disk.

Quarto derives the supporting-files directory from the input filename, so two
formats rendered from one .qmd will fight over the same "<name>_files" folder
unless they use separate output directories. When that happens the deck still
looks fine as markup but loses reveal.js, so it renders as a plain document.
This check fails the build instead of shipping a broken deck.

Usage:
  python verify_output.py path/to/_output
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

REF_ATTRS = ("src", "href", "data-src")
SKIP_PREFIXES = ("http://", "https://", "//", "data:", "mailto:", "#", "javascript:")


class RefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in REF_ATTRS and value:
                self.refs.append(value)


def local_refs(html: str) -> list[str]:
    collector = RefCollector()
    collector.feed(html)
    refs = []
    for ref in collector.refs:
        ref = ref.strip()
        if not ref or ref.startswith(SKIP_PREFIXES):
            continue
        path = unquote(urlparse(ref).path)
        if path:
            refs.append(path)
    return refs


def check_document(html_path: Path) -> list[str]:
    html = html_path.read_text(encoding="utf-8", errors="replace")
    problems = []

    for ref in sorted(set(local_refs(html))):
        if not (html_path.parent / ref).exists():
            problems.append(f"missing asset: {ref}")

    is_deck = "reveal" in html_path.name or 'class="reveal"' in html
    if is_deck:
        if 'class="reveal"' not in html:
            problems.append("no reveal container found")
        if not re.search(r"Reveal\.initialize", html):
            problems.append("no Reveal.initialize() call found")
        slides = len(re.findall(r'class="[^"]*\bslide\b[^"]*level\d', html))
        if slides < 2:
            problems.append(f"expected multiple slides, found {slides}")
        # Nested <section> wrappers mean slides became a vertical stack, which
        # only advances with the down arrow.
        if re.search(r"<section>\s*<section", html):
            problems.append("slides are nested in vertical stacks")
    else:
        headings = len(re.findall(r"<h1\b", html))
        if headings > 1:
            problems.append(f"expected a single h1, found {headings}")

    return problems


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    output_dir = Path(sys.argv[1])
    if not output_dir.is_dir():
        print(f"Output directory not found: {output_dir}", file=sys.stderr)
        return 1

    documents = sorted(output_dir.rglob("*.html"))
    if not documents:
        print(f"No HTML found under {output_dir}", file=sys.stderr)
        return 1

    failed = False
    for document in documents:
        problems = check_document(document)
        label = document.relative_to(output_dir)
        if problems:
            failed = True
            print(f"  FAIL {label}")
            for problem in problems:
                print(f"        - {problem}")
        else:
            print(f"  OK   {label}")

    if failed:
        print("\nVerification failed.", file=sys.stderr)
        return 1

    print("\nAll rendered documents verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
