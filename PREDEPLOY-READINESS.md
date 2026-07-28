# Final pre-deployment release readiness

This package is the hardened release candidate for `bhalaji.com`. The creative direction is frozen: seven-section academic portfolio, ivory/ink/teal/cyan/rust visual system, BK monogram, current Ph.D. positioning, connected article-thesis-software package, and robotics presented only as experimental infrastructure.

## CI failures corrected

The supplied GitHub Actions log established that Hugo itself rendered successfully, producing 77 pages. The job then failed in the generated-site audit for two concrete reasons:

1. Hugo minification removed an empty `alt` attribute from the visually hidden IndieWeb identity photograph.
2. The homepage linked to `/research/#resolve-structure`, while the rendered heading ID is `/research/#resolve-structure-under-stimuli`.

The identity photograph now has a durable non-empty alternative, remains visually and assistively hidden, and is checked by source regression tests. The research link now targets the exact generated heading ID and the stale target is blocked from returning.

## Architecture decision

The portfolio is now a self-contained plain-Hugo project. The obsolete HugoBlox module, Go module files, module configuration, inherited Wowchemy settings, Dart Sass installation, and module-defined output formats were removed. The public interface already used custom layouts, CSS, JavaScript, data, and built-in Hugo HTML/RSS generation, so this removes an unnecessary failure surface without changing the approved visual system.

## Mandatory pull-request gates

A pull request to `main` runs all pre-deployment checks but does not deploy. The workflow requires:

1. Official Hugo 0.124.1 package download with checksum verification.
2. Immutable 40-character commit-SHA pins for every GitHub Action.
3. Node.js 24 and exact direct versions of Pa11y CI and Lighthouse CI.
4. Deterministic CV-source regeneration without installing TeX during normal site builds.
5. Source-regression, color-contrast, template, JavaScript, and workflow-security audits.
6. Production Hugo rendering with path warnings enabled.
7. Generated HTML validation for metadata, robots policy, canonical and Open Graph agreement, Twitter metadata, JSON-LD syntax, landmarks, headings, skip-link target, image alternatives and dimensions, safe external-tab links, local links, fragments, RSS, sitemap, manifest, IndieWeb identity links, and required discovery files.
8. External-link validation that fails confirmed HTTP 404/410 records while reporting provider bot blocks and transient failures separately.
9. Pa11y WCAG 2 AA checks at 1440 px and 390 px with zero permitted errors.
10. Browser-level tests at 390, 680, 768, 980, 1180, 1440, and 1920 px plus a 200%-zoom-equivalent viewport.
11. Browser checks for horizontal overflow, detached arrows, one H1/main landmark, mobile-menu state, Escape handling, focus restoration, desktop navigation, and reduced-motion behavior.
12. Lighthouse mobile and desktop gates for accessibility, SEO, best practices, performance, CLS, LCP, and total transfer weight.
13. Successful-PR evidence artifact containing responsive screenshots and machine-readable audit reports.
14. Failure diagnostics containing rendered HTML, screenshots, browser reports, and server logs.

Only a successful push to `main` uploads the Pages artifact. Deployment is followed by a live smoke test for the new headline, current Ph.D. status, research-page markers, crawler policy, and sitemap. IndexNow runs afterward and is deliberately non-blocking.

## Separate CV gate

CV compilation is isolated to a path-filtered workflow. When CV source or output changes, the workflow installs XeLaTeX, regenerates the document, verifies the committed TeX and PDF byte-for-byte, checks PDF metadata, and requires exactly two pages. The normal website build therefore avoids the approximately 890 MB TeX installation shown in the earlier run.

## Local verification completed for this package

- Source audit passed across 41 text files.
- Color, focus, hidden-microformat, breakpoint, and reduced-motion audit passed.
- Sixteen Hugo templates passed both the repository template audit and an independent Go-template syntax parse.
- Three GitHub workflows passed immutable-pin, timeout, permission, and checkout-credential checks.
- Nine YAML files and two JSON files parsed successfully.
- All Python scripts compiled; JavaScript and CI configuration files passed Node syntax checks.
- CV source regeneration was deterministic.
- The CV compiled to a visually inspected two-page PDF with SHA-256 `069a48ed6429f0549f7248bd3eeafde14db12343575a9a7ee051d874c35264b0`.
- The generated-site audit itself passed a controlled fixture covering normal and noindex/404 pages.

The exact final Hugo executable could not be downloaded into this isolated packaging runtime. The supplied run nevertheless proves the immediately preceding source rendered under Hugo 0.124.1; the new pull-request workflow is the authoritative render, browser, accessibility, and performance proof for this hardened package.

## Recommended release sequence

1. Push this package to a new branch, not directly to `main`.
2. Open a pull request against `main`.
3. Require the complete `Build and deploy portfolio / build` job to pass.
4. Download `portfolio-predeployment-evidence-1` and inspect the responsive screenshots and Lighthouse/Pa11y reports.
5. Merge only after that review. The merge triggers the gated production deployment and live smoke test.

## Account-level activation after the first green deployment

Repository code cannot create account credentials or ownership verification. Complete these after deployment:

- Verify `bhalaji.com` in Google Search Console and Bing Webmaster Tools.
- Add the issued verification values to `config/_default/params.yaml` and redeploy.
- Submit `https://bhalaji.com/sitemap.xml` and inspect `/`, `/research/`, and the principal publication page.
- Add `https://bhalaji.com/` to ORCID, LinkedIn, GitHub, and other supported profiles for reciprocal identity links.
- Configure Webmention, IndieAuth, Micropub, or automated POSSE only after selecting real providers and authorizing the relevant accounts.

Blank verification and IndieWeb endpoint fields are deliberate. Invented values would be invalid and unsafe.
