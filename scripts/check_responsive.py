#!/usr/bin/env python3
"""Browser-level responsive, zoom-equivalent, reduced-motion, menu, and TOC audit."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
from typing import Any
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

import websocket

VIEWPORTS = [
    (390, 844, "390-mobile"),
    (680, 900, "680-small"),
    (768, 900, "768-tablet"),
    (980, 900, "980-laptop-boundary"),
    (1180, 900, "1180-desktop-boundary"),
    (1440, 1000, "1440-desktop"),
    (1920, 1080, "1920-wide"),
    (720, 500, "200-percent-zoom-equivalent"),
]
PAGES = [
    ("", "home"),
    ("research/", "research"),
    ("publication/adhesives-wearable/", "publication"),
    ("project/peel-trace-evaluation/", "project"),
]


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def read_json(url: str, method: str = "GET", timeout: float = 10.0) -> dict[str, Any]:
    request = Request(url, method=method)
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class CDP:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(
            websocket_url,
            timeout=25,
            origin="http://127.0.0.1",
            suppress_origin=True,
        )
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def command(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        command_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": command_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") != command_id:
                continue
            if "error" in message:
                raise RuntimeError(f"CDP {method} failed: {message['error']}")
            return message.get("result", {})

    def evaluate(self, expression: str) -> Any:
        result = self.command(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
        )
        remote = result.get("result", {})
        if remote.get("subtype") == "error":
            raise RuntimeError(remote.get("description", "JavaScript evaluation failed"))
        return remote.get("value")


def wait_ready(cdp: CDP, expected_url: str, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    expected_path = expected_url.rstrip("/")
    state = {}
    while time.time() < deadline:
        state = cdp.evaluate("({ready:document.readyState,url:location.href})")
        current = str(state.get("url", "")).rstrip("/")
        if state.get("ready") == "complete" and current == expected_path:
            cdp.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
            return
        time.sleep(0.1)
    raise TimeoutError(f"page did not finish navigating to {expected_url}; last state={state}")


LAYOUT_EXPRESSION = r"""
(() => {
  const root = document.documentElement;
  const body = document.body;
  const width = root.clientWidth;
  const overflowNodes = [...body.querySelectorAll('*')]
    .filter((element) => {
      const style = getComputedStyle(element);
      if (style.display === 'none' || style.visibility === 'hidden') return false;
      const rect = element.getBoundingClientRect();
      return rect.width > 1 && (rect.right > width + 2 || rect.left < -2);
    })
    .slice(0, 12)
    .map((element) => {
      const rect = element.getBoundingClientRect();
      return {
        selector: element.id ? `#${element.id}` : `${element.tagName.toLowerCase()}.${[...element.classList].join('.')}`,
        left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width)
      };
    });
  const arrowIssues = [...document.querySelectorAll('.lnk .arw')]
    .filter((arrow) => {
      const link = arrow.closest('.lnk');
      const arrowRect = arrow.getBoundingClientRect();
      const linkRect = link.getBoundingClientRect();
      return arrowRect.right > width + 2 || arrowRect.bottom > linkRect.bottom + 1;
    })
    .map((arrow) => (arrow.closest('.lnk')?.textContent || '').trim());
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('#site-nav');
  const toc = document.querySelector('.toc-disclosure[data-responsive-toc]');
  return {
    url: location.href,
    viewportWidth: width,
    scrollWidth: Math.max(root.scrollWidth, body.scrollWidth),
    horizontalOverflow: Math.max(root.scrollWidth, body.scrollWidth) > width + 2,
    overflowNodes,
    arrowIssues,
    menuDisplay: menu ? getComputedStyle(menu).display : null,
    navDisplay: nav ? getComputedStyle(nav).display : null,
    tocOpen: toc ? toc.open : null,
    h1Count: document.querySelectorAll('h1').length,
    mainCount: document.querySelectorAll('main').length
  };
})()
"""


def audit_menu(cdp: CDP, mobile: bool) -> list[str]:
    errors: list[str] = []
    state = cdp.evaluate("({menu:getComputedStyle(document.querySelector('.menu-button')).display, nav:getComputedStyle(document.querySelector('#site-nav')).display})")
    if mobile:
        if state["menu"] == "none":
            errors.append("mobile menu button is not visible")
        cdp.evaluate("document.querySelector('.menu-button').click()")
        opened = cdp.evaluate("({expanded:document.querySelector('.menu-button').getAttribute('aria-expanded'), open:document.querySelector('#site-nav').classList.contains('is-open'), display:getComputedStyle(document.querySelector('#site-nav')).display})")
        if opened["expanded"] != "true" or not opened["open"] or opened["display"] == "none":
            errors.append("mobile menu did not open with synchronized aria-expanded state")
        cdp.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))")
        closed = cdp.evaluate("({expanded:document.querySelector('.menu-button').getAttribute('aria-expanded'), open:document.querySelector('#site-nav').classList.contains('is-open'), focused:document.activeElement===document.querySelector('.menu-button')})")
        if closed["expanded"] != "false" or closed["open"] or not closed["focused"]:
            errors.append("Escape did not close the mobile menu and restore focus")
    else:
        if state["menu"] != "none":
            errors.append("desktop menu button should be hidden")
        if state["nav"] == "none":
            errors.append("desktop navigation should be visible")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/responsive-layout.json")
    parser.add_argument("--screenshots", default="artifacts/responsive-screenshots")
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
    with tempfile.TemporaryDirectory(prefix="portfolio-chrome-") as profile:
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
                results: list[dict[str, Any]] = []
                errors: list[str] = []
                base_url = args.base_url.rstrip("/") + "/"

                for width, height, label in VIEWPORTS:
                    cdp.command("Emulation.setDeviceMetricsOverride", {
                        "width": width, "height": height, "deviceScaleFactor": 1,
                        "mobile": width <= 480,
                    })
                    for path, page_name in PAGES:
                        url = urljoin(base_url, path)
                        cdp.command("Page.navigate", {"url": url})
                        wait_ready(cdp, url)
                        layout = cdp.evaluate(LAYOUT_EXPRESSION)
                        record = {"viewport": label, "page": page_name, **layout}
                        record_errors: list[str] = []
                        if layout["horizontalOverflow"]:
                            record_errors.append(f"horizontal overflow: scrollWidth={layout['scrollWidth']} viewport={layout['viewportWidth']}")
                        if layout["arrowIssues"]:
                            record_errors.append(f"detached/wrapped link arrows: {layout['arrowIssues']}")
                        if layout["h1Count"] != 1:
                            record_errors.append(f"expected one h1, found {layout['h1Count']}")
                        if layout["mainCount"] != 1:
                            record_errors.append(f"expected one main, found {layout['mainCount']}")
                        if page_name == "home" and label in {"390-mobile", "1440-desktop"}:
                            record_errors.extend(audit_menu(cdp, width <= 480))
                        if page_name == "research":
                            expected_open = width >= 981
                            if layout["tocOpen"] is None:
                                record_errors.append("responsive table of contents is missing")
                            elif bool(layout["tocOpen"]) != expected_open:
                                state = "open" if expected_open else "closed"
                                record_errors.append(f"responsive table of contents should be {state} at {width}px")
                        record["errors"] = record_errors
                        results.append(record)
                        errors.extend(f"{label}/{page_name}: {message}" for message in record_errors)

                        if page_name == "home" or (page_name == "research" and label in {"390-mobile", "1440-desktop"}):
                            image = cdp.command("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                            (screenshots / f"{label}-{page_name}.png").write_bytes(base64.b64decode(image["data"]))

                cdp.command("Emulation.setDeviceMetricsOverride", {
                    "width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False,
                })
                cdp.command("Emulation.setEmulatedMedia", {
                    "features": [{"name": "prefers-reduced-motion", "value": "reduce"}],
                })
                cdp.command("Page.navigate", {"url": base_url})
                wait_ready(cdp, base_url)
                reduced = cdp.evaluate("({scroll:getComputedStyle(document.documentElement).scrollBehavior, transition:getComputedStyle(document.querySelector('.lnk .arw')).transitionDuration})")
                if reduced["scroll"] != "auto" or reduced["transition"] not in {"0s", "0ms"}:
                    errors.append(f"reduced-motion preference not fully honored: {reduced}")

                report_path.write_text(json.dumps({"results": results, "reducedMotion": reduced, "errors": errors}, indent=2) + "\n")
                if errors:
                    print("\n".join(f"ERROR: {error}" for error in errors))
                    return 1
                print(f"Responsive browser audit passed: {len(results)} page/viewport combinations plus reduced-motion, menu, and TOC checks.")
                return 0
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
