#!/usr/bin/env python3
"""Check local links and asset references in ToolStack's static HTML pages."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.rglob("*.html"))
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data", "blob"}


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attr in ("href", "src", "action"):
            value = values.get(attr)
            if value:
                self.targets.append((attr, value.strip()))
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def resolve_local_path(source: Path, url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return source
    if path_text.startswith("/"):
        # Support the existing GitHub Pages project prefix and root-relative paths.
        path_text = path_text.lstrip("/")
        if path_text.startswith("toolstack/"):
            path_text = path_text[len("toolstack/"):]
        candidate = ROOT / path_text
    else:
        candidate = source.parent / path_text
    candidate = candidate.resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return ROOT / "__path_outside_repo__"
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


def main() -> int:
    errors: list[str] = []
    if not HTML_FILES:
        print("ERROR: no HTML files found", file=sys.stderr)
        return 1
    for html_file in HTML_FILES:
        parser = References()
        try:
            parser.feed(html_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{html_file.relative_to(ROOT)}: cannot read HTML: {exc}")
            continue
        for attr, url in parser.targets:
            if not url or url.startswith("#"):
                continue
            target = resolve_local_path(html_file, url)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{html_file.relative_to(ROOT)}: broken {attr}={url!r}")
            elif target.suffix.lower() in {".html", ".htm"} and urlsplit(url).fragment:
                fragment = urlsplit(url).fragment
                try:
                    target_parser = References()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    if fragment not in target_parser.ids:
                        errors.append(f"{html_file.relative_to(ROOT)}: missing fragment #{fragment} in {url!r}")
                except (OSError, UnicodeError):
                    pass
        if parser.duplicate_ids:
            errors.append(f"{html_file.relative_to(ROOT)}: duplicate IDs: {', '.join(sorted(parser.duplicate_ids))}")
    if errors:
        print(f"Found {len(errors)} issue(s) across {len(HTML_FILES)} HTML pages:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: checked {len(HTML_FILES)} HTML pages; local links, assets, fragments, and IDs passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
