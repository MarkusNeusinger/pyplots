# 🎨 pyplots

**AI-powered Python plotting examples that work with YOUR data.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> Transform any Python plot example into production-ready code for your specific data in seconds.

## ✨ What makes pyplots different?

### 📊 **Try with YOUR data**
Don't just look at examples with fake data. Upload your CSV/Excel/JSON and see how every plot looks with YOUR actual data.

### 🔍 **Compare all libraries at once**
Why guess which library is best? See the same visualization in matplotlib, seaborn, plotly, bokeh, and altair simultaneously.

### 🤖 **AI understands context**
No rigid categories. Our AI understands what you're trying to visualize and suggests the best approaches.

### ⚡ **Instant code generation**
Get working code tailored to your exact data structure, not generic examples you need to adapt.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/USERNAME/pyplots.git
cd pyplots

# Install with UV (blazing fast)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Start the backend
cd api
uv run uvicorn api.main:app --reload

# In another terminal, start the frontend
cd app
yarn install
yarn dev

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 🎯 Current Status

**⚠️ Early Development Phase**

We're building pyplots following a specification-first architecture. Currently implemented:

- ✅ **Minimal FastAPI backend** - Hello world API ready for plot endpoints
- ✅ **React 19 + TypeScript + Vite frontend** - Modern UI framework setup
- ✅ **Docker + Cloud Run ready** - Deployment infrastructure configured
- ✅ **Architecture documented** - Specification-driven design with Vision-based QA
- ✅ **Google Cloud setup** - europe-west4 region, GCS, Cloud SQL, Cloud Run
- 🔨 **Plot specifications** - Markdown-based specs (in development)
- 🔨 **matplotlib integration** - First library implementation (in development)

### Coming Next
- 📝 Create first plot specifications (scatter, line, bar)
- 🎨 Implement matplotlib plot generators
- 🔍 Vision-based quality checking with Claude
- 📊 "Try with your data" upload functionality
- 🗄️ Database integration (Cloud SQL PostgreSQL)

## 📁 Project Structure

```
pyplots/
├── specs/                     # Plot specifications (Markdown)
│   ├── scatter-basic-001.md   # Generic, library-agnostic specs
│   ├── line-timeseries-002.md
│   └── bar-grouped-003.md
│
├── plots/                     # Library-specific implementations
│   └── matplotlib/            # matplotlib implementations
│       ├── scatter/
│       │   └── scatter-basic-001/
│       │       ├── default.py
│       │       ├── preview.png
│       │       └── quality_report.json
│       └── line/
│
├── core/                      # Shared business logic
│   ├── database.py            # Database connection
│   ├── config.py              # Configuration
│   └── repositories/          # Repository pattern
│
├── api/                       # FastAPI backend
│   ├── main.py                # Application entry point
│   ├── routers/               # API endpoints
│   ├── Dockerfile             # Cloud Run deployment
│   └── cloudbuild.yaml        # Google Cloud Build
│
├── app/                       # React frontend
│   ├── src/
│   │   ├── App.tsx            # Main application
│   │   └── main.tsx           # Entry point
│   ├── Dockerfile             # Multi-stage build
│   ├── nginx.conf             # Production server
│   └── cloudbuild.yaml        # Google Cloud Build
│
├── automation/                # AI code generation
│   └── generators/
│       ├── claude_generator.py    # Plot code generation
│       └── quality_checker.py     # Vision-based QA
│
├── tests/                     # Test suite
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── architecture.md        # Detailed architecture
│   └── vision.md              # Product vision
│
└── pyproject.toml             # Python dependencies
```

## 🏗️ Architecture

### Specification-First Approach

Every plot starts with a **Markdown specification** that's library-agnostic:

```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Description
Create a simple scatter plot showing the relationship between two numeric variables.

## Data Requirements
- **x**: Numeric values for x-axis
- **y**: Numeric values for y-axis

## Quality Criteria
- [ ] X and Y axes are labeled
- [ ] Grid is visible but subtle
- [ ] Points are clearly distinguishable
- [ ] No overlapping axis labels
```

**Why Markdown?**
- ✅ GitHub Issues are Markdown (community can submit specs)
- ✅ Easy for humans to write
- ✅ AI can parse and generate code from it
- ✅ Built-in checklists for quality criteria
- ✅ Renders beautifully on the website

### Vision-Based Quality Assurance

Every generated plot image is analyzed by Claude Vision against the specification's quality criteria. Only plots scoring ≥85 are accepted.

### Multi-Library Support

Same specification, multiple implementations:
```
specs/scatter-basic-001.md  → plots/matplotlib/scatter/scatter-basic-001/default.py
                           → plots/seaborn/scatterplot/scatter-basic-001/default.py
                           → plots/plotly/scatter/scatter-basic-001/default.py
```

## 🛠️ Technology Stack

### Backend
- **Python 3.10+** - Modern Python with type hints
- **UV** - 10-100x faster package manager than pip
- **FastAPI** - High-performance async web framework
- **PostgreSQL** - Cloud SQL database (europe-west4)
- **SQLAlchemy** - Async ORM
- **Pytest** - Testing framework
- **Ruff** - Fast linting and formatting

### Frontend
- **React 19** - Modern UI library
- **TypeScript** - Type safety
- **Vite 7** - Lightning-fast build tool
- **MUI 7** - Material UI components
- **nginx** - Production web server

### Plotting Libraries (Planned)
- **matplotlib** ≥ 3.8.0 (starting with this)
- **seaborn** (coming soon)
- **plotly** (coming soon)
- **bokeh** (planned)
- **altair** (planned)

### Infrastructure
- **Google Cloud Platform** - europe-west4 (Netherlands)
- **Cloud Run** - Serverless container deployment
- **Cloud SQL** - Managed PostgreSQL
- **Google Cloud Storage** - Plot image storage
- **Cloud Build** - CI/CD pipeline

## 💻 Development

### Prerequisites

- Python 3.10+
- Node.js 20+
- UV package manager
- Yarn
- Docker (optional)
- Google Cloud SDK (for deployment)

### Setup

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Install frontend dependencies
cd app
yarn install
cd ..
```

### Run Locally

```bash
# Terminal 1: Start backend
cd api
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd app
yarn dev
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test
uv run pytest tests/unit/test_specific.py

# Test across Python versions
uv run --python 3.10 pytest
uv run --python 3.11 pytest
uv run --python 3.12 pytest
```

### Code Quality

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check (when mypy is added)
uv run mypy .
```

## ☁️ Deployment

### Backend to Cloud Run

```bash
gcloud builds submit --config=api/cloudbuild.yaml
```

### Frontend to Cloud Run

```bash
# Update VITE_API_URL to your backend URL first
gcloud builds submit \
  --config=app/cloudbuild.yaml \
  --substitutions=_VITE_API_URL=https://pyplots-backend-YOUR-PROJECT.run.app
```

### Configuration

Both services deploy to:
- **Region**: europe-west4
- **Platform**: Cloud Run
- **Min instances**: 0 (scale to zero)
- **Max instances**: 3 (backend), 3 (frontend)

## 📊 Supported Plot Types (Roadmap)

Starting with the most common plot types:

### Phase 1: Basics
- [ ] Scatter plots
- [ ] Line plots
- [ ] Bar charts
- [ ] Histograms
- [ ] Box plots

### Phase 2: Statistical
- [ ] Violin plots
- [ ] Heatmaps
- [ ] Correlation matrices
- [ ] Distribution plots
- [ ] Pair plots

### Phase 3: Advanced
- [ ] 3D plots
- [ ] Animations
- [ ] Geographic maps
- [ ] Network graphs
- [ ] Sankey diagrams

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **Add plot specifications** - Create Markdown specs for new plots
2. **Implement plot code** - Code matplotlib/seaborn/plotly implementations
3. **Report bugs** - Found something broken? Let us know
4. **Improve documentation** - Help others understand the project
5. **Test and provide feedback** - Try the platform and share your thoughts

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/pyplots.git

# 2. Create feature branch
git checkout -b feature/scatter-plot-implementation

# 3. Make changes and test
uv run pytest

# 4. Format code
uv run ruff format .

# 5. Commit and push
git add .
git commit -m "feat: implement scatter plot for matplotlib"
git push origin feature/scatter-plot-implementation

# 6. Create Pull Request
```

## 📖 Documentation

- [Architecture](docs/architecture.md) - Detailed system design
- [Vision](docs/vision.md) - Product vision and roadmap
- [API README](api/README.md) - Backend documentation
- [App README](app/README.md) - Frontend documentation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All Python visualization library maintainers
- The data science community
- Anthropic for Claude AI
- Google Cloud Platform
- Early contributors and testers

## 🔗 Links

- 📦 [UV Package Manager](https://github.com/astral-sh/uv)
- ⚡ [Ruff Formatter](https://github.com/astral-sh/ruff)
- 🚀 [FastAPI](https://fastapi.tiangolo.com/)
- ⚛️ [React 19](https://react.dev/)
- ☁️ [Google Cloud Run](https://cloud.google.com/run)

---

<div align="center">
<b>Stop adapting examples to your data. Start visualizing your data directly.</b>

🌟 Star us on GitHub | 📧 Contribute | 💡 Share Ideas
</div>
