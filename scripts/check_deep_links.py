#!/usr/bin/env python3
"""Browser audit for contextual navigation, evidence deep links, and governed layout states."""
from __future__ import annotations

import argparse
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

PRIMARY_DESTINATIONS = ["about/", "research/", "outputs/", "experience/", "engagement/", "contact/"]
DETAIL_PARENTS = {
    "publication/adhesives-wearable/": "/outputs/",
    "publication/masters-thesis/": "/outputs/",
    "project/peel-trace-evaluation/": "/outputs/",
    "project/optical-metrology/": "/research/",
    "project/quantitative-thermal-imaging/": "/outputs/",
    "project/fda-project/": "/experience/",
    "project/supply-chain-automation/": "/experience/",
}
SERIES_IDS = ["adhesion-soft-wearable-interfaces", "computer-vision-mechanochromic-textiles"]


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
        self.ws = websocket.create_connection(websocket_url, timeout=25, origin="http://127.0.0.1", suppress_origin=True)
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
        result = self.command("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
        return result.get("result", {}).get("value")


def wait_ready(cdp: CDP, expected_url: str, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    expected = expected_url.rstrip("/")
    while time.time() < deadline:
        state = cdp.evaluate("({ready:document.readyState,url:location.href})")
        if state and state.get("ready") == "complete" and str(state.get("url", "")).rstrip("/") == expected:
            cdp.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
            return
        time.sleep(0.1)
    raise TimeoutError(f"page did not finish navigating to {expected_url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/deep-links.json")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    base_url = args.base_url.rstrip("/") + "/"
    errors: list[str] = []
    observations: list[dict[str, Any]] = []

    port = free_port()
    with tempfile.TemporaryDirectory(prefix="portfolio-deep-links-", ignore_cleanup_errors=True) as profile:
        process = subprocess.Popen([
            chrome, "--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
            "--hide-scrollbars", "--remote-allow-origins=*", f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}", "about:blank",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.time() + 20
            while True:
                try:
                    read_json(f"http://127.0.0.1:{port}/json/version", timeout=1)
                    break
                except Exception:
                    if time.time() >= deadline:
                        raise RuntimeError("Chrome DevTools endpoint did not start")
                    time.sleep(0.2)

            target = read_json(f"http://127.0.0.1:{port}/json/new?{quote('about:blank', safe=':/?=&')}", method="PUT")
            cdp = CDP(target["webSocketDebuggerUrl"])
            try:
                cdp.command("Page.enable")
                cdp.command("Runtime.enable")
                cdp.command("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False})

                for path in PRIMARY_DESTINATIONS:
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    state = cdp.evaluate("({back:!!document.querySelector('.back-link'), current:[...document.querySelectorAll('#site-nav a[aria-current=\"page\"]')].map(a=>a.getAttribute('href'))})")
                    observations.append({"path": path, "kind": "primary", **state})
                    if state.get("back"):
                        errors.append(f"primary destination exposes redundant back-link: {path}")

                for path, expected_parent in DETAIL_PARENTS.items():
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    state = cdp.evaluate("(() => { const a=document.querySelector('.back-link'); return {href:a?new URL(a.href).pathname:null,label:a?a.textContent.trim():null}; })()")
                    observations.append({"path": path, "kind": "detail", **state})
                    if state.get("href") != expected_parent:
                        errors.append(f"detail parent mismatch for {path}: expected {expected_parent}, got {state.get('href')}")

                for series_id in SERIES_IDS:
                    path = f"engagement/#{series_id}"
                    url = urljoin(base_url, path)
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    state = cdp.evaluate(f"""(() => {{
                      const target=document.getElementById({json.dumps(series_id)});
                      const header=document.querySelector('.site-head');
                      if (!target) return {{exists:false}};
                      const rect=target.getBoundingClientRect();
                      const style=getComputedStyle(target);
                      return {{
                        exists:true,
                        open:target.open===true,
                        isTarget:target.matches(':target'),
                        top:Math.round(rect.top),
                        headerBottom:Math.round(header?.getBoundingClientRect().bottom || 0),
                        borderLeftWidth:style.borderLeftWidth,
                        borderLeftColor:style.borderLeftColor
                      }};
                    }})()""")
                    observations.append({"path": path, "kind": "series-target", **state})
                    if not state.get("exists"):
                        errors.append(f"deep-link target missing: {series_id}")
                        continue
                    if not state.get("open"):
                        errors.append(f"deep-linked presentation series did not open: {series_id}")
                    if not state.get("isTarget"):
                        errors.append(f"deep-linked presentation series is not :target: {series_id}")
                    if state.get("top", 0) < state.get("headerBottom", 0):
                        errors.append(f"deep-linked presentation series is obscured by sticky header: {series_id}")
                    if state.get("borderLeftWidth") in (None, "0px"):
                        errors.append(f"deep-linked presentation series lacks persistent target emphasis: {series_id}")

                cdp.command("Emulation.setDeviceMetricsOverride", {"width": 820, "height": 900, "deviceScaleFactor": 1, "mobile": False})
                cdp.command("Page.navigate", {"url": base_url})
                wait_ready(cdp, base_url)
                tablet = cdp.evaluate(r"""(() => {
                  const hero=document.querySelector('.hero');
                  const copy=document.querySelector('.hero__copy');
                  const visual=document.querySelector('.hero__visual');
                  const note=document.querySelector('.identity-note');
                  const appHeading=document.querySelector('.trajectory-grid .application-card h3');
                  const appBody=document.querySelector('.trajectory-grid .application-card h3 + p');
                  const desktopSig=document.querySelector('.research-signature__desktop');
                  const mobileSig=document.querySelector('.research-signature__mobile');
                  const copyRect=copy?.getBoundingClientRect();
                  const visualRect=visual?.getBoundingClientRect();
                  const hRect=appHeading?.getBoundingClientRect();
                  const pRect=appBody?.getBoundingClientRect();
                  return {
                    columns:hero?getComputedStyle(hero).gridTemplateColumns:null,
                    visualAfterCopy:!!(copyRect&&visualRect&&visualRect.top>=copyRect.bottom+12),
                    identityPosition:note?getComputedStyle(note).position:null,
                    headingBodyGap:Math.round((pRect?.top||0)-(hRect?.bottom||0)),
                    desktopSignatureDisplay:desktopSig?getComputedStyle(desktopSig).display:null,
                    mobileSignatureDisplay:mobileSig?getComputedStyle(mobileSig).display:null
                  };
                })()""")
                observations.append({"path": "", "kind": "tablet-820", **tablet})
                if not tablet.get("visualAfterCopy"):
                    errors.append("820px hero has not transitioned to an intentional stacked composition")
                if tablet.get("identityPosition") != "static":
                    errors.append(f"820px hero identity note should be static, got {tablet.get('identityPosition')}")
                if tablet.get("headingBodyGap", 0) < 7:
                    errors.append(f"doctoral application heading/body rhythm is too tight: {tablet.get('headingBodyGap')}px")
                if tablet.get("desktopSignatureDisplay") != "none" or tablet.get("mobileSignatureDisplay") == "none":
                    errors.append("820px research signature did not switch to the legible mobile/tablet representation")
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    report_path.write_text(json.dumps({"errors": errors, "observations": observations}, indent=2), encoding="utf-8")
    if errors:
        print("Deep-link and contextual-navigation audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Deep-link, contextual-navigation, and governed tablet-layout audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
