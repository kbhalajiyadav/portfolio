# Scientific figure source-export handoff (PR #85)

**Status:** Figure source assets have been prepared from files provided by the portfolio owner. Publication front matter on `feature/homepage-evidence-figure` now specifies the replacement dimensions. **The four binary PNGs are not yet on GitHub.** The draft PR must not be merged until matching binaries are uploaded and CI passes.

## Prepared figures

| Repository destination (`static/media/research/`) | Pixels | Source | Derivation | SHA-256 of prepared PNG |
| --- | --- | --- | --- | --- |
| `polymers-2026-fig2a-peel-traces.png` | 2520 × 1504 | Uploaded manuscript figure `Figure 2.png` (4211 × 1504) from the 2026 paper's supplied `Paper figures.zip` | Panel A crop, coordinates x=0–2520, native pixels, PNG lossless | `ed1f3d8c08a8465c7787148692394b9f477ca8133cc416fb74dd762330096f6c` |
| `polymers-2026-fig4-radar.png` | 3221 × 2433 | Uploaded `Figure 4.png` from the same archive | Opaque RGB conversion and lossless PNG encoding; no resize/crop | `8c763cbc8488d110b46bbacd4659677806d7ada4e4b07f907638d8b3c0c856f8` |
| `polymers-2026-fig5-conductive-traces.png` | 4984 × 1654 | Uploaded `Figure 5.png` from the same archive | Opaque RGB conversion and lossless PNG encoding; no resize/crop | `d15be7c39e908e93563ef0ffcf0bac54541bb3fa0c64a162f042329c9b98037a` |
| `polymers-2025-fig1-sem.png` | 2152 × 508 | Uploaded `polymers-17-01777-v2.pdf`, page 5, image bands xref 77 and 82, each 2152 × 254 | Reassembled contiguous upper/lower image bands at native pixels; no interpolation or changes to scale bars | `7b497cf64aad86d01b0bb33309af3df59d84725985d91c63ff75f193c7743aa6` |

**Licenses:** Kantepalle et al., `https://doi.org/10.3390/polym18121504`, CC BY 4.0; Caloian et al., `https://doi.org/10.3390/polym17131777`, CC BY 4.0. The corresponding publication records provide authorship/DOI/permission and describe each source-file transformation. These paper figures are not portfolio all-rights-reserved originals.

## Release gate

1. Extract the four replacement PNGs from the associated handoff archive into `static/media/research/` of the PR branch. Do **not** upload the entire zip into the static website.
2. Verify all four files match the dimensions and SHA-256 values above. `scripts/check_research_figures.py` enforces correct dimensions at build time.
3. Confirm Figure 2A has all four traces, labels, and full force/displacement axes; Figure 4 retains its legend/criteria; Figure 5 retains all panels and scale bars; and SEM Figure 1 retains panels A–C and all 100 µm bars.
4. Run the existing Hugo build, source/document audits, WCAG/responsive checks and mobile/desktop Lighthouse thresholds. Audit baseline vs branch, especially for the previously observed article-page LCP issue. Consider a separate tested WebP strategy if the high-resolution source images increase transfer size.
5. Keep PR #85 a draft until visual QA and CI succeed. Do not deploy to main or reference unpublished research data.

The uploaded raw manuscript source ZIP itself remains outside the website and GitHub repository. Only the four published, specifically credited figures should be published.
