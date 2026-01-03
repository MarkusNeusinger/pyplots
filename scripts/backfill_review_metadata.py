#!/usr/bin/env python3
"""
Backfill extended review data in metadata YAML files from PR comments.

This script searches through merged PRs to find AI Review comments and extracts:
- image_description
- criteria_checklist
- verdict

IMPORTANT: When multiple AI Review comments exist (repair attempts),
always takes the LAST one (the one that led to merge).

Usage:
    python automation/scripts/backfill_review_metadata.py --dry-run
    python automation/scripts/backfill_review_metadata.py --execute

Requires:
    - gh CLI authenticated
    - PyYAML installed
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run_gh_command(args: list[str]) -> dict | list | str:
    """Run a gh CLI command and return JSON output."""
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout.strip()


def find_merged_pr_for_implementation(spec_id: str, library: str) -> dict | None:
    """Find the merged PR for a given spec_id and library."""
    # Search for PRs with the implementation branch pattern
    branch_pattern = f"implementation/{spec_id}/{library}"

    prs = run_gh_command([
        "pr", "list",
        "--state", "merged",
        "--head", branch_pattern,
        "--json", "number,headRefName,mergedAt,comments",
        "--limit", "1"
    ])

    if prs and len(prs) > 0:
        return prs[0]

    # Fallback: search by title pattern
    prs = run_gh_command([
        "pr", "list",
        "--state", "merged",
        "--search", f"feat({library}): implement {spec_id}",
        "--json", "number,headRefName,mergedAt",
        "--limit", "5"
    ])

    if prs:
        for pr in prs:
            if spec_id in pr.get("headRefName", "") and library in pr.get("headRefName", ""):
                return pr

    return None


def get_pr_comments(pr_number: int) -> list[dict]:
    """Get all comments from a PR."""
    comments = run_gh_command([
        "pr", "view", str(pr_number),
        "--json", "comments",
        "-q", ".comments"
    ])
    return comments if comments else []


def parse_ai_review_comment(comment_body: str) -> dict | None:
    """
    Parse an AI Review comment to extract structured data.

    Returns dict with:
        - image_description: str
        - criteria_checklist: dict
        - verdict: str
        - strengths: list[str]
        - weaknesses: list[str]
    """
    if "## AI Review" not in comment_body:
        return None

    result = {
        "image_description": None,
        "criteria_checklist": None,
        "verdict": None,
        "strengths": [],
        "weaknesses": [],
    }

    # Extract Image Description (multi-line quote block)
    img_desc_match = re.search(
        r"### Image Description\s*\n((?:>\s*.*\n?)+)",
        comment_body,
        re.MULTILINE
    )
    if img_desc_match:
        # Remove leading > and whitespace from each line
        lines = img_desc_match.group(1).strip().split("\n")
        cleaned_lines = [re.sub(r"^>\s*", "", line) for line in lines]
        result["image_description"] = "\n".join(cleaned_lines).strip()

    # Extract Verdict
    verdict_match = re.search(r"### Verdict:\s*(APPROVED|REJECTED)", comment_body, re.IGNORECASE)
    if verdict_match:
        result["verdict"] = verdict_match.group(1).upper()

    # Extract Strengths
    strengths_match = re.search(r"### Strengths\s*\n((?:[-*]\s+.*\n?)+)", comment_body, re.MULTILINE)
    if strengths_match:
        lines = strengths_match.group(1).strip().split("\n")
        result["strengths"] = [re.sub(r"^[-*]\s+", "", line).strip() for line in lines if line.strip()]

    # Extract Weaknesses
    weaknesses_match = re.search(r"### Weaknesses\s*\n((?:[-*]\s+.*\n?)+)", comment_body, re.MULTILINE)
    if weaknesses_match:
        lines = weaknesses_match.group(1).strip().split("\n")
        result["weaknesses"] = [re.sub(r"^[-*]\s+", "", line).strip() for line in lines if line.strip()]

    # Extract Criteria Checklist
    result["criteria_checklist"] = parse_criteria_checklist(comment_body)

    return result


def parse_criteria_checklist(comment_body: str) -> dict | None:
    """
    Parse the criteria checklist from the AI Review comment.

    Format in comment:
    **Visual Quality (36/40 pts)**
    - [x] VQ-01: Text Legibility (10) - All text readable ✓
    - [ ] VQ-02: No Overlap (0/8) - Some elements overlap
    """
    checklist = {}

    # Define category patterns
    categories = {
        "visual_quality": r"\*\*Visual Quality \((\d+)/(\d+) pts?\)\*\*",
        "spec_compliance": r"\*\*Spec Compliance \((\d+)/(\d+) pts?\)\*\*",
        "data_quality": r"\*\*Data Quality \((\d+)/(\d+) pts?\)\*\*",
        "code_quality": r"\*\*Code Quality \((\d+)/(\d+) pts?\)\*\*",
        "library_features": r"\*\*Library Features \((\d+)/(\d+) pts?\)\*\*",
    }

    # Item pattern: - [x] VQ-01: Name (score) - comment
    # or: - [ ] VQ-01: Name (score/max) - comment
    item_pattern = re.compile(
        r"- \[([ xX])\] ([A-Z]{2}-\d+): ([^(]+)\((\d+)(?:/(\d+))?\)\s*[-–]?\s*(.*?)(?=\n|$)"
    )

    for cat_key, cat_pattern in categories.items():
        cat_match = re.search(cat_pattern, comment_body)
        if cat_match:
            cat_score = int(cat_match.group(1))
            cat_max = int(cat_match.group(2))

            # Find the section for this category
            cat_start = cat_match.end()
            next_cat = None
            for other_key, other_pattern in categories.items():
                if other_key != cat_key:
                    other_match = re.search(other_pattern, comment_body[cat_start:])
                    if other_match:
                        if next_cat is None or other_match.start() < next_cat:
                            next_cat = other_match.start()

            if next_cat:
                section = comment_body[cat_start:cat_start + next_cat]
            else:
                # Find next section header (### )
                next_section = re.search(r"\n###\s", comment_body[cat_start:])
                if next_section:
                    section = comment_body[cat_start:cat_start + next_section.start()]
                else:
                    section = comment_body[cat_start:]

            items = []
            for match in item_pattern.finditer(section):
                checked = match.group(1).lower() == "x"
                item_id = match.group(2)
                item_name = match.group(3).strip()
                item_score = int(match.group(4))
                item_max = int(match.group(5)) if match.group(5) else item_score if checked else 0
                item_comment = match.group(6).strip() if match.group(6) else ""

                # Clean up comment (remove trailing checkmark or x)
                item_comment = re.sub(r"\s*[✓✗✔✘]$", "", item_comment)

                items.append({
                    "id": item_id,
                    "name": item_name,
                    "score": item_score,
                    "max": item_max if item_max > 0 else item_score,
                    "passed": checked,
                    "comment": item_comment,
                })

            checklist[cat_key] = {
                "score": cat_score,
                "max": cat_max,
                "items": items,
            }

    return checklist if checklist else None


def update_metadata_file(metadata_path: Path, review_data: dict, dry_run: bool) -> bool:
    """
    Update a metadata YAML file with extended review data.

    Preserves existing fields, only adds/updates review section.
    """
    import yaml

    if not metadata_path.exists():
        print(f"  ⚠️  Metadata file not found: {metadata_path}")
        return False

    with open(metadata_path) as f:
        data = yaml.safe_load(f)

    if "review" not in data:
        data["review"] = {}

    # Update with new data (only if not None)
    if review_data.get("image_description"):
        data["review"]["image_description"] = review_data["image_description"]
    if review_data.get("criteria_checklist"):
        data["review"]["criteria_checklist"] = review_data["criteria_checklist"]
    if review_data.get("verdict"):
        data["review"]["verdict"] = review_data["verdict"]

    # Also update strengths/weaknesses if missing
    if review_data.get("strengths") and not data["review"].get("strengths"):
        data["review"]["strengths"] = review_data["strengths"]
    if review_data.get("weaknesses") and not data["review"].get("weaknesses"):
        data["review"]["weaknesses"] = review_data["weaknesses"]

    if dry_run:
        print(f"  📝 Would update: {metadata_path}")
        if review_data.get("image_description"):
            print(f"      - image_description: {len(review_data['image_description'])} chars")
        if review_data.get("criteria_checklist"):
            print(f"      - criteria_checklist: {len(review_data['criteria_checklist'])} categories")
        if review_data.get("verdict"):
            print(f"      - verdict: {review_data['verdict']}")
        return True

    # Custom representer for multi-line strings
    def str_representer(dumper, data):
        if isinstance(data, str) and "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        if isinstance(data, str) and data.endswith("Z") and "T" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_representer)

    with open(metadata_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  ✅ Updated: {metadata_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Backfill extended review data from PR comments")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--execute", action="store_true", help="Actually modify files")
    parser.add_argument("--spec-id", help="Process only this spec ID")
    parser.add_argument("--library", help="Process only this library")
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("Error: Must specify --dry-run or --execute")
        sys.exit(1)

    dry_run = args.dry_run

    # Find all metadata files
    plots_dir = Path("plots")
    if not plots_dir.exists():
        print("Error: plots/ directory not found. Run from repository root.")
        sys.exit(1)

    metadata_files = list(plots_dir.glob("*/metadata/*.yaml"))
    print(f"Found {len(metadata_files)} metadata files")

    # Filter if spec-id or library specified
    if args.spec_id:
        metadata_files = [f for f in metadata_files if args.spec_id in str(f)]
    if args.library:
        metadata_files = [f for f in metadata_files if f.stem == args.library]

    print(f"Processing {len(metadata_files)} files...")

    updated = 0
    skipped = 0
    errors = 0

    for metadata_file in sorted(metadata_files):
        # Extract spec_id and library from path
        # Path: plots/{spec-id}/metadata/{library}.yaml
        spec_id = metadata_file.parent.parent.name
        library = metadata_file.stem

        print(f"\n📦 {spec_id}/{library}")

        # Check if already has extended review data
        try:
            with open(metadata_file) as f:
                existing_data = yaml.safe_load(f)
            existing_review = existing_data.get("review", {}) if existing_data else {}
            if existing_review.get("image_description") and existing_review.get("criteria_checklist"):
                print(f"  ✓ Already has extended review data, skipping")
                skipped += 1
                continue
        except Exception:
            pass  # Continue with backfill if we can't read

        # Find the merged PR
        pr = find_merged_pr_for_implementation(spec_id, library)
        if not pr:
            print(f"  ⏭️  No merged PR found")
            skipped += 1
            continue

        pr_number = pr["number"]
        print(f"  🔗 Found PR #{pr_number}")

        # Get all comments
        comments = get_pr_comments(pr_number)
        if not comments:
            print(f"  ⏭️  No comments found")
            skipped += 1
            continue

        # Filter for AI Review comments
        review_comments = [c for c in comments if "## AI Review" in c.get("body", "")]
        if not review_comments:
            print(f"  ⏭️  No AI Review comments found")
            skipped += 1
            continue

        print(f"  📝 Found {len(review_comments)} AI Review comment(s)")

        # Take the LAST AI Review comment (the one that led to merge)
        # Sort by createdAt and take the last one
        review_comments.sort(key=lambda c: c.get("createdAt", ""))
        final_review = review_comments[-1]

        # Parse the review
        review_data = parse_ai_review_comment(final_review["body"])
        if not review_data:
            print(f"  ⚠️  Failed to parse review comment")
            errors += 1
            continue

        # Check if there's anything new to add
        has_new_data = (
            review_data.get("image_description") or
            review_data.get("criteria_checklist") or
            review_data.get("verdict")
        )

        if not has_new_data:
            print(f"  ⏭️  No extended data found in review")
            skipped += 1
            continue

        # Update the metadata file
        if update_metadata_file(metadata_file, review_data, dry_run):
            updated += 1
        else:
            errors += 1

    print(f"\n{'=' * 50}")
    print(f"Summary: {updated} updated, {skipped} skipped, {errors} errors")

    if dry_run:
        print("\n⚠️  DRY RUN - no files were modified")
        print("Run with --execute to apply changes")


if __name__ == "__main__":
    main()
