<img src="app/public/logo.svg" alt="pyplots.ai" width="250">

**→ [pyplots.ai](https://pyplots.ai)**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/MarkusNeusinger/pyplots/actions/workflows/ci-tests.yml/badge.svg?branch=main)](https://github.com/MarkusNeusinger/pyplots/actions/workflows/ci-tests.yml)
[![Ruff](https://github.com/MarkusNeusinger/pyplots/actions/workflows/ci-lint.yml/badge.svg?branch=main)](https://github.com/MarkusNeusinger/pyplots/actions/workflows/ci-lint.yml)
[![codecov](https://codecov.io/github/MarkusNeusinger/pyplots/graph/badge.svg?token=4EGPSHH0H0)](https://codecov.io/github/MarkusNeusinger/pyplots)

> library-agnostic, ai-powered python plotting examples. automatically generated, tested, and maintained.

---

## What is pyplots?

**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and
maintains plotting examples. Browse hundreds of plots across all major Python libraries - matplotlib, seaborn, plotly,
bokeh, altair, plotnine, pygal, highcharts, and lets-plot.

**Community-driven, AI-maintained** - Propose plot ideas via GitHub Issues, AI generates the code, multi-LLM quality
checks ensure excellence. Zero manual coding required.

---

## Features

- **AI-generated code** - All implementations automatically generated and maintained by AI
- **Compare libraries** - View matplotlib, seaborn, plotly side-by-side for the same plot
- **Always current** - AI agents continuously update examples with latest library versions
- **Natural language search** - Find plots by asking "show correlation between variables"
- **Multi-LLM quality checks** - Claude + Gemini + GPT ensure every plot meets quality standards
- **Open source** - Community proposes ideas via Issues, AI generates the code

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/MarkusNeusinger/pyplots.git
cd pyplots

# Install dependencies with uv (fast!)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-extras

# Database setup (optional - API works without DB in limited mode)
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations
uv run alembic upgrade head

# Start backend
uv run uvicorn api.main:app --reload

# Visit http://localhost:8000/docs
```

---

## Architecture

**Specification-first design**: Every plot starts as a Markdown spec (library-agnostic), then AI generates
implementations for all 9 supported libraries.

```
plots/scatter-basic/
├── specification.md     # Library-agnostic specification
├── specification.yaml   # Tags, created, issue, suggested
├── metadata/            # Per-library metadata (quality scores, preview URLs)
│   ├── matplotlib.yaml
│   └── ...
└── implementations/
    ├── matplotlib.py
    ├── seaborn.py
    ├── plotly.py
    └── ... (6 more)
```

**Issue-based workflow**: GitHub Issues as state machine for plot lifecycle. Status tracked via live-updating table (no sub-issues). Each library generates in parallel, creating PRs to a feature branch.

**AI quality review**: Claude evaluates generated plots (score ≥ 90 required). Automatic feedback loops (max 3 attempts per library). Quality scores flow via PR labels → per-library metadata files.

See [docs/architecture/](docs/architecture/) for details.

---

## Tech Stack

**Backend**: FastAPI • PostgreSQL • SQLAlchemy • Python 3.10+

**Frontend**: React 19 • Vite • TypeScript • MUI

**Plotting**: matplotlib • seaborn • plotly • bokeh • altair • plotnine • pygal • highcharts • lets-plot

**Infrastructure**: Google Cloud Run • Cloud SQL • Cloud Storage

**Automation**: GitHub Actions • n8n Cloud Pro

**AI**: Claude (Code Max) • Vertex AI (Multi-LLM)

---

## License Notes

Most plotting libraries are fully open source. Note these exceptions:

- **Highcharts**: Free for non-commercial use. Commercial use requires a license from [highcharts.com](https://www.highcharts.com/license)

---

## Project Structure

```
pyplots/
├── plots/              # Plot-centric directories (spec + metadata + implementations)
│   └── {spec-id}/
│       ├── specification.md
│       ├── specification.yaml
│       ├── metadata/
│       └── implementations/
├── prompts/            # AI agent prompts
├── core/               # Shared business logic
├── api/                # FastAPI backend
├── app/                # React frontend (Vite + MUI)
├── tests/              # Test suite (pytest)
└── docs/               # Documentation
```

**For detailed structure and file organization**, see [Repository Structure](docs/architecture/repository.md)

---

## Documentation

- **[Vision](docs/vision.md)** - Product vision and mission
- **[Workflow](docs/workflow.md)** - Automation flows (Discovery → Deployment → Social Media)
- **[Development](docs/development.md)** - Local setup, testing, deployment
- **[Specs Guide](docs/specs-guide.md)** - How to write plot specifications
- **[Architecture](docs/architecture/)** - API, database, repository structure

---

## Contributing

We welcome contributions! **All code is AI-generated** - you propose ideas, AI implements them.

**How to contribute**:

1. **Propose plot ideas** - Create GitHub Issue with plot description (what you want to visualize)
2. **Improve specs** - Suggest better descriptions for existing plots
3. **Report issues** - Found bugs or quality problems? Open an Issue
4. **Improve docs** - Help others understand the project

**The workflow**:

1. You create Issue with plot idea + add `spec-request` label
2. AI generates spec, creates feature branch
3. Maintainer reviews and adds `approved` label
4. 9 library implementations generate in parallel (tracked via live status table)
5. AI quality review per library (score ≥ 90 required)
6. Auto-merge to feature branch, then to main

**Important**: Don't submit code directly! If a plot has quality issues, it means the spec needs improvement, not the
code.

See [development.md](docs/development.md) for details.

---

## Development

```bash
# Install dependencies (uv is a fast Python package installer)
uv sync --all-extras

# Run tests
uv run pytest

# Start backend
uv run uvicorn api.main:app --reload
```

**For detailed development setup, testing, and code quality tools**, see [Development Guide](docs/development.md)

**Python versions**: 3.10+ | **Coverage target**: 90%+

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Links

- **Website**: [pyplots.ai](https://pyplots.ai)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/MarkusNeusinger/pyplots/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MarkusNeusinger/pyplots/discussions)
- **Stats**: [Public Analytics](https://plausible.io/pyplots.ai)

---

<div align="center">

**Built by [Markus Neusinger](https://linkedin.com/in/markus-neusinger/)**

[⭐ Star us on GitHub](https://github.com/MarkusNeusinger/pyplots) • [🐛 Report Bug](https://github.com/MarkusNeusinger/pyplots/issues) • [💡 Request Feature](https://github.com/MarkusNeusinger/pyplots/issues)

</div>
