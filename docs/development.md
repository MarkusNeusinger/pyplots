# 🛠️ Development Guide

## Getting Started

### Prerequisites

**Required**:
- Python 3.10+ (3.12 recommended)
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- PostgreSQL 15+ (for local development)

**Optional**:
- Docker (for containerized database)
- Node.js 20+ (for frontend development)

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/pyplots.git
cd pyplots
```

### 2. Install Dependencies

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --all-extras
```

This installs:
- Core dependencies
- Development tools (pytest, ruff, mypy)
- All plotting libraries (matplotlib, seaborn, plotly)

### 3. Database Setup

**Option A: Local PostgreSQL**

```bash
# Create database
createdb pyplots

# Set environment variables
cp .env.example .env
# Edit .env and set DATABASE_URL
```

**Option B: Docker**

```bash
docker run -d \
  --name pyplots-postgres \
  -e POSTGRES_DB=pyplots \
  -e POSTGRES_USER=pyplots \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  postgres:15
```

### 4. Run Migrations

```bash
uv run alembic upgrade head
```

### 5. Start Backend

```bash
uv run uvicorn api.main:app --reload --port 8000
```

API available at: `http://localhost:8000`
Docs available at: `http://localhost:8000/docs`

### 6. Start Frontend (Optional)

```bash
cd app
npm install
npm run dev
```

Frontend available at: `http://localhost:3000`

---

## Environment Variables

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://pyplots:dev_password@localhost:5432/pyplots

# API Keys (for AI generation)
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...  # For Vertex AI (optional)
OPENAI_API_KEY=sk-...  # For GPT (optional)

# Google Cloud (for preview uploads)
GCS_BUCKET=pyplots-images-dev
GCS_CREDENTIALS_PATH=/path/to/credentials.json

# Environment
ENVIRONMENT=development

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

**Never commit `.env`!** (Already in `.gitignore`)

---

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/unit/api/test_routers.py

# Run specific test
uv run pytest tests/unit/api/test_routers.py::test_get_specs
```

### Code Formatting

```bash
# Check formatting
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

### Type Checking (Optional)

```bash
# Install mypy first
uv sync --extra typecheck

# Then run type checking
uv run mypy .
```

**Note**: Type checking is optional. Ruff already catches most issues.

### Pre-commit Hook (Recommended)

```bash
# Install pre-commit
uv pip install pre-commit

# Install git hooks
pre-commit install

# Now formatting runs automatically on git commit
```

---

## Code Standards

### Python

**Style Guide**: PEP 8 (enforced by Ruff)

**Line Length**: 120 characters

**Type Hints**: Required for all functions

```python
# ✅ Good
def create_plot(data: pd.DataFrame, x: str, y: str, **kwargs) -> Figure:
    """Create a scatter plot"""
    pass

# ❌ Bad (no type hints)
def create_plot(data, x, y, **kwargs):
    pass
```

**Docstrings**: Required for all public functions (Google style)

```python
def create_plot(data: pd.DataFrame, x: str, y: str, **kwargs) -> Figure:
    """
    Create a scatter plot from DataFrame

    Args:
        data: Input DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        **kwargs: Additional plotting parameters

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If x or y column not found in data
    """
    pass
```

**Imports**: Organized by category

```python
# Standard library
import os
from pathlib import Path

# Third-party
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI

# Local
from core.database import get_session
from core.models import Spec
```

---

### Testing

**Coverage Target**: 90%+

**Test Structure**: Mirror source structure

```
plots/matplotlib/scatter/scatter_basic_001/default.py
tests/unit/plots/matplotlib/test_scatter_basic_001.py
```

**Test Naming**: `test_{what_it_does}`

```python
def test_scatter_basic_001_creates_figure():
    """Test that scatter-basic-001 creates a valid figure"""
    pass

def test_scatter_basic_001_labels_axes():
    """Test that axes are labeled with column names"""
    pass
```

**Fixtures**: Use pytest fixtures for reusable test data

```python
# tests/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })
```

**Example Test**:

```python
# tests/unit/plots/matplotlib/test_scatter_basic_001.py
import pandas as pd
import pytest
from plots.matplotlib.scatter.scatter_basic_001.default import create_plot


def test_creates_valid_figure(sample_data):
    """Test that create_plot returns a matplotlib Figure"""
    fig = create_plot(sample_data, x='x', y='y')

    assert fig is not None
    assert len(fig.axes) == 1


def test_axes_are_labeled(sample_data):
    """Test that axes have correct labels"""
    fig = create_plot(sample_data, x='x', y='y')
    ax = fig.axes[0]

    assert ax.get_xlabel() == 'x'
    assert ax.get_ylabel() == 'y'


def test_handles_missing_column(sample_data):
    """Test that ValueError is raised for missing columns"""
    with pytest.raises(KeyError):
        create_plot(sample_data, x='missing', y='y')
```

---

## Writing Plot Implementations

### Template

Every implementation file should follow this structure:

```python
"""
scatter-basic-001: Basic 2D Scatter Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: float = 50,
    alpha: float = 0.8,
    title: str | None = None,
    **kwargs
) -> Figure:
    """
    Create a basic scatter plot

    Args:
        data: Input DataFrame
        x: Column name for x-axis
        y: Column name for y-axis
        color: Point color or column name for color mapping
        size: Point size in pixels
        alpha: Transparency (0-1)
        title: Plot title (optional)
        **kwargs: Additional parameters passed to ax.scatter()

    Returns:
        Matplotlib Figure object

    Raises:
        KeyError: If x or y column not found in data
        ValueError: If data is empty

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
        >>> fig = create_plot(data, x='x', y='y', color='blue')
    """
    if data.empty:
        raise ValueError("Data cannot be empty")

    if x not in data.columns or y not in data.columns:
        raise KeyError(f"Columns '{x}' or '{y}' not found in data")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data
    scatter_params = {
        's': size,
        'alpha': alpha,
        **kwargs
    }

    if color and color in data.columns:
        # Color mapping
        scatter = ax.scatter(data[x], data[y], c=data[color], **scatter_params)
        plt.colorbar(scatter, ax=ax, label=color)
    else:
        # Single color
        scatter_params['color'] = color or 'blue'
        ax.scatter(data[x], data[y], **scatter_params)

    # Labels and title
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    if title:
        ax.set_title(title)

    # Grid
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# Optional: Standalone execution for testing
if __name__ == '__main__':
    # Sample data
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })

    # Create plot
    fig = create_plot(data, x='x', y='y', title='Test Plot')

    # Save or show
    plt.savefig('test_output.png', dpi=150)
    print("Plot saved to test_output.png")
```

### Best Practices

**1. Validation First**

```python
# Check data
if data.empty:
    raise ValueError("Data cannot be empty")

# Check columns
if x not in data.columns:
    raise KeyError(f"Column '{x}' not found")
```

**2. Sensible Defaults**

```python
# Good defaults that work for most cases
figsize=(10, 6)  # Not too large, not too small
alpha=0.8        # Slightly transparent for overlapping points
grid=True        # Helps readability
```

**3. Handle Optional Parameters**

```python
# Support both direct value and column mapping
if color and color in data.columns:
    # Color mapping
    ax.scatter(..., c=data[color])
else:
    # Direct color
    ax.scatter(..., color=color or 'blue')
```

**4. Clear Error Messages**

```python
# ✅ Good
raise KeyError(f"Column '{x}' not found in data. Available: {list(data.columns)}")

# ❌ Bad
raise KeyError("Column not found")
```

---

## Contributing

### Proposing New Plots

**Option 1: GitHub Issue (Recommended)**

1. Create issue using spec template
2. Fill in description, requirements, use cases
3. Add label `plot-idea`
4. Wait for review and approval
5. AI generates implementations automatically

**Option 2: Pull Request (Advanced)**

1. Create spec file: `specs/{spec-id}.md`
2. Implement for at least one library
3. Add tests
4. Create PR with previews
5. Wait for quality check and review

### Contribution Guidelines

**Before Submitting**:
- [ ] Code passes all tests (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] Type hints are present (`mypy`)
- [ ] Coverage is >90% for new code
- [ ] Docstrings are complete
- [ ] Preview image looks good

**PR Description Template**:

```markdown
## Description

Implements scatter-basic-001 for matplotlib

## Checklist

- [x] Spec file created/updated
- [x] Implementation code written
- [x] Tests added (coverage: 95%)
- [x] Preview generated
- [ ] Quality check passed (waiting for CI)

## Preview

![Preview](link-to-preview.png)

## Related Issue

Closes #123
```

---

## Project Structure Deep Dive

### Implementation File Naming

```
plots/{library}/{plot_type}/{spec_id}/{variant}.py
```

Examples:
```
plots/matplotlib/scatter/scatter-basic-001/default.py
plots/matplotlib/scatter/scatter-basic-001/ggplot_style.py
plots/seaborn/scatterplot/scatter-basic-001/default.py
plots/plotly/scatter/scatter-basic-001/default.py
```

**Note**: `plot_type` may differ by library:
- matplotlib: `scatter`
- seaborn: `scatterplot`
- plotly: `scatter`

### Test File Naming

```
tests/unit/plots/{library}/test_{spec_id}.py
```

Example:
```
tests/unit/plots/matplotlib/test_scatter_basic_001.py
```

Tests all variants in one file:
```python
def test_default_variant():
    from plots.matplotlib.scatter.scatter_basic_001.default import create_plot
    # ...

def test_ggplot_style_variant():
    from plots.matplotlib.scatter.scatter_basic_001.ggplot_style import create_plot
    # ...
```

---

## Common Tasks

### Add a New Library

1. **Update database**:
```sql
INSERT INTO libraries (id, name, version, documentation_url)
VALUES ('bokeh', 'Bokeh', '3.3.0', 'https://docs.bokeh.org');
```

2. **Create directory structure**:
```bash
mkdir -p plots/bokeh/scatter
```

3. **Implement existing specs**:
```bash
# Start with most popular specs
plots/bokeh/scatter/scatter-basic-001/default.py
```

4. **Add tests**:
```bash
tests/unit/plots/bokeh/test_scatter_basic_001.py
```

### Update an Existing Implementation

1. **Create GitHub issue** referencing original:
```
Issue #456: "Update scatter-basic-001 for matplotlib 4.0"
References: #123
```

2. **Update implementation file**
3. **Run tests**: `pytest tests/unit/plots/matplotlib/test_scatter_basic_001.py`
4. **Generate preview**: Run implementation standalone
5. **Create PR** with new preview
6. **Quality check** runs automatically

### Add a Style Variant

1. **Create new file**:
```python
# plots/matplotlib/scatter/scatter-basic-001/dark_style.py
def create_plot(data, x, y, **kwargs):
    plt.style.use('dark_background')
    # ... rest of implementation
```

2. **Add test**:
```python
def test_dark_style_variant(sample_data):
    from plots.matplotlib.scatter.scatter_basic_001.dark_style import create_plot
    fig = create_plot(sample_data, x='x', y='y')
    assert fig is not None
```

3. **Add to database**:
```sql
INSERT INTO implementations (spec_id, library_id, variant, file_path, ...)
VALUES ('scatter-basic-001', 'matplotlib', 'dark_style', 'plots/matplotlib/scatter/scatter-basic-001/dark_style.py', ...);
```

---

## Debugging Tips

### Database Connection Issues

```bash
# Test connection
psql -U pyplots -d pyplots -h localhost

# Check migrations
uv run alembic current
uv run alembic history
```

### Import Errors

```bash
# Verify package installation
uv pip list

# Reinstall
uv sync --reinstall
```

### Plot Generation Errors

```python
# Run implementation standalone
python plots/matplotlib/scatter/scatter_basic_001/default.py

# Add debug prints
print(f"Data shape: {data.shape}")
print(f"Columns: {data.columns.tolist()}")
```

### Test Failures

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb
```

---

## FAQ

### Q: How do I add a completely new plot type?

**A**: Create GitHub issue with spec → AI generates code → Review and merge

### Q: What if I want to use a different plotting style?

**A**: Create style variant (e.g., `ggplot_style.py`, `dark_style.py`)

### Q: How do I test plot generation locally?

**A**: Run implementation file directly: `python plots/matplotlib/scatter/scatter_basic_001/default.py`

### Q: Do I need to implement for all libraries?

**A**: No! Start with one library. Others can be added later.

### Q: How do I handle Python version differences?

**A**: Only create version-specific files if absolutely necessary (e.g., syntax changes). Prefer single `default.py` that works across 3.10-3.13.

---

## Resources

**Documentation**:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pytest Docs](https://docs.pytest.org/)
- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)

**Tools**:
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Ruff Linter/Formatter](https://github.com/astral-sh/ruff)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

**Community**:
- GitHub Issues: Report bugs, request features
- GitHub Discussions: Ask questions, share ideas

---

*For architecture details, see [architecture/](./architecture/)*
*For deployment, see [deployment.md](./deployment.md)*
