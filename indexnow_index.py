import os
import json
import time
import requests
import xml.etree.ElementTree as ET

# Configuration
HOST = "www.savingstactic.com"
API_KEY = "c8a2e79b4d1f46829f0e123456789abc
"  # Replace with your 32-char key
KEY_LOCATION = f"https://{HOST}/{API_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
DAILY_LIMIT = 10000  # IndexNow bulk limit


def get_urls_from_sitemap(sitemap_path="sitemap.xml"):
    urls = []
    if os.path.exists(sitemap_path):
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for url_elem in root.findall('ns:url', namespace):
                loc = url_elem.find('ns:loc', namespace)
                if loc is not None and loc.text:
                    urls.append(loc.text.strip())
        except Exception as e:
            print(f"ERROR: Failed to parse {sitemap_path}: {e}")
    return urls


def submit_indexnow_batch(urls):
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }

    try:
        response = requests.post(INDEXNOW_ENDPOINT, headers=headers, json=payload, timeout=15)
        
        if response.status_code in [200, 202]:
            print(f"SUCCESS: Submitted {len(urls)} URLs to IndexNow (Status Code: {response.status_code}).")
            return True
        else:
            print(f"FAILURE: IndexNow returned {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Request to IndexNow failed: {e}")
        return False


def main():
    urls_to_submit = get_urls_from_sitemap("sitemap.xml")
    total_found = len(urls_to_submit)

    if not urls_to_submit:
        print("No URLs found in sitemap.xml to submit.")
        return

    print(f"Found {total_found} URLs in sitemap for IndexNow submission.")
    
    batch = urls_to_submit[:DAILY_LIMIT]
    submit_indexnow_batch(batch)


if __name__ == "__main__":
    main()
