# Browser icon sources

The site header, browser tabs, Safari touch icon, and installable-app icons are
derived from `static/media/bk-monogram-canonical-20260730.svg`.

Run `bash scripts/build_browser_icons.sh` before a local Hugo build. The script
creates the cache-busted PNG and ICO files used by `seo_head.html` and
`site.webmanifest`; generated files are deployment artifacts and are not kept as
independent design sources.
