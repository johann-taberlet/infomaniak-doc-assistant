#!/usr/bin/env python3
"""
Clean scraped documentation for optimal RAG performance.

Produces two datasets for comparison:
1. data/cleaned/ - Images inline (simple approach)
2. data/cleaned_no_images/ - Images extracted as structured metadata

Usage:
    uv run python scripts/clean_docs.py
    uv run python scripts/clean_docs.py --dry-run  # Preview changes
"""

import argparse
import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict

INPUT_DIR = Path("data/raw")
OUTPUT_INLINE = Path("data/cleaned")
OUTPUT_STRUCTURED = Path("data/cleaned_no_images")


@dataclass
class ExtractedImage:
    """Structured image metadata."""
    url: str
    heading: str  # Parent heading (## Section)
    step: int | None  # Step number if in ordered list
    context: str  # Surrounding text (truncated)


def clean_text(content: str) -> str:
    """Clean document text while preserving structure."""

    # 1. Remove zero-width characters and other invisible Unicode
    invisible_chars = [
        '\u200b',  # Zero-width space
        '\u200c',  # Zero-width non-joiner
        '\u200d',  # Zero-width joiner
        '\u200e',  # Left-to-right mark
        '\u200f',  # Right-to-left mark
        '\u2060',  # Word joiner
        '\ufeff',  # BOM
    ]
    for char in invisible_chars:
        content = content.replace(char, '')

    # Replace non-breaking space with regular space
    content = content.replace('\xa0', ' ')

    # 2. Fix common scraping artifacts (stuck words)
    # Pattern: lowercase letter directly followed by uppercase (missing space)
    content = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', content)
    # Pattern: word ending with ] directly followed by word (missing space after link)
    content = re.sub(r'\]([A-Za-z])', r'] \1', content)
    # Pattern: period/colon directly followed by uppercase (missing space)
    content = re.sub(r'([.:])([A-Z])', r'\1 \2', content)

    # 3. Remove trailing whitespace from each line
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]

    # 4. Remove orphan punctuation lines
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in (':', '-', '*', '•', '>', '|'):
            continue
        if re.match(r'^\s*:\s*$', line):
            continue
        cleaned_lines.append(line)

    # 5. Collapse multiple blank lines into maximum of 2
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 6. Remove blank lines at start/end
    content = content.strip()

    return content


def extract_images_with_context(content: str) -> tuple[str, list[ExtractedImage]]:
    """
    Extract images from content and return (content_without_images, image_metadata).

    Preserves context by tracking:
    - Parent heading
    - Step number (if in ordered list)
    - Surrounding text
    """
    images: list[ExtractedImage] = []
    lines = content.split('\n')

    current_heading = ""
    current_step = None
    result_lines = []

    # Track if we're inside an ordered list
    step_pattern = re.compile(r'^(\d+)\.\s')
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Update current heading
        heading_match = heading_pattern.match(line)
        if heading_match:
            current_heading = heading_match.group(2).strip()
            current_step = None  # Reset step when new heading
            result_lines.append(line)
            i += 1
            continue

        # Check for step number
        step_match = step_pattern.match(line)
        if step_match:
            current_step = int(step_match.group(1))

        # Extract images from this line
        image_matches = list(image_pattern.finditer(line))

        if image_matches:
            # Get context: combine previous non-empty line + current line (without image)
            context_parts = []
            if result_lines:
                # Find last non-empty line for context
                for prev_line in reversed(result_lines[-3:]):
                    if prev_line.strip() and not prev_line.startswith('#'):
                        context_parts.append(prev_line.strip()[:100])
                        break

            # Add current line text (without image markdown)
            line_text = image_pattern.sub('', line).strip()
            if line_text:
                context_parts.append(line_text[:100])

            context = ' | '.join(context_parts)

            for match in image_matches:
                alt_text = match.group(1)
                url = match.group(2)

                images.append(ExtractedImage(
                    url=url,
                    heading=current_heading,
                    step=current_step,
                    context=context[:200]  # Truncate context
                ))

            # Remove images from line
            cleaned_line = image_pattern.sub('', line)
            # Clean up resulting empty list items or trailing colons
            cleaned_line = re.sub(r':\s*$', '', cleaned_line.rstrip())
            if cleaned_line.strip() and cleaned_line.strip() not in (':', '-'):
                result_lines.append(cleaned_line)
        else:
            result_lines.append(line)

        i += 1

    # Clean up the result
    content_without_images = '\n'.join(result_lines)
    # Remove empty list items that only contained images
    content_without_images = re.sub(r'^\d+\.\s*$', '', content_without_images, flags=re.MULTILINE)
    content_without_images = re.sub(r'\n{3,}', '\n\n', content_without_images)

    return content_without_images.strip(), images


def extract_metadata(content: str) -> dict:
    """Extract document metadata."""
    metadata = {
        'title': '',
        'source_url': '',
        'product': '',
        'faq_id': '',
    }

    lines = content.split('\n')

    # Extract title
    for line in lines:
        if line.startswith('# '):
            metadata['title'] = line[2:].strip()
            break

    # Extract source URL and FAQ ID
    for line in lines:
        if line.startswith('Source:'):
            url = line.replace('Source:', '').strip()
            metadata['source_url'] = url
            # Extract FAQ ID from URL
            match = re.search(r'/faq/(\d+)/', url)
            if match:
                metadata['faq_id'] = match.group(1)
            break

    # Infer product
    source = metadata['source_url'].lower()
    title = metadata['title'].lower()
    if 'kdrive' in source or 'kdrive' in title:
        metadata['product'] = 'kdrive'
    elif 'kmeet' in source or 'kmeet' in title:
        metadata['product'] = 'kmeet'
    elif 'kchat' in source or 'kchat' in title:
        metadata['product'] = 'kchat'

    return metadata


def process_file(input_path: Path, dry_run: bool = False) -> dict:
    """Process a single file and return stats."""
    content = input_path.read_text(encoding='utf-8')
    original_length = len(content)

    # Extract metadata
    metadata = extract_metadata(content)

    # Count original images
    original_images = len(re.findall(r'!\[.*?\]\(.*?\)', content))

    # === Dataset 1: Images inline (just text cleaning) ===
    cleaned_inline = clean_text(content)

    # === Dataset 2: Images extracted as metadata ===
    cleaned_no_images, extracted_images = extract_images_with_context(content)
    cleaned_no_images = clean_text(cleaned_no_images)

    stats = {
        'path': str(input_path),
        'original_length': original_length,
        'cleaned_inline_length': len(cleaned_inline),
        'cleaned_no_images_length': len(cleaned_no_images),
        'original_images': original_images,
        'extracted_images': len(extracted_images),
        **metadata,
    }

    if not dry_run:
        relative_path = input_path.relative_to(INPUT_DIR)

        # Write inline version
        inline_path = OUTPUT_INLINE / relative_path
        inline_path.parent.mkdir(parents=True, exist_ok=True)
        inline_path.write_text(cleaned_inline, encoding='utf-8')

        # Write no-images version
        no_images_path = OUTPUT_STRUCTURED / relative_path
        no_images_path.parent.mkdir(parents=True, exist_ok=True)
        no_images_path.write_text(cleaned_no_images, encoding='utf-8')

        # Write image metadata as JSON sidecar
        if extracted_images:
            json_path = no_images_path.with_suffix('.images.json')
            image_data = {
                'faq_id': metadata['faq_id'],
                'title': metadata['title'],
                'source_url': metadata['source_url'],
                'images': [asdict(img) for img in extracted_images]
            }
            json_path.write_text(json.dumps(image_data, indent=2), encoding='utf-8')

    return stats


def main():
    parser = argparse.ArgumentParser(description="Clean scraped documentation for RAG")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without writing")
    args = parser.parse_args()

    print("=== Cleaning Documentation ===")
    print(f"Input:    {INPUT_DIR}")
    print(f"Output 1: {OUTPUT_INLINE} (images inline)")
    print(f"Output 2: {OUTPUT_STRUCTURED} (images as metadata)")
    print(f"Mode:     {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    all_stats = []
    total_images_extracted = 0

    for product_dir in sorted(INPUT_DIR.iterdir()):
        if not product_dir.is_dir():
            continue

        print(f"\n--- {product_dir.name.upper()} ---")
        product_stats = {'docs': 0, 'images': 0}

        for md_file in sorted(product_dir.glob("*.md")):
            stats = process_file(md_file, dry_run=args.dry_run)
            all_stats.append(stats)
            product_stats['docs'] += 1
            product_stats['images'] += stats['extracted_images']

            if stats['extracted_images'] > 0:
                print(f"  {md_file.name}: {stats['extracted_images']} images extracted")

        print(f"  Total: {product_stats['docs']} docs, {product_stats['images']} images")
        total_images_extracted += product_stats['images']

    # Summary
    print(f"\n=== Summary ===")
    print(f"Total documents: {len(all_stats)}")
    print(f"Total images extracted: {total_images_extracted}")

    total_original = sum(s['original_length'] for s in all_stats)
    total_inline = sum(s['cleaned_inline_length'] for s in all_stats)
    total_no_images = sum(s['cleaned_no_images_length'] for s in all_stats)

    print(f"\nSize comparison:")
    print(f"  Raw:              {total_original:,} chars")
    print(f"  Cleaned (inline): {total_inline:,} chars ({(total_original-total_inline)/total_original*100:.1f}% reduction)")
    print(f"  Cleaned (no img): {total_no_images:,} chars ({(total_original-total_no_images)/total_original*100:.1f}% reduction)")

    if args.dry_run:
        print(f"\n[DRY RUN] No files were modified.")
    else:
        print(f"\nDatasets created:")
        print(f"  {OUTPUT_INLINE}/ - For RAG with inline images")
        print(f"  {OUTPUT_STRUCTURED}/ - For RAG with image metadata")

        # Show example of extracted metadata
        print(f"\nExample image metadata (first file with images):")
        for s in all_stats:
            if s['extracted_images'] > 0:
                json_path = OUTPUT_STRUCTURED / Path(s['path']).relative_to(INPUT_DIR)
                json_path = json_path.with_suffix('.images.json')
                if json_path.exists():
                    data = json.loads(json_path.read_text())
                    print(f"  File: {json_path.name}")
                    if data['images']:
                        img = data['images'][0]
                        print(f"    heading: {img['heading'][:50]}...")
                        print(f"    step: {img['step']}")
                        print(f"    context: {img['context'][:60]}...")
                        print(f"    url: {img['url'][:60]}...")
                break


if __name__ == "__main__":
    main()
