# Pre-deployment readiness

This package is the production-hardening release for `bhalaji.com`.

## Corrected blocking failure

The failed generated-site audit reported:

`authors/page/1/index.html: missing meta description`

The `/authors/` archive came from the legacy HugoBlox author profile and is not part of the portfolio's public information architecture. The release removes `content/authors/`, disables the unused author/category/publication-type taxonomies, and adds an explicit regression check that fails if `/authors/` is generated again.

## Additional hardening completed

- Added explicit publication, project, terms, and taxonomy metadata/templates.
- Added exactly-one-H1, language, viewport, canonical, Open Graph, Twitter card, image-alt, intrinsic-image-size, duplicate-ID, local-link, fragment, and required-deployment-file checks.
- Added CSS contrast validation for every text-bearing palette role.
- Darkened the cyan interaction color to meet WCAG AA against ivory and white surfaces.
- Added the missing visually-hidden utility. This prevents IndieWeb microformat metadata and the hidden identity photograph from appearing in the visible header or page body.
- Added Hugo-template and JavaScript syntax audits.
- Made structured-data `dateModified` derive from site/page data.
- Added CI timeouts, diagnostics, and monthly Dependabot checks.
- Removed the unused Node dependency-install step.
- Regenerated and visually inspected the two-page CV.

## Automated release gates

The workflow must pass, in order:

1. Generate the CV.
2. Audit source regressions.
3. Audit palette contrast and responsive-system markers.
4. Audit Hugo templates and JavaScript syntax.
5. Build Hugo with the pinned Extended release.
6. Audit every generated HTML page and local target.
7. Upload and deploy the Pages artifact.
8. Submit the canonical URLs to IndexNow without making deployment depend on IndexNow availability.

## Account-level steps after the first green deployment

- Verify `bhalaji.com` in Google Search Console and Bing Webmaster Tools.
- Add the issued verification values to `config/_default/params.yaml`.
- Submit `https://bhalaji.com/sitemap.xml` in both services.
- Request inspection/indexing for `/`, `/research/`, and the principal publication page.
- Add `https://bhalaji.com/` to ORCID, LinkedIn, GitHub, and other supported identity profiles to strengthen reciprocal `rel=me` identity links.
- Configure real Webmention/IndieAuth/Micropub endpoints only when a provider is selected; blank endpoints are intentional.
