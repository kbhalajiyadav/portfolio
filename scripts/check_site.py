#!/usr/bin/env python3
"""Check a generated Hugo site for broken local references and metadata regressions."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[str] = []
        self.ids: list[str] = []
        self.title = False
        self.description = False
        self.canonical = False
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if 'id' in data: self.ids.append(data['id'])
        if tag == 'a' and data.get('href'): self.links.append(data['href'])
        if tag == 'img' and data.get('src'): self.images.append(data['src'])
        if tag == 'title': self.title = True
        if tag == 'meta' and data.get('name') == 'description' and data.get('content'): self.description = True
        if tag == 'link' and data.get('rel') == 'canonical' and data.get('href'): self.canonical = True

def target_for(root: Path, source: Path, url: str) -> tuple[Path, str | None] | None:
    parsed = urlparse(url)
    if parsed.scheme in {'http', 'https', 'mailto', 'tel'} or url.startswith('//'):
        return None
    path = unquote(parsed.path)
    fragment = unquote(parsed.fragment) if parsed.fragment else None
    if not path:
        target = source
    elif path.startswith('/'):
        target = root / path.lstrip('/')
    else:
        target = source.parent / path
    if target.is_dir() or path.endswith('/'):
        target = target / 'index.html'
    elif not target.suffix:
        target = target / 'index.html'
    return target.resolve(), fragment

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}
    for html in root.rglob('*.html'):
        parser = PageParser(); parser.feed(html.read_text(encoding='utf-8', errors='replace')); pages[html.resolve()] = parser
        if not parser.title: errors.append(f'{html.relative_to(root)}: missing title')
        if not parser.description: errors.append(f'{html.relative_to(root)}: missing meta description')
        if not parser.canonical: errors.append(f'{html.relative_to(root)}: missing canonical URL')
        duplicates = {x for x in parser.ids if parser.ids.count(x) > 1}
        if duplicates: errors.append(f'{html.relative_to(root)}: duplicate IDs {sorted(duplicates)}')
    for html, parser in pages.items():
        for ref in parser.links + parser.images:
            result = target_for(root, html, ref)
            if result is None: continue
            target, fragment = result
            if not target.exists():
                errors.append(f'{html.relative_to(root)}: missing local target {ref}')
                continue
            if fragment and target.suffix == '.html':
                target_parser = pages.get(target)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f'{html.relative_to(root)}: missing fragment {ref}')
    for required in ('robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt'):
        if not (root / required).exists(): errors.append(f'missing generated {required}')
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr)
        return 1
    print(f'Generated-site audit passed: {len(pages)} HTML pages.')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
