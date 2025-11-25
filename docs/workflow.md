# 🔄 pyplots Automation Workflow

## Overview

pyplots is a **community-driven, AI-powered platform** that automatically discovers, generates, tests, and maintains Python plotting examples. This document describes the high-level automation architecture that makes this possible.

### Philosophy

- **Start Simple, Scale Intelligently**: Begin with basics (Twitter, matplotlib), expand based on learnings
- **Cost-Conscious Design**: Leverage existing subscriptions and smart resource allocation
- **Quality Over Quantity**: Multi-LLM validation ensures only excellent examples go live
- **Community-Driven**: Ideas from the data science community, curated by AI, approved by humans
- **Always Current**: Event-based maintenance keeps examples updated with latest libraries and LLMs

### Key Principles

1. **Images in GCS, Code in GitHub**: Plot PNGs stored in Google Cloud Storage with version history, source code version-controlled
2. **Multi-Version Support**: All plots tested across Python 3.11+ (3.11, 3.12, 3.13, 3.14 primary)
3. **Hybrid Automation**: AI handles routine tasks, humans approve critical decisions
4. **Standard Datasets**: Use well-known datasets (pandas iris, seaborn tips, kaggle) for realistic previews
5. **Event-Based Optimization**: Update plots when LLM/library versions change, not on fixed schedules

---

## System Architecture

```mermaid
graph TB
    subgraph "Discovery & Input"
        SM[Social Media<br/>Twitter, Reddit, GitHub, ArXiv]
        GI[GitHub Issues<br/>Community Ideas]
    end

    subgraph "Orchestration Layer"
        N8N[n8n Cloud<br/>Workflow Engine]
    end

    subgraph "AI Processing"
        CCM[Claude Code Max<br/>Primary AI]
        VTX[Vertex AI<br/>Multi-LLM Critical Decisions]
    end

    subgraph "Testing & Generation"
        GHA[GitHub Actions<br/>Multi-Version Tests + Preview Gen]
        DS[Standard Datasets<br/>pandas, seaborn, kaggle]
    end

    subgraph "Storage & Deployment"
        GH[GitHub Repository<br/>Code Storage]
        GCS[Google Cloud Storage<br/>Image Hosting]
        SQL[Cloud SQL<br/>Metadata]
        CR[Cloud Run<br/>Web Platform]
    end

    SM --> N8N
    GI --> N8N
    N8N --> CCM
    CCM --> GHA
    GHA --> DS
    GHA --> GCS
    GHA --> GH
    CCM --> VTX
    VTX --> SQL
    GCS --> CR
    SQL --> CR
    GH --> CR
```

### Component Responsibilities

| Component | Purpose | Usage Notes |
|-----------|---------|-------------|
| **GitHub Actions** | Code generation, testing, preview gen, quality checks, deployment | See [automation-workflows.md](docs/architecture/automation-workflows.md) for detailed responsibility table |
| **n8n Cloud Pro** | Social media monitoring, posting, issue triage, maintenance scheduling | External service integration (already subscribed) |
| **Claude Code Max** | Code generation, routine evaluation, post content | Primary AI workload |
| **Vertex AI (Multi-LLM)** | Critical quality decisions | Multi-LLM consensus for complex plots |
| **Google Cloud Storage** | PNG hosting with lifecycle management | Preview images + generated plots |
| **Cloud SQL (PostgreSQL)** | Metadata, tags, quality scores, promotion queue | All structured data |
| **X (Twitter) API** | Social media posting | Max 2 posts/day |

**For complete automation responsibilities breakdown**, see [Automation Workflows Documentation](docs/architecture/automation-workflows.md#github-actions-vs-n8n-division-of-responsibilities).

---

## Core Automation Flows

**Detailed technical implementation**: See [Automation Workflows](docs/architecture/automation-workflows.md)

**High-Level Overview**:

### Flow 1: Discovery & Ideation
n8n monitors social media daily → AI extracts plot ideas → Creates GitHub issues with draft specs → Human reviews and approves

### Flow 2: Code Generation
Approved issue → Claude generates implementation code with self-review loop (max 3 attempts) → Creates Pull Request

### Flow 3: Multi-Version Testing
PR created → `test-and-preview.yml` runs tests across Python 3.10+ → Reports results

### Flow 4: Plot Image Generation
Tests passed → GitHub Action generates PNG + thumbnail → Uploads to GCS with versioned paths (`plots/{spec-id}/{library}/{variant}/v{timestamp}.png`) → Stores previous version for before/after comparison

### Flow 4.5: Auto-Tagging
Preview uploaded → AI analyzes code + spec + image → Generates 5-level tag hierarchy → Stores in PostgreSQL with confidence scores

### Flow 5: AI Review
Tests passed + previews generated → `ai-review.yml` triggers → Claude evaluates Spec ↔ Code ↔ Preview → Score ≥85 required → On rejection: feedback loop (max 3 attempts) → Labels: `ai-approved` or `ai-failed`

### Flow 5.5: Auto-Merge
PR labeled `ai-approved` → `auto-merge.yml` triggers → Automatic squash merge

### Flow 6: Deployment & Maintenance
Merged to main → Deploy to Cloud Run → Publicly visible on website → Event-based maintenance (LLM/library updates) → A/B test improvements

### Flow 7: Social Media Promotion
Deployed plot → Added to promotion queue (prioritized by quality score) → n8n posts 2x/day at 10 AM & 3 PM CET → Claude generates content → Posts to X with preview image

---

## Flow Integration

```mermaid
graph TD
    A[Flow 1: Discovery] -->|GitHub Issue| B{Manual/Auto Approval?}
    B -->|Manual| C[Human Reviews Issue]
    B -->|Auto| D[Flow 2: Code Generation<br/>with Self-Review Loop]
    C -->|Approved| D
    C -->|Rejected| Z[End]

    D -->|Self-Review Pass<br/>Max 3 Attempts| E{Code Quality OK?}
    E -->|Yes| F[Flow 3: Multi-Version Testing]
    E -->|No after 3 tries| W[Mark Library as Not Feasible]
    W --> Z

    F -->|Tests Passed| G[Flow 4: Preview Generation]
    F -->|Tests Failed| D

    G -->|PNG in GCS| H{Flow 5: Quality Check}
    H -->|Routine Plot| I[Claude Evaluation]
    H -->|Critical Plot| J[Multi-LLM Consensus]

    I -->|Score ≥85| K{Attempt Count}
    J -->|Majority Approved| K

    I -->|Score <85| L[Store Feedback]
    J -->|Rejected| L

    L --> M{Attempts < 3?}
    M -->|Yes| N[Feed Feedback to Generator]
    N --> D
    M -->|No| O[Mark as Quality-Failed]
    O --> Z

    K -->|Approved| P[Flow 6: Deploy to Website]
    P --> Q[🌐 Publicly Visible]
    P --> U[Flow 7: Add to Promotion Queue]

    U --> V{Daily Post Limit?}
    V -->|< 2 posts today| X[Generate & Post to X]
    V -->|Limit reached| Y[Wait in Queue]
    X --> Z
    Y -.->|Next day| V

    R[Event: LLM/Library Update] -->|Trigger| S[Flow 6: Maintenance]
    S -->|Check Improvements| T{Better?}
    T -->|Yes + Re-approved| P
    T -->|No| Z

    style A fill:#e1f5ff
    style D fill:#fff4e1
    style H fill:#f0e1ff
    style P fill:#e1ffe1
    style Q fill:#90EE90
    style R fill:#ffe1e1
    style L fill:#FFB6C1
    style O fill:#FF6B6B
    style U fill:#E6E6FA
    style X fill:#98FB98
```

---

## Decision Framework

### AI Decides Automatically

✅ **Similar plots** (high semantic similarity to existing specs)
✅ **Routine quality checks** (standard visualizations)
✅ **Tag generation** (categorization and clustering)
✅ **Version compatibility** detection (which Python versions supported)
✅ **Standard optimizations** (code formatting, best practices)

### Human Approval Required

⚠️ **New plot types** (low similarity to existing specs)
⚠️ **Complex visualizations** (3D, animations, interactive)
⚠️ **Multi-LLM disagreement** (no majority consensus)
⚠️ **Breaking changes** (major spec modifications)

### Approval Mechanism

Via **GitHub Issue Labels**:
- `approved` → Proceed to code generation
- `rejected` → Close issue
- `needs-revision` → Request changes from proposer

---

## Resource Management

### Leveraging Existing Subscriptions

| Resource | Subscription | Usage | Monthly Cost |
|----------|-------------|-------|--------------|
| **GitHub Pro** | ✅ Active | Actions (testing + preview gen) | Included |
| **n8n Cloud Pro** | ✅ Active | Workflow orchestration | Included (subscribed) |
| **Claude Code Max** | ✅ Active | Primary AI workload | Included |
| **Google Cloud** | Pay-as-you-go | GCS, Cloud SQL, Cloud Run | Variable |
| **Vertex AI** | Pay-per-use | Multi-LLM critical decisions only | Minimal |

### Cost Optimization Strategies

1. **Smart AI Usage**:
   - Claude Code Max for routine work (already subscribed)
   - Vertex AI multi-LLM only for critical decisions
   - Avoid redundant evaluations

2. **Efficient Storage**:
   - GCS versioning: all versions kept permanently for history tracking
   - Path structure: `plots/{spec-id}/{library}/{variant}/v{ISO-timestamp}.png`
   - Thumbnails: `v{timestamp}_thumb.png` (400px width) for gallery views
   - Images never in git repository
   - Before/after comparison in Issues for updates

3. **Smart Scheduling**:
   - Event-based maintenance (not daily scheduled)
   - Batch processing when possible
   - GitHub Actions matrix for parallel testing

4. **Data Efficiency**:
   - Standard datasets (no AI generation needed)
   - Small CSVs in repo acceptable
   - Reuse datasets across similar plots

---

## Data & Testing Strategy

### Sample Data for Previews

**Critical Principle**: All plot code must be **100% standalone and deterministic**

**Data Embedding Strategy**:

1. **Small datasets** (recommended for most plots):
   ```python
   # Hardcoded dict/list directly in code
   data = pd.DataFrame({
       'category': ['A', 'B', 'C', 'D'],
       'value': [23, 45, 56, 78]
   })
   ```

2. **Standard datasets** (for known examples):
   ```python
   # Load standard dataset (always produces same data)
   data = sns.load_dataset('iris')
   ```

3. **AI-generated data** (when needed):
   - AI generates data **once** with fixed seed
   - Data is then **hardcoded** into the final code
   - Never use random generation without fixed seed

4. **Seeded random** (for demonstrations):
   ```python
   # Fixed seed ensures reproducibility
   np.random.seed(42)
   data = pd.DataFrame({
       'x': np.random.randn(100),
       'y': np.random.randn(100)
   })
   ```

**Why This Matters**:
- Same code must produce same image every single time
- Quality reviewers must see the exact image that will be deployed
- Users must see the exact image shown in previews
- No surprises, no randomness, complete reproducibility

**Code Requirements**:
- ✅ Self-contained (no external file loading)
- ✅ Deterministic (same output every run)
- ✅ Includes explanation text as docstring
- ✅ Sample data embedded directly in code
- ❌ No CSV file loading
- ❌ No random data without fixed seed
- ❌ No external API calls

### Multi-Version Testing

**Python Versions Supported**: 3.11+ (tested on 3.11, 3.12, 3.13, 3.14)

**Primary Version**: Python 3.14 (required to pass, generates plot images)

**Testing Infrastructure**:
```yaml
# GitHub Actions Matrix Strategy
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13', '3.14']
  fail-fast: false

# Python 3.14 is required to pass - older versions are compatibility tests
continue-on-error: ${{ matrix.python-version != '3.14' }}
```

**Test Triggers**:
- On Pull Request creation
- Before Quality Assurance flow
- Not on every commit (saves resources)

**Version Compatibility Documentation**:
- Code optimized for Python 3.14 (newest)
- Older versions (3.11-3.13) run as compatibility tests
- Failures in older versions don't block the PR

**Test Requirements**:
- Python 3.14 tests must pass (primary)
- Plot images only generated with Python 3.14
- Older version failures logged but don't block merge

---

## Phased Rollout

### Phase 1: MVP (Current Focus)

**Scope**:
- 🎯 **Monitoring**: Twitter only
- 📊 **Libraries**: matplotlib only
- 🐍 **Python**: 3.10+ (tested on 3.10, 3.11, 3.12, 3.13)
- ✋ **Approval**: Manual for all new plots
- ✅ **Quality**: Basic Claude evaluation
- 📱 **Promotion**: X (Twitter) posting with 2/day limit

**Goal**: Prove automation pipeline works end-to-end

---

### Phase 2: Expansion

**Add**:
- 🎯 **Monitoring**: + Reddit (r/dataisbeautiful, r/Python)
- 🎯 **Monitoring**: + GitHub Trending/Discussions
- 📊 **Libraries**: + seaborn, + plotly
- 🤖 **Approval**: Hybrid (auto for similar, manual for new)
- ✅ **Quality**: Multi-LLM for critical decisions
- 🐍 **Python**: 3.10+ (already supports all versions)
- 📱 **Promotion**: + LinkedIn posts for professional audience

**Goal**: Scale content production and improve automation

---

### Phase 3: Full Automation

**Add**:
- 🎯 **Monitoring**: + ArXiv papers (academic visualizations)
- 📊 **Libraries**: bokeh, altair, + specialized libraries
- 🤖 **Approval**: Intelligent auto-approval (high confidence)
- 🔄 **Maintenance**: Proactive optimization suggestions
- 🌐 **Community**: Public spec submissions via issues
- 📱 **Promotion**: + Reddit posts (r/dataisbeautiful, r/Python), cross-platform coordination

**Goal**: Comprehensive, self-maintaining plot library

---

## Rule Versioning & Testing

**NEW**: The system now includes versioned rules for code generation and quality evaluation.

**Location**: `rules/` directory

**Key Features**:
- 📋 **Versioned Rules**: Generation rules and quality criteria stored as Markdown (vX.Y.Z)
- 🧪 **A/B Testing**: Compare rule versions before deploying
- 📊 **Audit Trail**: Know which rule version generated each plot
- 🔄 **Rollback**: Instant rollback to previous rules if issues arise
- 📈 **Scientific Improvement**: Prove new rules are better with data

**Current Status** (Documentation Phase):
- ✅ Architecture documented (docs/architecture/rule-versioning.md)
- ✅ Rule templates created (rules/templates/)
- ✅ Initial draft rules (rules/generation/v1.0.0-draft/)
- ⏳ Automation not yet implemented
- ⏳ A/B testing framework planned

**Integration with Workflow**:
- When automation is implemented, all code generation will use specific rule versions
- Quality evaluation will reference versioned criteria
- Rule improvements will be A/B tested before deployment

**See Also**:
- [Rule Versioning Architecture](docs/architecture/rule-versioning.md)
- [A/B Testing Strategies](docs/concepts/ab-testing-rules.md)
- [Claude Skill Concept](docs/concepts/claude-skill-plot-generation.md)

---

## Summary

This workflow ensures:

✅ **Fully Automated** pipeline from discovery to deployment to promotion
✅ **Multi-Layer Quality Control**:
   - Self-review loop in code generation (max 3 attempts)
   - Multi-version testing across Python 3.11-3.14 (3.14 primary)
   - Multi-LLM consensus validation (Claude + Gemini + GPT)
   - Feedback-driven optimization on rejection
✅ **Only High-Quality Plots on Website**: Failed attempts never publicly visible
✅ **Automated Marketing**: Queue-based social media promotion with smart rate limiting (max 2 posts/day)
✅ **Cost-Conscious** design leveraging existing subscriptions
✅ **Smart Storage** with versioned GCS paths (all versions kept for history)
✅ **Deterministic & Reproducible**: Same code = same image every time
✅ **Community-Driven** with AI curation and human oversight
✅ **Event-Based Maintenance** for continuous improvement
✅ **Phased Rollout** starting simple, scaling intelligently
✅ **Feedback Storage**: All quality reviews saved for continuous learning

The system is designed to **scale from MVP to full automation** while maintaining the highest quality standards, controlling costs, and automatically promoting the best content to the community.
