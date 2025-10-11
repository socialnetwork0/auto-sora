#!/usr/bin/env python3
"""
Convert CSV to clean Markdown format for LLM reading.

Usage:
    python tools/csv_to_md.py <input.csv> <output.md> [limit]

Examples:
    python tools/csv_to_md.py top_1000.csv top_200.md 200
    .venv/bin/python tools/csv_to_md.py top_1000.csv top_200.md 200
"""

import csv
import sys
from pathlib import Path


def csv_to_markdown(csv_path, output_path, limit=None):
    """Convert CSV to simple markdown format."""

    prompts = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            prompts.append(row)

    # Generate markdown
    md_content = f"""# Sora Top Prompts

**Total entries:** {len(prompts)}
**Source:** {csv_path}

---

"""

    for i, p in enumerate(prompts, 1):
        md_content += f"""## {i}. Post ID: {p['post_id']}

**Views:** {p['view_count']} | **Likes:** {p['like_count']} | **Remixes:** {p['remix_count']}

**Prompt:**
```
{p['text']}
```

"""
        if p["parent_text"] and p["parent_text"] != "NULL":
            md_content += f"""**Parent Text:**
```
{p['parent_text']}
```

"""
        md_content += "---\n\n"

    # Write to file
    output_path.write_text(md_content, encoding="utf-8")
    print(f"✅ Converted {len(prompts)} entries")
    print(f"📄 Output: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python csv_to_md.py <input.csv> <output.md> [limit]")
        print("Example: python csv_to_md.py top_1000.csv top_200.md 200")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else None

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    try:
        csv_to_markdown(csv_path, output_path, limit)
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
