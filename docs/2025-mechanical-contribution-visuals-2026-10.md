# Correction: 2025 paper visuals should reflect contributed mechanical results

**Decision:** 2026-10-27. The two source-resolution mechanical figures have been uploaded, checked by Git blob identity against the prepared source assets, and integrated into the publication page. Final CI and deployment validation must still be completed.

The 2025 paper's Figure 1 is a useful overview of fiber morphology, but it was initially featured because SEM makes a recognizable scientific thumbnail—not because it best represented the portfolio owner's work. The owner identified **Figures 4 and 5 and Table 1** as their direct areas of contribution. The publication's author-contributions section independently lists B.Y.K. in formal analysis, validation, visualization, and methodology, while not assigning exclusive authorship of individual figures.

## Correct visual and editorial priority

1. **Figure 5, box-and-whisker comparison of Young's modulus:** primary image on this coauthored article page. Captures stiffness results, statistics, and the comparison of TPU, nylon, sequentially layered, and manually layered mats.
2. **Figure 4, representative engineering stress–strain curves:** secondary image contextualizing the underlying tensile response.
3. **Table 1, mechanical-property summary:** accessible semantic HTML table, not an image. Preserve Young's modulus, ultimate strength, elongation at break, sample sizes, and the paper's stated limitations.
4. **Figure 1 SEM:** background characterization, not the portfolio's lead illustration. The figure was removed from the portfolio article's featured figures pending the mechanical replacements. The existing file under static is intentionally left untouched during staging; decide on its removal when the new images land.

The public article page now displays Figure 5 followed by Figure 4, with DOI and CC BY 4.0 credit beside each figure, and a faithful accessible Table 1 transcription. Figure 1's superseded SEM binary has been deleted from the PR branch; its scientific context remains in the published paper.

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

## Release verification

- **Complete:** both mechanical PNGs are committed at the intended paths in `feature/homepage-evidence-figure`. The exact Git blobs match the source-export ZIP: Figure 5 `4c01605035f678f73c89c2e22096c3fff3727d6d`, Figure 4 `e2cc2601bdffcb5c0b690ea7fe7cd36c858c210c`.
- **Complete:** publication front matter references Figure 5 then Figure 4, with exact dimensions and CC BY 4.0 transformation notes.
- **Complete:** Figure 1 is no longer featured, and its unused binary has been deleted from `static/media/research/` on the PR branch.
- **Next release gate:** confirm fresh Hugo, figure-integrity, source/link, accessibility, responsive/WCAG and mobile/desktop Lighthouse results on the final PR head; review the merge and resulting live deployment before claiming public availability.
