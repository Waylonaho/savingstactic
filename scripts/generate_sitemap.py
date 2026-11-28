import glob
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
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(entries)} URLs to {SITEMAP_PATH} on {today}.")


if __name__ == "__main__":
    generate_sitemap()
