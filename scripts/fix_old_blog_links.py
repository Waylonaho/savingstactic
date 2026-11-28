#!/usr/bin/env python3
"""
fix_old_blog_links.py
GitHub Actions-ready script to rewrite stale /blog/<slug>.html links
to their migrated hub folders (earn/, tactics/, tools/, cvs/).
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("GITHUB_WORKSPACE", Path(__file__).resolve().parent.parent))
HUB_DIRS = ["earn", "tactics", "tools", "cvs"]
SCAN_DIRS = ["", "tools", "tactics", "cvs", "earn", "blog"]


def build_slug_map() -> dict[str, str]:
    """Map <filename.html> -> /<hub>/<filename.html> based on actual files in the repo."""
    slug_map: dict[str, str] = {}
    for hub in HUB_DIRS:
        hub_path = ROOT / hub
        if not hub_path.is_dir():
            continue
        for f in hub_path.glob("*.html"):
            if f.name != "index.html":
                slug_map[f.name] = f"/{hub}/{f.name}"
    return slug_map


def main() -> int:
    slug_map = build_slug_map()
    updated_files = 0
    rewritten_links = 0
    remaining_errors = []

    href_pattern = re.compile(r'(href=["\'])/blog/([^"\'#?]+)([#?][^"\']*)?(["\'])')

    for sub in SCAN_DIRS:
        folder = ROOT / sub if sub else ROOT
        if not folder.is_dir():
            continue

        for html_file in sorted(folder.glob("*.html")):
            rel = html_file.relative_to(ROOT).as_posix()
            original = html_file.read_text(encoding="utf-8", errors="replace")

            def _replace_href(match: re.Match) -> str:
                nonlocal rewritten_links
                prefix, slug_path, suffix, quote = match.groups()
                clean_slug = slug_path.lstrip("/")
                filename = Path(clean_slug).name

                if filename in slug_map:
                    target = slug_map[filename]
                elif clean_slug.startswith(("walmart-", "ibotta-", "fetch-", "target-", "cashback-", "receipt-")):
                    target = f"/earn/{filename}"
                elif clean_slug.startswith(("walgreens-", "cvs-")):
                    target = f"/tactics/{filename}"
                else:
                    target = f"/tactics/{filename}"

                rewritten_links += 1
                return f"{prefix}{target}{suffix or ''}{quote}"

            updated = href_pattern.sub(_replace_href, original)

            if updated != original:
                html_file.write_text(updated, encoding="utf-8")
                updated_files += 1
                print(f"Updated {rel}")

            for m in re.finditer(r'href=["\'](/blog/[^"\']+)["\']', updated):
                remaining_errors.append(f"[OLD /blog LINK] {rel} -> {m.group(1)}")

    print("\n--- Summary ---")
    print(f"Files updated: {updated_files}")
    print(f"Links rewritten: {rewritten_links}")

    if remaining_errors:
        for err in remaining_errors:
            print(f"::error::{err}")
        return 1

    print("Zero /blog/ links remaining.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
