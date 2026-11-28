import glob
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
        loc = f"{BASE_URL}{path}"
        if loc not in seen:
            seen.add(loc)
            entries.append((loc, today, freq, prio))

    for file_path in sorted(glob.glob(os.path.join(BLOG_DIR, "*.html"))):
        filename = os.path.basename(file_path)
        if filename == "index.html":
            continue
        loc = f"{BASE_URL}/blog/{filename}"
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
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ])
    lines.append("</urlset>")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(entries)} URLs to {SITEMAP_PATH} on {today}.")


if __name__ == "__main__":
    generate_sitemap()
