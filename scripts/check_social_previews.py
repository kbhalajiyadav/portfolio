#!/usr/bin/env python3
"""Verify branded social-preview assets and rendered metadata."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import struct
import sys
from urllib.parse import urlparse

REQUIRED_CARDS = {
    "portfolio.png",
    "research.png",
    "outputs.png",
    "experience.png",
    "engagement.png",
    "publication.png",
    "technology.png",
}

EXPECTED_PAGE_CARDS = {
    "index.html": "portfolio.png",
    "research/index.html": "research.png",
    "outputs/index.html": "outputs.png",
    "experience/index.html": "experience.png",
    "engagement/index.html": "engagement.png",
    "publication/adhesives-wearable/index.html": "publication.png",
    "project/quantitative-thermal-imaging/index.html": "technology.png",
    "project/peel-trace-evaluation/index.html": "outputs.png",
    "project/optical-metrology/index.html": "research.png",
    "project/fda-project/index.html": "experience.png",
}


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "meta":
            return
        data = dict(attrs)
        key = (data.get("property") or data.get("name") or "").lower().strip()
        value = (data.get("content") or "").strip()
        if key and value:
            self.meta[key] = value


def png_size(path: Path) -> tuple[int, int]:
    raw = path.read_bytes()[:24]
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return struct.unpack(">II", raw[16:24])


def local_social_target(root: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.hostname not in {"bhalaji.com", "www.bhalaji.com", "127.0.0.1", "localhost"}:
        return None
    if not parsed.path.startswith("/social/"):
        return None
    return root / parsed.path.lstrip("/")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    errors: list[str] = []
    social_dir = root / "social"

    for name in sorted(REQUIRED_CARDS):
        path = social_dir / name
        if not path.is_file():
            errors.append(f"missing social preview {path.relative_to(root)}")
            continue
        try:
            width, height = png_size(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        if (width, height) != (1200, 630):
            errors.append(f"{path.relative_to(root)}: expected 1200x630, found {width}x{height}")
        if path.stat().st_size < 20_000:
            errors.append(f"{path.relative_to(root)}: unexpectedly small rendered file")

    parsed_pages: dict[str, MetaParser] = {}
    for html in sorted(root.rglob("*.html")):
        relative = html.relative_to(root).as_posix()
        parser = MetaParser()
        parser.feed(html.read_text(encoding="utf-8", errors="replace"))
        parsed_pages[relative] = parser
        meta = parser.meta

        required = (
            "og:image", "og:image:type", "og:image:width", "og:image:height", "og:image:alt",
            "twitter:card", "twitter:image", "twitter:image:alt",
        )
        for key in required:
            if not meta.get(key):
                errors.append(f"{relative}: missing {key}")

        if meta.get("twitter:card") and meta["twitter:card"] != "summary_large_image":
            errors.append(f"{relative}: twitter:card must be summary_large_image")
        if meta.get("og:image:type") and meta["og:image:type"] != "image/png":
            errors.append(f"{relative}: og:image:type must be image/png")
        if meta.get("og:image:width") and meta["og:image:width"] != "1200":
            errors.append(f"{relative}: og:image:width must be 1200")
        if meta.get("og:image:height") and meta["og:image:height"] != "630":
            errors.append(f"{relative}: og:image:height must be 630")
        if meta.get("og:image") and meta.get("twitter:image") and meta["og:image"] != meta["twitter:image"]:
            errors.append(f"{relative}: OpenGraph and Twitter images differ")

        if meta.get("og:image"):
            target = local_social_target(root, meta["og:image"])
            if target is None:
                errors.append(f"{relative}: social image is not a canonical local /social/ asset: {meta['og:image']}")
            elif not target.is_file():
                errors.append(f"{relative}: social image target missing: {target.relative_to(root)}")

    for relative, expected_name in EXPECTED_PAGE_CARDS.items():
        parser = parsed_pages.get(relative)
        if parser is None:
            errors.append(f"missing representative page for social-card mapping: {relative}")
            continue
        actual = Path(urlparse(parser.meta.get("og:image", "")).path).name
        if actual != expected_name:
            errors.append(f"{relative}: expected social card {expected_name}, found {actual or 'none'}")

    if errors:
        print("Social-preview audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Social-preview audit passed: {len(REQUIRED_CARDS)} branded 1200x630 cards and {len(parsed_pages)} pages verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
