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

### 3. Planned/Unimplemented Features Documented as Real
- Multi-LLM quality review (mentioned but not implemented)
- User data upload / "Try with YOUR data" (planned premium feature)
- Rules versioning system (partial/incomplete)
- A/B testing for rules (concept only)
- Various "Future Optimization" sections in docs
- Features described in vision.md that don't exist yet

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
1. **Document what exists**: Only describe implemented features, not plans or wishes
2. **Clear separation**: CLAUDE.md for AI (comprehensive), docs/ for humans (organized by persona)
3. **Single source of truth**: Each fact documented once, no duplication between files
4. **Better structure**: Reorganize CLAUDE.md sections logically, remove internal redundancy
5. **Plans belong in GitHub**: Future features → Issues/Milestones, not documentation

---

## New Documentation Tree

```
/
├── README.md                    # [STREAMLINED] Quick start for humans
├── CLAUDE.md                    # [RESTRUCTURED] Complete AI assistant guide
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

### `/CLAUDE.md` (600-700 lines - comprehensive but well-structured)
**Target**: AI assistants (Claude, Copilot, etc.)

**Purpose**: Complete reference for AI - all rules, structure, and critical information in one place

**New Structure**:
```markdown
# CLAUDE.md

## Critical Rules (MUST READ)
- English-only output
- No commits/push in interactive mode
- NEVER bypass automation
- Always use workflow system

## Project Overview (100 lines)
- What pyplots does
- Core principle: Spec-first, AI-generated
- Supported libraries (9 total)
- Architecture overview (high-level only)

## File Structure (150 lines)
- plots/{spec-id}/ (what goes where)
- prompts/ (AI generation rules)
- core/, api/, app/ (backend/frontend)
- .github/workflows/ (automation)
- Where to find things (clear navigation)

## Workflows (200 lines)
- Specification workflow (Issue → Spec → Approve → Merge)
- Implementation workflow (Generate → Review → Repair → Merge)
- Label system (what labels mean and when they change)
- Human approval gates (when to wait)
- What NEVER to do manually

## Development Essentials (100 lines)
- Essential commands (setup, test, run)
- Code standards (Ruff, formatting)
- Testing approach (unit/integration/e2e)
- Common tasks (add plot, update impl)

## Key Metadata Systems (100 lines)
- specification.yaml (spec-level metadata)
- metadata/{library}.yaml (per-library metadata)
- Review feedback structure
- GCS storage structure

## Anti-Patterns (50 lines)
- Things to NEVER do
- Common mistakes to avoid
- Why certain patterns exist
```

**Keep**:
- ✅ All critical rules and workflow gates
- ✅ Complete "where things are" reference
- ✅ Workflow explanations (AI needs to understand the system)
- ✅ Essential commands (but concise - one example per concept)
- ✅ Label system (critical for automation)
- ✅ Metadata structure (AI generates this)

**Improve**:
- 📝 Better section organization (logical flow)
- 📝 Remove duplicate explanations (same thing explained 3x)
- 📝 Consolidate examples (one clear example, not 5 variations)
- 📝 Clear headers with line estimates (easier to navigate)
- 📝 Cross-references to docs/ where humans can read more

**Remove**:
- ❌ Complete database schema (keep overview, details in docs/reference/database.md)
- ❌ Complete API endpoint list (keep overview, details in docs/reference/api.md)
- ❌ Multiple code examples for same concept (one clear example enough)
- ❌ Detailed deployment steps (keep "what deploys where", not "how to deploy")
- ❌ ALL unimplemented features:
  - Multi-LLM quality review (if not active)
  - User data upload features
  - Rules versioning/A/B testing
  - Premium features that don't exist
  - "Future Optimization" sections
  - Any "planned" or "coming soon" content

**Principle**: CLAUDE.md stays comprehensive but becomes better organized with less redundancy

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

### Phase 2: Restructure Existing Files
1. **CLAUDE.md**: Reorganize sections logically, remove duplicate explanations, consolidate examples
2. **README.md**: Streamline for humans (remove tech details, add persona-based navigation)
3. **docs/development.md**: Split into docs/development/*.md (setup, testing, deployment)
4. **docs/workflow.md**: Simplify and move to docs/workflows/overview.md
5. **docs/architecture/*.md**: Keep detailed, add cross-refs from CLAUDE.md

### Phase 3: Remove Redundancy
1. **Within CLAUDE.md**: Remove duplicate explanations of same concepts
2. **Between files**: Ensure no duplication between CLAUDE.md and docs/
3. **Delete outdated content**:
   - References to unimplemented features (rules/ system if not active)
   - Outdated workflow descriptions
   - Unused examples
4. Update all cross-references
5. Verify all links work

### Phase 4: Quality Check
1. Read through as new user/contributor/developer
2. Verify no broken links
3. Check for remaining redundancy
4. Get feedback from actual users

---

## Success Metrics

### Before Refactoring
- CLAUDE.md: 937 lines (comprehensive but redundant and poorly organized)
- Total docs: ~3000+ lines
- Redundancy: High (same info in 3+ places, CLAUDE.md explains things multiple times)
- Navigation: Poor (no clear sections, info scattered)
- Outdated content: ~20%

### After Refactoring
- CLAUDE.md: 600-700 lines (comprehensive, well-structured, no internal redundancy)
- Total docs: ~2500 lines (better organized)
- Redundancy: Minimal (each fact once, no duplication between files)
- Navigation: Clear (logical sections, cross-references to docs/)
- Outdated content: <5% (easier to maintain)

---

## Key Principles to Maintain

### ✅ DO
- Focus on WHY and WHAT
- Organize by user persona
- Link to detailed docs instead of duplicating
- Use diagrams for complex processes
- Keep docs close to what they describe (API docs near API code)

### ❌ DON'T
- Duplicate information across files (CLAUDE.md ≠ docs/)
- Duplicate information within CLAUDE.md (explain once, reference later)
- Include excessive implementation details (show pattern, not every variation)
- Document things that change frequently (git history is better)
- Create docs for planned/unimplemented features
- Mix audiences: CLAUDE.md = AI, docs/ = humans

---

## Code Analysis: What Exists vs What's Documented

**Analysis completed by reviewing actual codebase**

### ✅ VERIFIED: Features That EXIST

| Feature | Evidence |
|---------|----------|
| **Single LLM Review (Claude)** | `impl-review.yml` uses `anthropics/claude-code-action@v1` |
| **Thumbnails** | `impl-generate.yml` calls `core/images.py` → `process_plot_image()` |
| **GCS staging/production** | Full workflow in `impl-generate.yml`, `impl-merge.yml` |
| **Tagging in specification.yaml** | JSONB tags stored in PostgreSQL `specs.tags` |
| **Basic API** | Routers: `specs`, `plots`, `libraries`, `health`, `download`, `stats` |
| **OG Image branding** | `core/images.py` → `create_branded_og_image()` |
| **Full spec/impl workflow** | Complete GitHub Actions pipeline working |

### ❌ VERIFIED: Features That DO NOT Exist

| Documented Feature | Reality |
|-------------------|---------|
| **"Claude + Gemini + GPT"** | Only Claude via `anthropics/claude-code-action` |
| **`/plots/generate` endpoint** | Does not exist in `api/routers/` |
| **Premium tier** | Not implemented |
| **n8n workflows** | No n8n integration in codebase |
| **Rules versioning** | Not implemented |
| **A/B testing** | Only concept doc, no code |
| **Claude Skill** | Only concept doc, no code |
| **Python/JS Client SDKs** | Do not exist |
| **Firestore** | Using PostgreSQL JSONB only |
| **Promotion queue** | Table exists but not used |

---

## Files to DELETE

```bash
rm docs/concepts/ab-testing-rules.md           # concept only, no implementation
rm docs/concepts/claude-skill-plot-generation.md  # concept only, no implementation
```

---

## Sections to REMOVE from Existing Docs

### CLAUDE.md
- Change "Multi-LLM quality: Claude + Gemini + GPT ensure quality" → "Claude AI quality review"
- Remove n8n workflow references
- Remove rule versioning/A/B testing mentions

### docs/vision.md
- Move "Premium (Future)" section → GitHub Milestone
- Remove "Multi-LLM quality" claims

### docs/architecture/api.md
- Remove `/plots/generate` endpoint documentation
- Remove Python/JS Client SDK sections
- Remove `/internal/promotion-queue` endpoints

### docs/architecture/database.md
- Remove "Future Optimization: Firestore" section
- Remove promotion_queue references (if not used)

### docs/workflow.md
- Remove "Rule Versioning & Testing" section
- Remove n8n workflow references
- Change Multi-LLM claims to single-LLM reality

---

## GitHub Issues to CREATE (Future Features)

These should be tracked as issues, not documented as existing:

1. **Multi-LLM Quality Review** - Add Gemini/GPT as secondary reviewers
2. **User Data Upload** - Implement `/plots/generate` with user data
3. **Premium Tier** - Define and implement premium features
4. **Social Media Automation** - Implement n8n or alternative
5. **API Client SDKs** - Create Python and JavaScript clients
6. **Firestore for Tags** - Consider when scale requires it

---

## Next Steps

1. **Review this proposal** with maintainer
2. **Prioritize changes** (what's most important?)
3. **Start with Phase 1** (create new structure)
4. **Iterate based on feedback**

---

**Goal**: Documentation that is **clear, concise, and useful** - not exhaustive but effective.
