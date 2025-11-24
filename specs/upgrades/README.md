# Spec Upgrade Instructions

This directory contains version-specific upgrade instructions for AI-powered spec upgrades.

## Format

Each upgrade instruction file is named: `{from_version}-to-{to_version}.md`

Example: `1.0.0-to-1.1.0.md`

## Purpose

These instructions tell Claude:
- What semantic improvements to make
- What new sections to add
- How to reformulate existing content
- What to preserve from the old version

## Usage

The `upgrade_specs_ai.py` script automatically loads these instructions when upgrading specs.

```bash
# Upgrade all specs from 1.0.0 to 1.1.0
# Uses specs/upgrades/1.0.0-to-1.1.0.md if it exists
python automation/scripts/upgrade_specs_ai.py --version 1.1.0
```

## Example Upgrade Instruction File

```markdown
# Upgrade Instructions: 1.0.0 → 1.1.0

## Major Changes
- Add "Performance Considerations" section
- Improve Quality Criteria specificity
- Add type annotations to all parameters

## Quality Criteria Improvements
Replace vague criteria with specific, measurable ones:

❌ Before (vague):
- [ ] Plot looks good
- [ ] Colors are nice

✅ After (specific):
- [ ] Grid is visible but subtle with alpha=0.3 and dashed linestyle
- [ ] Colors use colorblind-safe palette (viridis, tab10, or similar)

## Parameter Description Improvements
Add explicit types and ranges:

❌ Before:
- `alpha`: Transparency level (default: 0.8)

✅ After:
- `alpha`: Transparency level (type: float 0.0-1.0, default: 0.8)

## Preserve
- Spec ID and title (must not change)
- Core data requirements
- Use cases (can enhance but don't remove)
```

## Writing Good Upgrade Instructions

### 1. Be Specific About Changes
```markdown
## Changes
- Add "Performance Considerations" section after "Expected Output"
- Split "Quality Criteria" into "Visual Quality" and "Code Quality"
```

### 2. Show Before/After Examples
```markdown
## Example Transformation

Before:
- `color`: Point color or column name

After:
- `color`: Point color (type: string like "blue" or column name for color mapping, default: "steelblue")
```

### 3. List What Must Be Preserved
```markdown
## Preserve
- Spec ID (critical - must not change)
- Created date
- Core data requirements
- Existing optional parameters
```

### 4. Provide Rationale
```markdown
## Why This Change?
Quality criteria should be verifiable by AI without human interpretation.
Vague terms like "looks good" or "is readable" should be replaced with
measurable criteria like specific alpha values, font sizes, or color ranges.
```

## Future Upgrades

When creating a new template version:

1. **Create upgrade instructions**
   ```bash
   cat > specs/upgrades/1.0.0-to-1.1.0.md <<EOF
   # Upgrade Instructions: 1.0.0 → 1.1.0
   ...
   EOF
   ```

2. **Update template**
   ```bash
   # Update specs/.template.md
   # Increment version to 1.1.0
   ```

3. **Test on one spec**
   ```bash
   python automation/scripts/upgrade_specs_ai.py --spec scatter-basic-001 --version 1.1.0 --dry-run
   ```

4. **Review and adjust**
   - Check if improvements make sense
   - Adjust instructions if needed
   - Re-run dry-run

5. **Upgrade all specs**
   ```bash
   python automation/scripts/upgrade_specs_ai.py --version 1.1.0
   ```

## Tips

### For Minor Semantic Improvements
Use AI upgrade for:
- Better wording of quality criteria
- More specific parameter descriptions
- Enhanced use case examples
- Improved expected output descriptions

### For Major Structural Changes
Combine both scripts:
1. Use `upgrade_specs.py` for structural changes (new sections)
2. Use `upgrade_specs_ai.py` for semantic improvements

### Testing Upgrades
Always test on a single spec first:
```bash
# Dry run to see changes
python automation/scripts/upgrade_specs_ai.py --spec scatter-basic-001 --version 1.1.0 --dry-run

# Actual upgrade with backup
python automation/scripts/upgrade_specs_ai.py --spec scatter-basic-001 --version 1.1.0

# Review changes
git diff specs/scatter-basic-001.md

# If good, upgrade all
python automation/scripts/upgrade_specs_ai.py --version 1.1.0
```

## Backup Strategy

The AI upgrade script automatically creates backups:
- Format: `{spec-id}.md.backup-{old_version}`
- Example: `scatter-basic-001.md.backup-1.0.0`
- Disable with `--no-backup` flag

To restore from backup:
```bash
cp specs/scatter-basic-001.md.backup-1.0.0 specs/scatter-basic-001.md
```
