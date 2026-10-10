#!/usr/bin/env python3
"""Verify stable primary navigation and short-height About layout."""
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

EXPECTED_LINKS = {
    "About": "/about/",
    "Research": "/research/",
    "Outputs": "/outputs/",
    "Experience": "/experience/",
    "Engagement": "/engagement/",
    "Contact": "/contact/",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/home-navigation.json")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    port = free_port()
    errors: list[str] = []
    results: dict = {}

    with tempfile.TemporaryDirectory(prefix="portfolio-navigation-chrome-", ignore_cleanup_errors=True) as profile:
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
                base_url = args.base_url.rstrip("/") + "/"
                cdp.command("Page.enable")
                cdp.command("Runtime.enable")
                cdp.command("DOM.enable")
                cdp.command("CSS.enable")

                for width in (1180, 1440):
                    cdp.command(
                        "Emulation.setDeviceMetricsOverride",
                        {"width": width, "height": 1000, "deviceScaleFactor": 1, "mobile": False},
                    )
                    cdp.command("Page.navigate", {"url": base_url})
                    wait_ready(cdp, base_url)
                    layout = cdp.evaluate(
                        """
                        (() => {
                          const root = document.documentElement;
                          const items = [...document.querySelectorAll('#site-nav > a')]
                            .filter((link) => getComputedStyle(link).display !== 'none');
                          const centers = items.map((link) => {
                            const rect = link.getBoundingClientRect();
                            return rect.top + rect.height / 2;
                          });
                          return {
                            labels: items.map((link) => link.textContent.trim()),
                            hrefs: Object.fromEntries(items.map((link) => [link.textContent.trim(), link.getAttribute('href')])),
                            current: items.filter(link => link.getAttribute('aria-current') === 'page').map(link => link.textContent.trim()),
                            locationCurrent: items.filter(link => link.getAttribute('aria-current') === 'location').map(link => link.textContent.trim()),
                            navCenterSpread: centers.length ? Math.max(...centers) - Math.min(...centers) : null,
                            horizontalOverflow: root.scrollWidth > root.clientWidth + 2
                          };
                        })()
                        """
                    )
                    results[f"home-{width}"] = layout
                    if layout["labels"] != list(EXPECTED_LINKS):
                        errors.append(f"{width}px navigation labels/order {layout['labels']}, expected {list(EXPECTED_LINKS)}")
                    if layout["hrefs"] != EXPECTED_LINKS:
                        errors.append(f"{width}px primary navigation must use stable canonical destinations: {layout['hrefs']}")
                    if layout["current"] or layout["locationCurrent"]:
                        errors.append(f"{width}px homepage must not pretend a child destination is current: {layout}")
                    if layout["navCenterSpread"] is None or layout["navCenterSpread"] > 3:
                        errors.append(f"{width}px desktop navigation lost one-row center alignment: spread={layout['navCenterSpread']}")
                    if layout["horizontalOverflow"]:
                        errors.append(f"{width}px homepage has horizontal overflow")

                # About hover geometry remains a useful desktop-divider regression check.
                document_node = cdp.command("DOM.getDocument", {"depth": 1})["root"]["nodeId"]
                about_node = cdp.command("DOM.querySelector", {"nodeId": document_node, "selector": ".nav-about"})["nodeId"]
                cdp.command("CSS.forcePseudoState", {"nodeId": about_node, "forcedPseudoClasses": ["hover"]})
                cdp.evaluate("new Promise(resolve => setTimeout(resolve, 240))")
                hover_geometry = cdp.evaluate(
                    """
                    (() => {
                      const link = document.querySelector('.nav-about');
                      return {
                        pseudoRight: parseFloat(getComputedStyle(link, '::after').right),
                        paddingRight: parseFloat(getComputedStyle(link).paddingRight)
                      };
                    })()
                    """
                )
                cdp.command("CSS.forcePseudoState", {"nodeId": about_node, "forcedPseudoClasses": []})
                results["aboutHover"] = hover_geometry
                if abs(hover_geometry["pseudoRight"] - hover_geometry["paddingRight"]) > 1:
                    errors.append(f"About hover underline extends into divider spacing: {hover_geometry}")

                # Every primary page must keep the same destinations and mark exactly itself current.
                for label, path in EXPECTED_LINKS.items():
                    url = urljoin(base_url, path.lstrip("/"))
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    state = cdp.evaluate(
                        """
                        (() => {
                          const links = [...document.querySelectorAll('#site-nav > a')];
                          return {
                            hrefs:Object.fromEntries(links.map(link => [link.textContent.trim(), link.getAttribute('href')])),
                            current:links.filter(link => link.getAttribute('aria-current') === 'page').map(link => link.textContent.trim()),
                            active:links.filter(link => link.classList.contains('is-active') || link.classList.contains('is-current-page')).map(link => link.textContent.trim())
                          };
                        })()
                        """
                    )
                    results[f"destination-{label}"] = state
                    if state["hrefs"] != EXPECTED_LINKS:
                        errors.append(f"{label} page changed primary destinations: {state['hrefs']}")
                    if state["current"] != [label]:
                        errors.append(f"{label} page must expose exactly aria-current=page on itself: {state}")
                    if label not in state["active"]:
                        errors.append(f"{label} page does not visually identify the current destination: {state}")

                # Short laptop frame: About must remain balanced and keep profile facts in the first viewport.
                cdp.evaluate("document.querySelector('[data-consent-decline]')?.click()")
                cdp.command(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 1366, "height": 768, "deviceScaleFactor": 1, "mobile": False},
                )
                about_url = urljoin(base_url, "about/")
                cdp.command("Page.navigate", {"url": about_url})
                wait_ready(cdp, about_url)
                about_layout = cdp.evaluate(
                    """
                    (() => {
                      const root = document.documentElement;
                      const hero = document.querySelector('.about-hero');
                      const copy = document.querySelector('.about-hero__copy');
                      const portrait = document.querySelector('.about-portrait');
                      const heading = document.querySelector('.about-hero h1');
                      const facts = document.querySelector('.about-fact-strip');
                      const copyRect = copy.getBoundingClientRect();
                      const portraitRect = portrait.getBoundingClientRect();
                      return {
                        horizontalOverflow: root.scrollWidth > root.clientWidth + 2,
                        gridColumns: getComputedStyle(hero).gridTemplateColumns,
                        portraitWidth: portraitRect.width,
                        portraitRightOfCopy: portraitRect.left > copyRect.right,
                        headingSize: parseFloat(getComputedStyle(heading).fontSize),
                        pageTopPadding: parseFloat(getComputedStyle(document.querySelector('.about-page .page-shell')).paddingTop),
                        factStripTop: facts.getBoundingClientRect().top,
                        viewportHeight: window.innerHeight
                      };
                    })()
                    """
                )
                results["about-1366x768"] = about_layout
                if about_layout["horizontalOverflow"]:
                    errors.append("1366x768 About page has horizontal overflow")
                if not about_layout["portraitRightOfCopy"] or about_layout["gridColumns"] == "none":
                    errors.append(f"1366x768 About hero did not retain a balanced two-column layout: {about_layout}")
                if about_layout["portraitWidth"] > 305:
                    errors.append(f"1366x768 About portrait did not compact for short height: {about_layout['portraitWidth']}px")
                if about_layout["headingSize"] > 70:
                    errors.append(f"1366x768 About heading remained oversized: {about_layout['headingSize']}px")
                if about_layout["pageTopPadding"] > 41:
                    errors.append(f"1366x768 About top spacing did not compact: {about_layout['pageTopPadding']}px")
                if about_layout["factStripTop"] > about_layout["viewportHeight"] + 4:
                    errors.append(f"1366x768 About profile facts begin below the first viewport: {about_layout}")
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
    print("Primary navigation passed: all six destinations remain canonical and stable across pages; current-page state, desktop alignment, hover geometry, and short-height About adaptation are verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
