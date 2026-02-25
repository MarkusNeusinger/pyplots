#!/usr/bin/env python3
"""
Generate a catalog of all plot specifications.

Scans plots/*/specification.md files, extracts the spec ID, title, and
description, then writes a Markdown catalog file.
"""

import re
import sys
from pathlib import Path


PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "catalog.md"


def extract_spec_info(spec_path: Path) -> dict[str, str] | None:
    """Extract spec_id, title, and description from a specification.md file."""
    text = spec_path.read_text(encoding="utf-8")

    # Line 1 format: # {spec-id}: {Title}
    heading_match = re.match(r"^#\s+(\S+):\s+(.+)$", text, re.MULTILINE)
    if not heading_match:
        return None

    spec_id = heading_match.group(1)
    title = heading_match.group(2).strip()

    # Description: text between ## Description and the next ##
    desc_match = re.search(r"## Description\s*\n\s*\n(.+?)(?=\n\s*\n##|\Z)", text, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""
    # Collapse multi-line description into single line
    description = re.sub(r"\s+", " ", description)

    return {"spec_id": spec_id, "title": title, "description": description}


def main() -> None:
    output = OUTPUT_FILE
    if len(sys.argv) > 1:
        output = Path(sys.argv[1])

    spec_files = sorted(PLOTS_DIR.glob("*/specification.md"))
    if not spec_files:
        print("No specification files found.", file=sys.stderr)
        sys.exit(1)

    entries = []
    skipped = []
    for spec_file in spec_files:
        info = extract_spec_info(spec_file)
        if info:
            entries.append(info)
        else:
            skipped.append(spec_file.parent.name)

    lines = [
        "# Plot Catalog",
        "",
        f"Total: {len(entries)} specifications",
        "",
        "| # | Spec ID | Title | Description |",
        "|---|---------|-------|-------------|",
    ]

    for i, entry in enumerate(entries, 1):
        desc = entry["description"]
        # Truncate long descriptions for table readability
        if len(desc) > 200:
            desc = desc[:197] + "..."
        # Escape pipes in description
        desc = desc.replace("|", "\\|")
        lines.append(f"| {i} | `{entry['spec_id']}` | {entry['title']} | {desc} |")

    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Catalog written to {output} ({len(entries)} specs)")
    if skipped:
        print(f"Skipped (could not parse): {', '.join(skipped)}", file=sys.stderr)


if __name__ == "__main__":
    main()
