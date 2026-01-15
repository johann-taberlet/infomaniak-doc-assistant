#!/usr/bin/env python3
"""
Scrape Infomaniak documentation using BeautifulSoup.
Extracts clean content from FAQ pages.

Usage:
    uv run python scripts/scrape_docs.py
"""

import re
import time
import httpx
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

OUTPUT_DIR = Path("data/docs")

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
    match = re.search(r"/faq/(\d+)/(.+)$", url)
    if match:
        faq_id, slug = match.groups()
        return f"{product}_{faq_id}_{slug}.md"
    return f"{product}_{hash(url)}.md"


def html_to_markdown(element) -> str:
    """Convert BeautifulSoup element to clean markdown."""
    if element is None:
        return ""

    lines = []

    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                lines.append(text)
            continue

        tag = child.name

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            text = child.get_text(strip=True)
            if text and text != "\xa0":  # Skip empty headers
                lines.append(f"\n{'#' * level} {text}\n")

        elif tag == "p":
            text = process_inline(child)
            if text.strip():
                lines.append(f"\n{text}\n")

        elif tag == "ul":
            for li in child.find_all("li", recursive=False):
                text = process_inline(li)
                if text.strip():
                    lines.append(f"- {text}")
            lines.append("")

        elif tag == "ol":
            for i, li in enumerate(child.find_all("li", recursive=False), 1):
                text = process_inline(li)
                if text.strip():
                    lines.append(f"{i}. {text}")
            lines.append("")

        elif tag == "div":
            # Handle info/alert boxes
            if "alert" in child.get("class", []):
                inner_text = process_inline(child)
                if inner_text.strip():
                    lines.append(f"\n> **Note:** {inner_text}\n")
            else:
                # Recurse into other divs
                inner = html_to_markdown(child)
                if inner.strip():
                    lines.append(inner)

        elif tag == "img":
            src = child.get("src", "")
            alt = child.get("alt", "image")
            if src:
                lines.append(f"\n![{alt}]({src})\n")

        elif tag == "br":
            lines.append("\n")

        elif tag == "a":
            href = child.get("href", "")
            text = child.get_text(strip=True)
            if href and text:
                lines.append(f"[{text}]({href})")

        elif tag == "strong" or tag == "b":
            text = child.get_text(strip=True)
            if text:
                lines.append(f"**{text}**")

        elif tag == "em" or tag == "i":
            text = child.get_text(strip=True)
            if text:
                lines.append(f"*{text}*")

        elif tag == "code":
            text = child.get_text(strip=True)
            if text:
                lines.append(f"`{text}`")

        elif tag == "pre":
            text = child.get_text()
            lines.append(f"\n```\n{text}\n```\n")

        elif tag == "table":
            lines.append(process_table(child))

        elif tag in ("span", "section"):
            # Process inline or recurse
            inner = process_inline(child)
            if inner.strip():
                lines.append(inner)

    result = "\n".join(lines)
    # Clean up excessive newlines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def process_inline(element) -> str:
    """Process inline elements and return text."""
    if element is None:
        return ""

    parts = []

    for child in element.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
            continue

        tag = child.name

        if tag == "a":
            href = child.get("href", "")
            text = child.get_text(strip=True)
            if href and text:
                # Clean up internal FAQ links
                if "faq.infomaniak.com" in href:
                    href = href.replace("https://faq.infomaniak.com/", "https://www.infomaniak.com/en/support/faq/")
                parts.append(f"[{text}]({href})")
            elif text:
                parts.append(text)

        elif tag in ("strong", "b"):
            text = child.get_text(strip=True)
            if text:
                parts.append(f"**{text}**")

        elif tag in ("em", "i"):
            text = child.get_text(strip=True)
            if text:
                parts.append(f"*{text}*")

        elif tag == "code":
            text = child.get_text(strip=True)
            if text:
                parts.append(f"`{text}`")

        elif tag == "br":
            parts.append("\n")

        elif tag == "img":
            src = child.get("src", "")
            alt = child.get("alt", "image")
            if src:
                parts.append(f"\n![{alt}]({src})\n")

        elif tag in ("span", "div", "li", "p"):
            # Recurse
            inner = process_inline(child)
            if inner:
                parts.append(inner)

        else:
            # Fallback: just get text
            text = child.get_text()
            if text:
                parts.append(text)

    return "".join(parts)


def process_table(table) -> str:
    """Convert HTML table to markdown table."""
    rows = []
    headers = []

    # Find header row
    thead = table.find("thead")
    if thead:
        for th in thead.find_all("th"):
            headers.append(th.get_text(strip=True))

    # If no thead, check first row
    if not headers:
        first_row = table.find("tr")
        if first_row:
            ths = first_row.find_all("th")
            if ths:
                headers = [th.get_text(strip=True) for th in ths]

    # Process body rows
    tbody = table.find("tbody") or table
    for tr in tbody.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if cells:
            row = [cell.get_text(strip=True) for cell in cells]
            # Skip if this is the header row we already processed
            if row != headers:
                rows.append(row)

    if not headers and rows:
        headers = rows.pop(0)

    if not headers:
        return ""

    # Build markdown table
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        # Pad row if needed
        while len(row) < len(headers):
            row.append("")
        lines.append("| " + " | ".join(row[:len(headers)]) + " |")

    return "\n" + "\n".join(lines) + "\n"


def scrape_page(url: str) -> tuple[str, str] | None:
    """Scrape a single FAQ page and return (title, content)."""
    try:
        response = httpx.get(url, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"  Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    # Extract title
    title_el = soup.find("h1", class_="question_faq")
    title = title_el.get_text(strip=True) if title_el else "Untitled"

    # Extract FAQ body content
    faq_body = soup.find("div", class_="faq-body")
    if not faq_body:
        print(f"  No faq-body found in {url}")
        return None

    # Remove the "Link to this FAQ" section at the end
    for div in faq_body.find_all("div"):
        if div.find("strong") and "Link to this FAQ" in div.get_text():
            div.decompose()

    # Remove product icon
    for icon in faq_body.find_all("i", class_="sprite-support-22"):
        icon.decompose()
    for pull_right in faq_body.find_all("div", class_="pull-right"):
        pull_right.decompose()
    for clear in faq_body.find_all("div", class_="clear"):
        clear.decompose()

    # Convert to markdown
    content = html_to_markdown(faq_body)

    return title, content


def scrape_all():
    """Scrape all documentation pages."""
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
            result = scrape_page(url)

            if result:
                title, content = result
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"Source: {url}\n\n")
                    f.write("---\n\n")
                    f.write(content)
                print(f"  Saved: {filepath}")
            else:
                print(f"  Failed to scrape")

            # Rate limiting
            time.sleep(0.5)

    print(f"\n=== Done! Scraped {current} pages to {OUTPUT_DIR} ===")


if __name__ == "__main__":
    scrape_all()
