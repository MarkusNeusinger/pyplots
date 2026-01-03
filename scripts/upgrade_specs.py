#!/usr/bin/env python3
"""
Spec Version Upgrader

Automatically upgrades spec files to the latest template version.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def get_spec_version(spec_content: str) -> str:
    """Extract spec version from content"""
    match = re.search(r"\*\*Spec Version:\*\*\s+(\d+\.\d+\.\d+)", spec_content)
    if match:
        return match.group(1)

    # Check comment version (older format)
    match = re.search(r"Spec Template Version:\s+(\d+\.\d+\.\d+)", spec_content)
    if match:
        return match.group(1)

    return "0.0.0"  # Unknown/very old


def upgrade_to_1_0_0(spec_content: str, spec_id: str) -> str:
    """Upgrade spec to version 1.0.0 format"""
    # Check if already has version
    if "**Spec Version:**" in spec_content:
        return spec_content

    # Extract title
    title_match = re.search(r"^#\s+(.+)$", spec_content, re.MULTILINE)
    if not title_match:
        raise ValueError(f"Could not find title in spec: {spec_id}")

    title_line = title_match.group(0)

    # Insert version info after title
    version_block = """
<!--
Spec Template Version: 1.0.0
Created: 2025-01-24
Last Updated: 2025-01-24
-->

**Spec Version:** 1.0.0
"""

    # Replace title with title + version block
    upgraded = spec_content.replace(title_line, title_line + "\n" + version_block, 1)

    return upgraded


def upgrade_spec_file(spec_path: Path, target_version: str = "1.0.0") -> Tuple[bool, str]:
    """
    Upgrade a single spec file to target version

    Returns:
        (success: bool, message: str)
    """
    try:
        content = spec_path.read_text()
        current_version = get_spec_version(content)

        if current_version == target_version:
            return True, f"Already at version {target_version}"

        # Apply upgrades based on version
        if current_version < "1.0.0" and target_version >= "1.0.0":
            content = upgrade_to_1_0_0(content, spec_path.stem)

        # Future upgrades would go here:
        # if current_version < "1.1.0" and target_version >= "1.1.0":
        #     content = upgrade_to_1_1_0(content, spec_path.stem)

        # Write back
        spec_path.write_text(content)

        return True, f"Upgraded from {current_version} to {target_version}"

    except Exception as e:
        return False, f"Error: {str(e)}"


def find_all_specs() -> List[Path]:
    """Find all spec files (excluding template)"""
    specs_dir = Path("specs")
    return [f for f in specs_dir.glob("*.md") if f.name != ".template.md"]


def upgrade_all_specs(target_version: str = "1.0.0", dry_run: bool = False) -> Dict[str, Tuple[bool, str]]:
    """
    Upgrade all spec files to target version

    Args:
        target_version: Target template version
        dry_run: If True, don't write changes

    Returns:
        Dict mapping spec_id to (success, message)
    """
    results = {}
    specs = find_all_specs()

    for spec_path in specs:
        spec_id = spec_path.stem

        if dry_run:
            content = spec_path.read_text()
            current_version = get_spec_version(content)
            results[spec_id] = (True, f"Would upgrade from {current_version} to {target_version}")
        else:
            success, message = upgrade_spec_file(spec_path, target_version)
            results[spec_id] = (success, message)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upgrade spec files to latest template version")
    parser.add_argument("--version", default="1.0.0", help="Target version (default: 1.0.0)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying files")
    parser.add_argument("--spec", help="Upgrade specific spec file (e.g., scatter-basic-001)")

    args = parser.parse_args()

    print("🔄 Spec Version Upgrader")
    print(f"Target version: {args.version}")
    print(f"Dry run: {args.dry_run}")
    print("=" * 60)

    if args.spec:
        # Upgrade single spec
        spec_path = Path(f"specs/{args.spec}.md")
        if not spec_path.exists():
            print(f"❌ Spec not found: {spec_path}")
            exit(1)

        if args.dry_run:
            content = spec_path.read_text()
            current = get_spec_version(content)
            print(f"📄 {args.spec}")
            print(f"   Current: {current}")
            print(f"   Would upgrade to: {args.version}")
        else:
            success, message = upgrade_spec_file(spec_path, args.version)
            status = "✅" if success else "❌"
            print(f"{status} {args.spec}: {message}")
    else:
        # Upgrade all specs
        results = upgrade_all_specs(args.version, args.dry_run)

        total = len(results)
        succeeded = sum(1 for success, _ in results.values() if success)
        failed = total - succeeded

        for spec_id, (success, message) in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {spec_id}: {message}")

        print("=" * 60)
        print(f"Total: {total} | Succeeded: {succeeded} | Failed: {failed}")

        if failed > 0:
            exit(1)
