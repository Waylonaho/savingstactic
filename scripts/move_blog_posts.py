import os
import json
import glob
import shutil
from datetime import datetime, timezone

ROOT = os.getcwd()
BLOG_DIR = os.path.join(ROOT, "blog")

def classify_slug(filename):
    if filename in ("index.html",):
        return None
    if filename.startswith("cvs-") or filename.startswith("do-cvs-") or "extrabucks" in filename:
        return "cvs"
    if any(k in filename for k in ("calculator", "template", "ledger")):
        return "tools"
    if any(k in filename for k in ("ibotta", "fetch", "panel", "free-publix", "free-target")):
        return "earn"
    return "tactics"

moves = {}
for filepath in sorted(glob.glob(os.path.join(BLOG_DIR, "*.html"))):
    fname = os.path.basename(filepath)
    target_folder = classify_slug(fname)
    if not target_folder:
        continue

    target_dir = os.path.join(ROOT, target_folder)
    os.makedirs(target_dir, exist_ok=True)
    dest_path = os.path.join(target_dir, fname)

    shutil.move(filepath, dest_path)
    old_rel = f"/blog/{fname}"
    new_rel = f"/{target_folder}/{fname}"
    moves[old_rel] = new_rel
    print(f"Moved {old_rel} -> {new_rel}")

all_html = []
for dirpath, _, filenames in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        if fn.endswith(".html"):
            all_html.append(os.path.join(dirpath, fn))

for html_path in all_html:
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content
    for old_rel, new_rel in moves.items():
        updated = updated.replace(f"https://www.savingstactic.com{old_rel}", f"https://www.savingstactic.com{new_rel}")
        updated = updated.replace(f'href="{old_rel}"', f'href="{new_rel}"')
        updated = updated.replace(f"href='{old_rel}'", f"href='{new_rel}'")

    if updated != content:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated)

print(f"Updated internal links & canonicals across {len(all_html)} HTML files.")

vercel_path = os.path.join(ROOT, "vercel.json")
vercel_cfg = {}
if os.path.exists(vercel_path):
    with open(vercel_path, "r", encoding="utf-8") as f:
        try:
            vercel_cfg = json.load(f)
        except json.JSONDecodeError:
            vercel_cfg = {}

existing_redirects = vercel_cfg.get("redirects", [])
existing_sources = {r.get("source") for r in existing_redirects}

for old_rel, new_rel in sorted(moves.items()):
    if old_rel not in existing_sources:
        existing_redirects.append({
            "source": old_rel,
            "destination": new_rel,
            "permanent": True
        })

vercel_cfg["redirects"] = existing_redirects
with open(vercel_path, "w", encoding="utf-8") as f:
    json.dump(vercel_cfg, f, indent=2)
    f.write("\n")

print(f"Synced {len(moves)} 301 redirects in vercel.json.")

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
sitemap_urls = [
    ("https://www.savingstactic.com/", "1.0"),
    ("https://www.savingstactic.com/tools/", "0.9"),
    ("https://www.savingstactic.com/tactics/", "0.9"),
    ("https://www.savingstactic.com/cvs/", "0.9"),
    ("https://www.savingstactic.com/earn/", "0.9"),
    ("https://www.savingstactic.com/blog/", "0.7"),
]

for folder in ["tools", "tactics", "cvs", "earn", "blog"]:
    for filepath in sorted(glob.glob(os.path.join(ROOT, folder, "*.html"))):
        fn = os.path.basename(filepath)
        if fn == "index.html":
            continue
        sitemap_urls.append((f"https://www.savingstactic.com/{folder}/{fn}", "0.8"))

for static_page in ["about.html", "contact.html", "privacy.html", "terms.html"]:
    if os.path.exists(os.path.join(ROOT, static_page)):
        sitemap_urls.append((f"https://www.savingstactic.com/{static_page}", "0.4"))

xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, prio in sitemap_urls:
    xml_lines.append(f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>')
xml_lines.append("</urlset>\n")

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print(f"Rebuilt sitemap.xml with {len(sitemap_urls)} URLs.")
