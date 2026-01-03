#!/usr/bin/env python3
"""
Fix library versions in metadata files and implementation headers.

This script:
1. Gets the installed version of each library
2. Updates all metadata/*.yaml files with the correct library_version
3. Updates all implementations/*.py headers with the correct version
"""

import subprocess
import sys
from pathlib import Path
import yaml
import re

# Library name mapping (library name -> pip package name)
LIBRARY_TO_PACKAGE = {
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "bokeh": "bokeh",
    "altair": "altair",
    "plotnine": "plotnine",
    "pygal": "pygal",
    "highcharts": "highcharts-core",
    "letsplot": "lets-plot",
}


def get_installed_version(package_name: str) -> str:
    """Get the installed version of a package using uv pip show."""
    try:
        result = subprocess.run(
            ["uv", "pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.split("\n"):
            if line.startswith("Version:"):
                return line.split(":")[1].strip()
    except subprocess.CalledProcessError:
        pass
    return "unknown"


def get_all_library_versions() -> dict[str, str]:
    """Get versions of all supported libraries."""
    versions = {}
    for lib_name, package_name in LIBRARY_TO_PACKAGE.items():
        versions[lib_name] = get_installed_version(package_name)
        print(f"  {lib_name}: {versions[lib_name]}")
    return versions


def update_metadata_file(metadata_path: Path, version: str) -> bool:
    """Update library_version in a metadata file."""
    try:
        with open(metadata_path, "r") as f:
            data = yaml.safe_load(f)

        if data.get("library_version") == version:
            return False  # No change needed

        data["library_version"] = version

        with open(metadata_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        return True
    except Exception as e:
        print(f"  Error updating {metadata_path}: {e}")
        return False


def update_implementation_header(impl_path: Path, library: str, version: str) -> bool:
    """Update the library version in implementation header."""
    try:
        with open(impl_path, "r") as f:
            content = f.read()

        # Pattern to match the library line in the header
        # Library: matplotlib unknown | Python 3.13.11
        # Library: matplotlib 3.9.0 | Python 3.13.11
        pattern = rf'(Library: {library}) [^\|]+(\| Python [0-9.]+)'
        replacement = rf'\1 {version} \2'

        new_content, count = re.subn(pattern, replacement, content, count=1)

        if count == 0:
            return False  # No match found

        if new_content == content:
            return False  # No change

        with open(impl_path, "w") as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"  Error updating {impl_path}: {e}")
        return False


def main():
    plots_dir = Path(__file__).parent.parent.parent / "plots"

    if not plots_dir.exists():
        print(f"Error: plots directory not found at {plots_dir}")
        sys.exit(1)

    print("Getting installed library versions...")
    versions = get_all_library_versions()
    print()

    metadata_updated = 0
    impl_updated = 0

    # Find all spec directories
    spec_dirs = sorted([d for d in plots_dir.iterdir() if d.is_dir()])

    for spec_dir in spec_dirs:
        metadata_dir = spec_dir / "metadata"
        impl_dir = spec_dir / "implementations"

        if not metadata_dir.exists():
            continue

        for library, version in versions.items():
            if version == "unknown":
                continue

            # Update metadata file
            metadata_file = metadata_dir / f"{library}.yaml"
            if metadata_file.exists():
                if update_metadata_file(metadata_file, version):
                    metadata_updated += 1

            # Update implementation file
            impl_file = impl_dir / f"{library}.py"
            if impl_file.exists():
                if update_implementation_header(impl_file, library, version):
                    impl_updated += 1

    print(f"\nDone!")
    print(f"  Metadata files updated: {metadata_updated}")
    print(f"  Implementation files updated: {impl_updated}")


if __name__ == "__main__":
    main()
