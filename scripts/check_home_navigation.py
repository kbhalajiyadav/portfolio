#!/usr/bin/env python3
"""Verify homepage navigation order, fit, and scroll-state transitions."""
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

EXPECTED_LABELS = [
    "About",
    "Research",
    "Outputs",
    "Trajectory",
    "Experience",
    "Engagement",
    "Contact",
]


def active_state(cdp: CDP) -> dict:
    return cdp.evaluate(
        """
        (() => {
          const links = [...document.querySelectorAll('#site-nav > a')];
          return {
            active: links.filter((link) => link.classList.contains('is-active')).map((link) => link.textContent.trim()),
            currentLocation: links.filter((link) => link.getAttribute('aria-current') === 'location').map((link) => link.textContent.trim())
          };
        })()
        """
    )


def scroll_to(cdp: CDP, expression: str) -> None:
    cdp.evaluate(
        f"""
        new Promise((resolve) => {{
          window.scrollTo({{top: {expression}, behavior: 'auto'}});
          requestAnimationFrame(() => requestAnimationFrame(resolve));
        }})
        """
    )


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
                          const tops = items.map((link) => link.getBoundingClientRect().top);
                          return {
                            labels: items.map((link) => link.textContent.trim()),
                            navRowSpread: tops.length ? Math.max(...tops) - Math.min(...tops) : null,
                            horizontalOverflow: root.scrollWidth > root.clientWidth + 2
                          };
                        })()
                        """
                    )
                    results[f"layout-{width}"] = layout
                    if layout["labels"] != EXPECTED_LABELS:
                        errors.append(f"{width}px navigation labels/order {layout['labels']}, expected {EXPECTED_LABELS}")
                    if layout["navRowSpread"] is None or layout["navRowSpread"] > 3:
                        errors.append(f"{width}px desktop navigation wrapped: row spread={layout['navRowSpread']}")
                    if layout["horizontalOverflow"]:
                        errors.append(f"{width}px homepage has horizontal overflow")

                initial = active_state(cdp)
                results["initialHero"] = initial
                if initial["active"] or initial["currentLocation"]:
                    errors.append(f"hero must not retain a section highlight: {initial}")

                scroll_to(cdp, "document.querySelector('#research').offsetTop")
                research = active_state(cdp)
                results["research"] = research
                if research != {"active": ["Research"], "currentLocation": ["Research"]}:
                    errors.append(f"Research section did not activate Research exactly: {research}")

                scroll_to(cdp, "document.querySelector('#presentations').offsetTop")
                engagement = active_state(cdp)
                results["engagement"] = engagement
                if engagement != {"active": ["Engagement"], "currentLocation": ["Engagement"]}:
                    errors.append(f"presentations section did not activate Engagement exactly: {engagement}")

                scroll_to(cdp, "document.documentElement.scrollHeight")
                contact = active_state(cdp)
                results["contact"] = contact
                if contact != {"active": ["Contact"], "currentLocation": ["Contact"]}:
                    errors.append(f"page end did not activate Contact exactly: {contact}")

                scroll_to(cdp, "0")
                returned = active_state(cdp)
                results["returnedHero"] = returned
                if returned["active"] or returned["currentLocation"]:
                    errors.append(f"returning to the hero left a stale section highlight: {returned}")
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
    print("Homepage navigation audit passed: order, desktop fit, Research, Engagement, Contact, and hero reset verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
