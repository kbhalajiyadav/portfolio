#!/usr/bin/env python3
"""Protect persistent header geometry, output-filter stability, and bounded action density."""
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

PAGES = ["/", "/about/", "/outputs/", "/research/"]
VIEWPORTS = [(1440, 900, "desktop"), (390, 844, "mobile")]
TOLERANCE = 2.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/navigation-continuity.json")
    args = parser.parse_args()

    chrome = args.chrome or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("ERROR: Chrome/Chromium executable not found")
        return 1

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    port = free_port()
    errors: list[str] = []
    report: dict = {"headers": {}, "outputsFilter": {}, "actionDensity": {}}

    with tempfile.TemporaryDirectory(prefix="portfolio-continuity-chrome-", ignore_cleanup_errors=True) as profile:
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
                base = args.base_url.rstrip("/")

                for width, height, label in VIEWPORTS:
                    signatures: dict[str, dict] = {}
                    for path in PAGES:
                        cdp.command("Emulation.setDeviceMetricsOverride", {
                            "width": width,
                            "height": height,
                            "deviceScaleFactor": 1,
                            "mobile": width <= 680,
                        })
                        url = base + path
                        cdp.command("Page.navigate", {"url": url})
                        wait_ready(cdp, url)
                        cdp.evaluate("document.querySelector('[data-consent-decline]')?.click()")
                        signature = cdp.evaluate(
                            r"""
                            (() => {
                              const box = selector => {
                                const element = document.querySelector(selector);
                                if (!element || getComputedStyle(element).display === 'none') return null;
                                const r = element.getBoundingClientRect();
                                return {top:r.top,left:r.left,right:r.right,bottom:r.bottom,width:r.width,height:r.height};
                              };
                              const actionGroups = [...document.querySelectorAll('.actions')]
                                .filter(group => getComputedStyle(group).display !== 'none')
                                .map((group, index) => ({
                                  index,
                                  count:[...group.querySelectorAll(':scope > a, :scope > button')]
                                    .filter(item => getComputedStyle(item).display !== 'none').length,
                                  text:group.textContent.trim().replace(/\s+/g, ' ').slice(0, 160)
                                }));
                              return {
                                header:box('.site-head'),
                                inner:box('.site-head__inner'),
                                brand:box('.brand'),
                                nav:box('#site-nav'),
                                contact:box('.nav-contact'),
                                menu:box('.menu-button'),
                                actionGroups
                              };
                            })()
                            """
                        )
                        signatures[path] = signature
                        for group in signature["actionGroups"]:
                            if group["count"] > 3:
                                errors.append(
                                    f"{label}{path}: action group {group['index']} exposes {group['count']} actions; "
                                    f"bounded groups should expose at most 3 ({group['text']!r})"
                                )
                    report["headers"][label] = signatures
                    report["actionDensity"][label] = {
                        path: signatures[path]["actionGroups"] for path in PAGES
                    }

                    baseline = signatures["/"]
                    for path, current in signatures.items():
                        if path == "/":
                            continue
                        for part in ("header", "inner", "brand"):
                            base_box = baseline.get(part)
                            current_box = current.get(part)
                            if not base_box or not current_box:
                                errors.append(f"{label}{path}: missing persistent header element {part}")
                                continue
                            for metric in ("top", "left", "width", "height"):
                                if abs(current_box[metric] - base_box[metric]) > TOLERANCE:
                                    errors.append(
                                        f"{label}{path}: persistent {part} geometry shifted in {metric}: "
                                        f"{base_box[metric]:.1f}px -> {current_box[metric]:.1f}px"
                                    )
                        persistent_control = "nav" if label == "desktop" else "menu"
                        base_box = baseline.get(persistent_control)
                        current_box = current.get(persistent_control)
                        if not base_box or not current_box:
                            errors.append(f"{label}{path}: missing persistent {persistent_control}")
                        else:
                            for metric in ("top", "right", "width", "height"):
                                if abs(current_box[metric] - base_box[metric]) > TOLERANCE:
                                    errors.append(
                                        f"{label}{path}: persistent {persistent_control} geometry shifted in {metric}: "
                                        f"{base_box[metric]:.1f}px -> {current_box[metric]:.1f}px"
                                    )

                outputs_url = base + "/outputs/"
                cdp.command("Emulation.setDeviceMetricsOverride", {
                    "width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False,
                })
                cdp.command("Page.navigate", {"url": outputs_url})
                wait_ready(cdp, outputs_url)
                cdp.evaluate("document.querySelector('[data-consent-decline]')?.click()")
                filter_result = cdp.evaluate(
                    r"""
                    new Promise(async resolve => {
                      const buttons = [...document.querySelectorAll('[data-output-filter]')];
                      const filter = document.querySelector('.output-filter');
                      const list = document.querySelector('[data-output-list]');
                      const header = document.querySelector('.page-header');
                      if (!filter || !list || buttons.length !== 5) {
                        resolve({missing:true, count:buttons.length});
                        return;
                      }
                      const rect = element => {
                        const r = element.getBoundingClientRect();
                        return {top:r.top,left:r.left,width:r.width,height:r.height,bottom:r.bottom};
                      };
                      const baseline = {
                        filter:rect(filter),
                        list:rect(list),
                        header:rect(header),
                        scrollY:window.scrollY,
                        buttons:buttons.map(button => rect(button))
                      };
                      const states = [];
                      for (const button of buttons) {
                        button.click();
                        await new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)));
                        states.push({
                          filter:button.dataset.outputFilter,
                          filterRect:rect(filter),
                          listRect:rect(list),
                          headerRect:rect(header),
                          scrollY:window.scrollY,
                          buttons:buttons.map(item => rect(item))
                        });
                      }
                      resolve({missing:false, baseline, states});
                    })
                    """
                )
                report["outputsFilter"] = filter_result
                if filter_result.get("missing"):
                    errors.append(f"outputs filter stability test missing required controls: {filter_result}")
                else:
                    baseline = filter_result["baseline"]
                    for state in filter_result["states"]:
                        name = state["filter"]
                        for group_key, rect_key in (("filter", "filterRect"), ("list", "listRect"), ("header", "headerRect")):
                            before = baseline[group_key]
                            after = state[rect_key]
                            for metric in ("top", "left", "width"):
                                if abs(after[metric] - before[metric]) > 1.0:
                                    errors.append(
                                        f"outputs/{name}: {group_key} shifted in {metric}: "
                                        f"{before[metric]:.1f}px -> {after[metric]:.1f}px"
                                    )
                        if abs(state["filterRect"]["height"] - baseline["filter"]["height"]) > 1.0:
                            errors.append(f"outputs/{name}: filter control height changed after selection")
                        if abs(state["scrollY"] - baseline["scrollY"]) > 1.0:
                            errors.append(f"outputs/{name}: filter selection unexpectedly changed scroll position")
                        for index, after in enumerate(state["buttons"]):
                            before = baseline["buttons"][index]
                            for metric in ("top", "left", "width", "height"):
                                if abs(after[metric] - before[metric]) > 1.0:
                                    errors.append(
                                        f"outputs/{name}: filter button {index} shifted in {metric}: "
                                        f"{before[metric]:.1f}px -> {after[metric]:.1f}px"
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

    report_path.write_text(json.dumps({"report": report, "errors": errors}, indent=2) + "\n")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Navigation continuity passed: persistent header geometry, output-filter stability, and bounded action density verified across key pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
