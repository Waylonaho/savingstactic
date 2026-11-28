#!/usr/bin/env python3
"""
fix_remaining_issues.py
GitHub Actions-ready script to clean HTML entities in JSON-LD,
update stale October 2026 dates/labels to November 2026, verify IndexNow,
and fail the workflow if truncated/broken HTML files are detected.
"""

import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("GITHUB_WORKSPACE", Path(__file__).resolve().parent.parent))
TODAY_ISO = "2026-11-28"
CURRENT_MONTH_YEAR = "November 2026"
HTML_DIRS = ["", "tools", "tactics", "cvs", "earn", "blog"]


def unescape_jsonld_strings(obj):
    if isinstance(obj, dict):
        return {k: unescape_jsonld_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [unescape_jsonld_strings(v) for v in obj]
    if isinstance(obj, str):
        return html.unescape(obj)
    return obj


def clean_jsonld_blocks(content: str) -> tuple[str, int]:
    fixes = 0
    pattern = re.compile(
        r'(<script\s+type=["\']application/ld\+json["\']\s*>)(.*?)(</script>)',
        re.DOTALL | re.IGNORECASE,
    )

    def _replace(match):
        nonlocal fixes
        open_tag, raw_json, close_tag = match.groups()
        try:
            parsed = json.loads(raw_json)
            cleaned = unescape_jsonld_strings(parsed)
            formatted = json.dumps(cleaned, indent=2, ensure_ascii=False)
            new_block = f"{open_tag}\n{formatted}\n{close_tag}"
            if new_block != match.group(0):
                fixes += 1
            return new_block
        except json.JSONDecodeError:
            unescaped = re.sub(
                r'("(?:name|headline|description)"\s*:\s*")([^"]*&\w+;[^"]*)(")',
                lambda m: f"{m.group(1)}{html.unescape(m.group(2))}{m.group(3)}",
                raw_json,
            )
            if unescaped != raw_json:
                fixes += 1
            return f"{open_tag}{unescaped}{close_tag}"

    return pattern.sub(_replace, content), fixes


def refresh_october_2026(content: str) -> tuple[str, int]:
    updates = 0

    new_content, n1 = re.subn(
        r'("dateModified"\s*:\s*")2026-10-\d{2}(")',
        rf"\g<1>{TODAY_ISO}\g<2>",
        content,
    )
    updates += n1

    new_content, n2 = re.subn(
        r"\b(Updated(?:\s+for)?\s+)October\s+2026\b",
        rf"\g<1>{CURRENT_MONTH_YEAR}",
        new_content,
        flags=re.IGNORECASE,
    )
    updates += n2

    return new_content, updates


def check_indexnow() -> list[str]:
    notes = []
    script_path = ROOT / "scripts" / "indexnow_index.py"
    if not script_path.exists():
        notes.append("[IndexNow] scripts/indexnow_index.py not found.")
        return notes

    code = script_path.read_text(encoding="utf-8")
    m = re.search(r'INDEXNOW_KEY\s*=\s*["\']([a-f0-9]{32})["\']', code, re.IGNORECASE)
    if not m:
        notes.append("[IndexNow] Could not parse INDEXNOW_KEY in scripts/indexnow_index.py.")
        return notes

    key = m.group(1)
    key_file = ROOT / f"{key}.txt"
    if not key_file.exists():
        notes.append(f"[IndexNow] WARNING: Missing root verification file {key}.txt")
        return notes

    file_val = key_file.read_text(encoding="utf-8").strip()
    if file_val != key:
        notes.append(f"[IndexNow] WARNING: {key}.txt content ({file_val}) != INDEXNOW_KEY ({key})")
    elif key == "c8a2e79b4d1f46829f0e123456789abc":
        notes.append(f"[IndexNow] NOTE: Key matches {key}.txt — confirm this is your real Bing Webmaster Tools key.")
    else:
        notes.append(f"[IndexNow] OK: {key}.txt matches scripts/indexnow_index.py.")

    return notes


def main() -> int:
    entity_files = 0
    date_files = 0
    warnings = []

    for sub in HTML_DIRS:
        folder = ROOT / sub if sub else ROOT
        if not folder.is_dir():
            continue

        for fpath in sorted(folder.glob("*.html")):
            rel = fpath.relative_to(ROOT).as_posix()
            original = fpath.read_text(encoding="utf-8", errors="replace")

            updated, e_count = clean_jsonld_blocks(original)
            updated, d_count = refresh_october_2026(updated)

            if e_count:
                entity_files += 1
            if d_count:
                date_files += 1

            if updated != original:
                fpath.write_text(updated, encoding="utf-8")
                print(f"Updated {rel} (JSON-LD entities: {e_count}, Oct->Nov dates: {d_count})")

            stripped = updated.strip()
            if not stripped.lower().endswith("</html>"):
                warnings.append(f"[TRUNCATED HTML] {rel} — missing closing </html>")
            elif "</body>" not in stripped.lower():
                warnings.append(f"[MISSING </body>] {rel}")

            if updated.count("<script") != updated.count("</script>"):
                warnings.append(f"[UNCLOSED SCRIPT] {rel}")

            if re.search(r"\[span_\d+\]\((?:start|end)_span\)", updated):
                warnings.append(f"[SPAN ARTIFACT] {rel}")

            for m in re.finditer(r'href=["\'](/blog/[^"\']+)["\']', updated):
                warnings.append(f"[OLD /blog LINK] {rel} -> {m.group(1)}")

    print("\n--- Summary ---")
    print(f"JSON-LD entity cleanups: {entity_files} file(s)")
    print(f"October -> November 2026 updates: {date_files} file(s)")
    for note in check_indexnow():
        print(note)

    if warnings:
        print("\n--- Structural Errors Found ---")
        for w in warnings:
            print(f"::error::{w}")
        return 1

    print("\nAll HTML files passed structural & link checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
