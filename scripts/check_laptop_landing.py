#!/usr/bin/env python3
"""Verify the post-choice hero as one landing frame at 1366×768.

The first-visit analytics notice is validated separately while visible. This test
selects Decline, verifies that no analytics script loads, and then checks the
established laptop landing composition without a privacy overlay or notice.
"""
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
from urllib.parse import quote
from urllib.request import Request, urlopen

import websocket

WIDTH = 1366
HEIGHT = 768


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
    expected = expected_url.rstrip("/")
    state: dict[str, Any] = {}
    while time.time() < deadline:
        state = cdp.evaluate("({ready:document.readyState,url:location.href})")
        if state.get("ready") == "complete" and str(state.get("url", "")).rstrip("/") == expected:
            cdp.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
            return
        time.sleep(0.1)
    raise TimeoutError(f"page did not finish navigating to {expected_url}; last state={state}")


DECLINE_PRIVACY_EXPRESSION = r"""
(async () => {
  const banner = document.querySelector('[data-privacy-banner]');
  const decline = document.querySelector('[data-consent-decline]');
  if (!banner || !decline) {
    return {available: false};
  }
  decline.click();
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  let storedConsent = null;
  try {
    storedConsent = localStorage.getItem('bhalaji.analyticsConsent.v1');
  } catch (error) {
    storedConsent = 'storage-unavailable';
  }
  return {
    available: true,
    bannerHidden: banner.hidden,
    storedConsent,
    clarityScriptLoaded: Boolean(document.querySelector('script[data-clarity-project]')),
    clarityQueueCreated: typeof window.clarity === 'function'
  };
})()
"""


LANDING_EXPRESSION = r"""
(() => {
  const rect = (selector) => {
    const element = document.querySelector(selector);
    if (!element) return null;
    const box = element.getBoundingClientRect();
    return {
      top: Math.round(box.top),
      right: Math.round(box.right),
      bottom: Math.round(box.bottom),
      left: Math.round(box.left),
      width: Math.round(box.width),
      height: Math.round(box.height)
    };
  };
  const eyebrow = document.querySelector('.hero .eyebrow');
  const eyebrowStyle = eyebrow ? getComputedStyle(eyebrow) : null;
  const eyebrowLineHeight = eyebrowStyle ? parseFloat(eyebrowStyle.lineHeight) : 0;
  const eyebrowHeight = eyebrow ? eyebrow.getBoundingClientRect().height : 0;
  const root = document.documentElement;
  const privacyBanner = document.querySelector('[data-privacy-banner]');
  return {
    viewport: {width: innerWidth, height: innerHeight},
    scrollWidth: root.scrollWidth,
    hero: rect('.hero'),
    copy: rect('.hero__copy'),
    headline: rect('.hero h1'),
    portrait: rect('.hero__visual'),
    identity: rect('.identity-note'),
    status: rect('.status-line'),
    eyebrow: rect('.hero .eyebrow'),
    eyebrowLines: eyebrowLineHeight ? Math.round(eyebrowHeight / eyebrowLineHeight) : null,
    privacyBannerHidden: Boolean(privacyBanner && privacyBanner.hidden),
    clarityScriptLoaded: Boolean(document.querySelector('script[data-clarity-project]')),
    desktopNavigationVisible: getComputedStyle(document.querySelector('#site-nav')).display !== 'none',
    menuButtonHidden: getComputedStyle(document.querySelector('.menu-button')).display === 'none'
  };
})()
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/laptop-landing.json")
    parser.add_argument("--screenshot", default="artifacts/responsive-screenshots/1366x768-laptop-home.png")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report = Path(args.report)
    screenshot = Path(args.screenshot)
    report.parent.mkdir(parents=True, exist_ok=True)
    screenshot.parent.mkdir(parents=True, exist_ok=True)

    port = free_port()
    privacy_choice: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="portfolio-laptop-chrome-", ignore_cleanup_errors=True) as profile:
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
                cdp.command(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": WIDTH, "height": HEIGHT, "deviceScaleFactor": 1, "mobile": False},
                )
                url = args.base_url.rstrip("/") + "/"
                cdp.command("Page.navigate", {"url": url})
                wait_ready(cdp, url)
                privacy_choice = cdp.evaluate(DECLINE_PRIVACY_EXPRESSION)
                metrics = cdp.evaluate(LANDING_EXPRESSION)
                image = cdp.command("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                screenshot.write_bytes(base64.b64decode(image["data"]))
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    errors: list[str] = []
    if not privacy_choice.get("available"):
        errors.append("privacy decline control is unavailable")
    if not privacy_choice.get("bannerHidden") or not metrics.get("privacyBannerHidden"):
        errors.append("privacy notice did not leave the document flow after Decline")
    if privacy_choice.get("storedConsent") != "denied":
        errors.append(f"declined analytics preference was not stored: {privacy_choice.get('storedConsent')!r}")
    if privacy_choice.get("clarityScriptLoaded") or metrics.get("clarityScriptLoaded"):
        errors.append("Microsoft Clarity loaded after analytics was declined")

    viewport_height = int(metrics["viewport"]["height"])
    for name in ("hero", "copy", "headline", "portrait", "identity", "status", "eyebrow"):
        if not metrics.get(name):
            errors.append(f"missing hero element: {name}")
    if int(metrics.get("scrollWidth", WIDTH)) > WIDTH + 2:
        errors.append(f"horizontal overflow: scrollWidth={metrics['scrollWidth']} viewport={WIDTH}")
    if metrics.get("eyebrowLines") != 1:
        errors.append(f"research eyebrow must remain one line at 1366×768; found {metrics.get('eyebrowLines')}")
    if not metrics.get("desktopNavigationVisible") or not metrics.get("menuButtonHidden"):
        errors.append("1366×768 must use complete desktop navigation")

    for name in ("hero", "copy", "portrait", "identity", "status"):
        box = metrics.get(name)
        if box and int(box["bottom"]) > viewport_height - 8:
            errors.append(f"{name} extends below the landing frame: bottom={box['bottom']} viewport={viewport_height}")
        if box and int(box["top"]) < 0:
            errors.append(f"{name} begins above the visible viewport: top={box['top']}")

    report.write_text(json.dumps({"privacyChoice": privacy_choice, "metrics": metrics, "errors": errors}, indent=2) + "\n")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("1366×768 post-choice laptop landing-frame audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
