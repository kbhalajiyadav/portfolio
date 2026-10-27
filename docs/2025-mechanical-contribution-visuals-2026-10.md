# Correction: 2025 paper visuals should reflect contributed mechanical results

**Decision:** 2026-10-27. PR #85 stays a draft until the two source-resolution mechanical figures are added and verified.

The 2025 paper's Figure 1 is a useful overview of fiber morphology, but it was initially featured because SEM makes a recognizable scientific thumbnail—not because it best represented the portfolio owner's work. The owner identified **Figures 4 and 5 and Table 1** as their direct areas of contribution. The publication's author-contributions section independently lists B.Y.K. in formal analysis, validation, visualization, and methodology, while not assigning exclusive authorship of individual figures.

## Correct visual and editorial priority

1. **Figure 5, box-and-whisker comparison of Young's modulus:** primary image on this coauthored article page. Captures stiffness results, statistics, and the comparison of TPU, nylon, sequentially layered, and manually layered mats.
2. **Figure 4, representative engineering stress–strain curves:** secondary image contextualizing the underlying tensile response.
3. **Table 1, mechanical-property summary:** accessible semantic HTML table, not an image. Preserve Young's modulus, ultimate strength, elongation at break, sample sizes, and the paper's stated limitations.
4. **Figure 1 SEM:** background characterization, not the portfolio's lead illustration. The figure was removed from the portfolio article's featured figures pending the mechanical replacements. The existing file under static is intentionally left untouched during staging; decide on its removal when the new images land.

The public article page already contains a faithful Table 1 transcription with a CC BY 4.0 license credit and direct PDF links to Figures 5 and 4. Once the two PNGs have been uploaded to the PR branch, replace these external-only figure links with the reusable figure component and retire the unneeded SEM asset, leaving any meaningful context as text.

## Source files prepared from uploaded paper

From the 2025 article PDF `polymers-17-01777-v2.pdf`:

| Target path under `static/media/research/` | Native pixels | PDF page | Embedded image xref | SHA-256 (PNG) |
| --- | --- | --- | --- | --- |
| `polymers-2025-fig5-youngs-modulus.png` | 1265 × 987 | 9 | 155 | `e4a96eafefbb45d903c8476a6890ee5176b86dbfb7875f212001c6094861f729` |
| `polymers-2025-fig4-stress-strain.png` | 1195 × 802 | 8 | 128 | `40b763de9d590e4f3376f1dcc23ab2d3d69b92ce5fc0bed3f3b8d252d7451ee8` |

The original embedded JPEG pixels are encoded losslessly into PNG at native pixel dimensions, with **no pixel scaling, synthetic detail, axis edits, or changes to data**. The packed handoff ZIP is provided to the portfolio owner separately and deliberately excluded from the site repository.

## Author/license attribution

Caloian, I.; Trapp, J.; Kantepalle, B.Y.; Latimer, P.; Lawton, T.J.; Tang, C. *Mechanical Properties of Dual-Layer Electrospun Fiber Mats*. *Polymers* **2025**, 17(13), 1777. https://doi.org/10.3390/polym17131777. © 2025 the authors. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/.

The public webpage should reflect **the user's contribution to a coauthored paper**; it should not imply exclusive ownership of the complete paper or the underlying experiments.

## Release gate

- Upload just the two new PNGs into `feature/homepage-evidence-figure` at the paths above, preserving the filenames, not directly to `main`.
- Verify Git bytes, image dimensions, alt descriptions, source credits, responsive figure legibility, and scientific context.
- Add both to the 2025 publication front matter in Figure 5 then Figure 4 order, with CC BY 4.0 attribution and exact transformation notes. Do not link Figure 1 ahead of them.
- Re-run GitHub build, figure-integrity checks, site content audits, accessibility, responsive/WCAG, and Lighthouse mobile/desktop.
- Keep PR #85 as a **draft** and do not deploy until completed.
