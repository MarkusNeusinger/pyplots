# 🔌 API Specification

## Overview

The pyplots API is a **FastAPI-based REST API** that serves as the central data access layer for all components: frontend, n8n workflows, and GitHub Actions.

**Base URL**: `https://api.pyplots.ai`

**Key Principle**: All database access goes through the API - no direct database connections from frontend or automation tools.

---

## Authentication

### Public Endpoints

No authentication required:
- Browse plots
- View specs
- Search

### Authenticated Endpoints

API key required (header):
```http
Authorization: Bearer {api_key}
```

Used for:
- User data upload
- Plot generation with custom data
- Internal automation endpoints

---

## Core Endpoints

### 1. Specs

#### GET `/specs`

**Purpose**: List all plot specifications

**Query Parameters**:
- `tags` (optional): Comma-separated tags to filter by
- `search` (optional): Search in title and description
- `limit` (optional): Number of results (default: 50, max: 100)
- `offset` (optional): Pagination offset

**Response**:
```json
{
  "specs": [
    {
      "id": "scatter-basic-001",
      "title": "Basic 2D Scatter Plot",
      "description": "Create a simple scatter plot...",
      "tags": ["correlation", "bivariate", "basic"],
      "implementation_count": 3,
      "best_quality_score": 92.0,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

**Example**:
```bash
GET /specs?tags=correlation,finance&limit=10
```

---

#### GET `/specs/{spec_id}`

**Purpose**: Get detailed information about a specific spec

**Response**:
```json
{
  "id": "scatter-basic-001",
  "title": "Basic 2D Scatter Plot",
  "description": "Create a simple scatter plot...",
  "data_requirements": [
    {
      "name": "x",
      "type": "numeric",
      "description": "X-axis values"
    },
    {
      "name": "y",
      "type": "numeric",
      "description": "Y-axis values"
    }
  ],
  "optional_params": [
    {
      "name": "color",
      "type": "string|column",
      "default": null,
      "description": "Point color or column for mapping"
    },
    {
      "name": "alpha",
      "type": "float",
      "default": 0.8,
      "description": "Transparency (0-1)"
    }
  ],
  "tags": ["correlation", "bivariate", "basic"],
  "use_cases": [
    "Correlation analysis",
    "Outlier detection"
  ],
  "implementations": [
    {
      "library": "matplotlib",
      "variant": "default",
      "quality_score": 92.0,
      "preview_url": "https://storage.googleapis.com/...",
      "python_version": "3.10+"
    },
    {
      "library": "seaborn",
      "variant": "default",
      "quality_score": 90.0,
      "preview_url": "https://storage.googleapis.com/...",
      "python_version": "3.10+"
    }
  ],
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-16T14:30:00Z"
}
```

---

#### GET `/specs/{spec_id}/markdown`

**Purpose**: Get the original spec as Markdown

**Response**:
```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Description

Create a simple scatter plot showing the relationship...

## Data Requirements

- **x**: Numeric values for x-axis
- **y**: Numeric values for y-axis

...
```

**Content-Type**: `text/markdown`

---

### 2. Implementations

#### GET `/specs/{spec_id}/implementations`

**Purpose**: Get all implementations for a spec

**Query Parameters**:
- `library` (optional): Filter by library (matplotlib, seaborn, etc.)
- `variant` (optional): Filter by variant (default, ggplot_style, etc.)

**Response**:
```json
{
  "spec_id": "scatter-basic-001",
  "implementations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "library": "matplotlib",
      "library_name": "Matplotlib",
      "plot_function": "scatter",
      "variant": "default",
      "quality_score": 92.0,
      "preview_url": "https://storage.googleapis.com/...",
      "python_version": "3.10+",
      "tested": true,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

#### GET `/specs/{spec_id}/implementations/{library}/{variant}/code`

**Purpose**: Get the implementation code

**Response**:
```python
import matplotlib.pyplot as plt
import pandas as pd


def create_plot(data: pd.DataFrame, x: str, y: str, **kwargs):
    """
    Implementation for scatter-basic-001 using matplotlib

    Args:
        data: Input DataFrame
        x: Column name for x-axis
        y: Column name for y-axis
        **kwargs: Additional parameters (color, size, alpha, etc.)

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(data[x], data[y], **kwargs)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.grid(True, alpha=0.3)

    return fig
```

**Content-Type**: `text/x-python`

---

### 3. Plot Generation

#### POST `/plots/generate`

**Purpose**: Generate plot with user's data

**Authentication**: Required (API key)

**Request**:
```json
{
  "spec_id": "scatter-basic-001",
  "library": "matplotlib",
  "variant": "default",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10]
  },
  "params": {
    "color": "blue",
    "alpha": 0.8,
    "title": "My Scatter Plot"
  }
}
```

**Alternative (CSV upload)**:
```http
POST /plots/generate
Content-Type: multipart/form-data

spec_id=scatter-basic-001
library=matplotlib
variant=default
x=column1
y=column2
file={csv_file}
```

**Response**:
```json
{
  "image_url": "https://storage.googleapis.com/pyplots-images/generated/{session_id}/{plot_id}.png",
  "code": "import matplotlib.pyplot as plt\nimport pandas as pd\n\n...",
  "expires_at": "2025-01-19T10:00:00Z"
}
```

**Notes**:
- Image auto-deleted after 24 hours
- No user data stored permanently
- Maximum data size: 10 MB

---

### 4. Libraries

#### GET `/libraries`

**Purpose**: List all supported plotting libraries

**Response**:
```json
{
  "libraries": [
    {
      "id": "matplotlib",
      "name": "Matplotlib",
      "version": "3.8.0",
      "documentation_url": "https://matplotlib.org",
      "implementation_count": 42,
      "active": true
    },
    {
      "id": "seaborn",
      "name": "Seaborn",
      "version": "0.13.0",
      "documentation_url": "https://seaborn.pydata.org",
      "implementation_count": 38,
      "active": true
    }
  ]
}
```

---

### 5. Search & Discovery

#### GET `/search`

**Purpose**: Full-text search across specs

**Query Parameters**:
- `q`: Search query
- `tags` (optional): Filter by tags
- `libraries` (optional): Filter by available libraries
- `limit`: Results limit (default: 20)

**Response**:
```json
{
  "results": [
    {
      "spec_id": "scatter-basic-001",
      "title": "Basic 2D Scatter Plot",
      "description": "Create a simple scatter plot...",
      "relevance_score": 0.95,
      "tags": ["correlation", "bivariate"],
      "preview_url": "https://storage.googleapis.com/..."
    }
  ],
  "total": 5,
  "query": "correlation analysis"
}
```

---

#### GET `/tags`

**Purpose**: Get all available tags with counts

**Response**:
```json
{
  "tags": [
    {
      "tag": "correlation",
      "count": 15,
      "confidence": 1.0
    },
    {
      "tag": "finance",
      "count": 8,
      "confidence": 0.95
    }
  ]
}
```

---

#### GET `/similar/{spec_id}`

**Purpose**: Find similar plots (based on tags and description)

**Response**:
```json
{
  "spec_id": "scatter-basic-001",
  "similar": [
    {
      "spec_id": "scatter-advanced-005",
      "similarity_score": 0.85,
      "title": "Advanced Scatter Plot with Regression",
      "preview_url": "https://storage.googleapis.com/..."
    }
  ]
}
```

---

## Internal/Automation Endpoints

### 6. Deployment Management

#### POST `/internal/sync-from-repo`

**Purpose**: Sync metadata from repository to database

**Authentication**: Service account only

**Request**:
```json
{
  "trigger": "deployment"
}
```

**Response**:
```json
{
  "synced": {
    "specs": 5,
    "implementations": 15
  },
  "errors": []
}
```

**Usage**: Called by GitHub Actions after deployment

---

#### POST `/internal/specs/{spec_id}/deployed`

**Purpose**: Mark spec as deployed and add to promotion queue

**Authentication**: Service account only

**Request**:
```json
{
  "quality_score": 92.0,
  "preview_url": "https://storage.googleapis.com/..."
}
```

**Response**:
```json
{
  "status": "deployed",
  "added_to_promotion_queue": true
}
```

---

### 7. Promotion Queue

#### GET `/internal/promotion-queue`

**Purpose**: Get next item from promotion queue

**Authentication**: Service account (n8n)

**Query Parameters**:
- `limit`: Number of items (default: 1)
- `platform`: Filter by platform (twitter, linkedin, etc.)

**Response**:
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "spec_id": "scatter-basic-001",
      "title": "Basic 2D Scatter Plot",
      "quality_score": 92.0,
      "preview_url": "https://storage.googleapis.com/...",
      "platform": "twitter",
      "priority": "high"
    }
  ],
  "daily_count": 1,
  "limit_reached": false
}
```

---

#### POST `/internal/promotion-queue/{id}/mark-posted`

**Purpose**: Mark promotion as posted

**Authentication**: Service account (n8n)

**Request**:
```json
{
  "platform": "twitter",
  "post_url": "https://twitter.com/pyplots/status/123456789"
}
```

**Response**:
```json
{
  "status": "posted",
  "posted_at": "2025-01-18T15:00:00Z"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid spec_id format",
    "details": {
      "field": "spec_id",
      "expected": "Format: {type}-{variant}-{number}"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `NOT_FOUND` | 404 | Resource not found |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `SERVER_ERROR` | 500 | Internal server error |
| `DATA_TOO_LARGE` | 413 | Uploaded data exceeds 10 MB |
| `GENERATION_FAILED` | 500 | Plot generation failed |

---

## Rate Limiting

### Public Endpoints

- 100 requests per minute per IP
- 1000 requests per hour per IP

### Authenticated Endpoints

- 1000 requests per minute per API key
- 10000 requests per hour per API key

### Headers

Response includes rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705680000
```

---

## CORS Configuration

### Allowed Origins

```python
# Development
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Production
CORS_ORIGINS = [
    "https://pyplots.ai",
    "https://www.pyplots.ai"
]
```

### Allowed Methods

```
GET, POST, OPTIONS
```

---

## Caching

### Response Caching

Public endpoints cached with appropriate headers:

```http
Cache-Control: public, max-age=3600
ETag: "abc123"
```

### Cache Invalidation

- Specs: Invalidate on deployment
- Implementations: Invalidate on update
- Libraries: Invalidate on version change

---

## Request/Response Examples

### Browse Plots with Filtering

```bash
curl "https://api.pyplots.ai/specs?tags=correlation,finance&limit=5"
```

### Get Specific Spec

```bash
curl "https://api.pyplots.ai/specs/scatter-basic-001"
```

### Get Implementation Code

```bash
curl "https://api.pyplots.ai/specs/scatter-basic-001/implementations/matplotlib/default/code"
```

### Generate Plot with User Data

```bash
curl -X POST "https://api.pyplots.ai/plots/generate" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "spec_id": "scatter-basic-001",
    "library": "matplotlib",
    "data": {
      "x": [1, 2, 3, 4, 5],
      "y": [2, 4, 6, 8, 10]
    },
    "params": {
      "color": "blue",
      "title": "My Data"
    }
  }'
```

---

## Client SDKs

### Python Client

```python
from pyplots import Client

client = Client(api_key="YOUR_API_KEY")

# Browse specs
specs = client.specs.list(tags=["correlation"])

# Get spec details
spec = client.specs.get("scatter-basic-001")

# Generate plot
plot = client.plots.generate(
    spec_id="scatter-basic-001",
    library="matplotlib",
    data={"x": [1, 2, 3], "y": [2, 4, 6]}
)

# Download image
plot.save("output.png")

# Get code
print(plot.code)
```

### JavaScript Client

```javascript
import { PyplotsClient } from '@pyplots/client';

const client = new PyplotsClient({ apiKey: 'YOUR_API_KEY' });

// Browse specs
const specs = await client.specs.list({ tags: ['correlation'] });

// Get spec details
const spec = await client.specs.get('scatter-basic-001');

// Generate plot
const plot = await client.plots.generate({
  specId: 'scatter-basic-001',
  library: 'matplotlib',
  data: { x: [1, 2, 3], y: [2, 4, 6] }
});

// Get image URL
console.log(plot.imageUrl);
```

---

## API Versioning

### Current Version

API version: `v1` (implicit in URLs)

### Future Versioning

When breaking changes needed:
- `/v2/specs` (new version)
- `/specs` (alias to latest)
- Old versions deprecated with 6-month notice

---

## Health & Status

### GET `/health`

**Purpose**: Health check

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "storage": "accessible"
}
```

### GET `/status`

**Purpose**: System status

**Response**:
```json
{
  "api": "operational",
  "database": "operational",
  "storage": "operational",
  "stats": {
    "total_specs": 42,
    "total_implementations": 126,
    "active_libraries": 3
  }
}
```

---

## Security

### Input Validation

- All inputs validated with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- File upload size limits (10 MB)
- Allowed file types: CSV, Excel, JSON

### Sandboxed Execution

Plot generation runs in sandboxed environment:
- Import whitelist (pandas, numpy, matplotlib, etc.)
- Time limit: 30 seconds
- Memory limit: 512 MB
- No file system access

### Data Privacy

- User data never stored permanently
- Generated plots deleted after 24 hours
- No tracking of data content
- Anonymous session IDs only

---

*For database schema, see [database.md](./database.md)*
*For automation workflows, see `.github/workflows/`*
