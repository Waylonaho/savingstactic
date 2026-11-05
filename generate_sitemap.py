import os
from datetime import datetime
import xml.etree.ElementTree as ET

BLOG_DIR = "blog"
SITEMAP_PATH = "sitemap.xml"

# Base URL of your site
BASE_URL = "https://www.savingstactic.com"

def generate_sitemap():
    urls = []
    
    # Add core static pages
    core_pages = [
        ("/", datetime.today().strftime('%Y-%m-%d')),
        ("/privacy.html", "2026-10-29"),
        ("/terms.html", "2026-10-17")
    ]
    
    for path, lastmod in core_pages:
        urls.append((f"{BASE_URL}{path}", lastmod))
        
    # Scan blog folder for HTML files
    if os.path.exists(BLOG_DIR):
        for filename in os.listdir(BLOG_DIR):
            if filename.endswith(".html"):
                file_path = os.path.join(BLOG_DIR, filename)
                # Get the file's last modified time from git or file system
                mtime = os.path.getmtime(file_path)
                lastmod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
                page_url = f"{BASE_URL}/blog/{filename}"
                urls.append((page_url, lastmod_date))

    # Build XML structure manually to maintain clean formatting
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    
    for url, lastmod in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url}</loc>\n'
        xml_content += f'    <lastmod>{lastmod}</lastmod>\n'
        xml_content += '  </url>\n'
        
    xml_content += '</urlset>'

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Sitemap successfully generated and updated!")

if __name__ == "__main__":
    generate_sitemap()
