#!/usr/bin/env python3
"""Validate homepage attention hierarchy across desktop, laptop, and mobile frames."""
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
    (320, 800, "wcag-reflow", True),
    (390, 844, "mobile", True),
    (1024, 768, "compact-desktop", False),
    (1280, 720, "small-laptop", False),
    (1366, 768, "laptop", False),
    (1440, 900, "large-laptop", False),
    (1536, 864, "wide-laptop", False),
    (1920, 1080, "desktop", False),
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
  const lineCount = element => {
    if (!element) return null;
    const style = getComputedStyle(element);
    const lineHeight = parseFloat(style.lineHeight) || 0;
    return lineHeight ? Math.round(element.getBoundingClientRect().height / lineHeight) : null;
  };
  const headline = document.querySelector('.hero h1');
  const eyebrow = document.querySelector('.hero .eyebrow');
  const headlineStyle = headline ? getComputedStyle(headline) : null;
  const lede = document.querySelector('.hero .lede');
  const ledeStyle = lede ? getComputedStyle(lede) : null;
  const heroActions = [...document.querySelectorAll('.hero .actions a')];
  const primary = document.querySelector('.hero .button--primary');
  const secondary = document.querySelector('.hero .actions .lnk');
  const primaryStyle = primary ? getComputedStyle(primary) : null;
  const secondaryStyle = secondary ? getComputedStyle(secondary) : null;
  const selectedOutputs = document.querySelector('#outputs');
  return {
    viewport:{width:innerWidth,height:innerHeight},
    scrollWidth:document.documentElement.scrollWidth,
    hero:rect('.hero'),
    copy:rect('.hero__copy'),
    eyebrow:rect('.hero .eyebrow'),
    headline:rect('.hero h1'),
    lede:rect('.hero .lede'),
    actions:rect('.hero .actions'),
    primaryAction:rect('.hero .button--primary'),
    portrait:rect('.hero__visual'),
    identity:rect('.identity-note'),
    portraitToDoctoralGap:(() => {
      const identity=document.querySelector('.identity-note');
      const doctoral=document.querySelector('#research .section-head .kicker');
      return identity && doctoral ? doctoral.getBoundingClientRect().top - identity.getBoundingClientRect().bottom : null;
    })(),
    status:rect('.status-line'),
    eyebrowLines:lineCount(eyebrow),
    headlineLines:lineCount(headline),
    headlineFontSize:headlineStyle ? parseFloat(headlineStyle.fontSize) || 0 : 0,
    ledeFontSize:ledeStyle ? parseFloat(ledeStyle.fontSize) || 0 : 0,
    ledeLineHeight:ledeStyle ? parseFloat(ledeStyle.lineHeight) || 0 : 0,
    heroActionCount:heroActions.length,
    currentFocusVisible:!!document.querySelector('.hero__focus a[href="/research/#open-research-questions"]'),
    contactActionVisible:!!document.querySelector('.hero .actions a[href="/contact/"]'),
    cvVisible:!!document.querySelector('.hero__cv a[href*="cv.pdf"]'),
    highlightCount:document.querySelectorAll('.highlights__grid > .highlight').length,
    highlightDestinations:[...document.querySelectorAll('.highlights__grid .highlight h3 a')].map(a=>a.getAttribute('href')),
    primaryBackground:primaryStyle ? primaryStyle.backgroundColor : '',
    secondaryBackground:secondaryStyle ? secondaryStyle.backgroundColor : '',
    counterVisible:!!document.querySelector(".metrics"),
    doctoralHeading:document.querySelector('#research .section-head h2')?.textContent?.trim() || '',
    genericPillars:document.querySelectorAll('#research .pillar').length,
    selectedWorkGap:(() => {
      const cards=document.querySelector('.highlights__grid');
      const link=document.querySelector('.highlights__more');
      return cards && link ? link.getBoundingClientRect().top - cards.getBoundingClientRect().bottom : null;
    })(),
    researchPackageCount:selectedOutputs ? selectedOutputs.querySelectorAll('.research-package').length : 0,
    secondaryOutputCount:selectedOutputs ? selectedOutputs.querySelectorAll('.secondary-output').length : 0,
    selectedOutputsText:selectedOutputs ? (selectedOutputs.textContent || '').replace(/\s+/g,' ').trim() : '',
    selectedOutputsHeadingLines:lineCount(selectedOutputs?.querySelector('.section-head h2')),
    caseStudyHeading:selectedOutputs?.querySelector('.package-lead h3')?.textContent?.trim() || '',
    caseStudyFigureCount:selectedOutputs?.querySelectorAll('.package-lead > .research-figure').length || 0,
    caseStudyLinks:[...(selectedOutputs?.querySelectorAll('.package-artifacts a[href]') || [])].map(a=>a.getAttribute('href')),
    sectionHeadingPairs:[...document.querySelectorAll('main .section-head')]
      .filter(head => head.querySelector(':scope > h2') && head.querySelector(':scope > p:not(.kicker)'))
      .map(head => {
        const h2 = head.querySelector(':scope > h2').getBoundingClientRect();
        const intro = head.querySelector(':scope > p:not(.kicker)').getBoundingClientRect();
        const kicker = head.querySelector(':scope > .kicker')?.getBoundingClientRect();
        return {
          section:head.closest('[id]')?.id || 'unnamed',
          headingTop:h2.top,headingBottom:h2.bottom,introTop:intro.top,
          kickerBottom:kicker?.bottom ?? null,
          columns:getComputedStyle(head).gridTemplateColumns.split(/\s+/).filter(Boolean).length,
        };
      }),
    disclosures:[...document.querySelectorAll('main details.home-disclosure:not(.home-disclosure--experience)')].map(item=>({
      open:item.open,
      summaryHeight:item.querySelector(':scope > summary')?.getBoundingClientRect().height || 0,
      evidenceCount:item.querySelectorAll('.trajectory-grid article, .questions article, .compact-record').length,
      bodyVisible:!!item.querySelector('.home-disclosure__body')?.getClientRects().length,
    })),
    researchFollowup:(() => {
      const block=document.querySelector('.research-home-followup');
      const intro=document.querySelector('#research .section-head');
      const box=block?.getBoundingClientRect();
      const last=intro?.getBoundingClientRect();
      return {
        exists:!!block,
        linkDestinations:[...(block?.querySelectorAll('a[href]') || [])].map(a=>a.getAttribute('href')),
        gap:last && box ? box.top-last.bottom : null,
        duplicateQuestionCount:document.querySelectorAll('.research-extension .questions article').length,
        duplicateDiagramCount:document.querySelectorAll('#research .research-signature').length,
      };
    })(),
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


def visual_rows(items: list[dict], tolerance: float = 3.0) -> list[list[dict]]:
    rows: list[list[dict]] = []
    for item in sorted(items, key=lambda value: (value.get("top") or 0)):
        top = item.get("top")
        if top is None:
            continue
        for row in rows:
            row_top = row[0].get("top")
            if row_top is not None and abs(float(top) - float(row_top)) <= tolerance:
                row.append(item)
                break
        else:
            rows.append([item])
    return rows


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
                for width, height, name, mobile in VIEWPORTS:
                    cdp.command("Emulation.setDeviceMetricsOverride", {
                        "width": width,
                        "height": height,
                        "deviceScaleFactor": 1,
                        "mobile": mobile,
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
                    for key in ("hero", "copy", "eyebrow", "headline", "lede", "actions", "primaryAction", "portrait", "identity", "status"):
                        if not metrics.get(key):
                            errors.append(f"{prefix}: missing {key}")

                    if mobile:
                        copy = metrics.get("copy")
                        headline = metrics.get("headline")
                        portrait = metrics.get("portrait")
                        if copy and copy["width"] < width - 48:
                            errors.append(f"{prefix}: hero copy collapsed too narrowly ({copy['width']:.1f}px)")
                        if (metrics.get("eyebrowLines") or 99) > 3:
                            errors.append(f"{prefix}: eyebrow fragments into {metrics.get('eyebrowLines')} lines")
                        line_limit = 5 if width >= 390 else 6
                        if (metrics.get("headlineLines") or 99) > line_limit:
                            errors.append(f"{prefix}: headline fragments into {metrics.get('headlineLines')} lines (limit {line_limit})")
                        if not (36 <= metrics.get("headlineFontSize", 0) <= 48):
                            errors.append(f"{prefix}: headline size outside mobile range: {metrics.get('headlineFontSize')}px")
                        if headline and headline["width"] < (width - 48) * 0.9:
                            errors.append(f"{prefix}: headline block does not use the available mobile measure")
                        if copy and portrait and portrait["top"] < copy["bottom"] + 20:
                            errors.append(f"{prefix}: portrait is pulled into the hero copy")
                        gap = metrics.get("portraitToDoctoralGap")
                        if gap is None or not 34 <= gap <= 100:
                            errors.append(f"{prefix}: mobile portrait-to-doctoral transition has unstable blank space ({gap}px)")

                    else:
                        line_limit = 5 if width <= 1100 else 4
                        if not metrics.get("headlineLines") or metrics["headlineLines"] > line_limit:
                            errors.append(f"{prefix}: headline uses too many lines: {metrics.get('headlineLines')}")
                        if not (44 <= metrics.get("headlineFontSize", 0) <= 80):
                            errors.append(f"{prefix}: headline size outside attention-safe range: {metrics.get('headlineFontSize')}px")
                        if metrics.get("headline") and metrics["headline"]["height"] > height * 0.46:
                            errors.append(f"{prefix}: headline occupies too much of the first frame")
                        for key in ("lede", "primaryAction", "portrait", "identity", "status"):
                            box = metrics.get(key)
                            if box and box["bottom"] > height - 4:
                                errors.append(f"{prefix}: {key} falls below the first frame (bottom={box['bottom']:.1f})")
                        if overlaps(metrics.get("copy"), metrics.get("portrait")):
                            errors.append(f"{prefix}: hero copy and portrait overlap")
                        portrait = metrics.get("portrait")
                        hero = metrics.get("hero")
                        if portrait and hero and hero["width"]:
                            hero_share = portrait["width"] / hero["width"]
                            metrics["portraitHeroShare"] = hero_share
                            if not (0.23 <= hero_share <= 0.38):
                                errors.append(f"{prefix}: portrait share of hero composition is unbalanced ({hero_share:.3f})")

                    if not (16 <= metrics.get("ledeFontSize", 0) <= 23):
                        errors.append(f"{prefix}: lede size outside readable range: {metrics.get('ledeFontSize')}px")
                    if metrics.get("ledeFontSize", 0) and metrics.get("ledeLineHeight", 0) < metrics["ledeFontSize"] * 1.45:
                        errors.append(f"{prefix}: lede line height is too tight")
                    if not (metrics.get("currentFocusVisible") and metrics.get("contactActionVisible") and metrics.get("cvVisible")):
                        errors.append(f"{prefix}: hero research focus, contact and CV pathways are incomplete")
                    if metrics.get("highlightCount") != 3:
                        errors.append(f"{prefix}: homepage must present three concise highlighted outputs")
                    if set(metrics.get("highlightDestinations") or []) != {
                        "/publication/mechanochromic-textiles/",
                        "/publication/adhesives-wearable/",
                        "/project/peel-trace-evaluation/",
                    }:
                        errors.append(f"{prefix}: highlighted outputs must resolve to three distinct canonical records")
                    if metrics.get("heroActionCount") != 2:
                        errors.append(f"{prefix}: hero must expose exactly one primary and one secondary action")
                    if transparent(metrics.get("primaryBackground", "")):
                        errors.append(f"{prefix}: primary research action is not visually prominent")
                    if not transparent(metrics.get("secondaryBackground", "")):
                        errors.append(f"{prefix}: secondary CV action is competing with the primary action")

                    if metrics.get("genericPillars") != 0:
                        errors.append(f"{prefix}: homepage must not display repeated generic research method cards")
                    if "Liquid crystals as a model system" not in metrics.get("doctoralHeading", ""):
                        errors.append(f"{prefix}: specific doctoral research heading is missing")
                    work_gap=metrics.get("selectedWorkGap")
                    if work_gap is None or not 20 <= work_gap <= 42:
                        errors.append(f"{prefix}: all-outputs link should be clearly separated from the selected-work cards ({work_gap})")

                    if metrics.get("counterVisible"):
                        errors.append(f"{prefix}: marketing-style proof counter row has returned")
                    # The introductory paragraph must align with the heading, not
                    # float between the kicker and title (the original visual bug).
                    heading_pairs = metrics.get("sectionHeadingPairs", [])
                    if len(heading_pairs) < 4:
                        errors.append(f"{prefix}: missing editorial heading/intro pairs: {heading_pairs}")
                    for pair in heading_pairs:
                        offset = pair["introTop"] - pair["headingTop"]
                        label_gap = pair["headingTop"] - pair["kickerBottom"] if pair["kickerBottom"] is not None else None
                        if label_gap is not None and not 6 <= label_gap <= 30:
                            errors.append(
                                f"{prefix}/{pair['section']}: kicker/title spacing is inconsistent ({label_gap:.1f}px)"
                            )
                        if width >= 981:
                            if pair["columns"] != 2 or abs(offset) > 4:
                                errors.append(
                                    f"{prefix}/{pair['section']}: right intro does not align to the heading "
                                    f"(offset={offset:.1f}px, columns={pair['columns']})"
                                )
                            if pair["kickerBottom"] is not None and pair["introTop"] < pair["kickerBottom"] + 4:
                                errors.append(f"{prefix}/{pair['section']}: introduction intrudes into kicker row")
                        elif not 0 <= pair["introTop"] - pair["headingBottom"] <= 48:
                            errors.append(
                                f"{prefix}/{pair['section']}: stacked introduction has an unstable vertical gap "
                                f"({pair['introTop'] - pair['headingBottom']:.1f}px)"
                            )
                    title_lines = metrics.get("selectedOutputsHeadingLines")
                    if not title_lines or title_lines > 3:
                        errors.append(f"{prefix}: selected outputs headline is overly tall ({title_lines} lines)")
                    if metrics.get("researchPackageCount") != 1 or metrics.get("secondaryOutputCount") != 1:
                        errors.append(f"{prefix}: homepage outputs must stay curated to one flagship research group plus one IP record")
                    if metrics.get("caseStudyFigureCount") != 1 or metrics.get("caseStudyHeading") == "Multi-Criteria Selection of Adhesives for Wearable Textiles":
                        errors.append(f"{prefix}: lower homepage section must interpret one published figure, not repeat the article listing")
                    if not {
                        "/publication/masters-thesis/",
                        "/project/peel-trace-evaluation/",
                    }.issubset(set(metrics.get("caseStudyLinks") or [])):
                        errors.append(f"{prefix}: case study lost its thesis and methods provenance")
                    followup = metrics.get("researchFollowup") or {}
                    if not followup.get("exists") or set(followup.get("linkDestinations") or []) != {
                        "/research/#open-research-questions",
                        "/research-statement/",
                    }:
                        errors.append(f"{prefix}: doctoral detail must be linked instead of repeated: {followup}")
                    gap = followup.get("gap")
                    if gap is None or not 16 <= gap <= 100:
                        errors.append(f"{prefix}: research links are visually disconnected from the methods overview: {gap}")
                    if followup.get("duplicateQuestionCount") or followup.get("duplicateDiagramCount"):
                        errors.append(f"{prefix}: duplicate detailed questions or five-stage research diagram reappeared")
                    disclosures = metrics.get("disclosures", [])
                    if len(disclosures) != 1:
                        errors.append(f"{prefix}: only the engagement evidence should remain disclosed: {disclosures}")
                    else:
                        disclosure = disclosures[0]
                        if disclosure["open"] or disclosure["bodyVisible"] or disclosure["summaryHeight"] < 44 or disclosure["evidenceCount"] < 4:
                            errors.append(f"{prefix}: engagement must remain accessible and collapsed by default: {disclosure}")
                    expanded = cdp.evaluate("""(() => {
                      const item=document.querySelector('main details.home-disclosure--engagement');
                      if (!item) return {present:false};
                      item.open=true;
                      return {
                        present:true,
                        bodyVisible:!!item.querySelector('.home-disclosure__body')?.getClientRects().length,
                        overflow:document.documentElement.scrollWidth > innerWidth+2,
                        records:item.querySelectorAll('.compact-record').length,
                        summaryHeight:item.querySelector(':scope > summary')?.getBoundingClientRect().height || 0,
                      };
                    })()""")
                    if not expanded.get("present") or not expanded.get("bodyVisible") or expanded.get("overflow") or expanded.get("records", 0) < 4:
                        errors.append(f"{prefix}: expanded engagement evidence must remain fully readable: {expanded}")
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
    print("Homepage attention hierarchy passed across mobile, WCAG reflow, laptop, and desktop frames: the hero does not collapse, research-card spacing remains intrinsic, and selected evidence stays prioritized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
