# Scientific figure source-export handoff (PR #85)

**Status:** Original figure-source handoff record, retained for provenance. The three 2026 published figures have been committed on `feature/homepage-evidence-figure`, with verified matching dimensions and Git blob identities. The originally prepared 2025 Figure 1 SEM asset was subsequently superseded by 2025 Figures 5 and 4 to prioritize the portfolio owner's mechanical-analysis contribution. See `docs/2025-mechanical-contribution-visuals-2026-10.md`. All final image binaries are in the PR branch; a successful fresh CI run remains the release requirement.

## Original prepared figures (historical inventory)

| Repository destination (`static/media/research/`) | Pixels | Source | Derivation | SHA-256 of prepared PNG |
| --- | --- | --- | --- | --- |
| `polymers-2026-fig2a-peel-traces.png` | 2520 × 1504 | Uploaded manuscript figure `Figure 2.png` (4211 × 1504) from the 2026 paper's supplied `Paper figures.zip` | Panel A crop, coordinates x=0–2520, native pixels, PNG lossless | `ed1f3d8c08a8465c7787148692394b9f477ca8133cc416fb74dd762330096f6c` |
| `polymers-2026-fig4-radar.png` | 3221 × 2433 | Uploaded `Figure 4.png` from the same archive | Opaque RGB conversion and lossless PNG encoding; no resize/crop | `8c763cbc8488d110b46bbacd4659677806d7ada4e4b07f907638d8b3c0c856f8` |
| `polymers-2026-fig5-conductive-traces.png` | 4984 × 1654 | Uploaded `Figure 5.png` from the same archive | Opaque RGB conversion and lossless PNG encoding; no resize/crop | `d15be7c39e908e93563ef0ffcf0bac54541bb3fa0c64a162f042329c9b98037a` |
| `polymers-2025-fig1-sem.png` (superseded; removed from branch) | 2152 × 508 | Uploaded `polymers-17-01777-v2.pdf`, page 5, image bands xref 77 and 82, each 2152 × 254 | Reassembled contiguous upper/lower image bands at native pixels; no interpolation or changes to scale bars | `7b497cf64aad86d01b0bb33309af3df59d84725985d91c63ff75f193c7743aa6` |

**Licenses:** Kantepalle et al., `https://doi.org/10.3390/polym18121504`, CC BY 4.0; Caloian et al., `https://doi.org/10.3390/polym17131777`, CC BY 4.0. The corresponding publication records provide authorship/DOI/permission and describe each source-file transformation. These paper figures are not portfolio all-rights-reserved originals.

## Final publication selection

- **2026 article:** Figure 2A, Figure 4, and Figure 5 remain included at the native source-resolution dimensions recorded above.
- **2025 article:** Figure 5 (Young's modulus) and Figure 4 (engineering stress–strain) are included; Table 1 is provided as accessible, selectable text. Figure 1 SEM was removed from the published site asset tree.
- **2025 figure details:** see `docs/2025-mechanical-contribution-visuals-2026-10.md` for original embedded-image xrefs, dimensions, hashes, and scientific context.
- Verify the published-site build, site audits, WCAG responsiveness, and mobile/desktop Lighthouse checks on the final head. No private lab assets, embargoed thesis figures, or patent drawings are included.

The raw manuscript source ZIP remains outside the public repository; only selected open-access figures and their licenses are published.
