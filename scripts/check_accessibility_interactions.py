#!/usr/bin/env python3
"""Browser checks for WCAG reflow, target size, focus visibility, and stateful UI regressions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from urllib.parse import quote, urljoin

from check_responsive import CDP, free_port, read_json, wait_ready

PAGES = [
    ("", "home"),
    ("about/", "about"),
    ("outputs/", "outputs"),
    ("research/", "research"),
    ("publication/adhesives-wearable/", "publication"),
    ("project/quantitative-thermal-imaging/", "intellectual-property"),
    ("project/fda-project/", "industry"),
    ("privacy/", "privacy"),
]

REFLOW_EXPRESSION = r"""
(() => {
  const root = document.documentElement;
  const body = document.body;
  const width = root.clientWidth;
  const interactive = [...document.querySelectorAll('button, summary, a.button')]
    .filter((element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    })
    .map((element) => {
      const rect = element.getBoundingClientRect();
      return {
        tag: element.tagName.toLowerCase(),
        text: (element.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80),
        width: rect.width,
        height: rect.height,
      };
    });
  return {
    viewportWidth: width,
    scrollWidth: Math.max(root.scrollWidth, body.scrollWidth),
    horizontalOverflow: Math.max(root.scrollWidth, body.scrollWidth) > width + 2,
    targetIssues: interactive.filter((item) => item.width < 24 || item.height < 24),
    h1Count: document.querySelectorAll('h1').length,
    mainCount: document.querySelectorAll('main').length,
  };
})()
"""


def focus_check(cdp: CDP) -> dict:
    return cdp.evaluate(
        r"""
        new Promise((resolve) => {
          const target = [...document.querySelectorAll('main a[href], main button, main summary')]
            .find((element) => {
              const style = getComputedStyle(element);
              const rect = element.getBoundingClientRect();
              return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
            });
          if (!target) return resolve({missing:true});
          target.focus({preventScroll:true});
          target.scrollIntoView({block:'center', inline:'nearest'});
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const rect = target.getBoundingClientRect();
            const header = document.querySelector('.site-head')?.getBoundingClientRect();
            const style = getComputedStyle(target);
            resolve({
              missing:false,
              text:(target.textContent || '').trim().replace(/\s+/g, ' ').slice(0,80),
              top:rect.top,
              bottom:rect.bottom,
              left:rect.left,
              right:rect.right,
              viewportWidth:innerWidth,
              viewportHeight:innerHeight,
              headerBottom:header ? header.bottom : 0,
              outlineStyle:style.outlineStyle,
              outlineWidth:parseFloat(style.outlineWidth) || 0,
            });
          }));
        })
        """
    )


def series_check(cdp: CDP) -> dict:
    return cdp.evaluate(
        r"""
        new Promise((resolve) => {
          const cards = [...document.querySelectorAll('.series-grid .series')];
          if (cards.length < 2) return resolve({missing:true, count:cards.length});
          cards.forEach((card) => { card.open = false; });
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const firstBefore = cards[0].getBoundingClientRect().height;
            const secondBefore = cards[1].getBoundingClientRect().height;
            cards[0].open = true;
            requestAnimationFrame(() => requestAnimationFrame(() => {
              resolve({
                missing:false,
                firstBefore,
                secondBefore,
                firstAfter:cards[0].getBoundingClientRect().height,
                secondAfter:cards[1].getBoundingClientRect().height,
                firstOpen:cards[0].open,
                secondOpen:cards[1].open,
                gridAlignItems:getComputedStyle(cards[0].parentElement).alignItems,
                secondAlignSelf:getComputedStyle(cards[1]).alignSelf,
              });
            }));
          }));
        })
        """
    )


def copy_status_check(cdp: CDP) -> dict:
    return cdp.evaluate(
        r"""
        new Promise((resolve) => {
          const button = document.querySelector('.js-copy');
          const status = document.querySelector('[data-copy-status]');
          if (!button || !status) return resolve({missing:true});
          const semantics = {
            role:status.getAttribute('role'),
            live:status.getAttribute('aria-live'),
          };
          button.click();
          setTimeout(() => resolve({
            missing:false,
            ...semantics,
            message:(status.textContent || '').trim(),
            buttonText:(button.textContent || '').trim(),
          }), 80);
        })
        """
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/accessibility-interactions.json")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    results: dict = {"reflow": [], "series": None, "copyStatus": None}
    port = free_port()

    with tempfile.TemporaryDirectory(prefix="portfolio-a11y-chrome-", ignore_cleanup_errors=True) as profile:
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

                # 320 CSS px is the WCAG 2.2 AA reflow reference width.
                cdp.command("Emulation.setDeviceMetricsOverride", {
                    "width": 320, "height": 800, "deviceScaleFactor": 1, "mobile": True,
                })
                for path, name in PAGES:
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    reflow = cdp.evaluate(REFLOW_EXPRESSION)
                    focus = focus_check(cdp)
                    record = {"page": name, **reflow, "focus": focus}
                    results["reflow"].append(record)

                    if reflow["horizontalOverflow"]:
                        errors.append(f"320px/{name}: horizontal overflow ({reflow['scrollWidth']}px > {reflow['viewportWidth']}px)")
                    if reflow["targetIssues"]:
                        errors.append(f"320px/{name}: non-inline target below 24x24 CSS px: {reflow['targetIssues']}")
                    if reflow["h1Count"] != 1:
                        errors.append(f"320px/{name}: expected exactly one h1, found {reflow['h1Count']}")
                    if reflow["mainCount"] != 1:
                        errors.append(f"320px/{name}: expected exactly one main landmark, found {reflow['mainCount']}")
                    if focus.get("missing"):
                        errors.append(f"320px/{name}: no focusable main-content control found")
                    else:
                        if focus["top"] < focus["headerBottom"] - 2 or focus["bottom"] > focus["viewportHeight"] + 2:
                            errors.append(f"320px/{name}: focused control is obscured or outside viewport: {focus}")
                        if focus["left"] < -2 or focus["right"] > focus["viewportWidth"] + 2:
                            errors.append(f"320px/{name}: focused control overflows horizontally: {focus}")
                        if focus["outlineStyle"] == "none" or focus["outlineWidth"] < 2:
                            errors.append(f"320px/{name}: focused control lacks a visible >=2px outline: {focus}")

                # Reproduce the presentation-card bug at the desktop layout where
                # sibling grid items previously stretched when one details opened.
                cdp.command("Emulation.setDeviceMetricsOverride", {
                    "width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False,
                })
                home = base_url
                cdp.command("Page.navigate", {"url": home})
                wait_ready(cdp, home)
                series = series_check(cdp)
                results["series"] = series
                if series.get("missing"):
                    errors.append(f"presentation-series audit could not find two cards: {series}")
                else:
                    if not series["firstOpen"] or series["secondOpen"]:
                        errors.append(f"opening one presentation card changed the wrong details state: {series}")
                    if series["firstAfter"] <= series["firstBefore"] + 8:
                        errors.append(f"presentation card did not visibly expand: {series}")
                    if abs(series["secondAfter"] - series["secondBefore"]) > 2:
                        errors.append(f"closed sibling stretched when another presentation card opened: {series}")
                    if series["gridAlignItems"] != "start":
                        errors.append(f"presentation grid must top-align independent details cards: {series}")

                publication = urljoin(base_url, "publication/adhesives-wearable/")
                cdp.command("Page.navigate", {"url": publication})
                wait_ready(cdp, publication)
                copy_status = copy_status_check(cdp)
                results["copyStatus"] = copy_status
                if copy_status.get("missing"):
                    errors.append("publication copy control is missing its live status region")
                else:
                    if copy_status.get("role") != "status" or copy_status.get("live") != "polite":
                        errors.append(f"copy status semantics are incomplete: {copy_status}")
                    if not copy_status.get("message"):
                        errors.append(f"copy action produced no assistive-technology status message: {copy_status}")
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    report_path.write_text(json.dumps({"results": results, "errors": errors}, indent=2) + "\n")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "Accessibility interaction audit passed: 320px reflow, 24px non-inline targets, "
        "unobscured focus, independent presentation details, and live copy feedback verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
