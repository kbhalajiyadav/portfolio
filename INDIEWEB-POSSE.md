# IndieWeb and POSSE implementation

This repository now contains a restrained IndieWeb foundation without adding another
homepage section or navigation dropdown.

## Active now

- `rel="me"` identity links to ORCID, Google Scholar, GitHub, and LinkedIn.
- A representative `h-card` on the shared header.
- `h-entry` markup on publication, project, research, and future note pages.
- RSS/feed autodiscovery in the document head.
- Conditional discovery for Webmention, IndieAuth, and Micropub endpoints.
- A future `/notes/` template and archetype. It does not create a public page until
  note content is added.

## Why no public Notes link yet

An empty blog or a large stream of minor updates would dilute the academic portfolio.
Add Notes to the navigation only after at least three useful, durable posts exist.

Good first posts:

1. A public explanation of the stability-informed T-peel framework.
2. A beamtime or methods reflection that contains no restricted experimental details.
3. A reproducible research-software release note.
4. A conference or paper summary with a canonical link to the public record.

## POSSE workflow

POSSE means Publish on your Own Site, Syndicate Elsewhere.

1. Create a note:
   `hugo new notes/descriptive-slug.md`
2. Write and review it with `draft: true`.
3. Publish the site and confirm the canonical URL works.
4. Share a concise copy or excerpt to the selected network with the canonical URL.
5. Add each resulting social URL under the note's `syndication` front matter.
6. Rebuild so the canonical note exposes `u-syndication` links.

Start manually. Automation should be added only after the post format and target
networks are stable.

## Optional services

The following configuration values are intentionally blank in
`config/_default/params.yaml`:

- `indieweb.webmention_endpoint`
- `indieweb.pingback_endpoint`
- `indieweb.authorization_endpoint`
- `indieweb.token_endpoint`
- `indieweb.micropub_endpoint`

Do not publish invented endpoints. Configure Webmention reception first, then IndieAuth
or Micropub only when a real provider or self-hosted endpoint is operational.

For an initial professional workflow, use the site as the canonical source and share
manually to LinkedIn. Bridgy can later support selected networks such as Mastodon and
Bluesky, but network permissions and behavior should be tested before automation.
