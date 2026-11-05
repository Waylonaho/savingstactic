import os
from datetime import datetime
import re

BLOG_DIR = "blog"
SITEMAP_PATH = "sitemap.xml"
BASE_URL = "https://www.savingstactic.com"

def minify_html(content):
    # Simple, safe regex-based HTML minification (removes comments and extra spaces)
    content = re.sub(r'<!--(?!\s*(?:\[if [^\]]+]|<!|>))(?:(?!-->).)*-->', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+', ' ', content)
    # Restore spacing around tags to prevent layout breakdown
    content = content.replace('> <', '><')
    return content

def generate_sitemap_and_optimize():
    urls = [
        (f"{BASE_URL}/", datetime.today().strftime('%Y-%m-%d')),
        (f"{BASE_URL}/privacy.html", "2026-10-29"),
        (f"{BASE_URL}/terms.html", "2026-10-17")
    ]
    
    if os.path.exists(BLOG_DIR):
        for filename in os.listdir(BLOG_DIR):
            if filename.endswith(".html"):
                file_path = os.path.join(BLOG_DIR, filename)
                
                # Optional: Minify the HTML file in place
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                # Keep critical tags intact, minify whitespace safely
                minified = html_content.strip() # Keeps file fully intact while cleaning outer whitespace
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(minified)

                # Get modification timestamp for sitemap
                mtime = os.path.getmtime(file_path)
                lastmod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                urls.append((f"{BASE_URL}/blog/{filename}", lastmod_date))

    # Build XML sitemap
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    
    for url, lastmod in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url}</loc>\n'
        xml_content += f'    <lastmod>{lastmod}</lastmod>\n'
        xml_content  += '  </url>\n'
        
    xml_content += '</urlset>'

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Sitemap generated and HTML files optimized successfully!")

if __name__ == "__main__":
    generate_sitemap_and_optimize()
