# 💾 Database Schema

## Overview

pyplots uses **PostgreSQL** (Cloud SQL) to store metadata about plots, specs, and implementations. The database stores **references and metadata only** - not code or images.

**Key Principle**: Lightweight metadata store, not a code repository.

---

## Database Stack Decision

| Database | Status | Use Case | When to Consider |
|----------|--------|----------|------------------|
| **PostgreSQL** | ✅ **Current** | All data: specs, implementations, tags, quality scores, promotion queue | Start here - handles everything |
| **Google Cloud Storage** | ✅ **Current** | Preview images, user-generated plots | Already implemented |
| **GitHub** | ✅ **Current** | Code, specs, quality reports (as Issue comments) | Already implemented |
| **Firestore** | 📋 **Future Optimization** | Multi-dimensional tag queries (5-level hierarchy) | IF tag search becomes performance bottleneck with >10,000 specs |

**Current Approach**: All data in PostgreSQL + GCS + GitHub. This is sufficient for MVP and beyond.

**Future Optimization**: See [Firestore for Advanced Tagging](#future-optimization-firestore-for-advanced-tagging) section at the end of this document.

---

## What's Stored vs. What's Not

### ✅ Stored in Database

- Spec metadata (title, description, tags)
- Implementation metadata (library, variant, quality score)
- GCS URLs (preview images)
- Promotion queue (social media posts)
- Library information
- Usage analytics (optional)

### ❌ NOT Stored in Database

- Plot code (stored in GitHub repository)
- Preview images (stored in Google Cloud Storage)
- Quality reports (stored in GitHub Issues as comments)
- User uploaded data (processed in-memory only)

---

## Database Schema

### Tables

```sql
-- Generic plot specifications
CREATE TABLE specs
(
    id                VARCHAR PRIMARY KEY,      -- "scatter-basic-001"
    title             VARCHAR NOT NULL,         -- "Basic 2D Scatter Plot"
    description       TEXT,                     -- Full description
    data_requirements JSONB   NOT NULL,         -- [{"name": "x", "type": "numeric", ...}]
    optional_params   JSONB,                    -- [{"name": "color", "type": "string", ...}]
    tags              VARCHAR[] DEFAULT '{}',   -- ["correlation", "bivariate", "basic"]
    created_at        TIMESTAMP DEFAULT NOW(),
    updated_at        TIMESTAMP DEFAULT NOW()
);

-- Supported plotting libraries
CREATE TABLE libraries
(
    id                VARCHAR PRIMARY KEY,      -- "matplotlib", "seaborn", "plotly"
    name              VARCHAR NOT NULL,         -- "Matplotlib"
    version           VARCHAR,                  -- "3.8.0"
    documentation_url VARCHAR,                  -- "https://matplotlib.org"
    active            BOOLEAN DEFAULT true,     -- Is this library currently supported?
    created_at        TIMESTAMP DEFAULT NOW()
);

-- Library-specific implementations
CREATE TABLE implementations
(
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spec_id        VARCHAR NOT NULL REFERENCES specs (id) ON DELETE CASCADE,
    library_id     VARCHAR NOT NULL REFERENCES libraries (id) ON DELETE CASCADE,
    plot_function  VARCHAR NOT NULL,                     -- "scatter", "bar", "heatmap"
    variant        VARCHAR NOT NULL,                     -- "default", "ggplot_style", "py310"
    file_path      VARCHAR NOT NULL,                     -- "plots/matplotlib/scatter/scatter-basic-001/default.py"
    preview_url    VARCHAR,                              -- GCS URL: gs://pyplots-images/previews/...
    python_version VARCHAR          DEFAULT '3.10+',     -- "3.10+", "3.11+", "3.10-3.12", "all"
    tested         BOOLEAN          DEFAULT false,       -- Has this been tested?
    quality_score  FLOAT,                                -- 0-100 (median of LLM scores)
    created_at     TIMESTAMP        DEFAULT NOW(),
    updated_at     TIMESTAMP        DEFAULT NOW(),
    UNIQUE (spec_id, library_id, variant)
);

-- AI-generated and human-added tags
CREATE TABLE tags
(
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spec_id    VARCHAR NOT NULL REFERENCES specs (id) ON DELETE CASCADE,
    tag        VARCHAR NOT NULL,                         -- "correlation", "finance", "3d"
    confidence FLOAT            DEFAULT 1.0,             -- AI confidence (0-1)
    created_by VARCHAR          DEFAULT 'ai',            -- "ai" or "human"
    created_at TIMESTAMP        DEFAULT NOW(),
    UNIQUE (spec_id, tag)
);

-- Social media promotion queue
CREATE TABLE promotion_queue
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spec_id       VARCHAR NOT NULL REFERENCES specs (id) ON DELETE CASCADE,
    priority      VARCHAR          DEFAULT 'medium',     -- "high", "medium", "low"
    quality_score FLOAT,                                 -- Copy of implementation quality_score
    preview_url   VARCHAR,                               -- GCS URL for social media image
    created_at    TIMESTAMP        DEFAULT NOW(),
    posted_at     TIMESTAMP,                             -- NULL if not yet posted
    status        VARCHAR          DEFAULT 'queued',     -- "queued", "posted", "failed"
    attempt_count INT              DEFAULT 0,            -- How many times we tried to post
    platform      VARCHAR          DEFAULT 'twitter'     -- "twitter", "linkedin", "reddit"
);

-- User-generated plots (optional, for analytics)
CREATE TABLE plot_usage
(
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spec_id      VARCHAR REFERENCES specs (id) ON DELETE SET NULL,
    library_id   VARCHAR REFERENCES libraries (id) ON DELETE SET NULL,
    variant      VARCHAR,
    user_session VARCHAR,                                -- Anonymous session ID
    data_shape   JSONB,                                  -- {"rows": 100, "columns": 3}
    success      BOOLEAN,                                -- Did plot generation succeed?
    error_type   VARCHAR,                                -- If failed, what error?
    created_at   TIMESTAMP        DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_implementations_spec ON implementations (spec_id);
CREATE INDEX idx_implementations_library ON implementations (library_id);
CREATE INDEX idx_tags_spec ON tags (spec_id);
CREATE INDEX idx_tags_tag ON tags (tag);                -- For tag search
CREATE INDEX idx_plot_usage_spec ON plot_usage (spec_id);
CREATE INDEX idx_plot_usage_created ON plot_usage (created_at);
CREATE INDEX idx_promotion_queue_status ON promotion_queue (status, created_at);
CREATE INDEX idx_promotion_queue_posted ON promotion_queue (posted_at);
```

---

## Table Details

### `specs`

**Purpose**: Store generic plot specifications

**Key Fields**:
- `id` - Spec identifier (e.g., "scatter-basic-001")
- `data_requirements` - JSONB array of required parameters
- `optional_params` - JSONB array of optional parameters
- `tags` - Array of keywords for search

**Example Row**:
```json
{
  "id": "scatter-basic-001",
  "title": "Basic 2D Scatter Plot",
  "description": "Create a simple scatter plot...",
  "data_requirements": [
    {"name": "x", "type": "numeric", "description": "X-axis values"},
    {"name": "y", "type": "numeric", "description": "Y-axis values"}
  ],
  "optional_params": [
    {"name": "color", "type": "string|column", "default": null},
    {"name": "alpha", "type": "float", "default": 0.8}
  ],
  "tags": ["correlation", "bivariate", "basic", "2d"]
}
```

---

### `libraries`

**Purpose**: Track supported plotting libraries

**Key Fields**:
- `id` - Library identifier (e.g., "matplotlib")
- `version` - Current version supported
- `active` - Is this library currently supported?

**Example Rows**:
```sql
INSERT INTO libraries (id, name, version, documentation_url) VALUES
('matplotlib', 'Matplotlib', '3.8.0', 'https://matplotlib.org'),
('seaborn', 'Seaborn', '0.13.0', 'https://seaborn.pydata.org'),
('plotly', 'Plotly', '5.18.0', 'https://plotly.com/python');
```

---

### `implementations`

**Purpose**: Track library-specific implementations of specs

**Key Fields**:
- `spec_id` - References spec
- `library_id` - Which library (matplotlib, seaborn, etc.)
- `variant` - Which variant (default, ggplot_style, py310, etc.)
- `file_path` - Relative path in repository
- `preview_url` - GCS URL to preview image
- `quality_score` - Median LLM quality score (0-100)
- `python_version` - Which Python versions supported

**Example Row**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "spec_id": "scatter-basic-001",
  "library_id": "matplotlib",
  "plot_function": "scatter",
  "variant": "default",
  "file_path": "plots/matplotlib/scatter/scatter-basic-001/default.py",
  "preview_url": "gs://pyplots-images/previews/matplotlib/scatter-basic-001/default/v1705603200.png",
  "python_version": "3.10+",
  "tested": true,
  "quality_score": 92.0
}
```

**Unique Constraint**: `(spec_id, library_id, variant)`
- Same spec can have multiple libraries
- Same library can have multiple variants
- But combination must be unique

---

### `tags`

**Purpose**: Searchable tags for plots

**Key Fields**:
- `spec_id` - Which spec this tag belongs to
- `tag` - Keyword (lowercase)
- `confidence` - AI confidence (0-1, for AI-generated tags)
- `created_by` - "ai" or "human"

**Example Rows**:
```sql
INSERT INTO tags (spec_id, tag, confidence, created_by) VALUES
('scatter-basic-001', 'correlation', 1.0, 'human'),
('scatter-basic-001', 'bivariate', 1.0, 'human'),
('scatter-basic-001', 'exploratory', 0.95, 'ai');
```

**Tag Sources**:
- Human-defined in spec (confidence = 1.0)
- AI-suggested based on description (confidence < 1.0)

---

### `promotion_queue`

**Purpose**: Social media promotion queue

**Key Fields**:
- `spec_id` - Which plot to promote
- `priority` - high/medium/low (based on quality_score)
- `status` - queued/posted/failed
- `attempt_count` - Retry counter
- `platform` - Which social platform

**Example Row**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "spec_id": "scatter-basic-001",
  "priority": "high",
  "quality_score": 92.0,
  "preview_url": "gs://pyplots-images/previews/matplotlib/scatter-basic-001/default/v1705603200.png",
  "status": "posted",
  "posted_at": "2025-01-18T15:00:00Z",
  "platform": "twitter"
}
```

**Queue Logic**:
- Items ordered by: `priority DESC, quality_score DESC, created_at ASC`
- Rate limit: Max 2 posts per day
- Failed items retry max 3 times

---

### `plot_usage`

**Purpose**: Anonymous usage analytics (optional)

**Key Fields**:
- `spec_id` - Which plot was used
- `library_id` - Which library
- `data_shape` - Size of user data
- `success` - Did it work?

**Privacy**:
- No user data stored
- No personally identifiable information
- Anonymous session IDs only
- Data auto-deleted after 90 days

**Example Row**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "spec_id": "scatter-basic-001",
  "library_id": "matplotlib",
  "variant": "default",
  "user_session": "anon_abc123",
  "data_shape": {"rows": 150, "columns": 3},
  "success": true
}
```

---

## Data Access Patterns

### 1. Browse All Plots

```sql
SELECT s.id, s.title, s.description, s.tags,
       COUNT(DISTINCT i.library_id) as library_count,
       MAX(i.quality_score) as best_quality_score
FROM specs s
LEFT JOIN implementations i ON s.id = i.spec_id
WHERE i.tested = true
GROUP BY s.id, s.title, s.description, s.tags
ORDER BY best_quality_score DESC, s.created_at DESC;
```

### 2. Get Implementations for a Spec

```sql
SELECT i.*, l.name as library_name
FROM implementations i
JOIN libraries l ON i.library_id = l.id
WHERE i.spec_id = 'scatter-basic-001'
  AND i.tested = true
ORDER BY i.quality_score DESC;
```

### 3. Search by Tags

```sql
SELECT DISTINCT s.*
FROM specs s
JOIN tags t ON s.id = t.spec_id
WHERE t.tag IN ('correlation', 'finance')
ORDER BY s.created_at DESC;
```

### 4. Get Next Item from Promotion Queue

```sql
SELECT *
FROM promotion_queue
WHERE status = 'queued'
  AND (posted_at IS NULL OR DATE(posted_at) < CURRENT_DATE)
ORDER BY
  CASE priority
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 3
  END,
  quality_score DESC,
  created_at ASC
LIMIT 1;
```

---

## Database Migrations

### Migration Strategy

Use **Alembic** for schema migrations:

```bash
# Create new migration
alembic revision -m "add promotion queue table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Migration Files

```python
# migrations/versions/001_initial_schema.py
def upgrade():
    op.create_table('specs', ...)
    op.create_table('libraries', ...)
    op.create_table('implementations', ...)

def downgrade():
    op.drop_table('implementations')
    op.drop_table('libraries')
    op.drop_table('specs')
```

---

## Connection Management

### Connection Modes

pyplots supports two connection modes (priority order):

| Mode | Environment | Variable | Description |
|------|-------------|----------|-------------|
| Direct URL | Local development | `DATABASE_URL` | Connects via public IP |
| Cloud SQL Connector | Cloud Run | `INSTANCE_CONNECTION_NAME` | Uses IAM auth, no public IP needed |

### Local Development (Direct Connection)

```bash
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@34.x.x.x:5432/pyplots
```

Requires IP to be authorized in Cloud SQL Authorized Networks.

### Cloud Run (Cloud SQL Connector)

```bash
# Set via Secret Manager / cloudbuild.yaml
INSTANCE_CONNECTION_NAME=project:region:instance
DB_USER=pyplots
DB_PASS=xxx
DB_NAME=pyplots
```

Uses `cloud-sql-python-connector[asyncpg]` for secure connection without exposing public IP.

### Connection Pooling

```python
# core/database/connection.py
engine = create_async_engine(
    "postgresql+asyncpg://",
    async_creator=get_conn,  # Cloud SQL Connector
    pool_size=5,             # Connections in pool
    max_overflow=10,         # Additional connections if needed
    pool_pre_ping=True       # Verify connection before use
)
```

---

## Backup Strategy

### Automated Backups

Cloud SQL automatic backups:
- Daily backups at 3:00 AM UTC
- Retained for 7 days
- Point-in-time recovery enabled

### Manual Backups

Before major changes:
```bash
gcloud sql backups create \
  --instance=pyplots-db \
  --description="Before migration 005"
```

---

## Performance Considerations

### Indexes

Strategic indexes for common queries:
- Spec lookups by ID (primary key)
- Implementation searches by spec_id and library_id
- Tag searches by tag value
- Promotion queue ordering

### Query Optimization

Use `EXPLAIN ANALYZE` for slow queries:
```sql
EXPLAIN ANALYZE
SELECT s.*, COUNT(i.id) as impl_count
FROM specs s
LEFT JOIN implementations i ON s.id = i.spec_id
GROUP BY s.id;
```

### Caching

Redis cache (optional) for frequent queries:
- Spec metadata
- Library list
- Popular tag combinations

---

## Data Lifecycle

### New Plot Flow

```
1. Spec created
   → INSERT INTO specs

2. Implementations generated
   → INSERT INTO implementations (tested=false, quality_score=NULL)

3. Quality check passes
   → UPDATE implementations SET tested=true, quality_score=92

4. Deployment
   → INSERT INTO promotion_queue
```

### Update Flow

```
1. New version of implementation
   → UPDATE implementations SET preview_url=..., quality_score=..., updated_at=NOW()

2. Old GCS images auto-deleted (30 days)
   → Database still references latest URL
```

### Deletion Flow

```
1. Spec deprecated
   → UPDATE specs SET active=false (soft delete)

2. Complete removal (rare)
   → DELETE FROM specs WHERE id=...
   → Cascade deletes implementations, tags, etc.
```

---

## Security

### Access Control

- API has full read/write access (service account)
- Frontend has read-only access via API
- No direct database access from frontend or n8n
- Secrets stored in Google Secret Manager

### SQL Injection Prevention

Use parameterized queries (SQLAlchemy ORM):
```python
# ✅ Good
await session.execute(
    select(Spec).where(Spec.id == spec_id)
)

# ❌ Bad (never do this)
await session.execute(f"SELECT * FROM specs WHERE id = '{spec_id}'")
```

### Data Privacy

- No user data stored permanently
- Anonymous session IDs only
- Usage data auto-deleted after 90 days
- GDPR-compliant (no personal data)

---

## Future Optimization: Firestore for Advanced Tagging

**Status**: 📋 **Planned** (not currently implemented)

**Current State**: All tags are stored in PostgreSQL `tags` table (simple array). This is sufficient for MVP and early growth.

**Future Consideration**: As the platform scales beyond 10,000+ specs with complex multi-dimensional search requirements, consider adding Firestore for advanced tag functionality.

---

### Why Firestore Could Help (Future)

**Problem it solves**:
- Multi-dimensional tag queries (5-level hierarchy: Library → Plot Type → Data Type → Domain → Features)
- Filtering across multiple dimensions simultaneously (e.g., "matplotlib + timeseries + finance + beginner")
- Real-time search index updates
- Automatic scaling for high-volume tag searches

**When to implement**:
- PostgreSQL tag queries become slow (>500ms for common searches)
- Need for complex tag hierarchy beyond simple array
- User feedback requests advanced filtering
- Catalog grows beyond 10,000 specs

---

### Proposed Architecture (When Implemented)

**Data Split**:
- **PostgreSQL**: Spec metadata, implementation records, quality scores, promotion queue (no change)
- **Firestore**: Multi-dimensional tags, search keywords, similarity clusters

**Example Document Structure**:
```javascript
{
  "plot_id": "matplotlib-scatter-basic-001-default",
  "spec_id": "scatter-basic-001",
  "tags": {
    "library": "matplotlib",
    "plot_type": "scatter",
    "data_type": "tabular",
    "domain": "data-science",
    "features": {"complexity": "beginner", "interactivity": "static"}
  },
  "search_keywords": ["scatter", "matplotlib", "basic", "2d"],
  "confidence_scores": {"overall": 0.89}
}
```

**Query Example**:
```javascript
// Find all beginner matplotlib plots for data-science
db.collection('plot_tags')
  .where('tags.library', '==', 'matplotlib')
  .where('tags.domain', '==', 'data-science')
  .where('tags.features.complexity', '==', 'beginner')
  .get();
```

---

### Implementation Checklist (When Ready)

- [ ] Confirm PostgreSQL performance is actually bottleneck
- [ ] Design detailed Firestore schema (based on actual usage patterns)
- [ ] Create composite indices for common query combinations
- [ ] Implement sync mechanism (PostgreSQL → Firestore)
- [ ] Add consistency checks (daily verification)
- [ ] Monitor costs (estimated <$1/month for 10K docs)
- [ ] Migrate existing tags from PostgreSQL to Firestore
- [ ] Update API to query Firestore for tag searches
- [ ] Keep PostgreSQL tags as backup/audit trail

---

### Cost Estimate (For Future Reference)

**Storage**: 10,000 documents × 3 KB = ~30 MB → <$0.50/month
**Reads**: 1M reads/month → ~$0.36/month
**Writes**: 100K writes/month → ~$0.18/month
**Total**: <$1/month

---

**See Also**:
- **Tag Taxonomy**: `docs/concepts/tagging-system.md`
- **Tagging Rules**: `rules/generation/v1.0.0-draft/tagging-rules.md`
- **Auto-Tagging Workflow**: `docs/workflow.md` (Flow 4.5)

---

## Monitoring

### Key Metrics

Track in Cloud SQL:
- Query performance (slow query log)
- Connection pool usage
- Storage usage
- Backup success/failure

### Alerting

Set up alerts for:
- Storage > 80% full
- Connection pool exhausted
- Failed backups
- Slow queries > 1 second

---

*For API endpoints using this database, see [api.md](./api.md)*
