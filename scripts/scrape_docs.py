#!/usr/bin/env python3
"""
Scrape Infomaniak documentation using Jina Reader API.
Converts web pages to clean markdown.

Usage:
    export JINA_API_KEY="your_key_here"
    python scripts/scrape_docs.py
"""

import os
import re
import time
import httpx
from pathlib import Path

JINA_API_KEY = os.environ.get("JINA_API_KEY")
OUTPUT_DIR = Path("data/docs")
JINA_BASE_URL = "https://r.jina.ai"

# Documentation URLs organized by product
DOCS = {
    "kchat": [
        "https://www.infomaniak.com/en/support/faq/2076/getting-started-kchat",
        "https://www.infomaniak.com/en/support/faq/2001/connect-external-applications-to-kchat",
        "https://www.infomaniak.com/en/support/faq/1467/translate-the-content-of-a-message-on-the-kchat-infomaniak-app",
        "https://www.infomaniak.com/en/support/faq/2244/create-an-event-reminder-via-webhooks-with-the-web-calendar-app-infomaniak",
        "https://www.infomaniak.com/en/support/faq/1886/manage-kchat-members",
        "https://www.infomaniak.com/en/support/faq/1190/manage-emoticons-and-gifs-on-kchat",
        "https://www.infomaniak.com/en/support/faq/2480/use-euria-on-kchat-summarize-a-discussion",
        "https://www.infomaniak.com/en/support/faq/1758/manage-kchat-conversations",
        "https://www.infomaniak.com/en/support/faq/144/download-and-install-kchat",
        "https://www.infomaniak.com/en/support/faq/1622/receive-your-daily-schedule-by-email-or-kchat",
        "https://www.infomaniak.com/en/support/faq/2732/manage-a-kchat-channel",
        "https://www.infomaniak.com/en/support/faq/2733/understanding-kchat-data-security",
        "https://www.infomaniak.com/en/support/faq/1455/invite-a-user-to-use-kchat",
        "https://www.infomaniak.com/en/support/faq/2870/manage-dark-mode",
        "https://www.infomaniak.com/en/support/faq/1407/format-text-image-on-kchat",
        "https://www.infomaniak.com/en/support/faq/2827/create-a-kmeet-meeting-from-kchat",
        "https://www.infomaniak.com/en/support/faq/2840/use-euria-on-kchat-conversational-agent",
        "https://www.infomaniak.com/en/support/faq/1460/manage-kchat-notifications",
        "https://www.infomaniak.com/en/support/faq/2134/using-kchat-slash-commands",
        "https://www.infomaniak.com/en/support/faq/2734/customize-kchat",
        "https://www.infomaniak.com/en/support/faq/2846/invite-an-external-user-to-use-kchat",
    ],
    "kmeet": [
        "https://www.infomaniak.com/en/support/faq/2474/getting-started-guide-kmeet",
        "https://www.infomaniak.com/en/support/faq/2475/create-a-kmeet-meeting",
        "https://www.infomaniak.com/en/support/faq/2452/resolve-a-video-issue-on-kmeet",
        "https://www.infomaniak.com/en/support/faq/289/solving-a-problem-on-kmeet",
        "https://www.infomaniak.com/en/support/faq/2441/fix-an-audio-issue-on-kmeet",
        "https://www.infomaniak.com/en/support/faq/2473/join-a-kmeet-meeting",
        "https://www.infomaniak.com/en/support/faq/2472/save-a-kmeet-meeting-on-kdrive",
        "https://www.infomaniak.com/en/support/faq/2477/share-your-screen-on-kmeet",
        "https://www.infomaniak.com/en/support/faq/2397/create-a-kmeet-meeting-side-room",
        "https://www.infomaniak.com/en/support/faq/1431/transcribe-a-kmeet-meeting-in-real-time-automatic-subtitles",
        "https://www.infomaniak.com/en/support/faq/2476/manage-kmeet-participants",
        "https://www.infomaniak.com/en/support/faq/2478/discuss-during-a-kmeet-meeting",
        "https://www.infomaniak.com/en/support/faq/1355/broadcast-a-kmeet-meeting-via-live-streaming-mode",
        "https://www.infomaniak.com/en/support/faq/2622/remotely-control-a-device-with-kmeet",
        "https://www.infomaniak.com/en/support/faq/2464/secure-a-kmeet-meeting-with-a-password-and-encryption-key",
        "https://www.infomaniak.com/en/support/faq/2620/draw-on-kmeet",
        "https://www.infomaniak.com/en/support/faq/2890/replace-skype-with-infomaniak",
    ],
    "kdrive": [
        "https://www.infomaniak.com/en/support/faq/2366/getting-started-guide-kdrive",
        "https://www.infomaniak.com/en/support/faq/2374/sync-kdrive-across-different-devices",
        "https://www.infomaniak.com/en/support/faq/2410/understanding-kdrive-folders-personal-shared-common",
        "https://www.infomaniak.com/en/support/faq/617/install-kdrive-on-linux",
        "https://www.infomaniak.com/en/support/faq/2454/manage-the-folders-to-sync-on-kdrive",
        "https://www.infomaniak.com/en/support/faq/2562/manage-the-lite-sync-kdrive-option-windows",
        "https://www.infomaniak.com/en/support/faq/2456/access-kdrive-files-locally-and-online",
        "https://www.infomaniak.com/en/support/faq/2382/share-data-from-the-kdrive-web-app",
        "https://www.infomaniak.com/en/support/faq/2386/manage-kdrive-drop-boxes",
        "https://www.infomaniak.com/en/support/faq/1633/manage-a-users-rights-within-an-organization",
        "https://www.infomaniak.com/en/support/faq/1610/manage-a-organization-users-product-access",
        "https://www.infomaniak.com/en/support/faq/2406/import-external-data-to-kdrive",
        "https://www.infomaniak.com/en/support/faq/2394/import-photos-to-the-kdrive-mobile-app-ios",
        "https://www.infomaniak.com/en/support/faq/2024/transfer-a-product-from-one-organization-to-another",
        "https://www.infomaniak.com/en/support/faq/2153/fix-a-kdrive-synchronization-issue",
        "https://www.infomaniak.com/en/support/faq/2403/resolve-a-kdrive-synchronization-conflict",
        "https://www.infomaniak.com/en/support/faq/1822/resolve-a-kdrive-block-antivirus-firewall-etc",
        "https://www.infomaniak.com/en/support/faq/2685/fixing-an-unrecognized-device-error",
        "https://www.infomaniak.com/en/support/faq/2364/manage-kdrive-users",
        "https://www.infomaniak.com/en/support/faq/2365/manage-a-kdrive-users-rights",
        "https://www.infomaniak.com/en/support/faq/1793/manage-sharing-of-the-common-folder-on-kdrive",
        "https://www.infomaniak.com/en/support/faq/2404/sync-synology-with-kdrive",
    ],
}


def url_to_filename(url: str, product: str) -> str:
    """Convert URL to a safe filename."""
    # Extract the slug from URL (last part after the ID)
    match = re.search(r"/faq/(\d+)/(.+)$", url)
    if match:
        faq_id, slug = match.groups()
        return f"{product}_{faq_id}_{slug}.md"
    return f"{product}_{hash(url)}.md"


def fetch_with_jina(url: str) -> str | None:
    """Fetch a URL using Jina Reader API and return markdown content."""
    jina_url = f"{JINA_BASE_URL}/{url}"
    headers = {}
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"

    try:
        response = httpx.get(jina_url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as e:
        print(f"  Error fetching {url}: {e}")
        return None


def scrape_all():
    """Scrape all documentation pages."""
    if not JINA_API_KEY:
        print("Warning: JINA_API_KEY not set. Using Jina without authentication (rate limited).")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = sum(len(urls) for urls in DOCS.values())
    current = 0

    for product, urls in DOCS.items():
        product_dir = OUTPUT_DIR / product
        product_dir.mkdir(exist_ok=True)

        print(f"\n=== Scraping {product.upper()} ({len(urls)} pages) ===")

        for url in urls:
            current += 1
            filename = url_to_filename(url, product)
            filepath = product_dir / filename

            # Skip if already scraped
            if filepath.exists():
                print(f"[{current}/{total}] Skipping (exists): {filename}")
                continue

            print(f"[{current}/{total}] Fetching: {filename}")
            content = fetch_with_jina(url)

            if content:
                # Add source URL as metadata at the top
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"<!-- source: {url} -->\n\n")
                    f.write(content)
                print(f"  Saved: {filepath}")
            else:
                print(f"  Failed to fetch")

            # Rate limiting - be nice to Jina API
            time.sleep(1.0)

    print(f"\n=== Done! Scraped {current} pages to {OUTPUT_DIR} ===")


if __name__ == "__main__":
    scrape_all()
