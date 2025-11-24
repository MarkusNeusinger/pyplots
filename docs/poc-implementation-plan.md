# 🚀 POC Implementation Plan

## Überblick

Dieser Plan beschreibt die erste POC-Version von pyplots mit **manueller Orchestrierung durch Claude Code im Web**. Ziel ist es, den gesamten Workflow von GitHub Issue bis zur Anzeige auf der Webseite einmal durchzuspielen und zu validieren.

### POC Scope

**Was ist drin:**
- ✅ GitHub Issue mit Spec-Vorschlag (manuell erstellt)
- ✅ Claude Code im Web führt Workflow manuell aus
- ✅ Code-Generierung für matplotlib und seaborn
- ✅ Self-Review Loop (bis zu 3 Versuche)
- ✅ Multi-Version Testing (Python 3.10-3.13)
- ✅ Preview-Generierung und Optimierung
- ✅ Upload zu Google Cloud Storage
- ✅ Metadaten-Speicherung in PostgreSQL
- ✅ API-Endpunkte zum Abrufen von Plots
- ✅ Minimales Frontend zur Anzeige

**Was ist NICHT drin (kommt später):**
- ❌ GitHub Actions Automation
- ❌ n8n Workflows
- ❌ Multi-LLM Quality Checks (nur Claude)
- ❌ Auto-Tagging
- ❌ Social Media Integration
- ❌ Schönes Frontend (nur funktional)

### Ziel des POC

Validieren, dass:
1. Der manuelle Workflow funktioniert
2. Code-Generierung → Self-Review → Test → Preview → Upload funktioniert
3. API und Frontend können Plots anzeigen
4. Die Architektur skalierbar ist für spätere Automatisierung

---

## Phase 1: Setup & Prerequisites (30 min)

### 1.1 Infrastruktur vorbereiten

**Datenbank (PostgreSQL)**
```bash
# Prüfen, ob DB läuft
psql -U pyplots -d pyplots -h localhost -c "SELECT 1"

# Migrations ausführen
uv run alembic upgrade head

# Datenbank-Status prüfen
uv run alembic current
```

**Google Cloud Storage**
```bash
# Bucket erstellen (falls nicht vorhanden)
gsutil mb -l europe-west4 gs://pyplots-images-dev

# Bucket-Struktur vorbereiten
gsutil ls gs://pyplots-images-dev/previews/

# Lifecycle-Policy setzen (optional für POC)
# gsutil lifecycle set gcs-lifecycle.json gs://pyplots-images-dev
```

**Environment Variables**
```bash
# .env prüfen
cat .env

# Mindestens erforderlich:
# DATABASE_URL=postgresql+asyncpg://...
# ANTHROPIC_API_KEY=sk-ant-...
# GCS_BUCKET=pyplots-images-dev
# GCS_CREDENTIALS_PATH=/path/to/credentials.json
```

### 1.2 Dependencies installieren

```bash
# Python-Dependencies
uv sync --all-extras

# Frontend (optional für POC)
cd app && yarn install && cd ..

# Tools installieren
uv pip install pytest pytest-cov ruff
```

### 1.3 Backend starten

```bash
# API starten
uv run uvicorn api.main:app --reload --port 8000

# In separatem Terminal: Testen
curl http://localhost:8000/health
```

---

## Phase 2: Test-Issue erstellen (10 min)

### 2.1 GitHub Issue Template

Erstelle ein GitHub Issue mit folgendem Inhalt:

```markdown
Title: scatter-basic-001: Basic 2D Scatter Plot

## Description

Create a simple scatter plot showing the relationship between two numeric variables.
Perfect for correlation analysis, outlier detection, and exploring bivariate relationships.
Works with any dataset containing two numeric columns.

## Data Requirements

- **x**: Numeric values for x-axis (continuous or discrete)
- **y**: Numeric values for y-axis (continuous or discrete)

## Optional Parameters

- `color`: Point color (string like "blue") or column name for color mapping
- `size`: Point size in pixels (numeric, default: 50) or column name for size mapping
- `alpha`: Transparency level (0.0-1.0, default: 0.8)
- `title`: Plot title (string, optional)
- `xlabel`: Custom x-axis label (default: column name)
- `ylabel`: Custom y-axis label (default: column name)

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels)
- [ ] Grid is visible but subtle (not overpowering the data)
- [ ] Points are clearly distinguishable (appropriate size and alpha)
- [ ] No overlapping axis labels or tick marks
- [ ] Legend is shown if color/size mapping is used
- [ ] Colorblind-safe colors when color mapping is used
- [ ] Appropriate figure size (10x6 inches default, or responsive)
- [ ] Title is centered and clearly readable (if provided)

## Expected Output

A 2D scatter plot with clearly visible points showing the correlation or distribution
between x and y variables. The plot should be immediately understandable without
additional explanation. If color or size mapping is used, the legend should clearly
indicate what each variation means.

## Tags

correlation, bivariate, basic, 2d, statistical, exploratory, scatter

## Use Cases

- Correlation analysis between two variables (e.g., height vs weight)
- Outlier detection in bivariate data
- Pattern recognition in data (linear, quadratic, clusters)
- Relationship visualization (e.g., price vs demand)
- Quality control charts (e.g., measurement vs target)
- Scientific data exploration (e.g., temperature vs pressure)
```

**Labels hinzufügen:**
- `plot-idea`
- `approved` (für POC direkt approved)
- `poc`

---

## Phase 3: Spec-Datei erstellen (5 min)

### 3.1 Spec aus Issue extrahieren

```bash
# Erstelle specs/scatter-basic-001.md
cat > specs/scatter-basic-001.md << 'EOF'
# scatter-basic-001: Basic 2D Scatter Plot

[... Issue-Inhalt kopieren ...]
EOF
```

### 3.2 Spec validieren

```bash
# Prüfe, ob alle erforderlichen Sections vorhanden sind
python automation/scripts/validate_spec.py specs/scatter-basic-001.md
```

**Falls Script nicht existiert, manuell prüfen:**
- ✅ Title mit spec-id
- ✅ Description
- ✅ Data Requirements
- ✅ Quality Criteria (min 5 items)

---

## Phase 4: Code-Generierung (matplotlib) (30 min)

### 4.1 Implementierung generieren

**Erstelle:** `plots/matplotlib/scatter/scatter-basic-001/default.py`

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
    xlabel: str | None = None,
    ylabel: str | None = None,
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
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
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
        scatter_params['color'] = color or 'steelblue'
        ax.scatter(data[x], data[y], **scatter_params)

    # Labels
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    plt.tight_layout()
    return fig


if __name__ == '__main__':
    # Sample data for testing
    import numpy as np

    np.random.seed(42)
    n_points = 100

    data = pd.DataFrame({
        'x': np.random.randn(n_points),
        'y': 2 * np.random.randn(n_points) + 3,
        'category': np.random.choice(['A', 'B', 'C'], n_points)
    })

    # Create plot
    fig = create_plot(data, x='x', y='y', title='Test Scatter Plot')

    # Save
    plt.savefig('test_output.png', dpi=150, bbox_inches='tight')
    print("✅ Plot saved to test_output.png")
```

### 4.2 Self-Review durchführen

**Checklist durchgehen:**
- [ ] Type hints vorhanden?
- [ ] Docstring vollständig?
- [ ] Input-Validierung vorhanden?
- [ ] Error handling implementiert?
- [ ] Sensible defaults verwendet?
- [ ] Grid vorhanden?
- [ ] Colorblind-safe colors?
- [ ] Standalone execution möglich?

**Falls Probleme gefunden → Code verbessern → Erneut reviewen (max 3x)**

### 4.3 Test erstellen

**Erstelle:** `tests/unit/plots/matplotlib/test_scatter_basic_001.py`

```python
import pandas as pd
import pytest
from plots.matplotlib.scatter.scatter_basic_001.default import create_plot


@pytest.fixture
def sample_data():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })


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


def test_custom_labels(sample_data):
    """Test custom axis labels"""
    fig = create_plot(sample_data, x='x', y='y', xlabel='Time', ylabel='Value')
    ax = fig.axes[0]

    assert ax.get_xlabel() == 'Time'
    assert ax.get_ylabel() == 'Value'


def test_title(sample_data):
    """Test that title is set correctly"""
    fig = create_plot(sample_data, x='x', y='y', title='Test Plot')
    ax = fig.axes[0]

    assert ax.get_title() == 'Test Plot'


def test_handles_empty_data():
    """Test that ValueError is raised for empty data"""
    empty_data = pd.DataFrame()

    with pytest.raises(ValueError, match="Data cannot be empty"):
        create_plot(empty_data, x='x', y='y')


def test_handles_missing_column(sample_data):
    """Test that KeyError is raised for missing columns"""
    with pytest.raises(KeyError, match="not found"):
        create_plot(sample_data, x='missing', y='y')


def test_color_mapping(sample_data):
    """Test color mapping by column"""
    sample_data['color_val'] = [1, 2, 3, 4, 5]

    fig = create_plot(sample_data, x='x', y='y', color='color_val')
    ax = fig.axes[0]

    # Check that colorbar was created
    assert len(fig.axes) == 2  # Main axis + colorbar axis
```

### 4.4 Tests ausführen

```bash
# Einzelnen Test ausführen
uv run pytest tests/unit/plots/matplotlib/test_scatter_basic_001.py -v

# Mit Coverage
uv run pytest tests/unit/plots/matplotlib/test_scatter_basic_001.py --cov=plots.matplotlib.scatter.scatter_basic_001 --cov-report=term

# Erwartung: >90% Coverage, alle Tests grün
```

### 4.5 Preview generieren

```bash
# Standalone ausführen
python plots/matplotlib/scatter/scatter-basic-001/default.py

# Prüfen, ob test_output.png erstellt wurde
ls -lh test_output.png

# Bild anschauen
# (Im Browser oder mit Image Viewer)
```

### 4.6 Preview optimieren

**Checklist durchgehen (aus Spec):**
- [ ] X and Y axes labeled?
- [ ] Grid visible but subtle?
- [ ] Points clearly distinguishable?
- [ ] No overlapping labels?
- [ ] Appropriate figure size?

**Falls Probleme:**
1. Code anpassen (z.B. Figsize, Grid-Alpha, Font-Size)
2. Erneut Preview generieren
3. Erneut reviewen
4. Max 3 Iterationen

---

## Phase 5: Code-Generierung (seaborn) (30 min)

### 5.1 Implementierung generieren

**Erstelle:** `plots/seaborn/scatterplot/scatter-basic-001/default.py`

```python
"""
scatter-basic-001: Basic 2D Scatter Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: str | None = None,
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs
) -> Figure:
    """
    Create a basic scatter plot using seaborn

    Args:
        data: Input DataFrame
        x: Column name for x-axis
        y: Column name for y-axis
        color: Column name for color mapping (hue)
        size: Column name for size mapping
        alpha: Transparency (0-1)
        title: Plot title (optional)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        **kwargs: Additional parameters passed to sns.scatterplot()

    Returns:
        Matplotlib Figure object

    Raises:
        KeyError: If x or y column not found in data
        ValueError: If data is empty

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
        >>> fig = create_plot(data, x='x', y='y')
    """
    if data.empty:
        raise ValueError("Data cannot be empty")

    if x not in data.columns or y not in data.columns:
        raise KeyError(f"Columns '{x}' or '{y}' not found in data")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data
    sns.scatterplot(
        data=data,
        x=x,
        y=y,
        hue=color if color and color in data.columns else None,
        size=size if size and size in data.columns else None,
        alpha=alpha,
        ax=ax,
        **kwargs
    )

    # Labels
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    plt.tight_layout()
    return fig


if __name__ == '__main__':
    # Sample data for testing
    import numpy as np

    np.random.seed(42)
    n_points = 100

    data = pd.DataFrame({
        'x': np.random.randn(n_points),
        'y': 2 * np.random.randn(n_points) + 3,
        'category': np.random.choice(['A', 'B', 'C'], n_points)
    })

    # Create plot with color mapping
    fig = create_plot(data, x='x', y='y', color='category', title='Test Seaborn Scatter')

    # Save
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    print("✅ Plot saved to test_output_seaborn.png")
```

### 5.2 Self-Review + Tests + Preview

**Gleicher Prozess wie matplotlib:**
1. Self-Review durchführen
2. Test erstellen: `tests/unit/plots/seaborn/test_scatter_basic_001.py`
3. Tests ausführen
4. Preview generieren
5. Preview optimieren (max 3 Iterationen)

---

## Phase 6: Multi-Version Testing (20 min)

### 6.1 Test-Matrix erstellen

```bash
# Manuelle Version (für POC)
# In Produktion: GitHub Actions Matrix

# Python 3.13
pyenv shell 3.13.0 || echo "Skipping 3.13"
uv run pytest tests/unit/plots/ -v

# Python 3.12
pyenv shell 3.12.0 || echo "Skipping 3.12"
uv run pytest tests/unit/plots/ -v

# Python 3.11
pyenv shell 3.11.0 || echo "Skipping 3.11"
uv run pytest tests/unit/plots/ -v

# Python 3.10
pyenv shell 3.10.0 || echo "Skipping 3.10"
uv run pytest tests/unit/plots/ -v
```

**Erwartung:** Alle Tests grün auf allen Versionen

**Falls Tests fehlschlagen:**
- Version-spezifische Probleme dokumentieren
- Code anpassen (falls möglich)
- Oder: Supported versions einschränken

---

## Phase 7: Upload zu GCS (15 min)

### 7.1 Upload-Script erstellen

**Erstelle:** `automation/scripts/upload_preview.py`

```python
#!/usr/bin/env python3
"""
Upload preview images to Google Cloud Storage
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from google.cloud import storage


def upload_preview(
    local_path: str,
    spec_id: str,
    library: str,
    variant: str = "default",
    bucket_name: str = "pyplots-images-dev"
) -> dict:
    """
    Upload preview image to GCS

    Args:
        local_path: Path to local PNG file
        spec_id: Spec ID (e.g., "scatter-basic-001")
        library: Library name (e.g., "matplotlib")
        variant: Variant name (default: "default")
        bucket_name: GCS bucket name

    Returns:
        dict with URL and metadata
    """
    # Initialize GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Calculate file hash
    with open(local_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()[:8]

    # Generate GCS path
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    gcs_path = f"previews/{library}/{spec_id}/{variant}/v{timestamp}_{file_hash}.png"

    # Upload
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)

    # Set metadata
    blob.metadata = {
        "spec_id": spec_id,
        "library": library,
        "variant": variant,
        "file_hash": file_hash,
        "uploaded_at": timestamp
    }
    blob.patch()

    # Make public
    blob.make_public()

    # Get public URL
    public_url = blob.public_url

    return {
        "gcs_path": gcs_path,
        "public_url": public_url,
        "file_hash": file_hash,
        "uploaded_at": timestamp
    }


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print("Usage: python upload_preview.py <local_path> <spec_id> <library> [variant]")
        sys.exit(1)

    local_path = sys.argv[1]
    spec_id = sys.argv[2]
    library = sys.argv[3]
    variant = sys.argv[4] if len(sys.argv) > 4 else "default"

    result = upload_preview(local_path, spec_id, library, variant)
    print(json.dumps(result, indent=2))
```

### 7.2 Previews hochladen

```bash
# matplotlib Preview
python automation/scripts/upload_preview.py \
  test_output.png \
  scatter-basic-001 \
  matplotlib

# seaborn Preview
python automation/scripts/upload_preview.py \
  test_output_seaborn.png \
  scatter-basic-001 \
  seaborn

# URLs notieren für später
```

---

## Phase 8: Metadaten in DB speichern (20 min)

### 8.1 Datenbank-Schema prüfen

```bash
# Prüfe, ob Tabellen existieren
psql -U pyplots -d pyplots -c "\dt"

# Erwartete Tabellen:
# - specs
# - implementations
# - libraries
```

### 8.2 Daten einfügen

**Erstelle:** `automation/scripts/save_metadata.py`

```python
#!/usr/bin/env python3
"""
Save spec and implementation metadata to database
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import os
from pathlib import Path


async def save_spec(
    spec_id: str,
    title: str,
    description: str,
    tags: list[str],
    spec_file_path: str
):
    """Save spec metadata to database"""

    # Database URL from env
    db_url = os.getenv("DATABASE_URL")
    engine = create_async_engine(db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if spec exists
        from core.models import Spec

        result = await session.execute(
            select(Spec).where(Spec.id == spec_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Spec {spec_id} already exists, updating...")
            existing.title = title
            existing.description = description
            existing.tags = tags
            existing.spec_file_path = spec_file_path
        else:
            print(f"Creating new spec {spec_id}...")
            new_spec = Spec(
                id=spec_id,
                title=title,
                description=description,
                tags=tags,
                spec_file_path=spec_file_path
            )
            session.add(new_spec)

        await session.commit()
        print(f"✅ Spec {spec_id} saved to database")


async def save_implementation(
    spec_id: str,
    library_id: str,
    variant: str,
    file_path: str,
    preview_url: str,
    tested: bool = True,
    quality_score: int | None = None
):
    """Save implementation metadata to database"""

    db_url = os.getenv("DATABASE_URL")
    engine = create_async_engine(db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        from core.models import Implementation

        # Check if implementation exists
        result = await session.execute(
            select(Implementation).where(
                Implementation.spec_id == spec_id,
                Implementation.library_id == library_id,
                Implementation.variant == variant
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Implementation {spec_id}/{library_id}/{variant} exists, updating...")
            existing.file_path = file_path
            existing.preview_url = preview_url
            existing.tested = tested
            if quality_score:
                existing.quality_score = quality_score
        else:
            print(f"Creating new implementation {spec_id}/{library_id}/{variant}...")
            new_impl = Implementation(
                spec_id=spec_id,
                library_id=library_id,
                variant=variant,
                file_path=file_path,
                preview_url=preview_url,
                tested=tested,
                quality_score=quality_score
            )
            session.add(new_impl)

        await session.commit()
        print(f"✅ Implementation {spec_id}/{library_id}/{variant} saved")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python save_metadata.py <command> [args...]")
        print("\nCommands:")
        print("  spec <spec_id> <title> <description> <tags> <file_path>")
        print("  impl <spec_id> <library> <variant> <file_path> <preview_url>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "spec":
        spec_id = sys.argv[2]
        title = sys.argv[3]
        description = sys.argv[4]
        tags = sys.argv[5].split(',')
        file_path = sys.argv[6]

        asyncio.run(save_spec(spec_id, title, description, tags, file_path))

    elif command == "impl":
        spec_id = sys.argv[2]
        library = sys.argv[3]
        variant = sys.argv[4]
        file_path = sys.argv[5]
        preview_url = sys.argv[6]

        asyncio.run(save_implementation(spec_id, library, variant, file_path, preview_url))
```

### 8.3 Metadaten speichern

```bash
# Spec speichern
python automation/scripts/save_metadata.py spec \
  scatter-basic-001 \
  "Basic 2D Scatter Plot" \
  "Create a simple scatter plot showing the relationship between two numeric variables" \
  "correlation,bivariate,basic,2d,statistical" \
  "specs/scatter-basic-001.md"

# matplotlib Implementation speichern
python automation/scripts/save_metadata.py impl \
  scatter-basic-001 \
  matplotlib \
  default \
  "plots/matplotlib/scatter/scatter-basic-001/default.py" \
  "<GCS_URL_MATPLOTLIB>"

# seaborn Implementation speichern
python automation/scripts/save_metadata.py impl \
  scatter-basic-001 \
  seaborn \
  default \
  "plots/seaborn/scatterplot/scatter-basic-001/default.py" \
  "<GCS_URL_SEABORN>"
```

---

## Phase 9: API-Endpunkte erstellen (30 min)

### 9.1 API Router erweitern

**Prüfe/erstelle:** `api/routers/specs.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from core.database import get_session
from core.models import Spec, Implementation
from api.schemas import SpecResponse, ImplementationResponse

router = APIRouter(prefix="/specs", tags=["specs"])


@router.get("/", response_model=List[SpecResponse])
async def list_specs(
    session: AsyncSession = Depends(get_session)
):
    """List all specs"""
    result = await session.execute(select(Spec))
    specs = result.scalars().all()
    return specs


@router.get("/{spec_id}", response_model=SpecResponse)
async def get_spec(
    spec_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get spec by ID"""
    result = await session.execute(
        select(Spec).where(Spec.id == spec_id)
    )
    spec = result.scalar_one_or_none()

    if not spec:
        raise HTTPException(status_code=404, detail="Spec not found")

    return spec


@router.get("/{spec_id}/implementations", response_model=List[ImplementationResponse])
async def list_implementations(
    spec_id: str,
    session: AsyncSession = Depends(get_session)
):
    """List all implementations for a spec"""
    result = await session.execute(
        select(Implementation).where(Implementation.spec_id == spec_id)
    )
    implementations = result.scalars().all()
    return implementations
```

**Schemas erstellen:** `api/schemas.py`

```python
from pydantic import BaseModel
from typing import Optional, List


class SpecResponse(BaseModel):
    id: str
    title: str
    description: str
    tags: List[str]
    spec_file_path: str

    class Config:
        from_attributes = True


class ImplementationResponse(BaseModel):
    spec_id: str
    library_id: str
    variant: str
    file_path: str
    preview_url: str
    tested: bool
    quality_score: Optional[int] = None

    class Config:
        from_attributes = True
```

### 9.2 API testen

```bash
# API neu starten (falls nötig)
# uv run uvicorn api.main:app --reload --port 8000

# Specs abrufen
curl http://localhost:8000/specs/ | jq

# Einzelne Spec abrufen
curl http://localhost:8000/specs/scatter-basic-001 | jq

# Implementations abrufen
curl http://localhost:8000/specs/scatter-basic-001/implementations | jq
```

---

## Phase 10: Minimales Frontend (45 min)

### 10.1 Frontend-Struktur prüfen

```bash
cd app

# Prüfe, ob Next.js läuft
yarn dev

# Öffne http://localhost:3000
```

### 10.2 Plot-Liste Seite

**Erstelle/erweitere:** `app/src/pages/plots/index.tsx`

```typescript
import { useEffect, useState } from 'react';
import Link from 'next/link';

interface Spec {
  id: string;
  title: string;
  description: string;
  tags: string[];
}

export default function PlotsPage() {
  const [specs, setSpecs] = useState<Spec[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/specs/')
      .then(res => res.json())
      .then(data => {
        setSpecs(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Plot Gallery (POC)</h1>

      {specs.length === 0 ? (
        <p>No plots found</p>
      ) : (
        <div style={{ display: 'grid', gap: '20px' }}>
          {specs.map(spec => (
            <div key={spec.id} style={{ border: '1px solid #ccc', padding: '15px' }}>
              <h2>
                <Link href={`/plots/${spec.id}`}>
                  {spec.title}
                </Link>
              </h2>
              <p>{spec.description}</p>
              <div>
                {spec.tags.map(tag => (
                  <span key={tag} style={{
                    background: '#eee',
                    padding: '3px 8px',
                    marginRight: '5px',
                    borderRadius: '3px',
                    fontSize: '12px'
                  }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 10.3 Plot-Detail Seite

**Erstelle:** `app/src/pages/plots/[id].tsx`

```typescript
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

interface Spec {
  id: string;
  title: string;
  description: string;
  tags: string[];
}

interface Implementation {
  library_id: string;
  variant: string;
  preview_url: string;
  file_path: string;
  tested: boolean;
  quality_score?: number;
}

export default function PlotDetailPage() {
  const router = useRouter();
  const { id } = router.query;

  const [spec, setSpec] = useState<Spec | null>(null);
  const [implementations, setImplementations] = useState<Implementation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    // Fetch spec
    fetch(`http://localhost:8000/specs/${id}`)
      .then(res => res.json())
      .then(data => setSpec(data))
      .catch(err => console.error(err));

    // Fetch implementations
    fetch(`http://localhost:8000/specs/${id}/implementations`)
      .then(res => res.json())
      .then(data => {
        setImplementations(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!spec) {
    return <div>Plot not found</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>{spec.title}</h1>
      <p>{spec.description}</p>

      <div style={{ marginTop: '10px' }}>
        {spec.tags.map(tag => (
          <span key={tag} style={{
            background: '#eee',
            padding: '3px 8px',
            marginRight: '5px',
            borderRadius: '3px',
            fontSize: '12px'
          }}>
            {tag}
          </span>
        ))}
      </div>

      <h2 style={{ marginTop: '30px' }}>Implementations</h2>

      {implementations.length === 0 ? (
        <p>No implementations found</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
          {implementations.map(impl => (
            <div key={`${impl.library_id}-${impl.variant}`} style={{
              border: '1px solid #ccc',
              padding: '15px'
            }}>
              <h3>{impl.library_id} ({impl.variant})</h3>

              <img
                src={impl.preview_url}
                alt={`${impl.library_id} preview`}
                style={{ width: '100%', height: 'auto' }}
              />

              <div style={{ marginTop: '10px' }}>
                <p>
                  <strong>Tested:</strong> {impl.tested ? '✅' : '❌'}
                </p>
                {impl.quality_score && (
                  <p><strong>Quality:</strong> {impl.quality_score}/100</p>
                )}
                <p><strong>File:</strong> <code>{impl.file_path}</code></p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 10.4 CORS konfigurieren

**API CORS aktivieren:** `api/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS für lokale Entwicklung
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of app
```

### 10.5 Frontend testen

```bash
# Frontend starten (falls nicht läuft)
cd app && yarn dev

# Browser öffnen
open http://localhost:3000/plots

# Prüfen:
# - Liste der Plots wird angezeigt
# - Klick auf Plot öffnet Detail-Seite
# - Preview-Bilder werden angezeigt
# - Metadaten werden angezeigt
```

---

## Phase 11: End-to-End Test (15 min)

### 11.1 Kompletter Durchlauf

**Von GitHub Issue bis Frontend:**

1. ✅ GitHub Issue erstellt
2. ✅ Spec-Datei generiert
3. ✅ Code für matplotlib generiert
4. ✅ Code für seaborn generiert
5. ✅ Self-Review durchgeführt
6. ✅ Tests geschrieben und ausgeführt
7. ✅ Previews generiert
8. ✅ Previews optimiert
9. ✅ Multi-Version Tests
10. ✅ Previews zu GCS hochgeladen
11. ✅ Metadaten in DB gespeichert
12. ✅ API liefert Daten
13. ✅ Frontend zeigt Plots an

### 11.2 Smoke Tests

```bash
# Backend Health Check
curl http://localhost:8000/health

# API Spec abrufen
curl http://localhost:8000/specs/scatter-basic-001

# Frontend öffnen
open http://localhost:3000/plots/scatter-basic-001

# Prüfen:
# - Bilder laden?
# - Metadaten korrekt?
# - Keine Fehler in Console?
```

---

## Phase 12: Dokumentation & Commit (20 min)

### 12.1 Änderungen committen

```bash
# Git Status prüfen
git status

# Änderungen committen
git add specs/scatter-basic-001.md
git add plots/matplotlib/scatter/scatter-basic-001/default.py
git add plots/seaborn/scatterplot/scatter-basic-001/default.py
git add tests/unit/plots/matplotlib/test_scatter_basic_001.py
git add tests/unit/plots/seaborn/test_scatter_basic_001.py
git add automation/scripts/upload_preview.py
git add automation/scripts/save_metadata.py
git add api/routers/specs.py
git add api/schemas.py
git add app/src/pages/plots/

git commit -m "feat: POC implementation - scatter-basic-001 with matplotlib and seaborn

- Create spec file for scatter-basic-001
- Implement matplotlib version with self-review
- Implement seaborn version with self-review
- Add comprehensive tests for both libraries
- Generate and optimize preview images
- Upload previews to GCS
- Save metadata to PostgreSQL
- Create API endpoints for specs and implementations
- Create minimal frontend to display plots

Tested on Python 3.10-3.13
"
```

### 12.2 Issue aktualisieren

**Im GitHub Issue kommentieren:**

```markdown
## ✅ POC Implementation Complete

### Generated Implementations

- ✅ matplotlib: `plots/matplotlib/scatter/scatter-basic-001/default.py`
- ✅ seaborn: `plots/seaborn/scatterplot/scatter-basic-001/default.py`

### Testing Results

- ✅ All tests pass on Python 3.10, 3.11, 3.12, 3.13
- ✅ Coverage: >90%

### Preview Images

- matplotlib: [View](GCS_URL_MATPLOTLIB)
- seaborn: [View](GCS_URL_SEABORN)

### Live Demo

- Frontend: http://localhost:3000/plots/scatter-basic-001
- API: http://localhost:8000/specs/scatter-basic-001

### Next Steps

- [ ] Push to GitHub
- [ ] Deploy to Cloud Run (later)
- [ ] Add more plot types
- [ ] Automate with GitHub Actions
```

---

## Phase 13: Push & PR (10 min)

### 13.1 Branch pushen

```bash
# Branch pushen
git push -u origin claude/github-issue-poc-plan-01QbVSDkhbSCB2w6qKJe59m5

# Falls Fehler: Retry mit exponential backoff
# (siehe Git Operations im Prompt)
```

### 13.2 Pull Request erstellen

**PR erstellen über GitHub UI oder:**

```bash
# Falls gh CLI verfügbar
gh pr create \
  --title "feat: POC implementation for scatter-basic-001" \
  --body "$(cat <<'EOF'
## Summary

First POC implementation demonstrating the full workflow:

- Manual orchestration through Claude Code
- Spec creation from GitHub Issue
- Code generation for matplotlib and seaborn
- Self-review loop
- Multi-version testing (Python 3.10-3.13)
- Preview generation and optimization
- Upload to GCS
- Metadata storage in PostgreSQL
- API endpoints
- Minimal frontend

## Testing

- [x] All tests pass on Python 3.10-3.13
- [x] Coverage >90%
- [x] Previews generated and uploaded
- [x] API returns correct data
- [x] Frontend displays plots

## Preview

- matplotlib: [View](GCS_URL_MATPLOTLIB)
- seaborn: [View](GCS_URL_SEABORN)

## Related Issue

Implements #ISSUE_NUMBER
EOF
)" \
  --base main
```

---

## Erfolgs-Kriterien

Der POC ist erfolgreich, wenn:

- ✅ Spec-Datei korrekt erstellt wurde
- ✅ Code für beide Libraries generiert und reviewed
- ✅ Alle Tests grün auf allen Python-Versionen
- ✅ Preview-Bilder generiert und optimiert
- ✅ Bilder auf GCS hochgeladen
- ✅ Metadaten in PostgreSQL gespeichert
- ✅ API liefert korrekte Daten
- ✅ Frontend zeigt Plots korrekt an
- ✅ Keine Fehler im gesamten Flow
- ✅ Code committed und gepusht

---

## Nächste Schritte (nach POC)

1. **Weitere Plot-Typen hinzufügen**
   - Bar Charts
   - Line Plots
   - Heatmaps
   - Box Plots

2. **Automatisierung mit GitHub Actions**
   - `spec-to-code.yml` Workflow
   - `test-and-preview.yml` Workflow
   - `deploy.yml` Workflow

3. **Quality Checks verbessern**
   - Multi-LLM Consensus
   - Automated feedback loop

4. **Frontend verbessern**
   - Styling mit MUI
   - Code-Anzeige
   - Copy-to-Clipboard
   - Filter und Suche

5. **Deployment**
   - Backend zu Cloud Run
   - Frontend zu Cloud Run
   - Production GCS Bucket

---

## Troubleshooting

### Problem: Tests schlagen fehl

**Lösung:**
```bash
# Dependencies neu installieren
uv sync --reinstall

# Cache löschen
rm -rf .pytest_cache __pycache__

# Tests einzeln ausführen
uv run pytest tests/unit/plots/matplotlib/test_scatter_basic_001.py::test_creates_valid_figure -v
```

### Problem: GCS Upload schlägt fehl

**Lösung:**
```bash
# Credentials prüfen
gcloud auth application-default login

# Bucket-Berechtigungen prüfen
gsutil iam get gs://pyplots-images-dev

# Manuell hochladen
gsutil cp test_output.png gs://pyplots-images-dev/test/
```

### Problem: API gibt 500 zurück

**Lösung:**
```bash
# Logs prüfen
# (Im Terminal wo uvicorn läuft)

# Datenbank-Verbindung prüfen
psql $DATABASE_URL -c "SELECT 1"

# Migrations prüfen
uv run alembic current
uv run alembic upgrade head
```

### Problem: Frontend zeigt keine Bilder

**Lösung:**
```bash
# CORS prüfen (siehe Browser Console)
# API CORS Middleware aktivieren

# Bild-URLs prüfen
curl http://localhost:8000/specs/scatter-basic-001/implementations | jq '.[] | .preview_url'

# GCS Permissions prüfen (Bilder müssen public sein)
```

---

## Zeitschätzung

**Gesamtdauer:** ~4-5 Stunden

- Phase 1 (Setup): 30 min
- Phase 2 (Issue): 10 min
- Phase 3 (Spec): 5 min
- Phase 4 (matplotlib): 30 min
- Phase 5 (seaborn): 30 min
- Phase 6 (Multi-Version): 20 min
- Phase 7 (Upload): 15 min
- Phase 8 (DB): 20 min
- Phase 9 (API): 30 min
- Phase 10 (Frontend): 45 min
- Phase 11 (E2E): 15 min
- Phase 12 (Docs): 20 min
- Phase 13 (Push): 10 min

**Buffer:** 30-60 min für Troubleshooting

---

## Zusammenfassung

Dieser POC demonstriert den kompletten Workflow von pyplots:

1. **Manuelle Orchestrierung** durch Claude Code (statt GitHub Actions)
2. **Spec-First Approach** (GitHub Issue → Spec File → Code)
3. **Multi-Library Support** (matplotlib + seaborn)
4. **Quality Assurance** (Self-Review + Tests + Visual Inspection)
5. **Cloud Storage** (GCS für Bilder)
6. **Database Metadata** (PostgreSQL)
7. **API + Frontend** (FastAPI + Next.js)

**Der POC beweist:**
- Der Workflow funktioniert End-to-End
- Die Architektur ist skalierbar
- Automatisierung ist möglich (später mit GitHub Actions)
- Das Produkt ist technisch machbar

**Nächster Schritt:** Automatisierung und mehr Plot-Typen! 🚀
