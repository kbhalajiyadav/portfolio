#!/usr/bin/env python3
"""Browser-level responsive, zoom-equivalent, reduced-motion, menu, footer, and TOC audit."""
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
    (414, 896, "414-iphone-viewport"),
    (680, 900, "680-small"),
    (768, 900, "768-tablet"),
    (980, 900, "980-laptop-boundary"),
    (1180, 900, "1180-desktop-boundary"),
    (1440, 1000, "1440-desktop"),
    (1725, 1000, "1725-wide-hero"),
    (1920, 1080, "1920-wide"),
    (720, 500, "200-percent-zoom-equivalent"),
]
PAGES = [
    ("", "home"),
    ("about/", "about"),
    ("research/", "research"),
    ("research-statement/", "research-statement"),
    ("outputs/", "outputs"),
    ("experience/", "experience"),
    ("engagement/", "engagement"),
    ("contact/", "contact"),
    ("publication/adhesives-wearable/", "publication"),
    ("publication/electrospun-fiber-mats/", "publication-fiber-mats"),
    ("project/peel-trace-evaluation/", "project"),
    ("project/optical-metrology/", "optical-metrology"),
]
EVIDENCE_PAGES = {"home", "about", "research", "outputs", "experience", "engagement", "contact"}
EVIDENCE_VIEWPORTS = {"390-mobile", "1440-desktop"}


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
  const footerItems = [...document.querySelectorAll('.site-footer nav > a, .site-footer nav > button')]
    .filter((element) => {
      const style = getComputedStyle(element);
      return style.display !== 'none' && style.visibility !== 'hidden';
    });
  const footerTops = footerItems.map((element) => element.getBoundingClientRect().top);
  const footerRowSpread = footerTops.length ? Math.max(...footerTops) - Math.min(...footerTops) : null;
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('#site-nav');
  const toc = document.querySelector('.toc-disclosure[data-responsive-toc]');
  const researchFigures = [...document.querySelectorAll('.research-figure')].map((figure) => {
    const media = figure.querySelector('.research-figure__media');
    const open = figure.querySelector('.research-figure__open');
    const mediaStyle = media ? getComputedStyle(media) : null;
    const openStyle = open ? getComputedStyle(open) : null;
    return {
      mediaBorders: mediaStyle
        ? [mediaStyle.borderTopWidth, mediaStyle.borderRightWidth, mediaStyle.borderBottomWidth, mediaStyle.borderLeftWidth]
        : null,
      separatorWidth: getComputedStyle(figure).borderTopWidth,
      openBorders: openStyle
        ? [openStyle.borderTopWidth, openStyle.borderRightWidth, openStyle.borderBottomWidth, openStyle.borderLeftWidth]
        : null,
      openBackground: openStyle ? openStyle.backgroundColor : null,
      visibleFullSizeLink: Boolean(open && open.textContent.includes('View full-resolution figure')),
    };
  });
  const seriesPairs = [...document.querySelectorAll('.series-grid')]
    .filter((grid) => grid.querySelectorAll(':scope > .series').length === 2)
    .map((grid) => {
      const cards = [...grid.querySelectorAll(':scope > .series')];
      return {
        columnCount: getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length,
        cardTopDifference: Math.abs(cards[0].getBoundingClientRect().top - cards[1].getBoundingClientRect().top),
        bothClosed: cards.every(card => !card.open),
        cardHeightDifference: Math.abs(cards[0].getBoundingClientRect().height - cards[1].getBoundingClientRect().height)
      };
    });
  const contactHeader = document.querySelector('.contact-page .page-header');
  const contactHeading = document.querySelector('.contact-section--page h2');
  const contactIntroGap = contactHeader && contactHeading
    ? contactHeading.getBoundingClientRect().top - contactHeader.getBoundingClientRect().bottom
    : null;
  const homepageShell = document.querySelector('.hero')?.getBoundingClientRect().width ?? null;
  const outputPackage = document.querySelector('.research-package');
  const outputFigure = outputPackage?.querySelector('.research-figure--featured');
  const outputMedia = outputFigure?.querySelector('.research-figure__media');
  const outputCaption = outputFigure?.querySelector('figcaption');
  const outputGrid = outputPackage?.querySelector('.package-artifacts');
  const journalLink = outputPackage?.querySelector('.package-lead > .actions a[target="_blank"]');
  const captionLinkLabels = outputCaption
    ? [...outputCaption.querySelectorAll('.actions a')].map(link => link.textContent.trim())
    : [];
  const patentRecord = document.querySelector('#outputs > .secondary-output');
  const browseOutputs = document.querySelector('#outputs > .actions');
  const outputRecords = [...document.querySelectorAll('.package-artifacts > article')];
  const outputLayout = outputPackage && outputFigure && outputMedia && outputCaption
    && outputGrid && patentRecord && browseOutputs && outputRecords.length === 2
    ? (() => {
        const figureMedia = outputMedia.getBoundingClientRect();
        const figureCaption = outputCaption.getBoundingClientRect();
        const figureBox = outputFigure.getBoundingClientRect();
        const gridBox = outputGrid.getBoundingClientRect();
        const patentBox = patentRecord.getBoundingClientRect();
        const browseBox = browseOutputs.getBoundingClientRect();
        const first = outputRecords[0].getBoundingClientRect();
        const second = outputRecords[1].getBoundingClientRect();
        const contentBottom = Math.max(first.bottom, second.bottom);
        return {
          outerBorder: getComputedStyle(outputPackage).borderTopWidth,
          packageDisplay: getComputedStyle(outputPackage).display,
          figureDisplay: getComputedStyle(outputFigure).display,
          figureColumns: getComputedStyle(outputFigure).gridTemplateColumns.split(/\s+/).filter(Boolean).length,
          figureRowOffset: Math.abs(figureMedia.top - figureCaption.top),
          figureWidths: [figureMedia.width, figureCaption.width],
          figureRelativePosition: figureMedia.left - figureCaption.right,
          fullSizeInCaption: Boolean(outputCaption.querySelector('.research-figure__open[href]')),
          fullSizeUnderMedia: Boolean(outputMedia.querySelector('.research-figure__open')),
          recordDisplay: getComputedStyle(outputGrid).display,
          recordColumns: getComputedStyle(outputGrid).gridTemplateColumns.split(/\s+/).filter(Boolean).length,
          recordRows: getComputedStyle(outputGrid).gridTemplateRows.split(/\s+/).filter(Boolean).length,
          recordTopOffset: Math.abs(first.top - second.top),
          recordVerticalGap: Math.round(second.top - first.bottom),
          recordHeights: [first.height, second.height],
          unusedGridHeight: Math.max(0, gridBox.bottom - contentBottom),
          contentToPatentGap: Math.round(patentBox.top - contentBottom),
          gridToPatentGap: Math.round(patentBox.top - gridBox.bottom),
          figureToRecordsGap: Math.round(gridBox.top - figureBox.bottom),
          patentToBrowseGap: Math.round(browseBox.top - patentBox.bottom),
          journalArticleLinks: journalLink
            ? [...outputPackage.querySelectorAll('a[href]')].filter(link => link.href === journalLink.href).length
            : 0,
          captionDatasetLink: captionLinkLabels.some(label => label.includes('Dataset')),
          captionCodeLink: captionLinkLabels.some(label => label.includes('Source code')),
          captionLicenseLink: Boolean(outputCaption.querySelector('a[rel~="license"]'))
        };
      })()
    : null;
  const borderEdges = element => {
    if (!element) return null;
    const style = getComputedStyle(element);
    return ['borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth']
      .map(key => parseFloat(style[key]) || 0);
  };
  const aboutMethods = document.querySelector('.about-method-grid');
  const aboutMethodBorders = aboutMethods ? {
    grid: borderEdges(aboutMethods),
    cards: [...aboutMethods.querySelectorAll(':scope > article')].map(borderEdges),
    gap:parseFloat(getComputedStyle(aboutMethods).rowGap) || 0,
  } : null;
  const filter = document.querySelector('.output-filter');
  const list = document.querySelector('.output-list');
  const outputFilterRules = filter && list
    ? {filterBottom:borderEdges(filter)[2], listTop:borderEdges(list)[0]}
    : null;
  const schematic = document.querySelector('.method-schematic');
  const schematicBorders = schematic
    ? [getComputedStyle(schematic).borderTopWidth, getComputedStyle(schematic).borderBottomWidth]
    : null;
  return {
    url: location.href,
    viewportWidth: width,
    scrollWidth: Math.max(root.scrollWidth, body.scrollWidth),
    horizontalOverflow: Math.max(root.scrollWidth, body.scrollWidth) > width + 2,
    overflowNodes,
    arrowIssues,
    footerItemCount: footerItems.length,
    footerRowSpread,
    menuDisplay: menu ? getComputedStyle(menu).display : null,
    navDisplay: nav ? getComputedStyle(nav).display : null,
    tocOpen: toc ? toc.open : null,
    researchFigures,
    seriesPairs,
    contactIntroGap,
    outputLayout,
    homepageShell,
    aboutMethodBorders,
    headerSurface:(() => {
      const header = document.querySelector('.site-head');
      return header ? getComputedStyle(header).backgroundColor : null;
    })(),
    heroTypography:(() => {
      const title = document.querySelector('.hero h1');
      if (!title) return null;
      const style = getComputedStyle(title);
      const rect=title.getBoundingClientRect();
      const copy=title.closest('.hero__copy');
      return {
        fontSize:parseFloat(style.fontSize),
        lineHeight:parseFloat(style.lineHeight),
        letterSpacing:parseFloat(style.letterSpacing),
        renderedLines:rect.height/parseFloat(style.lineHeight),
        titleWidth:rect.width,
        copyWidth:copy?.getBoundingClientRect().width ?? null,
        measuredLedeWidth:document.querySelector('.hero .lede')?.getBoundingClientRect().width ?? null
      };
    })(),
    homeExperience:(() => {
      const section=document.querySelector('#experience');
      if(!section) return null;
      const block=section.querySelector('.home-experience');
      const disclosure=block?.querySelector('details[data-responsive-experience]');
      const summary=disclosure?.querySelector(':scope > summary');
      const actions=block?.querySelector(':scope > .actions a[href="/experience/"]');
      const styles=summary ? getComputedStyle(summary) : null;
      return {
        blockCount:section.querySelectorAll('.home-experience').length,
        disclosureCount:section.querySelectorAll('details[data-responsive-experience]').length,
        timelineCount:section.querySelectorAll('.timeline').length,
        educationPanelCount:section.querySelectorAll('.education-panel').length,
        open:!!disclosure?.open,
        summaryVisible:!!summary && styles?.display !== 'none' && summary.getBoundingClientRect().height >= 44,
        summaryHidden:!!summary && styles?.display === 'none',
        directLinkVisible:!!actions && actions.getClientRects().length > 0,
        educationCount:section.querySelectorAll('.education-panel article').length,
        roleCount:section.querySelectorAll('.timeline-item').length,
      };
    })(),
    counterPresent:!!document.querySelector('.metrics'),
    softwareReference:(() => {
      const figure=document.querySelector('.software-evidence');
      if(!figure) return null;
      const image=figure.querySelector('img');
      return {hasAlt:!!image?.alt, lazy:image?.loading==='lazy', width:image?.getAttribute('width'), height:image?.getAttribute('height'),
        citation:!!figure.querySelector('figcaption a[href*="Peel-Trace-Evaluation"]'), caption:figure.querySelector('figcaption')?.textContent||''};
    })(),
    homeResearchDiagramGap:(() => {
      const section = document.querySelector('#research');
      const introduction = section?.querySelector(':scope > .section-head > p:not(.kicker)');
      const first = section?.querySelector(':scope > .research-signature .research-signature__flow > li:first-child');
      if (!introduction || !first) return null;
      return {
        introductionBottom:introduction.getBoundingClientRect().bottom,
        firstStageTop:first.getBoundingClientRect().top,
        gap:first.getBoundingClientRect().top - introduction.getBoundingClientRect().bottom
      };
    })(),
    scholarlyInlineArrows:[...document.querySelectorAll('.article-content p .content-link__arrow, .article-content li .content-link__arrow')]
      .filter(el => getComputedStyle(el).display !== 'none').length,
    researchDiagramGap:(() => {
      const figure = document.querySelector('.research-signature');
      const before = figure?.previousElementSibling;
      const stages = figure?.querySelector('.research-signature__flow');
      const first = stages?.querySelector('li');
      if (!figure || !before || !first) return null;
      return {previousTag:before.tagName,gap:first.getBoundingClientRect().top - before.getBoundingClientRect().bottom};
    })(),
    aboutTimeline:(() => {
      const timeline = document.querySelector('.about-path');
      if (!timeline) return null;
      const milestones = [...timeline.querySelectorAll(':scope > article')];
      const css = getComputedStyle(timeline);
      return {
        count:milestones.length,
        outerRules:[css.borderTopWidth, css.borderBottomWidth].map(parseFloat),
        rowRules:milestones.map(item => {
          const computed = getComputedStyle(item);
          return [computed.borderTopWidth, computed.borderBottomWidth].map(parseFloat);
        }),
        lengths:milestones.map(item => item.querySelector('.about-path__content')?.textContent.trim().split(/\s+/).length || 0),
        milestoneLinks:milestones.map(item => [...item.querySelectorAll('a[href]')].map(link => link.getAttribute('href'))),
        headingGaps:milestones.map(item => {
          const title = item.querySelector('.about-path__content h3');
          const body = item.querySelector('.about-path__content p');
          return title && body ? body.getBoundingClientRect().top - title.getBoundingClientRect().bottom : null;
        }),
        headingLeading:milestones.map(item => {
          const title = item.querySelector('.about-path__content h3');
          if (!title) return 0;
          const style = getComputedStyle(title);
          return parseFloat(style.lineHeight) / parseFloat(style.fontSize);
        }),
        visibleInlineArrows:[...timeline.querySelectorAll('.about-path__content .content-link__arrow')].filter(item => getComputedStyle(item).display !== 'none').length,
        periods:milestones.map(item => item.querySelector('.about-path__period')?.textContent.trim() || ''),
      };
    })(),
    editorialPairs:[...document.querySelectorAll('main .section-head')]
      .filter(section => section.querySelector(':scope > h2') && section.querySelector(':scope > p:not(.kicker)'))
      .map(section => {
        const title = section.querySelector(':scope > h2').getBoundingClientRect();
        const prose = section.querySelector(':scope > p:not(.kicker)').getBoundingClientRect();
        const label = section.querySelector(':scope > .kicker')?.getBoundingClientRect();
        return {
          id:section.closest('[id]')?.id || 'unnamed',
          titleTop:title.top,titleBottom:title.bottom,proseTop:prose.top,
          labelBottom:label?.bottom ?? null,
          columns:getComputedStyle(section).gridTemplateColumns.split(/\s+/).filter(Boolean).length
        };
      }),
    aboutIntroPairs:[...document.querySelectorAll('.about-section__intro')]
      .map(section => {
        const title = section.querySelector('.about-section__intro > h2')?.getBoundingClientRect();
        const prose = section.querySelector('.about-section__summary p')?.getBoundingClientRect();
        return title && prose ? {
          id:section.closest('[id]')?.id || 'unnamed',
          titleTop:title.top,titleBottom:title.bottom,proseTop:prose.top,
          columnCount:getComputedStyle(section).gridTemplateColumns.split(/\s+/).filter(Boolean).length
        } : null;
      }).filter(Boolean),
    outputFilterRules,
    schematicBorders,
    diagramReadability:(() => {
      const diagram = document.querySelector('.research-signature, .method-schematic');
      if (!diagram) return null;
      const shown = diagram.querySelector('ol');
      const labels = [...(shown?.querySelectorAll('li strong') || [])];
      const visibleRows = [...(shown?.querySelectorAll('li') || [])];
      const responsiveColumns = shown ? getComputedStyle(shown).gridTemplateColumns.trim().split(/\s+/).filter(Boolean).length : 0;
      const hasHorizontalRule = element => {
        if (!element) return false;
        const style = getComputedStyle(element);
        return parseFloat(style.borderTopWidth) > 0 || parseFloat(style.borderBottomWidth) > 0;
      };
      return {
        count:labels.length,
        listCount:diagram.querySelectorAll('ol').length,
        isResearchSignature:diagram.classList.contains('research-signature'),
        stageGeometry:visibleRows.map(item => {
          const r = item.getBoundingClientRect();
          return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width};
        }),
        stageTextOverflow:labels.some((label,index) => {
          const labelRect=label.getBoundingClientRect();
          const itemRect=visibleRows[index]?.getBoundingClientRect();
          const indexRect=visibleRows[index]?.querySelector('.research-signature__index')?.getBoundingClientRect();
          return !itemRect || labelRect.right>itemRect.right+1 ||
            (indexRect && labelRect.left<indexRect.right+4);
        }),
        stageCollisions:visibleRows.some((item,i) => {
          const a=item.getBoundingClientRect();
          return visibleRows.slice(i+1).some(next => {
            const b=next.getBoundingClientRect();
            return Math.min(a.right,b.right)>Math.max(a.left,b.left)+1 &&
              Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)+1;
          });
        }),
        minFontSize:labels.length ? Math.min(...labels.map(el => parseFloat(getComputedStyle(el).fontSize))) : 0,
        overflowing:labels.some(el => el.getBoundingClientRect().right > width + 1),
        mobileDisplayed:responsiveColumns === 1,
        hasExtraRules:[diagram, shown, ...visibleRows].some(hasHorizontalRule),
        internalDisclaimer:diagram.textContent.includes('Schematic; no quantitative data are implied.')
      };
    })(),
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
    with tempfile.TemporaryDirectory(prefix="portfolio-chrome-", ignore_cleanup_errors=True) as profile:
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
                        if page_name in {"home", "engagement"}:
                            expected_columns = 2 if width >= 981 else 1
                            for pair in layout["seriesPairs"]:
                                if pair["columnCount"] != expected_columns:
                                    record_errors.append(f"two presentation groups should use {expected_columns} column(s), not {pair['columnCount']}")
                                if width >= 981 and pair["cardTopDifference"] > 2:
                                    record_errors.append("paired presentation groups do not share a desktop row")
                                if width >= 981 and pair["bothClosed"] and pair["cardHeightDifference"] > 2:
                                    record_errors.append(
                                        f"two collapsed presentation cards have uneven bottom edges ({pair['cardHeightDifference']:.1f}px)"
                                    )
                        if page_name == "home":
                            if layout.get("counterPresent"):
                                record_errors.append("homepage numerical counter row should be removed")
                            exp=layout.get("homeExperience")
                            if not exp:
                                record_errors.append("home Experience responsive composition missing")
                            else:
                                if any(exp[key] != 1 for key in ("blockCount", "disclosureCount", "timelineCount", "educationPanelCount")):
                                    record_errors.append(f"Experience records must appear only once in HTML: {exp}")
                                if not exp["directLinkVisible"] or exp["educationCount"] < 2 or exp["roleCount"] < 2:
                                    record_errors.append(f"Experience evidence or always-visible full-page link missing: {exp}")
                                if width <= 820:
                                    if exp["open"] or not exp["summaryVisible"]:
                                        record_errors.append(f"mobile Experience must be collapsed with accessible summary: {exp}")
                                elif not exp["open"] or not exp["summaryHidden"]:
                                    record_errors.append(f"desktop Experience must be expanded without redundant summary: {exp}")
                            shell = layout.get("homepageShell")
                            if width >= 1900 and (shell is None or not 1450 <= shell <= 1580):
                                record_errors.append(f"large-monitor content shell must be wide but editorially bounded: {shell}")
                            if layout.get("diagramReadability") is not None:
                                record_errors.append("homepage repeats the five-stage diagram already on the Research page")
                            output = layout["outputLayout"]
                            if output is None:
                                record_errors.append("featured research package is missing its attributed figure or related records")
                            else:
                                if output["outerBorder"] != "0px" or output["packageDisplay"] != "block":
                                    record_errors.append("featured research should be an unboxed full-width editorial feature")
                                if output["figureDisplay"] != "grid":
                                    record_errors.append("featured figure and interpretation lost their grid layout")
                                expected_figure_columns = 2 if width > 820 else 1
                                if output["figureColumns"] != expected_figure_columns:
                                    record_errors.append(f"feature should use {expected_figure_columns} plot/caption column(s), not {output['figureColumns']}")
                                if expected_figure_columns == 2 and output["figureRowOffset"] > 2:
                                    record_errors.append("plot and interpretation are not aligned in the same row")
                                if width > 820 and output["figureRelativePosition"] < 0:
                                    record_errors.append("desktop featured plot must appear right of the research interpretation")
                                if not output["fullSizeInCaption"] or output["fullSizeUnderMedia"]:
                                    record_errors.append("featured full-size action must be grouped with figure attribution and data/code links")
                                if min(output["figureWidths"]) < 160:
                                    record_errors.append(f"featured plot/caption column is too narrow: {output['figureWidths']}")
                                if output["recordDisplay"] != "grid":
                                    record_errors.append("thesis and software should share a related-outputs grid")
                                expected_record_columns = 1 if width <= 680 else 2
                                if output["recordColumns"] != expected_record_columns:
                                    record_errors.append(f"related outputs should use {expected_record_columns} column(s), not {output['recordColumns']}")
                                if expected_record_columns == 2 and output["recordTopOffset"] > 2:
                                    record_errors.append("thesis and software entries are not aligned on the same row")
                                if expected_record_columns == 1 and not 12 <= output["recordVerticalGap"] <= 70:
                                    record_errors.append(f"stacked related outputs have an unnatural gap: {output['recordVerticalGap']}px")
                                if max(output["recordHeights"]) > 340:
                                    record_errors.append(f"related output is stretched into an oversized card: {output['recordHeights']}")
                                # A two-column grid with two records must not retain a second
                                # empty row. Previous checks saw aligned cards but missed >200px
                                # of blank grid track between the software and patent entries.
                                expected_record_rows = 2 if width <= 680 else 1
                                if output["recordRows"] != expected_record_rows:
                                    record_errors.append(
                                        f"related-output grid has {output['recordRows']} row(s); expected {expected_record_rows} "
                                        "(unused tracks create unexplained whitespace)"
                                    )
                                if output["unusedGridHeight"] > 24:
                                    record_errors.append(
                                        f"related-output grid reserves {output['unusedGridHeight']:.1f}px below its actual content"
                                    )
                                if not 24 <= output["contentToPatentGap"] <= 72:
                                    record_errors.append(
                                        f"unexpected blank gap between thesis/software content and patent record: "
                                        f"{output['contentToPatentGap']}px"
                                    )
                                if not 24 <= output["gridToPatentGap"] <= 72:
                                    record_errors.append(
                                        f"grid-to-patent section spacing is outside editorial rhythm: "
                                        f"{output['gridToPatentGap']}px"
                                    )
                                if not 20 <= output["figureToRecordsGap"] <= 150:
                                    record_errors.append(
                                        f"figure-to-related-outputs gap is inconsistent: "
                                        f"{output['figureToRecordsGap']}px"
                                    )
                                if not 8 <= output["patentToBrowseGap"] <= 96:
                                    record_errors.append(
                                        f"patent-to-output-index link gap is inconsistent: "
                                        f"{output['patentToBrowseGap']}px"
                                    )
                                if output["journalArticleLinks"] != 1:
                                    record_errors.append(
                                        f"featured publication must have one journal DOI action, not "
                                        f"{output['journalArticleLinks']} duplicates"
                                    )
                                if not (output["captionDatasetLink"] and output["captionCodeLink"] and output["captionLicenseLink"]):
                                    record_errors.append(
                                        "featured figure must retain dataset, source code, and license links"
                                    )
                        if page_name in {"home", "experience", "engagement"}:
                            pairs = layout.get("editorialPairs", [])
                            minimum = 4 if page_name == "home" else 1
                            if len(pairs) < minimum:
                                record_errors.append(f"missing shared heading/intro pairs: {pairs}")
                            for pair in pairs:
                                if width >= 981:
                                    if pair["columns"] != 2 or abs(pair["proseTop"] - pair["titleTop"]) > 4:
                                        record_errors.append(f"{pair['id']}: introduction/title desktop misalignment: {pair}")
                                elif pair["columns"] != 1 or not 0 <= pair["proseTop"] - pair["titleBottom"] <= 48:
                                    record_errors.append(f"{pair['id']}: stacked heading/intro spacing is unstable: {pair}")
                        if page_name in {"home", "about", "research"}:
                            header_surface = layout.get("headerSurface")
                            if not header_surface or header_surface in {"transparent", "rgba(0, 0, 0, 0)"} or (
                                header_surface.startswith("rgba(") and float(header_surface.rstrip(")").split(",")[-1]) < 1
                            ):
                                record_errors.append(f"sticky header must be opaque to prevent text ghosting: {header_surface}")
                        if page_name == "home" and layout.get("homeResearchDiagramGap") is not None:
                            record_errors.append("homepage duplicates the Research page's five-stage diagram")
                        if page_name == "research":
                            workflow = layout.get("diagramReadability")
                            if not workflow or not workflow.get("isResearchSignature") or len(workflow.get("stageGeometry", [])) != 5:
                                record_errors.append("Research page's five-stage processing sequence is missing")
                            else:
                                steps=workflow["stageGeometry"]
                                if workflow.get("stageTextOverflow") or workflow.get("stageCollisions"):
                                    record_errors.append(f"research stages or labels overlap within the article column: {workflow}")
                                if any(steps[i+1]["top"] < steps[i]["top"] - 2 for i in range(4)):
                                    record_errors.append(f"research stage reading order is not preserved: {steps}")
                                rows={}
                                for step in steps:
                                    key=round(step["top"]/5)*5
                                    rows.setdefault(key,[]).append(step)
                                for stage_row in rows.values():
                                    if any(stage_row[i]["left"] >= stage_row[i+1]["left"] for i in range(len(stage_row)-1)):
                                        record_errors.append(f"research stage order must read left-to-right within each row: {steps}")
                        if page_name == "research" and layout.get("scholarlyInlineArrows"):
                            record_errors.append("scholarly prose has redundant directional arrows after inline links")
                        if page_name == "home" and width >= 1680:
                            heading = layout.get("heroTypography")
                            if not heading or not 1.8 <= heading["renderedLines"] <= 2.2 or heading["copyWidth"] < 880:
                                record_errors.append(f"wide desktop hero must have a readable two-line headline without a cramped text column: {heading}")
                            elif heading["measuredLedeWidth"] is not None and heading["measuredLedeWidth"] > 680:
                                record_errors.append(f"wide desktop hero paragraph is too long to read comfortably: {heading}")
                        if page_name == "home" and width <= 680:
                            heading = layout.get("heroTypography")
                            if not heading or not 1.08 <= heading["lineHeight"] / heading["fontSize"] <= 1.28 or heading["letterSpacing"] < -0.023 * heading["fontSize"]:
                                record_errors.append(f"mobile hero title needs readable leading and uncramped tracking: {heading}")
                        if page_name == "research" and width <= 820:
                            diagram_gap = layout.get("researchDiagramGap")
                            if not diagram_gap or diagram_gap["previousTag"] != "P" or not 8 <= diagram_gap["gap"] <= 75:
                                record_errors.append(f"research explanation and first diagram stage are visually disconnected: {diagram_gap}")
                        if page_name == "about":
                            timeline = layout.get("aboutTimeline")
                            if not timeline or timeline["count"] != 4:
                                record_errors.append(f"About chronology must have four dated entries: {timeline}")
                            elif timeline["periods"] != ["2018–2022", "2022–2024", "2024–2026", "2026–present"]:
                                record_errors.append(f"About chronology order differs from canonical source: {timeline['periods']}")
                            if timeline:
                                if any(value > 0 for value in timeline["outerRules"] + [
                                    edge for row in timeline["rowRules"] for edge in row
                                ]):
                                    record_errors.append(f"About chronology has redundant horizontal row separators: {timeline}")
                                link_set = set(timeline["milestoneLinks"][2]) if len(timeline["milestoneLinks"]) >= 3 else set()
                                required = {
                                    "/publication/adhesives-wearable/",
                                    "https://scholarscompass.vcu.edu/etd/8456/",
                                    "/project/peel-trace-evaluation/",
                                }
                                if not required.issubset(link_set):
                                    record_errors.append(f"About M.S. milestone lacks evidence links: {sorted(required - link_set)}")
                                if timeline["visibleInlineArrows"]:
                                    record_errors.append("About chronology has directional arrows inside sentences")
                                if any(gap is None or not 8 <= gap <= 30 for gap in timeline["headingGaps"]) or min(timeline["headingLeading"]) < 1.19:
                                    record_errors.append(f"About chronology headings and paragraphs are crowded: {timeline['headingGaps']}")
                            pairs = layout.get("aboutIntroPairs", [])
                            if len(pairs) < 5:
                                record_errors.append(f"About editorial headings/introductions are missing: {pairs}")
                            for pair in pairs:
                                if width >= 981:
                                    if pair["columnCount"] != 2 or abs(pair["proseTop"] - pair["titleTop"]) > 4:
                                        record_errors.append(
                                            f"About/{pair['id']} summary does not align with the heading: {pair}"
                                        )
                                elif pair["columnCount"] != 1 or not 0 <= pair["proseTop"] - pair["titleBottom"] <= 56:
                                    record_errors.append(f"About/{pair['id']} stacked heading/summary gap is unstable: {pair}")
                            methods = layout.get("aboutMethodBorders")
                            if not methods or len(methods.get("cards", [])) != 3:
                                record_errors.append("About method columns are missing")
                            elif any(value > 0 for edges in [methods["grid"], *methods["cards"]] for value in edges) or methods["gap"] < 20:
                                record_errors.append(f"About methods regained table-cell borders or lost spacing: {methods}")
                        if page_name == "outputs":
                            junction = layout.get("outputFilterRules")
                            if not junction or not (0 < junction["filterBottom"] <= 2) or junction["listTop"] > 0:
                                record_errors.append(f"Outputs filter/list junction has duplicated or missing rule: {junction}")
                        if page_name == "contact":
                            contact_gap = layout["contactIntroGap"]
                            if contact_gap is None or not 16 <= contact_gap <= 90:
                                record_errors.append(f"contact introduction gap is inconsistent: {contact_gap}")

                        if page_name == "project":
                            reference = layout.get("softwareReference")
                            if not reference or not reference["hasAlt"] or not reference["lazy"] or not reference["citation"] or reference["width"] != "3993" or reference["height"] != "1350" or "not a result from the published wearable-textile experiment" not in reference["caption"]:
                                record_errors.append(f"Peel Trace reference figure is absent, uncredited, unoptimized or misleading: {reference}")
                        if page_name in {"home", "publication", "publication-fiber-mats"} and not layout["researchFigures"]:
                            record_errors.append("expected source-attributed research figures")
                        for index, figure in enumerate(layout["researchFigures"]):
                            if figure["mediaBorders"] is None or any(v != "0px" for v in figure["mediaBorders"]):
                                record_errors.append(f"research figure {index + 1} has a card-style image border")
                            if figure["separatorWidth"] != "0px":
                                record_errors.append(f"research figure {index + 1} has a decorative separator rule")
                            if figure["openBorders"] is None or any(v != "0px" for v in figure["openBorders"]):
                                record_errors.append(f"research figure {index + 1} has a boxed full-size link")
                            if figure["openBackground"] not in {"rgba(0, 0, 0, 0)", "transparent"}:
                                record_errors.append(f"research figure {index + 1} has a shaded full-size link")
                            if not figure["visibleFullSizeLink"]:
                                record_errors.append(f"research figure {index + 1} lacks a visible full-size link")
                        if layout["schematicBorders"] is not None and any(v != "0px" for v in layout["schematicBorders"]):
                            record_errors.append("explanatory method schematic has decorative outer borders")
                        if page_name in {"research", "project", "optical-metrology"}:
                            diagram = layout.get("diagramReadability")
                            expected_steps = 5 if page_name != "project" else 6
                            if not diagram or diagram["listCount"] != 1 or diagram["count"] != expected_steps or diagram["minFontSize"] < 14 or diagram["overflowing"]:
                                record_errors.append(f"scientific workflow labels must remain readable at {width}px: {diagram}")
                            if diagram and diagram["mobileDisplayed"] != (width <= 820):
                                record_errors.append(f"scientific workflow must reflow at 820px: {diagram}")
                            if diagram and (diagram["hasExtraRules"] or diagram["internalDisclaimer"]):
                                record_errors.append(f"scientific workflow has redundant rules or internal caption: {diagram}")
                        if page_name == "home" and width >= 981:
                            if layout["footerItemCount"] < 2:
                                record_errors.append("desktop footer navigation items are missing")
                            elif layout["footerRowSpread"] is None or layout["footerRowSpread"] > 3:
                                record_errors.append(f"desktop footer navigation wrapped or lost baseline alignment: row spread={layout['footerRowSpread']}px")
                        if page_name == "home" and label in EVIDENCE_VIEWPORTS:
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

                        if page_name in EVIDENCE_PAGES and label in EVIDENCE_VIEWPORTS:
                            image = cdp.command("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                            (screenshots / f"{label}-{page_name}.png").write_bytes(base64.b64decode(image["data"]))

                cdp.command("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False})
                cdp.command("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
                cdp.command("Page.navigate", {"url": base_url})
                wait_ready(cdp, base_url)
                reduced = cdp.evaluate("({scroll:getComputedStyle(document.documentElement).scrollBehavior, transition:getComputedStyle(document.querySelector('.lnk .arw')).transitionDuration})")
                if reduced["scroll"] != "auto" or reduced["transition"] not in {"0s", "0ms"}:
                    errors.append(f"reduced-motion preference not fully honored: {reduced}")

                report_path.write_text(json.dumps({"results": results, "reducedMotion": reduced, "errors": errors}, indent=2) + "\n")
                if errors:
                    print("\n".join(f"ERROR: {error}" for error in errors))
                    return 1
                print(f"Responsive browser audit passed: {len(results)} page/viewport combinations plus reduced-motion, menu, footer, and TOC checks; desktop/mobile evidence captured for all seven primary destinations.")
                return 0
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
