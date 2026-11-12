import os
import requests
import xml.etree.ElementTree as ET

HOST = "www.savingstactic.com"
API_KEY = "c8a2e79b4d1f46829f0e123456789abc"  # Replace with your 32-char hex key
KEY_LOCATION = f"https://{HOST}/{API_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
DAILY_LIMIT = 10000


def file_path_to_url(filepath):
    clean = filepath.strip().lstrip("./")
    if not clean.endswith(".html"):
        return None
    if clean == "index.html":
        return f"https://{HOST}/"
    if clean.endswith("/index.html"):
        folder = clean[: -len("index.html")]
        return f"https://{HOST}/{folder}"
    return f"https://{HOST}/{clean}"


def get_urls_from_sitemap(sitemap_path="sitemap.xml"):
    urls = []
    if os.path.exists(sitemap_path):
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url_elem in root.findall("ns:url", namespace):
            loc = url_elem.find("ns:loc", namespace)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
    return urls


def submit_indexnow_batch(urls):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    try:
        response = requests.post(INDEXNOW_ENDPOINT, headers=headers, json=payload, timeout=15)
        if response.status_code in [200, 202]:
            print(f"SUCCESS: Submitted {len(urls)} URL(s) to IndexNow (HTTP {response.status_code}).")
        else:
            print(f"FAILURE: IndexNow returned {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: IndexNow request failed: {e}")


def main():
    changed_files_env = os.environ.get("CHANGED_FILES", "").strip()
    deleted_files_env = os.environ.get("DELETED_FILES", "").strip()

    urls = []
    if changed_files_env or deleted_files_env:
        for path in (changed_files_env + "\n" + deleted_files_env).splitlines():
            url = file_path_to_url(path)
            if url and url not in urls:
                urls.append(url)
    else:
        urls = get_urls_from_sitemap("sitemap.xml")

    if not urls:
        print("No HTML URLs to submit to IndexNow.")
        return

    submit_indexnow_batch(urls[:DAILY_LIMIT])


if __name__ == "__main__":
    main()
