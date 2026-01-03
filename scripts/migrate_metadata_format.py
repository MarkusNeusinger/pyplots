#!/usr/bin/env python3
"""
Migrate metadata files to new format.

Changes:
1. specification.yaml: Remove history, add updated
2. metadata/{library}.yaml: Flatten current:, remove history, add created/updated/review
3. implementations/*.py: Update docstring header to new format

Run: uv run python scripts/migrate_metadata_format.py
"""

import re
from datetime import datetime
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).parent.parent.parent
PLOTS_DIR = BASE_DIR / "plots"


def migrate_specification_yaml(spec_yaml: Path) -> bool:
    """Migrate specification.yaml to new format."""
    if not spec_yaml.exists():
        return False

    content = spec_yaml.read_text()
    data = yaml.safe_load(content)

    if data is None:
        return False

    modified = False

    # Remove history if present
    if "history" in data:
        del data["history"]
        modified = True

    # Add updated if not present (set to created or now)
    if "updated" not in data:
        data["updated"] = data.get("created") or datetime.utcnow().isoformat() + "Z"
        modified = True

    if modified:
        # Write with preserved order
        write_spec_yaml(spec_yaml, data)
        print(f"  Migrated: {spec_yaml.name}")

    return modified


def write_spec_yaml(path: Path, data: dict) -> None:
    """Write specification.yaml with correct field order."""
    lines = [
        "# Specification-level metadata for " + data.get("spec_id", "unknown"),
        "# Auto-synced to PostgreSQL on push to main",
        "",
        f"spec_id: {data.get('spec_id', '')}",
        f"title: {data.get('title', '')}",
        "",
        "# Specification tracking",
    ]

    # Handle timestamps
    created = data.get("created")
    if isinstance(created, datetime):
        created = created.isoformat().replace("+00:00", "Z")
    lines.append(f"created: {created}")

    updated = data.get("updated")
    if isinstance(updated, datetime):
        updated = updated.isoformat().replace("+00:00", "Z")
    lines.append(f"updated: {updated}")

    if data.get("issue"):
        lines.append(f"issue: {data['issue']}")
    else:
        lines.append("issue: null")

    if data.get("suggested"):
        lines.append(f"suggested: {data['suggested']}")
    else:
        lines.append("suggested: null")

    # Tags section
    tags = data.get("tags", {})
    lines.append("")
    lines.append("# Classification tags (applies to all library implementations)")
    lines.append("tags:")

    for dim in ["plot_type", "data_type", "domain", "features"]:
        values = tags.get(dim, [])
        lines.append(f"  {dim}:")
        for v in values:
            lines.append(f"    - {v}")

    lines.append("")
    path.write_text("\n".join(lines))


def migrate_library_metadata(meta_yaml: Path) -> bool:
    """Migrate per-library metadata to new flat format."""
    if not meta_yaml.exists():
        return False

    content = meta_yaml.read_text()
    data = yaml.safe_load(content)

    if data is None:
        return False

    modified = False

    # Flatten current: if present
    current = data.pop("current", None)
    if current:
        # Move fields from current: to top level
        for key in ["generated_at", "generated_by", "workflow_run", "issue",
                    "quality_score", "python_version", "library_version", "version"]:
            if key in current and key not in data:
                data[key] = current[key]
                modified = True

    # Remove version (no longer needed)
    if "version" in data:
        del data["version"]
        modified = True

    # Remove history
    if "history" in data:
        del data["history"]
        modified = True

    # Add created from generated_at if not present
    if "created" not in data and "generated_at" in data:
        data["created"] = data["generated_at"]
        modified = True

    # Add updated if not present
    if "updated" not in data:
        data["updated"] = data.get("created") or data.get("generated_at")
        modified = True

    # Add empty review section if not present
    if "review" not in data:
        data["review"] = {"strengths": [], "weaknesses": [], "improvements": []}
        modified = True

    if modified:
        write_library_metadata(meta_yaml, data)
        print(f"  Migrated: {meta_yaml.relative_to(PLOTS_DIR)}")

    return modified


def write_library_metadata(path: Path, data: dict) -> None:
    """Write library metadata with correct format."""
    lines = [
        f"library: {data.get('library', '')}",
        f"specification_id: {data.get('specification_id', '')}",
        "",
        "# Timestamps",
    ]

    # Timestamps
    for field in ["created", "updated"]:
        val = data.get(field)
        if isinstance(val, datetime):
            val = val.isoformat().replace("+00:00", "Z")
        lines.append(f"{field}: {val if val else 'null'}")

    lines.append("")
    lines.append("# Generation")

    for field in ["generated_by", "workflow_run", "issue"]:
        val = data.get(field)
        lines.append(f"{field}: {val if val is not None else 'null'}")

    lines.append("")
    lines.append("# Versions")

    for field in ["python_version", "library_version"]:
        val = data.get(field)
        if val:
            lines.append(f'{field}: "{val}"')
        else:
            lines.append(f"{field}: null")

    lines.append("")
    lines.append("# Previews")

    for field in ["preview_url", "preview_thumb", "preview_html"]:
        val = data.get(field)
        lines.append(f"{field}: {val if val else 'null'}")

    lines.append("")
    lines.append("# Quality")
    qs = data.get("quality_score")
    lines.append(f"quality_score: {qs if qs is not None else 'null'}")

    lines.append("")
    lines.append("# Review feedback")
    lines.append("review:")

    review = data.get("review", {})
    for key in ["strengths", "weaknesses", "improvements"]:
        items = review.get(key, [])
        lines.append(f"  {key}:")
        if items:
            for item in items:
                # Escape quotes in strings
                item_str = str(item).replace('"', '\\"')
                lines.append(f'    - "{item_str}"')
        else:
            lines.append("    []")

    lines.append("")
    path.write_text("\n".join(lines))


def migrate_implementation_py(impl_py: Path, spec_id: str, library: str, meta: dict) -> bool:
    """Update implementation header to new format."""
    if not impl_py.exists():
        return False

    content = impl_py.read_text()

    # Extract current header
    header_match = re.match(r'^"""(.*?)"""', content, re.DOTALL)
    if not header_match:
        return False

    old_header = header_match.group(0)

    # Get values for new header
    title = extract_title_from_header(old_header) or spec_id
    lib_version = meta.get("library_version") or ""
    py_version = meta.get("python_version") or "3.13"
    quality = meta.get("quality_score")
    quality_str = f"{quality}/100" if quality else "pending"

    created = meta.get("created")
    if isinstance(created, datetime):
        created_str = created.strftime("%Y-%m-%d")
    elif isinstance(created, str):
        created_str = created[:10]  # Take YYYY-MM-DD
    else:
        created_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Build new header
    lib_line = f"Library: {library}"
    if lib_version:
        lib_line += f" {lib_version}"
    lib_line += f" | Python {py_version}"

    new_header = f'''""" pyplots.ai
{spec_id}: {title}
{lib_line}
Quality: {quality_str} | Created: {created_str}
"""'''

    if old_header != new_header:
        new_content = content.replace(old_header, new_header, 1)
        impl_py.write_text(new_content)
        print(f"  Migrated: {impl_py.relative_to(PLOTS_DIR)}")
        return True

    return False


def extract_title_from_header(header: str) -> str:
    """Extract title from old header format."""
    # Old format: """\n{spec-id}: {Title}\nLibrary: ...
    lines = header.strip('"\n').split("\n")
    for line in lines:
        if ":" in line and not line.lower().startswith("library"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return ""


def migrate_plot(plot_dir: Path) -> dict:
    """Migrate all files in a plot directory."""
    stats = {"spec": 0, "meta": 0, "impl": 0}

    spec_id = plot_dir.name
    spec_yaml = plot_dir / "specification.yaml"
    meta_dir = plot_dir / "metadata"
    impl_dir = plot_dir / "implementations"

    # 1. Migrate specification.yaml
    if migrate_specification_yaml(spec_yaml):
        stats["spec"] = 1

    # 2. Migrate metadata/*.yaml
    if meta_dir.exists():
        for meta_yaml in meta_dir.glob("*.yaml"):
            if migrate_library_metadata(meta_yaml):
                stats["meta"] += 1

    # 3. Migrate implementations/*.py
    if impl_dir.exists():
        for impl_py in impl_dir.glob("*.py"):
            if impl_py.name.startswith("_"):
                continue
            library = impl_py.stem

            # Load metadata for this library
            meta = {}
            meta_file = meta_dir / f"{library}.yaml"
            if meta_file.exists():
                meta = yaml.safe_load(meta_file.read_text()) or {}

            if migrate_implementation_py(impl_py, spec_id, library, meta):
                stats["impl"] += 1

    return stats


def main():
    """Run migration on all plots."""
    print("=" * 60)
    print("Migrating metadata to new format")
    print("=" * 60)

    total = {"spec": 0, "meta": 0, "impl": 0}

    for plot_dir in sorted(PLOTS_DIR.iterdir()):
        if not plot_dir.is_dir() or plot_dir.name.startswith("."):
            continue

        print(f"\n{plot_dir.name}/")
        stats = migrate_plot(plot_dir)

        for key in total:
            total[key] += stats[key]

    print("\n" + "=" * 60)
    print("Migration complete!")
    print(f"  Specs migrated: {total['spec']}")
    print(f"  Metadata files migrated: {total['meta']}")
    print(f"  Implementation headers migrated: {total['impl']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
