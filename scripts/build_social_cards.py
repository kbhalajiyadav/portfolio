#!/usr/bin/env python3
"""Generate deterministic 1200x630 branded social-preview PNGs."""
from __future__ import annotations

from html import escape
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "social"

CARDS = {
    "portfolio": {
        "kicker": "RESEARCH PORTFOLIO",
        "lines": (
            "Making material response",
            "measurable and",
            "interpretable.",
        ),
        "subtitle": "Soft matter · Rheology · Quantitative imaging",
        "motif": "trace",
        "size": 56,
    },
    "research": {
        "kicker": "RESEARCH PROGRAM",
        "lines": (
            "Stimulus → structure →",
            "response → measurement →",
            "translation",
        ),
        "subtitle": "Soft materials · liquid crystals · rheology · neutron scattering",
        "motif": "rings",
        "size": 58,
    },
    "outputs": {
        "kicker": "RESEARCH OUTPUTS",
        "lines": (
            "Publications, software,",
            "and intellectual property",
        ),
        "subtitle": "Evidence linked to methods, records, and reproducible workflows",
        "motif": "grid",
        "size": 62,
    },
    "experience": {
        "kicker": "EXPERIENCE & EDUCATION",
        "lines": (
            "Research and engineering",
            "across materials, data,",
            "and regulated systems",
        ),
        "subtitle": "Scientific training · industry practice · reproducible technical work",
        "motif": "trace",
        "size": 56,
    },
    "engagement": {
        "kicker": "ENGAGEMENT",
        "lines": (
            "Research communicated,",
            "taught, reviewed, and",
            "translated beyond the lab",
        ),
        "subtitle": "Presentations · teaching · service · professional engagement",
        "motif": "rings",
        "size": 56,
    },
    "publication": {
        "kicker": "PEER-REVIEWED RESEARCH",
        "lines": (
            "Wearable-textile adhesion",
            "measured beyond a single",
            "maximum-force value",
        ),
        "subtitle": "Multi-criteria selection · mechanics-consistent analysis · reproducibility",
        "motif": "trace",
        "size": 56,
    },
    "technology": {
        "kicker": "PATENT-PENDING TECHNOLOGY",
        "lines": (
            "Quantitative Thermal",
            "Imaging",
        ),
        "subtitle": "Visible-light, camera-based interpretation of thermochromic materials",
        "motif": "grid",
        "size": 68,
    },
}


def motif_svg(kind: str) -> str:
    if kind == "rings":
        return """
        <g opacity=".34" stroke="#0e5a5e" fill="none">
          <circle cx="1020" cy="286" r="74"/><circle cx="1020" cy="286" r="44"/><circle cx="1020" cy="286" r="17"/>
          <line x1="870" y1="506" x2="1110" y2="506" stroke="#cfc7b8"/>
        </g>"""
    if kind == "grid":
        lines = []
        for x in range(930, 1111, 30):
            lines.append(f'<line x1="{x}" y1="212" x2="{x}" y2="392"/>')
        for y in range(212, 393, 30):
            lines.append(f'<line x1="930" y1="{y}" x2="1110" y2="{y}"/>')
        return f"""
        <g opacity=".28" stroke="#0e5a5e" fill="none">
          {''.join(lines)}
          <rect x="972" y="254" width="96" height="96" stroke="#0d7a82" stroke-width="2"/>
        </g>"""
    return """
      <g opacity=".34" fill="none" stroke-linecap="round">
        <path d="M900 255 L1110 225" stroke="#0e5a5e" stroke-width="2"/>
        <path d="M900 285 L1110 250" stroke="#0d7a82" stroke-width="2"/>
        <path d="M900 315 L1110 280" stroke="#0e5a5e" stroke-width="2"/>
        <path d="M900 345 L1110 310" stroke="#0d7a82" stroke-width="2"/>
      </g>"""


def render_svg(card: dict[str, object]) -> str:
    lines = tuple(card["lines"])
    size = int(card["size"])
    start_y = 286 if len(lines) <= 2 else 278
    gap = 74
    text_lines = "\n".join(
        f'<text x="56" y="{start_y + i*gap}" font-family="DejaVu Serif, Georgia, serif" '
        f'font-size="{size}" font-weight="700" fill="#16191c">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    subtitle_y = start_y + len(lines)*gap + 30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img">
  <rect width="1200" height="630" fill="#f7f5f0"/>
  <rect x="56" y="56" width="56" height="56" fill="#ffffff" stroke="#16191c" stroke-width="2"/>
  <text x="84" y="92" text-anchor="middle" font-family="DejaVu Serif, Georgia, serif" font-size="22" font-weight="700" fill="#16191c">BK</text>
  <text x="132" y="79" font-family="DejaVu Sans, Arial, sans-serif" font-size="22" font-weight="700" fill="#16191c">Bhalaji Kantepalle</text>
  <text x="132" y="105" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" letter-spacing="2" fill="#565e66">RESEARCH PORTFOLIO</text>
  <line x1="56" y1="144" x2="1144" y2="144" stroke="#e3ded3"/>
  <text x="56" y="206" font-family="DejaVu Sans, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="2.2" fill="#0e5a5e">{escape(str(card["kicker"]))}</text>
  {text_lines}
  <text x="56" y="{subtitle_y}" font-family="DejaVu Sans, Arial, sans-serif" font-size="20" fill="#565e66">{escape(str(card["subtitle"]))}</text>
  {motif_svg(str(card["motif"]))}
  <line x1="56" y1="552" x2="1144" y2="552" stroke="#cfc7b8"/>
  <circle cx="64" cy="590" r="5" fill="#a84f2b"/>
  <text x="82" y="597" font-family="DejaVu Sans, Arial, sans-serif" font-size="16" fill="#565e66">bhalaji.com</text>
</svg>"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    renderer = shutil.which("rsvg-convert")
    fallback = shutil.which("magick") or shutil.which("convert")
    if not renderer and not fallback:
        raise SystemExit("No SVG renderer found (rsvg-convert or ImageMagick).")

    with tempfile.TemporaryDirectory(prefix="portfolio-social-") as tmp:
        temp = Path(tmp)
        for name, card in CARDS.items():
            source = temp / f"{name}.svg"
            target = OUT / f"{name}.png"
            source.write_text(render_svg(card), encoding="utf-8")
            if renderer:
                subprocess.run([renderer, "--width", "1200", "--height", "630", "--output", str(target), str(source)], check=True)
            elif Path(fallback).name == "magick":
                subprocess.run([fallback, str(source), str(target)], check=True)
            else:
                subprocess.run([fallback, str(source), str(target)], check=True)
            if target.stat().st_size < 20_000:
                raise SystemExit(f"Generated social preview is unexpectedly small: {target}")
    print(f"Generated {len(CARDS)} branded social previews in {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
