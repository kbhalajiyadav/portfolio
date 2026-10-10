#!/usr/bin/env python3
"""Validate homepage attention hierarchy across common desktop and laptop frames."""
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
    (1024, 768, "compact-desktop"),
    (1280, 720, "small-laptop"),
    (1366, 768, "laptop"),
    (1440, 900, "large-laptop"),
    (1536, 864, "wide-laptop"),
    (1920, 1080, "desktop"),
]

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

PAGE_METRICS = r"""
(() => {
  const rect = (selector) => {
    const element = document.querySelector(selector);
    if (!element) return null;
    const box = element.getBoundingClientRect();
    return {top:box.top,right:box.right,bottom:box.bottom,left:box.left,width:box.width,height:box.height};
  };
  const headline = document.querySelector('.hero h1');
  const headlineStyle = headline ? getComputedStyle(headline) : null;
  const headlineLineHeight = headlineStyle ? parseFloat(headlineStyle.lineHeight) || 0 : 0;
  const headlineHeight = headline ? headline.getBoundingClientRect().height : 0;
  const lede = document.querySelector('.hero .lede');
  const ledeStyle = lede ? getComputedStyle(lede) : null;
  const heroActions = [...document.querySelectorAll('.hero .actions a')];
  const primary = document.querySelector('.hero .button--primary');
  const secondary = document.querySelector('.hero .actions .lnk');
  const primaryStyle = primary ? getComputedStyle(primary) : null;
  const secondaryStyle = secondary ? getComputedStyle(secondary) : null;
  const proof = [...document.querySelectorAll('.metrics > div')].map((item) => ({
    value:(item.querySelector('strong')?.textContent || '').trim(),
    label:(item.querySelector('span')?.textContent || '').trim(),
  }));
  const pillars = [...document.querySelectorAll('.pillar')].map((item) => {
    const box = item.getBoundingClientRect();
    const title = item.querySelector('h3')?.getBoundingClientRect();
    const body = item.querySelector(':scope > p')?.getBoundingClientRect();
    const tags = item.querySelector('.tag-list')?.getBoundingClientRect();
    const link = item.querySelector(':scope > .lnk')?.getBoundingClientRect();
    const motif = item.querySelector('.motif');
    return {
      top:box.top,
      bottom:box.bottom,
      height:box.height,
      titleTop:title?.top ?? null,
      bodyTop:body?.top ?? null,
      tagsTop:tags?.top ?? null,
      linkBottom:link?.bottom ?? null,
      motifOpacity:motif ? parseFloat(getComputedStyle(motif).opacity) : null,
    };
  });
  const selectedOutputs = document.querySelector('#outputs');
  return {
    viewport:{width:innerWidth,height:innerHeight},
    scrollWidth:document.documentElement.scrollWidth,
    hero:rect('.hero'),
    copy:rect('.hero__copy'),
    headline:rect('.hero h1'),
    lede:rect('.hero .lede'),
    actions:rect('.hero .actions'),
    primaryAction:rect('.hero .button--primary'),
    portrait:rect('.hero__visual'),
    identity:rect('.identity-note'),
    status:rect('.status-line'),
    headlineFontSize:headlineStyle ? parseFloat(headlineStyle.fontSize) || 0 : 0,
    headlineLines:headlineLineHeight ? Math.round(headlineHeight / headlineLineHeight) : null,
    ledeFontSize:ledeStyle ? parseFloat(ledeStyle.fontSize) || 0 : 0,
    ledeLineHeight:ledeStyle ? parseFloat(ledeStyle.lineHeight) || 0 : 0,
    heroActionCount:heroActions.length,
    primaryBackground:primaryStyle ? primaryStyle.backgroundColor : '',
    secondaryBackground:secondaryStyle ? secondaryStyle.backgroundColor : '',
    proof,
    pillars,
    researchPackageCount:selectedOutputs ? selectedOutputs.querySelectorAll('.research-package').length : 0,
    secondaryOutputCount:selectedOutputs ? selectedOutputs.querySelectorAll('.secondary-output').length : 0,
    selectedOutputsText:selectedOutputs ? (selectedOutputs.textContent || '').replace(/\s+/g,' ').trim() : '',
  };
})()
"""


def overlaps(a: dict | None, b: dict | None) -> bool:
    if not a or not b:
        return False
    return not (
        a["right"] <= b["left"] + 2
        or b["right"] <= a["left"] + 2
        or a["bottom"] <= b["top"] + 2
        or b["bottom"] <= a["top"] + 2
    )


def transparent(value: str) -> bool:
    normalized = value.replace(" ", "").lower()
    return normalized in {"transparent", "rgba(0,0,0,0)"}


def spread(values: list[float | int | None]) -> float | None:
    usable = [float(value) for value in values if value is not None]
    if not usable:
        return None
    return max(usable) - min(usable)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173/")
    parser.add_argument("--chrome", default="")
    parser.add_argument("--report", default="artifacts/attention-hierarchy.json")
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

    with tempfile.TemporaryDirectory(prefix="portfolio-attention-chrome-", ignore_cleanup_errors=True) as profile:
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
                url = args.base_url.rstrip("/") + "/"
                for width, height, name in VIEWPORTS:
                    cdp.command("Emulation.setDeviceMetricsOverride", {
                        "width": width,
                        "height": height,
                        "deviceScaleFactor": 1,
                        "mobile": False,
                    })
                    cdp.command("Page.navigate", {"url": url})
                    wait_ready(cdp, url)
                    cdp.evaluate(DECLINE_PRIVACY)
                    metrics = cdp.evaluate(PAGE_METRICS)
                    metrics["name"] = name
                    results.append(metrics)

                    prefix = f"{width}x{height}/{name}"
                    if metrics["scrollWidth"] > width + 2:
                        errors.append(f"{prefix}: horizontal overflow ({metrics['scrollWidth']}px)")

                    for key in ("hero", "copy", "headline", "lede", "actions", "primaryAction", "portrait", "identity", "status"):
                        if not metrics.get(key):
                            errors.append(f"{prefix}: missing {key}")

                    line_limit = 5 if width <= 1100 else 4
                    if not metrics.get("headlineLines") or metrics["headlineLines"] > line_limit:
                        errors.append(f"{prefix}: headline uses too many lines: {metrics.get('headlineLines')}")
                    if not (44 <= metrics.get("headlineFontSize", 0) <= 80):
                        errors.append(f"{prefix}: headline size outside attention-safe range: {metrics.get('headlineFontSize')}px")
                    if metrics.get("headline") and metrics["headline"]["height"] > height * 0.46:
                        errors.append(f"{prefix}: headline occupies too much of the first frame")
                    if not (16 <= metrics.get("ledeFontSize", 0) <= 23):
                        errors.append(f"{prefix}: lede size outside readable range: {metrics.get('ledeFontSize')}px")
                    if metrics.get("ledeFontSize", 0) and metrics.get("ledeLineHeight", 0) < metrics["ledeFontSize"] * 1.45:
                        errors.append(f"{prefix}: lede line height is too tight")

                    if metrics.get("heroActionCount") != 2:
                        errors.append(f"{prefix}: hero must expose exactly one primary and one secondary action")
                    if transparent(metrics.get("primaryBackground", "")):
                        errors.append(f"{prefix}: primary research action is not visually prominent")
                    if not transparent(metrics.get("secondaryBackground", "")):
                        errors.append(f"{prefix}: secondary CV action is competing with the primary action")

                    for key in ("lede", "primaryAction", "portrait", "identity", "status"):
                        box = metrics.get(key)
                        if box and box["bottom"] > height - 4:
                            errors.append(f"{prefix}: {key} falls below the first frame (bottom={box['bottom']:.1f})")
                    if overlaps(metrics.get("copy"), metrics.get("portrait")):
                        errors.append(f"{prefix}: hero copy and portrait overlap")
                    portrait = metrics.get("portrait")
                    hero = metrics.get("hero")
                    if portrait and hero and hero["width"]:
                        # The site uses a fixed maximum content shell, so portrait balance
                        # must be judged against that composition rather than the full
                        # browser width on large monitors.
                        hero_share = portrait["width"] / hero["width"]
                        metrics["portraitHeroShare"] = hero_share
                        if not (0.23 <= hero_share <= 0.38):
                            errors.append(f"{prefix}: portrait share of hero composition is unbalanced ({hero_share:.3f})")

                    pillars = metrics.get("pillars", [])
                    if len(pillars) != 3:
                        errors.append(f"{prefix}: expected exactly three research-program cards, found {len(pillars)}")
                    elif width >= 1280:
                        alignment = {
                            "cardTops": spread([item.get("top") for item in pillars]),
                            "cardHeights": spread([item.get("height") for item in pillars]),
                            "titleTops": spread([item.get("titleTop") for item in pillars]),
                            "bodyTops": spread([item.get("bodyTop") for item in pillars]),
                            "tagTops": spread([item.get("tagsTop") for item in pillars]),
                            "linkBottoms": spread([item.get("linkBottom") for item in pillars]),
                        }
                        metrics["pillarAlignment"] = alignment
                        for label, delta in alignment.items():
                            if delta is None or delta > 3:
                                errors.append(f"{prefix}: research-card {label} lost alignment (spread={delta})")
                        opacities = [item.get("motifOpacity") for item in pillars if item.get("motifOpacity") is not None]
                        if len(opacities) != 3:
                            errors.append(f"{prefix}: research motifs missing opacity metrics")
                        elif max(opacities) > 0.5 or spread(opacities) > 0.02:
                            errors.append(f"{prefix}: research motifs are visually unbalanced: {opacities}")

                    expected_labels = [
                        "Peer-reviewed articles",
                        "Patent-pending technology",
                        "Citable software release",
                        "Student projects guided",
                    ]
                    labels = [item["label"] for item in metrics.get("proof", [])]
                    if labels != expected_labels:
                        errors.append(f"{prefix}: proof strip labels drifted: {labels}")
                    values = {item["label"]: item["value"] for item in metrics.get("proof", [])}
                    if values.get("Patent-pending technology") != "1":
                        errors.append(f"{prefix}: patent-pending proof count must remain 1")
                    if values.get("Citable software release") != "1":
                        errors.append(f"{prefix}: citable-software proof count must remain 1")

                    if metrics.get("researchPackageCount") != 1 or metrics.get("secondaryOutputCount") != 1:
                        errors.append(f"{prefix}: homepage outputs must stay curated to one flagship package plus one IP record")
                    if "Mechanical Properties of Dual-Layer Electrospun Fiber Mats" in metrics.get("selectedOutputsText", ""):
                        errors.append(f"{prefix}: complete coauthor publication record belongs on Outputs, not homepage selected evidence")
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    report_path.write_text(json.dumps({"viewports": results, "errors": errors}, indent=2) + "\n")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Homepage attention hierarchy passed across six desktop/laptop frames: proposition, primary action, portrait, proof signals, aligned research cards, decorative restraint, and selected evidence remain prioritized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
