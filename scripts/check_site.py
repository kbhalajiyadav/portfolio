#!/usr/bin/env python3
"""Audit generated Hugo HTML, local references, metadata, and deployment files."""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.ids: list[str] = []
        self.title = False
        self.description = False
        self.canonical = False
        self.viewport = False
        self.html_lang = False
        self.h1_count = 0
        self.og_title = False
        self.og_description = False
        self.og_image = False
        self.twitter_card = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html" and (data.get("lang") or "").strip():
            self.html_lang = True
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag == "img" and data.get("src"):
            self.images.append({
                "src": data.get("src"), "alt": data.get("alt"),
                "width": data.get("width"), "height": data.get("height"),
            })
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title = True
        if tag == "meta":
            name = (data.get("name") or "").lower()
            prop = (data.get("property") or "").lower()
            content = (data.get("content") or "").strip()
            if name == "description" and content:
                self.description = True
            elif name == "viewport" and content:
                self.viewport = True
            elif name == "twitter:card" and content:
                self.twitter_card = True
            elif prop == "og:title" and content:
                self.og_title = True
            elif prop == "og:description" and content:
                self.og_description = True
            elif prop == "og:image" and content:
                self.og_image = True
        if tag == "link" and "canonical" in (data.get("rel") or "").split() and data.get("href"):
            self.canonical = True


def target_for(root: Path, source: Path, url: str) -> tuple[Path, str | None] | None:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https", "mailto", "tel"} or url.startswith("//"):
        return None
    path = unquote(parsed.path)
    fragment = unquote(parsed.fragment) if parsed.fragment else None
    if not path:
        target = source
    elif path.startswith("/"):
        target = root / path.lstrip("/")
    else:
        target = source.parent / path
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    elif not target.suffix:
        target = target / "index.html"
    return target.resolve(), fragment


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        print(f"ERROR: generated site directory does not exist: {root}", file=sys.stderr)
        return 1
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}
    for html in root.rglob("*.html"):
        parser = PageParser()
        parser.feed(html.read_text(encoding="utf-8", errors="replace"))
        relative = html.relative_to(root)
        pages[html.resolve()] = parser
        if not parser.html_lang: errors.append(f"{relative}: missing html lang")
        if not parser.viewport: errors.append(f"{relative}: missing viewport meta")
        if not parser.title: errors.append(f"{relative}: missing title")
        if not parser.description: errors.append(f"{relative}: missing meta description")
        if not parser.canonical: errors.append(f"{relative}: missing canonical URL")
        if not parser.og_title: errors.append(f"{relative}: missing og:title")
        if not parser.og_description: errors.append(f"{relative}: missing og:description")
        if not parser.og_image: errors.append(f"{relative}: missing og:image")
        if not parser.twitter_card: errors.append(f"{relative}: missing twitter card")
        if parser.h1_count != 1: errors.append(f"{relative}: expected exactly one h1, found {parser.h1_count}")
        duplicates = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
        if duplicates: errors.append(f"{relative}: duplicate IDs {duplicates}")
        for image in parser.images:
            if image["alt"] is None: errors.append(f"{relative}: image missing alt attribute: {image['src']}")
            if not image["width"] or not image["height"]:
                errors.append(f"{relative}: image missing intrinsic dimensions: {image['src']}")
    for html, parser in pages.items():
        for ref in parser.links + [str(image["src"]) for image in parser.images]:
            result = target_for(root, html, ref)
            if result is None: continue
            target, fragment = result
            if not target.exists():
                errors.append(f"{html.relative_to(root)}: missing local target {ref}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{html.relative_to(root)}: missing fragment {ref}")
    if (root / "authors").exists(): errors.append("unexpected generated authors archive")
    for required in (
        "robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt", "humans.txt",
        "CNAME", ".well-known/security.txt", "media/og-card.png",
    ):
        target = root / required
        if not target.exists(): errors.append(f"missing generated {required}")
        elif target.is_file() and target.stat().st_size == 0: errors.append(f"empty generated {required}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Generated-site audit passed: {len(pages)} HTML pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
