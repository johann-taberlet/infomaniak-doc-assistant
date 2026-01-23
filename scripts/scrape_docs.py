#!/usr/bin/env python3
"""
Scrape Infomaniak documentation using BeautifulSoup.
Auto-discovers and extracts clean content from FAQ pages.

Usage:
    uv run python scripts/scrape_docs.py
    uv run python scripts/scrape_docs.py --discover-only  # Just list URLs, don't scrape
"""

import argparse
import re
import time
import httpx
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

OUTPUT_DIR = Path("data/raw")

# Product IDs for Infomaniak FAQ search API
PRODUCTS = {
    "kchat": 54,
    "kmeet": 46,
    "kdrive": 40,
}

# FAQ search API endpoint
FAQ_SEARCH_URL = "https://www.infomaniak.com/en/support/faq/search"


def discover_faq_urls(product: str, product_id: int) -> list[str]:
    """
    Auto-discover all FAQ URLs for a product using the search API.

    Paginates through all pages until no more results.
    """
    urls = []
    page = 1

    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (compatible; InfomaniakDocBot/1.0)",
    }

    while True:
        params = {
            "q": "",  # Empty query = all FAQs
            "p": product_id,
            "hp": 1,
            "c": "",  # All categories
            "i": page,
        }

        try:
            response = httpx.get(FAQ_SEARCH_URL, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"  Error fetching page {page}: {e}")
            break

        # Parse FAQ URLs from HTML response
        soup = BeautifulSoup(response.text, "lxml")
        faq_links = soup.find_all("a", href=re.compile(r"/en/support/faq/\d+/"))

        page_urls = []
        for link in faq_links:
            href = link.get("href", "")
            if href and re.match(r"https://www\.infomaniak\.com/en/support/faq/\d+/", href):
                if href not in urls and href not in page_urls:
                    page_urls.append(href)

        if not page_urls:
            break

        urls.extend(page_urls)
        print(f"  Page {page}: found {len(page_urls)} FAQs (total: {len(urls)})")
        page += 1

        # Rate limiting
        time.sleep(0.3)

    return urls


def discover_all_docs() -> dict[str, list[str]]:
    """Discover all FAQ URLs for all products."""
    docs = {}

    for product, product_id in PRODUCTS.items():
        print(f"\n=== Discovering {product.upper()} FAQs (product_id={product_id}) ===")
        urls = discover_faq_urls(product, product_id)
        docs[product] = urls
        print(f"  Total: {len(urls)} FAQs")

    return docs


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


def scrape_all(docs: dict[str, list[str]], force: bool = False):
    """Scrape all documentation pages."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = sum(len(urls) for urls in docs.values())
    current = 0
    scraped = 0
    skipped = 0
    failed = 0

    for product, urls in docs.items():
        product_dir = OUTPUT_DIR / product
        product_dir.mkdir(exist_ok=True)

        print(f"\n=== Scraping {product.upper()} ({len(urls)} pages) ===")

        for url in urls:
            current += 1
            filename = url_to_filename(url, product)
            filepath = product_dir / filename

            # Skip if already scraped (unless force)
            if filepath.exists() and not force:
                print(f"[{current}/{total}] Skipping (exists): {filename}")
                skipped += 1
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
                scraped += 1
            else:
                print(f"  Failed to scrape")
                failed += 1

            # Rate limiting
            time.sleep(0.5)

    print(f"\n=== Done! ===")
    print(f"  Scraped: {scraped}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed:  {failed}")
    print(f"  Output:  {OUTPUT_DIR}")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Scrape Infomaniak FAQ documentation"
    )
    parser.add_argument(
        "--discover-only",
        action="store_true",
        help="Only discover FAQ URLs, don't scrape content",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-scrape even if files already exist",
    )
    parser.add_argument(
        "--product",
        choices=list(PRODUCTS.keys()),
        help="Only scrape a specific product",
    )
    args = parser.parse_args()

    # Filter products if specified
    products = {args.product: PRODUCTS[args.product]} if args.product else PRODUCTS

    # Discover FAQs
    print("=== Auto-discovering FAQ URLs ===")
    docs = {}
    for product, product_id in products.items():
        print(f"\n--- {product.upper()} (product_id={product_id}) ---")
        urls = discover_faq_urls(product, product_id)
        docs[product] = urls
        print(f"  Found: {len(urls)} FAQs")

    total = sum(len(urls) for urls in docs.values())
    print(f"\n=== Total: {total} FAQs discovered ===")

    if args.discover_only:
        print("\n=== FAQ URLs ===")
        for product, urls in docs.items():
            print(f"\n{product.upper()}:")
            for url in urls:
                print(f"  {url}")
        return

    # Scrape content
    scrape_all(docs, force=args.force)


if __name__ == "__main__":
    main()
