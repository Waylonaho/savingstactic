import os
import json
import time
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# Scope required for Google Indexing API
SCOPES = ["https://www.googleapis.com/auth/indexing"]
DAILY_LIMIT = 200  # Google Indexing API daily quota limit

def get_access_token(service_account_info):
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def notify_google_indexing(url, access_token):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "url": url,
        "type": "URL_UPDATED"
    }
    try:
        response = requests.post(endpoint, headers=headers, json=body, timeout=10)
        print(f"Indexing request for {url}: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: Failed to submit {url}: {e}")
        return False

def main():
    json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_str:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON environment variable is missing or empty.")
        exit(1)
        
    try:
        service_account_info = json.loads(json_str)
    except Exception as e:
        print(f"ERROR: Failed to parse JSON secret: {e}")
        exit(1)

    token = get_access_token(service_account_info)
    
    # Read sitemap.xml to extract URLs automatically
    urls_to_index = []
    if os.path.exists("sitemap.xml"):
        import xml.etree.ElementTree as ET
        tree = ET.parse("sitemap.xml")
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_elem in root.findall('ns:url', namespace):
            loc = url_elem.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls_to_index.append(loc.text.strip())

    total_found = len(urls_to_index)
    print(f"Found {total_found} URLs in sitemap to notify Google.")
    
    # Process up to the daily limit safely
    batch_to_process = urls_to_index[:DAILY_LIMIT]
    success_count = 0

    for i, url in enumerate(batch_to_process, 1):
        print(f"[{i}/{len(batch_to_process)}] Processing: {url}")
        if notify_google_indexing(url, token):
            success_count += 1
        # Brief pause to prevent rate limiting throttling
        time.sleep(0.2)

    print(f"\n--- Indexing Run Complete ---")
    print(f"Successfully notified Google for {success_count} out of {len(batch_to_process)} URLs.")
    if total_found > DAILY_LIMIT:
        print(f"Note: Sitemap contains {total_found} total URLs. Remaining {total_found - DAILY_LIMIT} URLs will need to roll over into subsequent daily runs.")

if __name__ == "__main__":
    main()
