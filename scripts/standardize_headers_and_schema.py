#!/usr/bin/env python3
"""
standardize_headers_and_schema.py
Standardizes robots meta tags, header navigation, and BreadcrumbList JSON-LD
across SavingsTactic HTML pages. Safe to re-run (idempotent).
"""

import json
import os
import re

ROOT = os.getcwd()
BASE_URL = "https://www.savingstactic.com"
TARGET_FOLDERS = ["tools", "tactics", "cvs", "earn", "blog"]

HUB_LABELS = {
    "tools": "Tools",
    "tactics": "Tactics",
    "cvs": "CVS Guides",
    "earn": "Earn & Cash Back",
    "blog": "All Guides",
}

ROBOTS_TAG = '<meta name="robots" content="index, follow, max-image-preview:large">'

STANDARD_HEADER = """<header class="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
    <a href="/" class="flex items-center gap-2.5 font-extrabold text-slate-900 tracking-tight text-lg">
      <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-600 text-white text-sm font-black">ST</span>
      <span>SavingsTactic</span>
    </a>
    <nav class="hidden md:flex items-center gap-6 text-sm font-semibold text-slate-700">
      <a href="/tools/" class="hover:text-emerald-700 transition">Tools</a>
      <a href="/tactics/" class="hover:text-emerald-700 transition">Tactics</a>
      <a href="/cvs/" class="hover:text-emerald-700 transition">CVS</a>
      <a href="/earn/" class="hover:text-emerald-700 transition">Earn</a>
      <a href="/blog/" class="hover:text-emerald-700 transition">Guides</a>
    </nav>
    <a href="/tools/grocery-unit-price-calculator.html" class="inline-flex items-center px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-bold transition">
      Unit Price Calc
    </a>
  </div>
</header>"""


def extract_title(html: str, fallback_slug: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        raw = re.sub(r"\s+", " ", m.group(1)).strip()
        # Strip trailing brand suffix if present
        raw = re.sub(r"\s*[\|\-–—]\s*SavingsTactic.*$", "", raw, flags=re.IGNORECASE).strip()
        if raw:
            return raw
    return fallback_slug.replace("-", " ").title()


def build_breadcrumb_schema(folder: str, filename: str, title: str) -> str:
    hub_label = HUB_LABELS.get(folder, folder.title())
    hub_url = f"{BASE_URL}/{folder}/"
    page_url = f"{BASE_URL}/{folder}/{filename}"

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{BASE_URL}/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": hub_label,
                "item": hub_url,
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": page_url,
            },
        ],
    }
    json_str = json.dumps(schema, indent=2, ensure_ascii=False)
    return f'<!-- BreadcrumbList Schema -->\n<script type="application/ld+json">\n{json_str}\n</script>'


def process_file(filepath: str, folder: str, filename: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    updated = original
    slug = os.path.splitext(filename)[0]
    page_title = extract_title(updated, slug)

    # 1. Ensure robots meta tag is present
    if 'name="robots"' not in updated.lower():
        if re.search(r"<meta\s+name=[\"']viewport[\"'][^>]*>", updated, re.IGNORECASE):
            updated = re.sub(
                r"(<meta\s+name=[\"']viewport[\"'][^>]*>)",
                rf"\1\n  {ROBOTS_TAG}",
                updated,
                count=1,
                flags=re.IGNORECASE,
            )
        elif "</head>" in updated.lower():
            updated = re.sub(
                r"(</head>)",
                f"  {ROBOTS_TAG}\n\\1",
                updated,
                count=1,
                flags=re.IGNORECASE,
            )

    # 2. Standardize <header> if it doesn't already have the [ST] badge
    if 'bg-emerald-600 text-white text-sm font-black">ST<' not in updated:
        if re.search(r"<header[\s\S]*?</header>", updated, re.IGNORECASE):
            updated = re.sub(
                r"<header[\s\S]*?</header>",
                STANDARD_HEADER,
                updated,
                count=1,
                flags=re.IGNORECASE,
            )

    # 3. Add BreadcrumbList JSON-LD if not already added
    if "<!-- BreadcrumbList Schema -->" not in updated and '"@type": "BreadcrumbList"' not in updated:
        breadcrumb_block = build_breadcrumb_schema(folder, filename, page_title)
        if "</head>" in updated.lower():
            updated = re.sub(
                r"(</head>)",
                f"{breadcrumb_block}\n</head>",
                updated,
                count=1,
                flags=re.IGNORECASE,
            )

    if updated != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def main():
    changed_count = 0
    for folder in TARGET_FOLDERS:
        folder_path = os.path.join(ROOT, folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in sorted(os.listdir(folder_path)):
            if not fname.endswith(".html") or fname == "index.html":
                continue
            fpath = os.path.join(folder_path, fname)
            if os.path.isfile(fpath) and process_file(fpath, folder, fname):
                changed_count += 1
                print(f"Updated: {folder}/{fname}")
    print(f"Done. Standardized {changed_count} page(s).")


if __name__ == "__main__":
    main()
