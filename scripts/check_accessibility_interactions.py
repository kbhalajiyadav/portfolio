#!/usr/bin/env python3
"""Browser checks for WCAG reflow, typography, target size, focus, and stateful UI regressions."""
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

TYPOGRAPHY_PAGES = [
    ("", "home"),
    ("outputs/", "outputs"),
    ("publication/adhesives-wearable/", "publication"),
    ("project/quantitative-thermal-imaging/", "intellectual-property"),
]

RELATED_PAGES = [
    "publication/adhesives-wearable/",
    "publication/masters-thesis/",
    "project/peel-trace-evaluation/",
    "project/quantitative-thermal-imaging/",
]

TYPOGRAPHY_VIEWPORTS = [
    (390, 844, "mobile"),
    (1366, 768, "laptop"),
    (1920, 1080, "desktop"),
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

ACTIVE_FOCUS_EXPRESSION = r"""
(() => {
  const target = document.activeElement;
  if (!target || target === document.body || target === document.documentElement) {
    return {found:false, inMain:false};
  }
  const rect = target.getBoundingClientRect();
  const header = document.querySelector('.site-head')?.getBoundingClientRect();
  const style = getComputedStyle(target);
  return {
    found:true,
    inMain:Boolean(target.closest('main')),
    tag:target.tagName.toLowerCase(),
    text:(target.textContent || target.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0,80),
    top:rect.top,
    bottom:rect.bottom,
    left:rect.left,
    right:rect.right,
    viewportWidth:innerWidth,
    viewportHeight:innerHeight,
    headerBottom:header ? header.bottom : 0,
    outlineStyle:style.outlineStyle,
    outlineWidth:parseFloat(style.outlineWidth) || 0,
    outlineOffset:parseFloat(style.outlineOffset) || 0,
  };
})()
"""

TYPOGRAPHY_EXPRESSION = r"""
(() => {
  const visible = (element) => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const unique = (items) => [...new Set(items)];
  const runningSelectors = ['.lede', '.page-lede', '.article-content p', '.article-content li', '.output-row__summary'];
  const running = unique(runningSelectors.flatMap((selector) => [...document.querySelectorAll(selector)]))
    .filter(visible)
    .map((element) => {
      const style = getComputedStyle(element);
      const fontSize = parseFloat(style.fontSize) || 0;
      const lineHeight = parseFloat(style.lineHeight) || 0;
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      if (context) context.font = style.font;
      const ch = context ? Math.max(context.measureText('0').width, 1) : Math.max(fontSize * .5, 1);
      const rect = element.getBoundingClientRect();
      return {
        selector: element.className || element.tagName.toLowerCase(),
        text: (element.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
        textLength: (element.textContent || '').trim().length,
        fontSize,
        lineHeight,
        lineHeightRatio: fontSize ? lineHeight / fontSize : 0,
        measureCh: rect.width / ch,
      };
    });
  const metadata = unique([
    ...document.querySelectorAll('.kicker, .eyebrow, .overline, .output-row__meta time, .output-row__meta span, .status-line, .site-footer a, .site-footer button')
  ]).filter(visible).map((element) => ({
    text: (element.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80),
    fontSize: parseFloat(getComputedStyle(element).fontSize) || 0,
  }));
  const nav = document.querySelector('#site-nav');
  const navStyle = nav ? getComputedStyle(nav) : null;
  return {
    bodyFontSize: parseFloat(getComputedStyle(document.body).fontSize) || 0,
    navVisible: Boolean(nav && visible(nav)),
    navFontSize: navStyle ? parseFloat(navStyle.fontSize) || 0 : 0,
    running,
    runningSizeIssues: running.filter((item) => item.fontSize < 16),
    lineHeightIssues: running.filter((item) => item.lineHeightRatio < 1.45),
    measureIssues: running.filter((item) => item.textLength >= 120 && item.measureCh > 90),
    tinyMetadataIssues: metadata.filter((item) => item.fontSize < 11),
  };
})()
"""

TEXT_SPACING_EXPRESSION = r"""
new Promise((resolve) => {
  const style = document.createElement('style');
  style.id = 'wcag-text-spacing-audit';
  style.textContent = `
    main p, main li, main a, main button, main summary, main small, main strong, main span {
      line-height: 1.5 !important;
      letter-spacing: .12em !important;
      word-spacing: .16em !important;
    }
    main p { margin-bottom: 2em !important; }
  `;
  document.head.appendChild(style);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const root = document.documentElement;
    const body = document.body;
    const visible = (element) => {
      const computed = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return computed.display !== 'none' && computed.visibility !== 'hidden' && rect.width > 0 && rect.height > 0 && !element.closest('.visually-hidden');
    };
    const clipped = [...document.querySelectorAll('main p, main li, main a, main button, main summary, main small, main strong, main span')]
      .filter(visible)
      .filter((element) => {
        const computed = getComputedStyle(element);
        const clipsX = computed.overflowX === 'hidden' || computed.overflowX === 'clip';
        const clipsY = computed.overflowY === 'hidden' || computed.overflowY === 'clip';
        return (clipsX && element.scrollWidth > element.clientWidth + 2) || (clipsY && element.scrollHeight > element.clientHeight + 2);
      })
      .slice(0, 12)
      .map((element) => ({
        tag: element.tagName.toLowerCase(),
        text: (element.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
        clientWidth: element.clientWidth,
        scrollWidth: element.scrollWidth,
        clientHeight: element.clientHeight,
        scrollHeight: element.scrollHeight,
      }));
    resolve({
      viewportWidth: root.clientWidth,
      scrollWidth: Math.max(root.scrollWidth, body.scrollWidth),
      horizontalOverflow: Math.max(root.scrollWidth, body.scrollWidth) > root.clientWidth + 2,
      clipped,
    });
  }));
})
"""


def press_tab(cdp: CDP) -> None:
    cdp.command(
        "Input.dispatchKeyEvent",
        {"type": "keyDown", "key": "Tab", "code": "Tab", "windowsVirtualKeyCode": 9},
    )
    cdp.command(
        "Input.dispatchKeyEvent",
        {"type": "keyUp", "key": "Tab", "code": "Tab", "windowsVirtualKeyCode": 9},
    )
    cdp.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")


def keyboard_focus_check(cdp: CDP) -> dict:
    cdp.evaluate(
        "document.documentElement.style.scrollBehavior='auto';"
        "document.body.style.scrollBehavior='auto';"
        "window.scrollTo(0,0);"
        "if(document.activeElement && document.activeElement.blur) document.activeElement.blur();"
    )
    visited: list[dict] = []
    for _ in range(30):
        press_tab(cdp)
        state = cdp.evaluate(ACTIVE_FOCUS_EXPRESSION)
        if state.get("found"):
            visited.append({"tag": state.get("tag"), "text": state.get("text"), "inMain": state.get("inMain")})
        if state.get("inMain"):
            state["visited"] = visited
            return state
    return {"missing": True, "visited": visited}


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


def output_filter_check(cdp: CDP) -> dict:
    return cdp.evaluate(
        r"""
        new Promise((resolve) => {
          const buttons = [...document.querySelectorAll('[data-output-filter]')];
          const records = [...document.querySelectorAll('[data-output-type][data-output-date]')];
          const status = document.querySelector('[data-output-filter-status]');
          if (buttons.length !== 5 || records.length !== 5) {
            return resolve({missing:true, buttonCount:buttons.length, recordCount:records.length});
          }
          const dates = records.map((record) => record.dataset.outputDate || '');
          const sorted = [...dates].sort().reverse();
          const initialPressed = buttons.find((button) => button.getAttribute('aria-pressed') === 'true')?.dataset.outputFilter || null;
          const publication = buttons.find((button) => button.dataset.outputFilter === 'publication');
          publication.click();
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const visible = records.filter((record) => !record.hidden);
            const pressed = buttons.find((button) => button.getAttribute('aria-pressed') === 'true')?.dataset.outputFilter || null;
            const publicationState = {
              visibleCount:visible.length,
              visibleTypes:[...new Set(visible.map((record) => record.dataset.outputType))],
              pressed,
              status:(status?.textContent || '').trim(),
            };
            buttons.find((button) => button.dataset.outputFilter === 'all').click();
            requestAnimationFrame(() => requestAnimationFrame(() => {
              resolve({
                missing:false,
                dates,
                chronological:JSON.stringify(dates) === JSON.stringify(sorted),
                initialPressed,
                publicationState,
                allVisibleCount:records.filter((record) => !record.hidden).length,
              });
            }));
          }));
        })
        """
    )


def related_links_check(cdp: CDP) -> dict:
    return cdp.evaluate(
        r"""
        (() => {
          const packageElement = document.querySelector('.related-package');
          if (!packageElement) return {missing:true};
          const links = [...packageElement.querySelectorAll('a[href]')];
          return {
            missing:false,
            count:links.length,
            labels:links.map((link) => (link.textContent || '').trim().replace(/\s+/g, ' ')),
          };
        })()
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
    results: dict = {
        "reflow": [],
        "typography": [],
        "textSpacing": [],
        "series": None,
        "copyStatus": None,
        "outputFilter": None,
        "relatedLinks": [],
    }
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
                cdp.command("Input.setIgnoreInputEvents", {"ignore": False})
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
                    focus = keyboard_focus_check(cdp)
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
                        errors.append(f"320px/{name}: keyboard traversal did not reach a main-content control: {focus.get('visited')}")
                    else:
                        if focus["top"] < focus["headerBottom"] - 2 or focus["bottom"] > focus["viewportHeight"] + 2:
                            errors.append(f"320px/{name}: keyboard-focused control is obscured or outside viewport: {focus}")
                        if focus["left"] < -2 or focus["right"] > focus["viewportWidth"] + 2:
                            errors.append(f"320px/{name}: keyboard-focused control overflows horizontally: {focus}")
                        if focus["outlineStyle"] == "none" or focus["outlineWidth"] < 2:
                            errors.append(f"320px/{name}: keyboard-focused control lacks a visible >=2px focus indicator: {focus}")

                # Check typography at representative device contexts.
                for width, height, viewport_name in TYPOGRAPHY_VIEWPORTS:
                    cdp.command("Emulation.setDeviceMetricsOverride", {
                        "width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 700,
                    })
                    for path, name in TYPOGRAPHY_PAGES:
                        url = urljoin(base_url, path)
                        cdp.command("Page.navigate", {"url": url})
                        wait_ready(cdp, url)
                        typography = cdp.evaluate(TYPOGRAPHY_EXPRESSION)
                        results["typography"].append({"viewport": viewport_name, "page": name, **typography})
                        if typography["bodyFontSize"] < 16:
                            errors.append(f"{viewport_name}/{name}: body text is below 16px: {typography['bodyFontSize']}")
                        if typography["navVisible"] and typography["navFontSize"] < 13:
                            errors.append(f"{viewport_name}/{name}: visible primary navigation is below 13px: {typography['navFontSize']}")
                        if typography["runningSizeIssues"]:
                            errors.append(f"{viewport_name}/{name}: running text below 16px: {typography['runningSizeIssues']}")
                        if typography["lineHeightIssues"]:
                            errors.append(f"{viewport_name}/{name}: running-text line height below 1.45: {typography['lineHeightIssues']}")
                        if typography["measureIssues"]:
                            errors.append(f"{viewport_name}/{name}: long-form text exceeds 90ch: {typography['measureIssues']}")
                        if typography["tinyMetadataIssues"]:
                            errors.append(f"{viewport_name}/{name}: visible metadata below 11px: {typography['tinyMetadataIssues']}")

                # WCAG 1.4.12 user text-spacing override must not cause loss or horizontal overflow.
                cdp.command("Emulation.setDeviceMetricsOverride", {
                    "width": 1280, "height": 900, "deviceScaleFactor": 1, "mobile": False,
                })
                for path, name in TYPOGRAPHY_PAGES:
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    spacing = cdp.evaluate(TEXT_SPACING_EXPRESSION)
                    results["textSpacing"].append({"page": name, **spacing})
                    if spacing["horizontalOverflow"]:
                        errors.append(f"text-spacing/{name}: horizontal overflow after WCAG text-spacing override: {spacing}")
                    if spacing["clipped"]:
                        errors.append(f"text-spacing/{name}: text clipped after WCAG text-spacing override: {spacing['clipped']}")

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

                outputs = urljoin(base_url, "outputs/")
                cdp.command("Page.navigate", {"url": outputs})
                wait_ready(cdp, outputs)
                output_filter = output_filter_check(cdp)
                results["outputFilter"] = output_filter
                if output_filter.get("missing"):
                    errors.append(f"research-output filter is incomplete: {output_filter}")
                else:
                    if not output_filter.get("chronological"):
                        errors.append(f"research outputs are not newest-first: {output_filter.get('dates')}")
                    if output_filter.get("initialPressed") != "all":
                        errors.append(f"research-output filter must default to All: {output_filter}")
                    publication_state = output_filter.get("publicationState", {})
                    if publication_state.get("visibleCount") != 2 or publication_state.get("visibleTypes") != ["publication"]:
                        errors.append(f"publication filter exposed incorrect records: {publication_state}")
                    if publication_state.get("pressed") != "publication" or not publication_state.get("status"):
                        errors.append(f"publication filter lacks state/status feedback: {publication_state}")
                    if output_filter.get("allVisibleCount") != 5:
                        errors.append(f"All filter did not restore every output: {output_filter}")

                for path in RELATED_PAGES:
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    related = related_links_check(cdp)
                    results["relatedLinks"].append({"page": path, **related})
                    if related.get("missing"):
                        errors.append(f"{path}: expected a concise related-output/research block")
                    elif related.get("count", 0) > 2:
                        errors.append(f"{path}: related block has excessive links: {related}")

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
        "Accessibility interaction audit passed: 320px reflow, 24px targets, keyboard focus, "
        "responsive typography, WCAG text spacing, chronological output filtering, concise related links, "
        "independent presentation details, and live copy feedback verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())