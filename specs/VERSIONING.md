# Spec Template Versioning

## Overview

All spec files follow a versioned template to ensure consistency and enable automated upgrades when the template is improved.

## Current Version

**Latest:** 1.0.0 (2025-01-24)

## Version Format

Each spec file contains:

```markdown
# {spec-id}: {Title}

<!--
Spec Template Version: 1.0.0
Created: YYYY-MM-DD
Last Updated: YYYY-MM-DD
-->

**Spec Version:** 1.0.0
```

## Version History

### 1.0.0 (2025-01-24)

**Initial standardized template**

Sections:
- Description
- Data Requirements
- Optional Parameters
- Quality Criteria (5-10 items)
- Expected Output
- Tags
- Use Cases

Features:
- Explicit version marker in spec file
- HTML comment with metadata
- Structured quality criteria as checklist
- Clear parameter type definitions

---

## Upgrading Specs

### Manual Upgrade

When creating a new spec, always use the latest template:

```bash
cp specs/.template.md specs/your-spec-id.md
```

Then fill in the placeholders.

### Automatic Upgrade

#### Structural Upgrades (Simple Script)

For simple structural changes (adding version markers, new sections):

```bash
# Dry run (see what would change)
python automation/scripts/upgrade_specs.py --dry-run

# Upgrade all specs
python automation/scripts/upgrade_specs.py

# Upgrade specific spec
python automation/scripts/upgrade_specs.py --spec scatter-basic-001
```

#### Semantic Upgrades (AI-Powered)

For semantic improvements (better wording, clearer criteria):

```bash
# Requires ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY=sk-ant-...

# Dry run (see what would change)
python automation/scripts/upgrade_specs_ai.py --dry-run

# Upgrade all specs (creates automatic backups)
python automation/scripts/upgrade_specs_ai.py

# Upgrade specific spec
python automation/scripts/upgrade_specs_ai.py --spec scatter-basic-001

# Upgrade without backups
python automation/scripts/upgrade_specs_ai.py --no-backup
```

**Why AI-Powered Upgrades?**
- Improves quality criteria to be more specific and measurable
- Enhances parameter descriptions with types and ranges
- Makes use cases more concrete with domain examples
- Preserves spec ID and core intent
- Creates backups automatically

### When to Upgrade

Upgrade specs when:
- Template gets new required sections
- Quality criteria format changes
- Parameter documentation structure improves
- Metadata requirements change

**Note:** Backward compatibility is maintained - old specs remain valid, but new features may be missing.

---

## Template Changes

### Adding a New Section (Minor Version)

Example: 1.0.0 → 1.1.0

```markdown
## New Section (v1.1.0+)

{New content}
```

**Migration:**
- Old specs (1.0.0) continue to work
- New specs include the section
- Upgrade script adds section with default content
- No breaking changes

### Restructuring Sections (Major Version)

Example: 1.x.x → 2.0.0

Breaking changes require:
1. Update template version to 2.0.0
2. Create upgrade function in `upgrade_specs.py`
3. Document migration in this file
4. Run upgrade script on all specs

**Migration:**
- Automated where possible
- Manual review recommended
- Clear changelog of changes

---

## Best Practices

### When Creating Specs

✅ **Always use the template:**
```bash
cp specs/.template.md specs/new-plot-001.md
```

✅ **Keep version in sync:**
- Use the template version at time of creation
- Update `Created` date
- Update `Last Updated` date when modifying

✅ **Document changes:**
- Update `Last Updated` date
- Consider if spec version should increment

### When Updating Template

✅ **Version bump rules:**
- **Patch (1.0.0 → 1.0.1):** Clarifications, typos, examples
- **Minor (1.0.0 → 1.1.0):** New optional sections, additional fields
- **Major (1.0.0 → 2.0.0):** Breaking changes, section renames/removals

✅ **Document changes:**
- Add entry to Version History section
- Update `upgrade_specs.py` if needed
- Test upgrade script with dry-run
- Commit template + upgrade script together

✅ **Communication:**
- Document breaking changes clearly
- Provide migration guide
- Consider automation for common upgrades

---

## Checking Spec Versions

### List all specs with versions

```bash
grep -r "Spec Version:" specs/*.md
```

### Find outdated specs

```python
from pathlib import Path
import re

def check_versions():
    template_version = "1.0.0"
    outdated = []

    for spec_file in Path("specs").glob("*.md"):
        if spec_file.name == ".template.md":
            continue

        content = spec_file.read_text()
        match = re.search(r'\*\*Spec Version:\*\*\s+(\d+\.\d+\.\d+)', content)

        if not match:
            outdated.append((spec_file.stem, "no version"))
        elif match.group(1) != template_version:
            outdated.append((spec_file.stem, match.group(1)))

    return outdated

# Run
outdated = check_versions()
for spec_id, version in outdated:
    print(f"⚠️  {spec_id}: version {version}")
```

---

## Future Enhancements

Potential future template improvements:

### v1.1.0 (Planned)
- [ ] Add "Performance Considerations" section
- [ ] Add "Accessibility" as separate section (not just in criteria)
- [ ] Add "Interactive Features" for plotly/bokeh

### v1.2.0 (Ideas)
- [ ] Add "Variants" section (list common style variants)
- [ ] Add "Related Plots" section (similar visualizations)
- [ ] Add "Common Pitfalls" section

### v2.0.0 (Breaking Changes - Future)
- [ ] Structured YAML front matter for metadata
- [ ] Machine-readable quality criteria format
- [ ] Separate visual vs. code quality criteria

---

## Questions?

- Template unclear? Open an issue with `template-feedback` label
- Upgrade script broken? Open an issue with `bug` label
- Proposal for new section? Open an issue with `template-enhancement` label
