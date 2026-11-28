import os
import sys
import json
import time
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
import google.auth.transport.requests

SCOPES = ["https://www.googleapis.com/auth/indexing"]
DAILY_LIMIT = 200
SITE_ORIGIN = "https://www.savingstactic.com"


def get_access_token(service_account_info):
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def file_path_to_url(filepath):
    clean = filepath.strip().lstrip("./")
    if not clean.endswith(".html"):
        return None
    if clean == "index.html":
        return f"{SITE_ORIGIN}/"
    if clean.endswith("/index.html"):
        folder = clean[: -len("index.html")]
        return f"{SITE_ORIGIN}/{folder}"
    return f"{SITE_ORIGIN}/{clean}"


def get_urls_from_sitemap(sitemap_path="sitemap.xml"):
    urls = []
    if os.path.exists(sitemap_path):
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url_elem in root.findall("ns:url", namespace):
            loc = url_elem.find("ns:loc", namespace)
            if loc is not None and loc.text:
                urls.append((loc.text.strip(), "URL_UPDATED"))
    return urls


def notify_google_indexing(url, action_type, access_token):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = {"url": url, "type": action_type}
    try:
        response = requests.post(endpoint, headers=headers, json=body, timeout=10)
        print(f"[{action_type}] {url} -> {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR submitting {url}: {e}")
        return False


def main():
    json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_str:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON environment variable is missing.")
        sys.exit(1)

    service_account_info = json.loads(json_str)
    token = get_access_token(service_account_info)

    tasks = []
    changed_files_env = os.environ.get("CHANGED_FILES", "").strip()
    deleted_files_env = os.environ.get("DELETED_FILES", "").strip()

    if changed_files_env or deleted_files_env:
        for path in changed_files_env.splitlines():
            url = file_path_to_url(path)
            if url:
                tasks.append((url, "URL_UPDATED"))
        for path in deleted_files_env.splitlines():
            url = file_path_to_url(path)
            if url:
                tasks.append((url, "URL_DELETED"))
    else:
        print("No git diff list detected (manual run) — falling back to sitemap.xml.")
        tasks = get_urls_from_sitemap("sitemap.xml")

    # Deduplicate while preserving order
    seen = set()
    unique_tasks = []
    for item in tasks:
        if item not in seen:
            seen.add(item)
            unique_tasks.append(item)

    if not unique_tasks:
        print("No HTML URLs changed or deleted in this commit. Skipping Google Indexing.")
        return

    batch = unique_tasks[:DAILY_LIMIT]
    print(f"Submitting {len(batch)} changed/deleted URL(s) to Google Indexing API...")
    success = sum(1 for url, action in batch if notify_google_indexing(url, action, token) and not time.sleep(0.2))
    print(f"Done. Successfully notified Google for {success}/{len(batch)} URL(s).")


if __name__ == "__main__":
    main()
