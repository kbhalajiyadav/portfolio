#!/usr/bin/env python3
"""Audit rendered Hugo output for metadata, semantics, links, and assets."""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = False
        self.viewport = False
        self.description = False
        self.robots = ""
        self.title_parts: list[str] = []
        self._in_title = False
        self.canonical = ""
        self.manifest = False
        self.icon = False
        self.has_feed = False
        self.rel_me: list[str] = []
        self.og_title = False
        self.og_description = False
        self.og_image = False
        self.og_url = ""
        self.og_image_dimensions: set[str] = set()
        self.twitter_card = False
        self.twitter_title = False
        self.twitter_description = False
        self.twitter_image = False
        self.twitter_image_alt = False
        self.ids: list[str] = []
        self.links: list[str] = []
        self.anchor_records: list[dict[str, str]] = []
        self.images: list[dict[str, str | None]] = []
        self.h1_count = 0
        self.main_count = 0
        self.skip_target = False
        self._anchor_depth = 0
        self._anchor_text: list[str] = []
        self._current_anchor: dict[str, str] | None = None
        self.json_ld_blocks: list[str] = []
        self._in_json_ld = False
        self._json_parts: list[str] = []

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html" and (data.get("lang") or "").strip():
            self.html_lang = True
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
            self._anchor_depth = 1
            self._anchor_text = []
            self._current_anchor = {
                "href": data.get("href", ""),
                "target": data.get("target", ""),
                "rel": data.get("rel", ""),
            }
        elif self._anchor_depth:
            self._anchor_depth += 1
        if tag == "img" and data.get("src"):
            self.images.append({
                "src": data.get("src"),
                "alt": data.get("alt"),
                "width": data.get("width"),
                "height": data.get("height"),
            })
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
            if data.get("id") == "main-content":
                self.skip_target = True
        if tag == "title":
            self._in_title = True
        if tag == "script" and (data.get("type") or "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []
        if tag == "meta":
            name = (data.get("name") or "").lower()
            prop = (data.get("property") or "").lower()
            content = (data.get("content") or "").strip()
            if name == "description" and content:
                self.description = True
            elif name == "viewport" and content:
                self.viewport = True
            elif name == "robots":
                self.robots = content.lower()
            elif name == "twitter:card" and content:
                self.twitter_card = True
            elif name == "twitter:title" and content:
                self.twitter_title = True
            elif name == "twitter:description" and content:
                self.twitter_description = True
            elif name == "twitter:image" and content:
                self.twitter_image = True
            elif name == "twitter:image:alt" and content:
                self.twitter_image_alt = True
            elif prop == "og:title" and content:
                self.og_title = True
            elif prop == "og:description" and content:
                self.og_description = True
            elif prop == "og:image" and content:
                self.og_image = True
            elif prop == "og:url" and content:
                self.og_url = content
            elif prop in {"og:image:width", "og:image:height"} and content:
                self.og_image_dimensions.add(prop)
        if tag == "link":
            rel_tokens = {token.lower() for token in (data.get("rel") or "").split()}
            href = (data.get("href") or "").strip()
            if "canonical" in rel_tokens and href:
                self.canonical = href
            if "manifest" in rel_tokens and href:
                self.manifest = True
            if "icon" in rel_tokens and href:
                self.icon = True
            if "alternate" in rel_tokens and href and (data.get("type") or "").lower() in {"application/rss+xml", "application/atom+xml"}:
                self.has_feed = True
            if "me" in rel_tokens and href:
                self.rel_me.append(href)

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._anchor_depth:
            self._anchor_text.append(data)
        if self._in_json_ld:
            self._json_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_json_ld:
            self.json_ld_blocks.append("".join(self._json_parts).strip())
            self._in_json_ld = False
            self._json_parts = []
        if self._anchor_depth:
            if tag == "a" and self._anchor_depth == 1:
                record = self._current_anchor or {"href": "", "target": "", "rel": ""}
                record["text"] = " ".join("".join(self._anchor_text).split())
                self.anchor_records.append(record)
                self._anchor_depth = 0
                self._anchor_text = []
                self._current_anchor = None
            elif self._anchor_depth > 1:
                self._anchor_depth -= 1


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


def validate_json_ld(relative: Path, parser: PageParser, errors: list[str]) -> None:
    if not parser.json_ld_blocks:
        errors.append(f"{relative}: missing JSON-LD")
        return
    parsed_blocks: list[object] = []
    for index, block in enumerate(parser.json_ld_blocks, 1):
        if not block:
            errors.append(f"{relative}: empty JSON-LD block {index}")
            continue
        try:
            parsed_blocks.append(json.loads(block))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON-LD block {index}: {exc}")
    if relative == Path("index.html"):
        types: set[str] = set()
        for block in parsed_blocks:
            if not isinstance(block, dict):
                continue
            graph = block.get("@graph", [])
            if isinstance(graph, list):
                for item in graph:
                    if isinstance(item, dict) and isinstance(item.get("@type"), str):
                        types.add(item["@type"])
        missing = {"WebSite", "ProfilePage", "Person"} - types
        if missing:
            errors.append(f"{relative}: identity JSON-LD missing types {sorted(missing)}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        print(f"ERROR: generated site directory does not exist: {root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    pages: dict[Path, PageParser] = {}
    for html in sorted(root.rglob("*.html")):
        parser = PageParser()
        parser.feed(html.read_text(encoding="utf-8", errors="replace"))
        relative = html.relative_to(root)
        pages[html.resolve()] = parser

        if not parser.html_lang: errors.append(f"{relative}: missing html lang")
        if not parser.viewport: errors.append(f"{relative}: missing viewport meta")
        if not parser.title: errors.append(f"{relative}: missing or empty title")
        if not parser.description: errors.append(f"{relative}: missing meta description")
        if not parser.canonical: errors.append(f"{relative}: missing canonical URL")
        elif urlparse(parser.canonical).scheme not in {"http", "https"}: errors.append(f"{relative}: canonical URL is not absolute: {parser.canonical}")
        if not parser.robots: errors.append(f"{relative}: missing robots directive")
        elif relative == Path("404.html") and "noindex" not in parser.robots: errors.append("404.html: must be noindex")
        elif relative != Path("404.html") and "noindex" in parser.robots: errors.append(f"{relative}: unexpectedly noindex")
        if not parser.manifest: errors.append(f"{relative}: missing web manifest discovery")
        if not parser.icon: errors.append(f"{relative}: missing favicon discovery")
        if not parser.has_feed: errors.append(f"{relative}: missing RSS discovery")
        if len(set(parser.rel_me)) < 4: errors.append(f"{relative}: expected four rel=me identity links")
        if not parser.og_title: errors.append(f"{relative}: missing og:title")
        if not parser.og_description: errors.append(f"{relative}: missing og:description")
        if not parser.og_image: errors.append(f"{relative}: missing og:image")
        if not parser.og_url: errors.append(f"{relative}: missing og:url")
        elif parser.canonical and parser.og_url != parser.canonical: errors.append(f"{relative}: og:url differs from canonical")
        if parser.og_image_dimensions != {"og:image:width", "og:image:height"}: errors.append(f"{relative}: missing Open Graph image dimensions")
        if not parser.twitter_card: errors.append(f"{relative}: missing Twitter card")
        if not parser.twitter_title: errors.append(f"{relative}: missing Twitter title")
        if not parser.twitter_description: errors.append(f"{relative}: missing Twitter description")
        if not parser.twitter_image: errors.append(f"{relative}: missing Twitter image")
        if not parser.twitter_image_alt: errors.append(f"{relative}: missing Twitter image alt")
        if parser.h1_count != 1: errors.append(f"{relative}: expected exactly one h1, found {parser.h1_count}")
        if parser.main_count != 1: errors.append(f"{relative}: expected exactly one main landmark, found {parser.main_count}")
        if not parser.skip_target: errors.append(f"{relative}: missing #main-content skip-link target")

        for anchor in parser.anchor_records:
            text = anchor.get("text", "").strip()
            if text.lower() in {"details", "more", "click here", "read more"}:
                errors.append(f"{relative}: ambiguous link text: {text!r}")
            if anchor.get("target") == "_blank" and "noopener" not in anchor.get("rel", "").split():
                errors.append(f"{relative}: target=_blank link missing noopener: {anchor.get('href')}")

        duplicates = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
        if duplicates: errors.append(f"{relative}: duplicate IDs {duplicates}")
        for image in parser.images:
            if image["alt"] is None: errors.append(f"{relative}: image missing alt attribute: {image['src']}")
            if not image["width"] or not image["height"]: errors.append(f"{relative}: image missing intrinsic dimensions: {image['src']}")
        validate_json_ld(relative, parser, errors)

    for html, parser in pages.items():
        for ref in parser.links + [str(image["src"]) for image in parser.images]:
            result = target_for(root, html, ref)
            if result is None:
                continue
            target, fragment = result
            if not target.exists():
                errors.append(f"{html.relative_to(root)}: missing local target {ref}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{html.relative_to(root)}: missing fragment {ref}")

    if (root / "authors").exists():
        errors.append("unexpected generated authors archive")
    for required in (
        "robots.txt", "sitemap.xml", "index.xml", "llms.txt", "llms-full.txt", "humans.txt",
        "CNAME", ".well-known/security.txt", "media/og-card.png", "media/icon.png", "site.webmanifest",
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
