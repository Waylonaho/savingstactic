#!/usr/bin/env python3
"""
phase3_upgrade_savingstactic.py
Cleans leftover survey JS/comments, aligns generate_sitemap.py with all site hubs,
and adds a practical quick-action checklist to shorter blog articles.
"""

import glob
import os
import re
from datetime import datetime, timezone

ORPHAN_SURVEY_SCRIPT_RE = re.compile(
    r"\s*<!--\s*Survey JS Logic\s*-->\s*<script>[\s\S]*?nextStep[\s\S]*?</script>",
    re.IGNORECASE,
)

SHORT_SURVEY_SCRIPT_RE = re.compile(
    r"\s*<script>\s*function finishSurvey\(\)[\s\S]*?</script>",
    re.IGNORECASE,
)

PRACTICAL_CHECKLIST_BLOCK = """<!-- Phase 3 Practical Action Checklist -->
<section class="bg-slate-50 border border-slate-200 rounded-2xl p-5 md:p-6 space-y-3">
    <h2 class="text-lg font-extrabold text-slate-900">Quick Action Checklist Before You Checkout</h2>
    <ol class="list-decimal pl-5 space-y-1.5 text-xs sm:text-sm text-slate-700 leading-relaxed">
        <li><strong>Check Unit Price First:</strong> Compare cost per ounce, pound, or count—never let a coupon or rebate push you into a higher unit price on a bigger or brand-name pack.</li>
        <li><strong>Clip &amp; Verify Before Entering the Store:</strong> Load digital offers ahead of time, confirm exact size/UPC eligibility in the app, and set your exact store location.</li>
        <li><strong>Separate Register Cash From Rebates:</strong> Track what you pay out of pocket at checkout separately from pending app rebates or gift card rewards.</li>
        <li><strong>Keep Your Receipt Until Rewards Post:</strong> Snap or save receipts right away and verify points/rebates before discarding proof of purchase.</li>
    </ol>
    <div class="pt-2 flex flex-wrap gap-3 text-xs font-bold">
        <a href="/blog/grocery-unit-price-calculator.html" class="text-blue-600 hover:underline">Open Unit Price Calculator &rarr;</a>
        <a href="/blog/free-grocery-price-book-template.html" class="text-emerald-700 hover:underline">2026 Price-Book Template &rarr;</a>
        <a href="/earn/" class="text-slate-800 hover:underline">Cashback &amp; Rewards Hub &rarr;</a>
    </div>
</section>"""


def clean_article(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    updated = html
    updated = re.sub(r"<!--\s*CPA SURVEY CARD.*?-->", "<!-- Editorial Tool Callout -->", updated)
    updated = ORPHAN_SURVEY_SCRIPT_RE.sub("", updated)
    updated = SHORT_SURVEY_SCRIPT_RE.sub("", updated)

    # Add the practical checklist if the article doesn't already have a table or calculator/checklist
    if (
        filepath.startswith("blog/")
        and os.path.basename(filepath) != "index.html"
        and "Phase 3 Practical Action Checklist" not in updated
        and "<table" not in updated
        and "calculator" not in os.path.basename(filepath)
    ):
        marker = '<div class="bg-gray-100 rounded-xl p-4'
        if marker in updated:
            updated = updated.replace(marker, PRACTICAL_CHECKLIST_BLOCK + "\n\n            " + marker, 1)

    if updated != html:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def sync_generate_sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    script_content = f'''import glob
import os
from datetime import datetime, timezone

BLOG_DIR = "blog"
SITEMAP_PATH = "sitemap.xml"
BASE_URL = "https://www.savingstactic.com"


def generate_sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    core_pages = [
        ("/", "1.0", "weekly"),
        ("/blog/grocery-unit-price-calculator.html", "0.95", "weekly"),
        ("/earn/", "0.90", "weekly"),
        ("/blog/", "0.85", "weekly"),
        ("/cvs/", "0.80", "weekly"),
        ("/about.html", "0.70", "monthly"),
        ("/contact.html", "0.65", "monthly"),
        ("/privacy.html", "0.50", "yearly"),
        ("/terms.html", "0.50", "yearly"),
    ]

    entries = []
    seen = set()

    for path, prio, freq in core_pages:
        loc = f"{{BASE_URL}}{{path}}"
        if loc not in seen:
            seen.add(loc)
            entries.append((loc, today, freq, prio))

    for file_path in sorted(glob.glob(os.path.join(BLOG_DIR, "*.html"))):
        filename = os.path.basename(file_path)
        if filename == "index.html":
            continue
        loc = f"{{BASE_URL}}/blog/{{filename}}"
        if loc not in seen:
            seen.add(loc)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc).strftime("%Y-%m-%d")
            entries.append((loc, mtime, "monthly", "0.75"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod, freq, prio in entries:
        lines.extend([
            "  <url>",
            f"    <loc>{{loc}}</loc>",
            f"    <lastmod>{{lastmod}}</lastmod>",
            f"    <changefreq>{{freq}}</changefreq>",
            f"    <priority>{{prio}}</priority>",
            "  </url>",
        ])
    lines.append("</urlset>")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines) + "\\n")
    print(f"Wrote {{len(entries)}} URLs to {{SITEMAP_PATH}} on {{today}}.")


if __name__ == "__main__":
    generate_sitemap()
'''
    with open("generate_sitemap.py", "w", encoding="utf-8") as f:
        f.write(script_content)


if __name__ == "__main__":
    changed = 0
    for path in glob.glob("**/*.html", recursive=True):
        if clean_article(path):
            changed += 1
            print(f"Cleaned: {path}")
    sync_generate_sitemap()
    print(f"Phase 3 script finished. Cleaned {changed} HTML file(s) and updated generate_sitemap.py.")
