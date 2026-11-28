#!/usr/bin/env python3
"""
cleanup_savingstactic.py
Run from the root of your SavingsTactic repository to:
1. Remove deceptive 'Eligibility Confirmed' CPA/survey cards (#survey-card / afflat3c1.com) from /blog/*.html
   and replace them with a clean Brevo PDF & Unit Calculator callout.
2. Fix broken internal links & placeholder referral IDs across all HTML files.
3. Strip leftover [span_x](start_span) / [span_x](end_span) citation artifacts from /cvs/index.html.
4. Regenerate sitemap.xml including /, /about.html, /contact.html, /earn/, /cvs/, and all /blog/ guides.
"""

import glob
import os
import re
from datetime import datetime, timezone

CLEAN_CTA_BLOCK = '''<!-- Clean Editorial Tool & PDF Callout -->
<aside class="my-8 bg-slate-900 text-white rounded-2xl p-6 space-y-3">
    <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">Free Shopper Toolkit</span>
    <h3 class="text-lg font-extrabold text-white">Compare Unit Prices &amp; Save Target Prices in Your Browser</h3>
    <p class="text-xs text-slate-300 leading-relaxed">
        Check whether a sale or coupon actually beats bulk pricing with our <a href="/blog/grocery-unit-price-calculator.html" class="text-emerald-300 underline font-bold">Free Grocery Unit Price Calculator &amp; Price-Book</a>, or get our 2-page printable cheat sheet:
    </p>
    <form action="https://2a1fb247.sibforms.com/serve/MUIFAGkJe4oLNt1pk848WoRGu5xI05BpDiWX1DPuNkVgOVvSEKxOqRgl6VtvDZyG4cIltSteYCSvxjcs6tT6RBkuI5B7G-8gzOOrbSJU6PVdqCuLlkeXzgPS1dBikYkRZj_4vCLNwLJnwCXiveTJQbg3IGGhriG54OclSktcyblQozqrkml2GYsPffFySt9tHtvFxkiAWEVEj5Mmkg==" method="POST" class="flex flex-col sm:flex-row gap-2 pt-1">
        <input type="email" name="EMAIL" placeholder="Enter your email for the free PDF..." required class="bg-white text-slate-900 placeholder-slate-400 text-xs font-semibold px-3.5 py-2.5 rounded-xl flex-grow">
        <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs px-4 py-2.5 rounded-xl transition whitespace-nowrap">Send Free PDF &rarr;</button>
    </form>
</aside>'''

LINK_FIXES = {
    "/blog/walgreens-pickup-order-not-picked-up.html": "/blog/did-not-pick-up-walgreens-order-what-happens.html",
    "/blog/do-you-get-extrabucks-back-if-you-return-an-item.html": "/blog/how-to-get-cvs-extrabucks-back-after-refund.html",
    "YOUR_PRIZEREBEL_ID": "1801489",
    "YOUR_IBOTTA_CODE": "jiiycks",
}

def clean_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Remove [span_X](start_span) / [span_X](end_span) artifacts
    content = re.sub(r"\[span_\d+\]\((?:start|end)_span\)", "", content)

    # 2. Replace #survey-card blocks containing ConsumersConnect / afflat3c1 CPA widgets
    content = re.sub(
        r'<div[^>]*id=["\']survey-card["\'][\s\S]*?afflat3c1\.com[\s\S]*?</div>\s*</div>',
        CLEAN_CTA_BLOCK,
        content,
        flags=re.IGNORECASE,
    )

    # 3. Fix broken internal URLs & placeholder referral IDs
    for bad, good in LINK_FIXES.items():
        content = content.replace(bad, good)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def rebuild_sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [
        ("https://www.savingstactic.com/", "1.0", "weekly"),
        ("https://www.savingstactic.com/blog/grocery-unit-price-calculator.html", "0.95", "weekly"),
        ("https://www.savingstactic.com/earn/", "0.90", "weekly"),
        ("https://www.savingstactic.com/blog/", "0.85", "weekly"),
        ("https://www.savingstactic.com/cvs/", "0.80", "weekly"),
        ("https://www.savingstactic.com/about.html", "0.70", "monthly"),
        ("https://www.savingstactic.com/contact.html", "0.65", "monthly"),
    ]

    seen = {u[0] for u in urls}
    for path in sorted(glob.glob("blog/*.html")):
        filename = os.path.basename(path)
        if filename == "index.html":
            continue
        loc = f"https://www.savingstactic.com/blog/{filename}"
        if loc not in seen:
            urls.append((loc, "0.75", "monthly"))
            seen.add(loc)

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, prio, freq in urls:
        xml_lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ])
    xml_lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    print(f"Rebuilt sitemap.xml with {len(urls)} URLs.")

if __name__ == "__main__":
    for html_path in glob.glob("**/*.html", recursive=True):
        clean_html_file(html_path)
    rebuild_sitemap()
