#!/usr/bin/env python3
"""
Clean scraped documentation files for better RAG quality.

Removes:
- Image markdown (screenshots not useful for LLM)
- Tracking URLs (infomaniak.com/gtl/...)
- Boilerplate sections (feedback, contact support)
- Incomplete warnings without values
- Empty lines and formatting issues

Usage:
    uv run python scripts/clean_docs.py
"""

import re
from pathlib import Path

DOCS_DIR = Path("data/docs")


def clean_content(content: str) -> str:
    """Clean markdown content for RAG."""

    # 1. Remove image markdown completely
    # ![alt](url) or ![](url)
    content = re.sub(r'!\[.*?\]\([^)]+\)\n*', '', content)

    # 2. Remove tracking URLs but keep link text
    # [text](https://infomaniak.com/gtl/...) -> text
    content = re.sub(r'\[([^\]]+)\]\(https?://infomaniak\.com/gtl/[^)]+\)', r'\1', content)

    # 3. Remove incomplete warning lines (no value after colon)
    # "**⚠ Max. number of...:**" with nothing after
    content = re.sub(r'\*\*⚠[^*]+:\*\*\s*\n', '', content)

    # 4. Remove boilerplate "question or feedback" sections
    patterns_to_remove = [
        r'##?\s*A question or feedback\?\n.*?(?=\n##|\n---|\Z)',
        r'##?\s*Une question ou un retour\s*\?\n.*?(?=\n##|\n---|\Z)',
        r'-\s*In case of a problem.*?contacting support.*?\.\n',
        r'-\s*\[Click here\].*?share feedback.*?product\.\n?',
        r'-\s*\[Contact.*?support\].*?\n',
    ]
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

    # 5. Clean up faq.infomaniak.com short URLs to full URLs
    content = re.sub(
        r'\[([^\]]+)\]\(https://faq\.infomaniak\.com/(\d+)\)',
        r'[\1](https://www.infomaniak.com/en/support/faq/\2)',
        content
    )

    # 6. Fix spacing issues
    # "word!Another" -> "word! Another"
    content = re.sub(r'([.!?])([A-Z])', r'\1 \2', content)

    # "word…… another" -> "word... another" (normalize ellipsis)
    content = re.sub(r'…+', '...', content)

    # 7. Remove empty list items
    content = re.sub(r'^-\s*\n', '', content, flags=re.MULTILINE)

    # 8. Remove lines that are just whitespace or dashes
    content = re.sub(r'^\s*-\s*$', '', content, flags=re.MULTILINE)

    # 9. Clean up excessive newlines (more than 2)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 10. Remove trailing whitespace on lines
    content = re.sub(r' +$', '', content, flags=re.MULTILINE)

    # 11. Ensure file ends with single newline
    content = content.strip() + '\n'

    return content


def clean_all_files():
    """Clean all markdown files in docs directory."""

    if not DOCS_DIR.exists():
        print(f"Error: {DOCS_DIR} does not exist")
        return

    md_files = list(DOCS_DIR.glob("**/*.md"))
    print(f"Found {len(md_files)} markdown files to clean\n")

    stats = {
        "files_processed": 0,
        "bytes_before": 0,
        "bytes_after": 0,
        "images_removed": 0,
    }

    for filepath in sorted(md_files):
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()

        # Count images before cleaning
        images_count = len(re.findall(r'!\[.*?\]\([^)]+\)', original))
        stats["images_removed"] += images_count

        cleaned = clean_content(original)

        stats["bytes_before"] += len(original.encode('utf-8'))
        stats["bytes_after"] += len(cleaned.encode('utf-8'))
        stats["files_processed"] += 1

        # Only write if changed
        if cleaned != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned)

            reduction = len(original) - len(cleaned)
            print(f"Cleaned: {filepath.name} (-{reduction} chars, -{images_count} images)")
        else:
            print(f"No changes: {filepath.name}")

    # Print summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Images removed: {stats['images_removed']}")
    print(f"  Size before: {stats['bytes_before']:,} bytes")
    print(f"  Size after: {stats['bytes_after']:,} bytes")
    reduction_pct = (1 - stats['bytes_after'] / stats['bytes_before']) * 100 if stats['bytes_before'] > 0 else 0
    print(f"  Reduction: {reduction_pct:.1f}%")


if __name__ == "__main__":
    clean_all_files()
