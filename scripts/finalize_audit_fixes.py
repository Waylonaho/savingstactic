#!/usr/bin/env python3
"""
finalize_audit_fixes.py
Fixes post-migration URLs, manifest.json, vercel.json redirect hops,
broken internal links, and rebuilds sitemap.xml + scripts/generate_sitemap.py.
"""

import glob
import json
import os
from datetime import datetime, timezone

ROOT = os.getcwd()
BASE_URL = "https://www.savingstactic.com"
HUB_FOLDERS = ["tools", "tactics", "cvs", "earn", "blog"]

# 1. Fix manifest.json start_url
manifest_path = os.path.join(ROOT, "manifest.json")
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest["start_url"] = "/tools/grocery-unit-price-calculator.html"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print("Fixed manifest.json start_url")

# 2. Fix direct destinations in vercel.json (eliminate double redirects)
vercel_path = os.path.join(ROOT, "vercel.json")
if os.path.exists(vercel_path):
    with open(vercel_path, "r", encoding="utf-8") as f:
        vercel_cfg = json.load(f)
    for rule in vercel_cfg.get("redirects", []):
        if rule.get("destination") == "/blog/how-to-get-free-publix-gift-cards-legit.html":
            rule["destination"] = "/earn/how-to-get-free-publix-gift-cards-legit.html"
    with open(vercel_path, "w", encoding="utf-8") as f:
        json.dump(vercel_cfg, f, indent=2)
        f.write("\n")
    print("Cleaned double-hop redirects in vercel.json")

# 3. Fix broken internal links & add Fetch referral code M9PDUJ across HTML files
REPLACEMENTS = {
    "/tactics/why-digital-coupons-fail-at-register.html": "/tactics/digital-coupon-not-working.html",
    "/blog/grocery-unit-price-calculator.html": "/tools/grocery-unit-price-calculator.html",
    "/blog/free-grocery-price-book-template.html": "/tools/free-grocery-price-book-template.html",
    "Fetch Rewards</td>": 'Fetch Rewards <span class="block font-normal text-[11px] text-slate-500">Code: <code class="bg-slate-100 px-1 rounded">M9PDUJ</code></span></td>',
}

updated_html = 0
for dirpath, _, filenames in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full_path = os.path.join(dirpath, fn)
        with open(full_path, "r", encoding="utf-8") as f:
            html = f.read()
        new_html = html
        for old, new in REPLACEMENTS.items():
            if old == "Fetch Rewards</td>" and "M9PDUJ" in new_html:
                continue
            new_html = new_html.replace(old, new)
        if new_html != html:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_html)
            updated_html += 1
print(f"Updated links/codes across {updated_html} HTML file(s)")

# 4. Update scripts/generate_sitemap.py & regenerate sitemap.xml
generator_code = '''import glob
import os
from datetime import datetime, timezone

BASE_URL = "https://www.savingstactic.com"
SITEMAP_PATH = "sitemap.xml"
HUB_FOLDERS = ["tools", "tactics", "cvs", "earn", "blog"]


def generate_sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    core_pages = [
        ("/", "1.0", "weekly"),
        ("/tools/", "0.95", "weekly"),
        ("/tactics/", "0.90", "weekly"),
        ("/cvs/", "0.90", "weekly"),
        ("/earn/", "0.90", "weekly"),
        ("/blog/", "0.85", "weekly"),
        ("/about.html", "0.70", "monthly"),
        ("/contact.html", "0.65", "monthly"),
        ("/privacy.html", "0.50", "yearly"),
        ("/terms.html", "0.50", "yearly"),
    ]

    entries = []
    seen = set()

    for path, prio, freq in core_pages:
        loc = f"{BASE_URL}{path}"
        if loc not in seen:
            seen.add(loc)
            entries.append((loc, today, freq, prio))

    for folder in HUB_FOLDERS:
        for file_path in sorted(glob.glob(os.path.join(folder, "*.html"))):
            filename = os.path.basename(file_path)
            if filename == "index.html":
                continue
            loc = f"{BASE_URL}/{folder}/{filename}"
            if loc not in seen:
                seen.add(loc)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc).strftime("%Y-%m-%d")
                prio = "0.85" if folder == "tools" else "0.80"
                entries.append((loc, mtime, "monthly", prio))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod, freq, prio in entries:
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ])
    lines.append("</urlset>")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines) + "\\n")
    print(f"Wrote {len(entries)} URLs to {SITEMAP_PATH} on {today}.")


if __name__ == "__main__":
    generate_sitemap()
'''

os.makedirs(os.path.join(ROOT, "scripts"), exist_ok=True)
gen_script_path = os.path.join(ROOT, "scripts", "generate_sitemap.py")
with open(gen_script_path, "w", encoding="utf-8") as f:
    f.write(generator_code)

# Execute sitemap rebuild immediately
exec(generator_code, {"__name__": "__main__"})
