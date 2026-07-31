#!/usr/bin/env python3
"""Browser-level audit for in-flow privacy controls and portfolio spacing rhythm."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from urllib.parse import quote, urljoin

from check_responsive import CDP, free_port, read_json, wait_ready

VIEWPORTS = [
    (390, 844, "390-mobile"),
    (768, 900, "768-tablet"),
    (1440, 1000, "1440-desktop"),
]
PAGES = [
    ("", "home"),
    ("research/", "research"),
    ("publication/adhesives-wearable/", "publication"),
    ("project/peel-trace-evaluation/", "project"),
]

GEOMETRY_EXPRESSION = r"""
(() => {
  const rect = (selector) => {
    const element = document.querySelector(selector);
    if (!element) return null;
    const box = element.getBoundingClientRect();
    return {
      top: box.top,
      right: box.right,
      bottom: box.bottom,
      left: box.left,
      width: box.width,
      height: box.height
    };
  };
  const number = (value) => Number.parseFloat(value) || 0;
  const banner = document.querySelector('[data-privacy-banner]');
  const sections = [...document.querySelectorAll('.section')];
  const articleHeadings = [...document.querySelectorAll('.article-content h2')];
  return {
    bannerVisible: Boolean(banner && !banner.hidden && getComputedStyle(banner).display !== 'none'),
    bannerPosition: banner ? getComputedStyle(banner).position : null,
    banner: rect('[data-privacy-banner]'),
    siteHeader: rect('.site-head'),
    main: rect('#main-content'),
    hero: rect('.hero'),
    heroPaddingTop: document.querySelector('.hero') ? number(getComputedStyle(document.querySelector('.hero')).paddingTop) : null,
    shell: rect('.page-shell'),
    backLink: rect('.back-link'),
    pageHeader: rect('.page-header'),
    articleLayout: rect('.article-layout'),
    sectionPadding: sections.map((element) => {
      const style = getComputedStyle(element);
      return {top: number(style.paddingTop), bottom: number(style.paddingBottom)};
    }),
    articleHeadingMargins: articleHeadings.map((element) => number(getComputedStyle(element).marginTop)),
    viewportHeight: innerHeight,
    viewportWidth: innerWidth
  };
})()
"""


def between(value: float, low: float, high: float) -> bool:
    return low <= value <= high


def validate(record: dict, page_name: str) -> list[str]:
    errors: list[str] = []
    banner = record.get("banner")
    header = record.get("siteHeader")
    main = record.get("main")

    if not record.get("bannerVisible") or not banner:
        return ["analytics privacy notice is not visible for a new visitor"]
    if record.get("bannerPosition") not in {"relative", "static"}:
        errors.append(f"privacy notice must remain in document flow; position={record.get('bannerPosition')!r}")
    if header and banner["top"] < header["bottom"] - 2:
        errors.append("privacy notice overlaps the site header")
    if main and banner["bottom"] > main["top"] + 2:
        errors.append(
            f"privacy notice overlaps main content: banner bottom={banner['bottom']:.1f}, main top={main['top']:.1f}"
        )
    if banner["height"] > record["viewportHeight"] * 0.52:
        errors.append(
            f"privacy notice is too tall for the viewport: {banner['height']:.1f}px of {record['viewportHeight']}px"
        )

    if page_name == "home":
        hero_padding = record.get("heroPaddingTop")
        if hero_padding is None or not between(hero_padding, 36, 96):
            errors.append(f"home introduction top spacing is outside the intended range: {hero_padding}")
        for index, padding in enumerate(record.get("sectionPadding", []), start=1):
            if not between(padding["top"], 64, 112) or not between(padding["bottom"], 64, 112):
                errors.append(f"homepage section {index} spacing is inconsistent: {padding}")
    else:
        shell = record.get("shell")
        back = record.get("backLink")
        page_header = record.get("pageHeader")
        article = record.get("articleLayout")
        if not all((shell, back, page_header, article)):
            errors.append("internal-page spacing anchors are missing")
        else:
            shell_top_space = back["top"] - shell["top"]
            back_to_header = page_header["top"] - back["bottom"]
            header_to_article = article["top"] - page_header["bottom"]
            if not between(shell_top_space, 28, 100):
                errors.append(f"internal page top spacing is inconsistent: {shell_top_space:.1f}px")
            if not between(back_to_header, 20, 72):
                errors.append(f"back-link to header spacing is inconsistent: {back_to_header:.1f}px")
            if not between(header_to_article, 24, 84):
                errors.append(f"header to article spacing is inconsistent: {header_to_article:.1f}px")
        for margin in record.get("articleHeadingMargins", []):
            if not between(margin, 32, 56):
                errors.append(f"article section-heading spacing is inconsistent: {margin:.1f}px")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/layout-spacing.json")
    parser.add_argument("--screenshots", default="artifacts/layout-spacing-screenshots")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    screenshots = Path(args.screenshots)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    screenshots.mkdir(parents=True, exist_ok=True)

    port = free_port()
    with tempfile.TemporaryDirectory(prefix="portfolio-spacing-chrome-", ignore_cleanup_errors=True) as profile:
        process = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--hide-scrollbars",
                "--remote-allow-origins=*",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            deadline = time.time() + 20
            while True:
                try:
                    read_json(f"http://127.0.0.1:{port}/json/version", timeout=1)
                    break
                except Exception:
                    if time.time() >= deadline:
                        stderr = process.stderr.read() if process.stderr else ""
                        raise RuntimeError(f"Chrome DevTools endpoint did not start: {stderr[-2000:]}")
                    time.sleep(0.2)

            target = read_json(
                f"http://127.0.0.1:{port}/json/new?{quote('about:blank', safe=':/?=&')}",
                method="PUT",
            )
            cdp = CDP(target["webSocketDebuggerUrl"])
            try:
                cdp.command("Page.enable")
                cdp.command("Runtime.enable")
                base_url = args.base_url.rstrip("/") + "/"
                results: list[dict] = []
                errors: list[str] = []

                for width, height, label in VIEWPORTS:
                    cdp.command("Emulation.setDeviceMetricsOverride", {
                        "width": width,
                        "height": height,
                        "deviceScaleFactor": 1,
                        "mobile": width <= 480,
                    })
                    for path, page_name in PAGES:
                        url = urljoin(base_url, path)
                        cdp.command("Page.navigate", {"url": url})
                        wait_ready(cdp, url)
                        geometry = cdp.evaluate(GEOMETRY_EXPRESSION)
                        record_errors = validate(geometry, page_name)
                        record = {"viewport": label, "page": page_name, **geometry, "errors": record_errors}
                        results.append(record)
                        errors.extend(f"{label}/{page_name}: {message}" for message in record_errors)

                        image = cdp.command("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                        (screenshots / f"{label}-{page_name}.png").write_bytes(base64.b64decode(image["data"]))

                report_path.write_text(json.dumps({"results": results, "errors": errors}, indent=2) + "\n")
                if errors:
                    print("\n".join(f"ERROR: {error}" for error in errors))
                    return 1
                print(f"Privacy and spacing audit passed: {len(results)} page/viewport combinations.")
                return 0
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
