#!/usr/bin/env python3
"""Exercise the deployed text and homepage stylesheet contract against a local Hugo build."""
from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

from check_live_site import EXPECTED_TEXT, normalize_optional_attribute_quotes, validate_homepage_styles


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    site = args.site.resolve()
    # Apply the same textual release contract to every generated page that the
    # deployed-site smoke test will inspect. Catch stale assertions before deploy.
    errors: list[str] = []
    body = ""
    for route, needles in EXPECTED_TEXT.items():
        path = site / route / "index.html" if not route or route.endswith("/") else site / route
        if not path.is_file():
            errors.append(f"generated release path missing: {route or '/'}")
            continue
        page_text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            page_text = normalize_optional_attribute_quotes(page_text)
        if not route:
            body = page_text
        errors.extend(
            f"generated {route or 'homepage'} missing {needle!r}"
            for needle in needles
            if needle not in page_text
        )
    for obsolete in ("From stimulus to structure to measurement.", "Schematic; no quantitative data are implied."):
        if obsolete in body:
            errors.append(f"generated homepage still contains stale text {obsolete!r}")

    def local_fetch(url: str, _nonce: str) -> tuple[int, str, bytes]:
        path = (site / urlsplit(url).path.lstrip("/")).resolve()
        if not path.is_relative_to(site) or not path.is_file():
            raise OSError(f"missing local generated CSS asset {path}")
        return 200, "text/css", path.read_bytes()

    with patch("check_live_site.fetch", side_effect=local_fetch):
        errors.extend(validate_homepage_styles("https://bhalaji.com/", body, "local"))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Generated site release text and deployed-stylesheet contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
