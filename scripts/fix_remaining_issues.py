#!/usr/bin/env python3
"""
fix_remaining_issues.py
Cleans HTML entities in JSON-LD, updates stale October 2026 dates/labels
to November 2026, checks IndexNow key consistency, and audits HTML integrity.
"""

import html
import json
import os
import re

ROOT = os.getcwd()
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
            # Fallback regex unescape if JSON block has minor syntax issues
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

    # 1. Update JSON-LD dateModified from 2026-10-XX to 2026-11-28
    new_content, n1 = re.subn(
        r'("dateModified"\s*:\s*")2026-10-\d{2}(")',
        rf"\g<1>{TODAY_ISO}\g<2>",
        content,
    )
    updates += n1

    # 2. Update visible "Updated for October 2026..." or "Updated October 2026" badges
    new_content, n2 = re.subn(
        r"\b(Updated(?:\s+for)?\s+)October\s+2026\b",
        rf"\g<1>{CURRENT_MONTH_YEAR}",
        new_content,
        flags=re.IGNORECASE,
    )
    updates += n2

    return new_content, updates


def check_indexnow():
    script_path = os.path.join(ROOT, "scripts", "indexnow_index.py")
    if not os.path.exists(script_path):
        print("[IndexNow] scripts/indexnow_index.py not found.")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    m = re.search(r'INDEXNOW_KEY\s*=\s*["\']([a-f0-9]{32})["\']', code, re.IGNORECASE)
    if not m:
        print("[IndexNow] Could not parse INDEXNOW_KEY in scripts/indexnow_index.py.")
        return

    key = m.group(1)
    key_file = os.path.join(ROOT, f"{key}.txt")
    if not os.path.exists(key_file):
        print(f"[IndexNow] WARNING: Missing root verification file {key}.txt")
        return

    with open(key_file, "r", encoding="utf-8") as f:
        file_val = f.read().strip()

    if file_val != key:
        print(f"[IndexNow] WARNING: {key}.txt content ({file_val}) != INDEXNOW_KEY ({key})")
    elif key == "c8a2e79b4d1f46829f0e123456789abc":
        print(f"[IndexNow] NOTE: Key matches {key}.txt, verify this isn't a sample key in Bing Webmaster Tools.")
    else:
        print(f"[IndexNow] OK: {key}.txt matches scripts/indexnow_index.py.")


def process_site():
    entity_files = 0
    date_files = 0
    warnings = []

    for sub in HTML_DIRS:
        folder = os.path.join(ROOT, sub) if sub else ROOT
        if not os.path.isdir(folder):
            continue

        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".html"):
                continue

            fpath = os.path.join(folder, fn)
            rel = os.path.relpath(fpath, ROOT)

            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                original = f.read()

            updated, e_count = clean_jsonld_blocks(original)
            updated, d_count = refresh_october_2026(updated)

            if e_count:
                entity_files += 1
            if d_count:
                date_files += 1

            if updated != original:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(updated)
                print(f"Updated {rel} (JSON-LD entities: {e_count}, Oct->Nov dates: {d_count})")

            # Integrity & truncation checks
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
    check_indexnow()

    if warnings:
        print("\n--- Files Requiring Manual Inspection ---")
        for w in warnings:
            print(" ", w)
    else:
        print("\nAll HTML files passed structural & link checks.")


if __name__ == "__main__":
    process_site()
