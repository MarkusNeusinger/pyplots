# Documentation Refactoring Proposal

## Current Problems

### 1. Massive Redundancy
- **CLAUDE.md (937 lines)** duplicates content from:
  - README.md (project overview, architecture, tech stack)
  - docs/development.md (commands, testing, deployment)
  - docs/workflow.md (GitHub Actions flows)
  - docs/architecture/*.md (database, repository structure)

### 2. Too Much Implementation Detail
- CLAUDE.md contains extensive "HOW" instead of "WHY/WHAT"
- Code examples, command snippets, exact file structures
- This belongs in code comments and READMEs, not high-level docs

### 3. Outdated/Orphaned Content
- References to `rules/` system (mentioned but not fully implemented)
- A/B testing concepts (planned, not active)
- Versioning systems that may not exist
- Development.md references pre-commit hooks not in use

### 4. Unclear Target Audiences
- README: Mix of users, contributors, and developers
- CLAUDE.md: AI assistant but duplicates everything
- docs/: Unclear who each file is for

### 5. Poor Information Hierarchy
- Too many top-level docs (README, CLAUDE, 4+ docs/, 3 architecture/)
- No clear entry points for different personas
- Workflow logic scattered across multiple files

---

## Proposed New Structure

### Philosophy
1. **Process over implementation** - Focus on WHY and WHAT, not HOW
2. **Single source of truth** - Each fact documented once
3. **Clear personas** - Docs organized by who needs them
4. **Let code speak** - Implementation details in code/comments, not docs
5. **Concise and actionable** - Shorter, clearer, more useful

---

## New Documentation Tree

```
/
├── README.md                    # [STREAMLINED] Quick start for everyone
├── CLAUDE.md                    # [MINIMAL] AI assistant rules only
│
├── docs/
│   ├── index.md                 # [NEW] Navigation hub - "Start here"
│   │
│   ├── getting-started/         # [NEW] For new users/contributors
│   │   ├── for-users.md         # Browse, search, use plots
│   │   ├── for-contributors.md  # Propose plots via issues
│   │   └── for-developers.md    # Local setup, first contribution
│   │
│   ├── concepts/                # [REORGANIZED] Understanding the system
│   │   ├── vision.md            # [KEEP] Product vision
│   │   ├── architecture.md      # [NEW] High-level architecture (WHY)
│   │   ├── specification-driven.md  # [NEW] Spec-first philosophy
│   │   ├── ai-workflow.md       # [NEW] How AI generates/reviews
│   │   └── quality-model.md     # [NEW] What makes a good plot
│   │
│   ├── workflows/               # [NEW] Process documentation
│   │   ├── overview.md          # [NEW] All workflows at a glance
│   │   ├── new-plot.md          # Issue → Spec → Implementations
│   │   ├── spec-lifecycle.md    # Create → Review → Approve
│   │   └── impl-lifecycle.md    # Generate → Review → Repair → Merge
│   │
│   ├── reference/               # [REORGANIZED] Technical details
│   │   ├── database.md          # [KEEP] Schema, migrations
│   │   ├── api.md               # [KEEP] Endpoints reference
│   │   ├── labels.md            # [NEW] GitHub label system
│   │   └── environment.md       # [NEW] Environment variables
│   │
│   └── development/             # [NEW] For active developers only
│       ├── setup.md             # Local dev environment
│       ├── testing.md           # Running tests
│       ├── deployment.md        # Cloud deployment
│       └── troubleshooting.md   # Common issues
│
└── prompts/                     # [KEEP] AI generation prompts
    └── README.md                # Brief explanation
```

---

## Proposed Content for Each File

### `/README.md` (150 lines max)
**Target**: First-time visitors (users, contributors, developers)

**Content**:
- **What is pyplots?** (2-3 sentences)
- **Quick start** (install, run, browse)
- **For different personas**:
  - Users → docs/getting-started/for-users.md
  - Contributors → docs/getting-started/for-contributors.md
  - Developers → docs/getting-started/for-developers.md
- **Key links** (website, docs, issues)
- **License**

**Remove**:
- ❌ Architecture details (→ docs/concepts/architecture.md)
- ❌ Tech stack lists (→ docs/reference/)
- ❌ Workflow explanations (→ docs/workflows/)
- ❌ Contribution guidelines (→ docs/getting-started/for-contributors.md)

---

### `/CLAUDE.md` (200 lines max)
**Target**: AI assistants (Claude, Copilot, etc.)

**Content**:
- **Critical rules** (English-only, no manual commits in interactive mode)
- **Workflow gates** (NEVER bypass automation, WAIT for approvals)
- **File structure** (plots/, prompts/, where things are)
- **Key principles** (spec-first, per-library metadata, GCS for images)
- **Links to detailed docs** (→ docs/workflows/, docs/reference/)

**Remove**:
- ❌ Complete command reference (→ docs/development/setup.md)
- ❌ Testing details (→ docs/development/testing.md)
- ❌ Database schema (→ docs/reference/database.md)
- ❌ API endpoints (→ docs/reference/api.md)
- ❌ Deployment instructions (→ docs/development/deployment.md)
- ❌ Example code blocks (code speaks for itself)

**Principle**: Claude should read the detailed docs when needed, not have everything duplicated.

---

### `/docs/index.md` (NEW - 50 lines)
**Navigation hub - the entry point for all documentation**

**Content**:
```markdown
# pyplots Documentation

## I want to...

### Use pyplots
- **Browse plots** → [Website](https://pyplots.ai)
- **Understand the vision** → [Vision](concepts/vision.md)

### Contribute
- **Propose a new plot** → [For Contributors](getting-started/for-contributors.md)
- **Understand workflows** → [Workflows Overview](workflows/overview.md)

### Develop
- **Set up locally** → [Development Setup](development/setup.md)
- **Understand architecture** → [Architecture Concepts](concepts/architecture.md)
- **Run tests** → [Testing Guide](development/testing.md)

### Reference
- **API Endpoints** → [API Reference](reference/api.md)
- **Database Schema** → [Database Reference](reference/database.md)
- **GitHub Labels** → [Label System](reference/labels.md)
```

---

### `/docs/concepts/architecture.md` (NEW - 200 lines max)
**High-level architecture - WHY and WHAT, not HOW**

**Content**:
- **Design principles**:
  - Specification-driven (why specs first)
  - Decoupled workflows (why separate spec/impl)
  - AI-powered (why AI generates everything)
  - Clean repository (why images in GCS, reports in Issues)

- **System components** (diagram + 2-3 sentences each):
  - GitHub repository (source of truth)
  - GitHub Actions (automation engine)
  - PostgreSQL (metadata store)
  - GCS (image hosting)
  - FastAPI (data access layer)

- **Key design decisions**:
  - Per-library metadata files (why → no merge conflicts)
  - Staging/production GCS structure (why → safe review)
  - Issue-based state machine (why → transparency)

**Remove**:
- ❌ Exact file paths
- ❌ Command examples
- ❌ Code snippets
- ❌ Detailed workflow steps (→ docs/workflows/)

---

### `/docs/workflows/new-plot.md` (NEW - 150 lines max)
**End-to-end: Idea → Live Plot**

**Content**:
- **Process overview** (simple flowchart)
- **Key stages**:
  1. Issue creation (user submits idea)
  2. Spec generation (AI creates spec.md)
  3. Human approval (maintainer reviews)
  4. Implementation generation (9 libraries in parallel)
  5. AI quality review (per library)
  6. Auto-merge (to main)
  7. Database sync (PostgreSQL updated)

- **State transitions** (label changes)
- **Human decision points** (when manual approval needed)
- **What happens automatically** (what AI handles)

**Remove**:
- ❌ Exact workflow YAML syntax
- ❌ GitHub Actions implementation details
- ❌ Command-line examples

---

### `/docs/development/setup.md` (Simplified - 100 lines max)
**For developers who need to run locally**

**Content**:
- Prerequisites (Python, uv, PostgreSQL)
- Installation steps (5-7 commands)
- Verification (how to test it works)
- Next steps (→ testing.md, troubleshooting.md)

**Remove**:
- ❌ Docker alternative (if not actively used)
- ❌ Pre-commit hooks (if not in repo)
- ❌ Rule versioning (if not implemented)
- ❌ Frontend setup (separate README in app/)

---

### `/docs/reference/labels.md` (NEW - 100 lines)
**GitHub label system reference**

**Content**:
- **Label categories** (spec, impl, quality, approval)
- **Lifecycle labels** (spec-request → spec-ready → impl:*:done)
- **Approval labels** (approved vs ai-approved distinction)
- **Quality labels** (quality:XX, ai-rejected, not-feasible)
- **When labels change** (which workflows set which labels)

**Format**: Table with Label | Meaning | Set By | Next State

---

## Migration Plan

### Phase 1: Create New Structure (No Breaking Changes)
1. Create new directories: `docs/getting-started/`, `docs/workflows/`, `docs/development/`
2. Write new files:
   - docs/index.md
   - docs/concepts/architecture.md
   - docs/workflows/overview.md
   - docs/workflows/new-plot.md
3. Keep old files unchanged

### Phase 2: Migrate Content
1. Streamline README.md (remove duplicated content, add links to new docs)
2. Minimize CLAUDE.md (remove implementation details, keep only rules)
3. Move development content to docs/development/
4. Consolidate architecture docs into docs/concepts/architecture.md

### Phase 3: Remove Redundancy
1. Delete or archive outdated files:
   - docs/development.md (→ docs/development/*.md)
   - docs/workflow.md (→ docs/workflows/*.md)
   - Redundant sections in CLAUDE.md
2. Update all cross-references
3. Verify all links work

### Phase 4: Quality Check
1. Read through as new user/contributor/developer
2. Verify no broken links
3. Check for remaining redundancy
4. Get feedback from actual users

---

## Success Metrics

### Before Refactoring
- CLAUDE.md: 937 lines
- Total docs: ~3000+ lines
- Redundancy: High (same info in 3+ places)
- Time to find info: 5+ minutes
- Outdated content: ~20%

### After Refactoring
- CLAUDE.md: <200 lines (rules only)
- Total docs: ~2000 lines (more focused)
- Redundancy: Minimal (each fact once)
- Time to find info: <2 minutes (clear navigation)
- Outdated content: <5% (less to maintain)

---

## Key Principles to Maintain

### ✅ DO
- Focus on WHY and WHAT
- Organize by user persona
- Link to detailed docs instead of duplicating
- Use diagrams for complex processes
- Keep docs close to what they describe (API docs near API code)

### ❌ DON'T
- Duplicate information across files
- Include implementation details (belongs in code)
- Document things that change frequently (git history is better)
- Create docs for planned features (wait until implemented)
- Mix multiple audiences in one document

---

## Questions to Resolve

1. **Keep or remove?**
   - docs/concepts/ab-testing-rules.md (planned feature, not implemented)
   - docs/concepts/claude-skill-plot-generation.md (concept doc, unclear status)
   - docs/concepts/tagging-system.md (implementation detail?)
   - docs/specs-guide.md (move to workflows/?)

2. **Frontend docs:**
   - Keep in app/README.md or duplicate in docs/?
   - Currently no app/README.md exists

3. **Prompts documentation:**
   - Currently prompts/README.md doesn't exist
   - Should we document the prompt system?

4. **Archive old content:**
   - Create docs/archive/ for outdated but historical docs?
   - Or just delete and rely on git history?

---

## Next Steps

1. **Review this proposal** with maintainer
2. **Prioritize changes** (what's most important?)
3. **Start with Phase 1** (create new structure)
4. **Iterate based on feedback**

---

**Goal**: Documentation that is **clear, concise, and useful** - not exhaustive but effective.
