import os
import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# Scope required for Google Indexing API
SCOPES = ["https://www.googleapis.com/auth/indexing"]

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
    response = requests.post(endpoint, headers=headers, json=body)
    print(f"Indexing request for {url}: {response.status_code} - {response.text}")

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

    print(f"Found {len(urls_to_index)} URLs in sitemap to notify Google.")
    for url in urls_to_index[:200]: # Indexing API limit is 200 per day
        notify_google_indexing(url, token)

if __name__ == "__main__":
    main()
