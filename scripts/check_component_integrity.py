#!/usr/bin/env python3
"""Detect rendered content collisions, overflow, and avoidable editorial slack.

The audit intentionally checks semantic component families rather than screenshot-perfect
pixel positions. It protects cards, record rows, timelines, profile facts, citation boxes,
and editorial panels against content overlap, horizontal escape, or large empty tails as
copy changes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from urllib.parse import quote

from check_responsive import CDP, free_port, read_json, wait_ready

VIEWPORTS = [
    (1440, 900, "desktop"),
    (1024, 768, "compact-desktop"),
    (680, 900, "tablet"),
    (390, 844, "mobile"),
]

PAGES = [
    ("/", "home"),
    ("/about/", "about"),
    ("/outputs/", "outputs"),
    ("/research/", "research"),
    ("/publication/", "publication-index"),
    ("/publication/adhesives-wearable/", "article"),
    ("/publication/masters-thesis/", "thesis"),
    ("/project/", "project-index"),
    ("/project/peel-trace-evaluation/", "software"),
    ("/project/optical-metrology/", "optical-metrology"),
    ("/project/quantitative-thermal-imaging/", "intellectual-property"),
    ("/project/fda-project/", "industry-quality"),
    ("/project/supply-chain-automation/", "industry-data"),
    ("/tags/", "topic-index"),
]

SELECTORS = [
    ".metrics div",
    ".pillar",
    ".questions article",
    ".trajectory-grid article",
    ".series",
    ".series summary",
    ".compact-record",
    ".secondary-output",
    ".research-package",
    ".package-artifacts article",
    ".output-row",
    ".education-panel",
    ".education-panel article",
    ".about-fact-strip div",
    ".about-program-grid article",
    ".about-method-grid article",
    ".about-profile-links a",
    ".about-path article",
    ".listing-grid article",
    ".abstract-block",
    ".citation-box",
    ".related-package",
]

# These are explanatory/editorial components, not promotional tiles. Large
# unused tails usually indicate row stretching or a fixed/minimum height that
# no longer reflects the content. Limits are deliberately generous so the
# audit catches discontinuities rather than normal padding.
EDITORIAL_SLACK_LIMITS = {
    ".trajectory-grid article": 56.0,
    ".series summary": 56.0,
    ".education-panel": 72.0,
    ".about-method-grid article": 56.0,
}

DECLINE_PRIVACY = r"""
(async () => {
  const decline = document.querySelector('[data-consent-decline]');
  if (decline && !document.querySelector('[data-privacy-banner]')?.hidden) {
    decline.click();
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  }
  return true;
})()
"""

MEASURE = r"""
(selectors => {
  const visible = element => {
    const closedDetails = element.closest('details:not([open])');
    if (closedDetails && !element.closest('summary')) return false;
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const rect = element => {
    const box = element.getBoundingClientRect();
    return {top:box.top,right:box.right,bottom:box.bottom,left:box.left,width:box.width,height:box.height};
  };
  const number = value => Number.parseFloat(value) || 0;
  const overlaps = (a, b) => !(
    a.right <= b.left + 1 || b.right <= a.left + 1 ||
    a.bottom <= b.top + 1 || b.bottom <= a.top + 1
  );
  const results = [];
  selectors.forEach(selector => {
    [...document.querySelectorAll(selector)].forEach((component, index) => {
      if (!visible(component)) return;
      const componentRect = rect(component);
      const componentStyle = getComputedStyle(component);
      const children = [...component.children]
        .filter(visible)
        .filter(child => {
          const style = getComputedStyle(child);
          return style.position !== 'absolute' && style.position !== 'fixed';
        })
        .map((child, childIndex) => ({
          index: childIndex,
          tag: child.tagName.toLowerCase(),
          className: child.className || '',
          box: rect(child),
        }));
      const collisions = [];
      for (let i = 0; i < children.length; i += 1) {
        for (let j = i + 1; j < children.length; j += 1) {
          if (overlaps(children[i].box, children[j].box)) {
            collisions.push([children[i], children[j]]);
          }
        }
      }
      const escaped = children.filter(child => (
        child.box.left < componentRect.left - 2 ||
        child.box.right > componentRect.right + 2 ||
        child.box.top < componentRect.top - 2 ||
        child.box.bottom > componentRect.bottom + 2
      ));
      const contentBottom = children.length ? Math.max(...children.map(child => child.box.bottom)) : componentRect.top;
      const trailingSlack = Math.max(0, componentRect.bottom - contentBottom - number(componentStyle.paddingBottom));
      results.push({
        selector,
        index,
        component: componentRect,
        scrollHeight: component.scrollHeight,
        clientHeight: component.clientHeight,
        scrollWidth: component.scrollWidth,
        clientWidth: component.clientWidth,
        trailingSlack,
        collisions,
        escaped,
      });
    });
  });
  return results;
})(__SELECTORS__)
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/component-integrity.json")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    errors: list[str] = []
    port = free_port()

    with tempfile.TemporaryDirectory(prefix="portfolio-components-chrome-", ignore_cleanup_errors=True) as profile:
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
                expression = MEASURE.replace("__SELECTORS__", json.dumps(SELECTORS))
                for path, page_name in PAGES:
                    url = args.base_url.rstrip("/") + path
                    for width, height, viewport_name in VIEWPORTS:
                        cdp.command("Emulation.setDeviceMetricsOverride", {
                            "width": width,
                            "height": height,
                            "deviceScaleFactor": 1,
                            "mobile": width <= 680,
                        })
                        cdp.command("Page.navigate", {"url": url})
                        wait_ready(cdp, url)
                        cdp.evaluate(DECLINE_PRIVACY)
                        measured = cdp.evaluate(expression)
                        case = {
                            "page": page_name,
                            "path": path,
                            "viewport": {"width": width, "height": height, "name": viewport_name},
                            "components": measured,
                        }
                        results.append(case)
                        prefix = f"{page_name}/{width}x{height}"
                        for component in measured:
                            label = f"{component['selector']}[{component['index']}]"
                            for collision in component.get("collisions", []):
                                first, second = collision
                                errors.append(
                                    f"{prefix}: {label} has overlapping direct content blocks "
                                    f"({first['tag']}.{first['className']} and {second['tag']}.{second['className']})"
                                )
                            if component.get("escaped"):
                                errors.append(f"{prefix}: {label} has content outside its component bounds")
                            if component.get("scrollWidth", 0) > component.get("clientWidth", 0) + 2:
                                errors.append(f"{prefix}: {label} has horizontal component overflow")
                            slack_limit = EDITORIAL_SLACK_LIMITS.get(component["selector"])
                            if slack_limit is not None and component.get("trailingSlack", 0) > slack_limit:
                                errors.append(
                                    f"{prefix}: {label} leaves {component['trailingSlack']:.1f}px of avoidable trailing whitespace "
                                    f"(limit {slack_limit:.0f}px)"
                                )
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    report_path.write_text(json.dumps({"cases": results, "errors": errors}, indent=2) + "\n")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "Component integrity passed: major cards, editorial records, timelines, profile facts, citation boxes, "
        "and related panels contain rendered content without collisions, horizontal overflow, or excessive editorial slack "
        f"across {len(PAGES) * len(VIEWPORTS)} page/viewport combinations."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
