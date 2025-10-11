#!/usr/bin/env python3
"""
Save webpage content to markdown file.
Extract page title as filename.

Usage:
    python tools/save_webpage.py <URL> [output_dir]

Examples:
    # Save to current directory
    python tools/save_webpage.py https://agents.md/

    # Save to specific directory
    python tools/save_webpage.py https://agents.md/ ./output

    # Using virtual environment
    .venv/bin/python tools/save_webpage.py https://agents.md/
"""

import re
import sys
from pathlib import Path

import html2text
import requests
from bs4 import BeautifulSoup


def sanitize_filename(title: str) -> str:
    """Convert page title to valid filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", title)
    # Replace spaces with underscores
    filename = filename.strip().replace(" ", "_")
    # Limit length
    filename = filename[:100]
    return filename or "untitled"


def save_webpage_to_markdown(url: str, output_dir: Path = Path(".")):
    """
    Fetch webpage and save as markdown file.

    Args:
        url: Target URL to fetch
        output_dir: Directory to save markdown file (default: current dir)
    """
    print(f"Fetching: {url}")

    # Fetch webpage
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract title
    title = soup.title.string if soup.title else "Untitled"
    title = title.strip()
    print(f"Page title: {title}")

    # Convert HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    markdown_content = h.handle(response.text)

    # Generate filename
    filename = sanitize_filename(title) + ".md"
    output_path = output_dir / filename

    # Save to file
    output_path.write_text(markdown_content, encoding="utf-8")
    print(f"Saved to: {output_path}")

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python save_webpage.py <URL> [output_dir]")
        print("Example: python save_webpage.py https://example.com")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")

    try:
        save_webpage_to_markdown(url, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
