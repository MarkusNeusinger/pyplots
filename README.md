# pyplots

**AI-powered Python plotting library that works with YOUR data.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> Stop adapting examples to your data. Start visualizing your data directly.

---

## What is pyplots?

**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples. Browse hundreds of plots across all major Python libraries - matplotlib, seaborn, plotly, and more.

**Community-driven, AI-maintained** - Propose plot ideas via GitHub Issues, AI generates the code, multi-LLM quality checks ensure excellence. Zero manual coding required.

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

# Start backend
uv run uvicorn api.main:app --reload

# Visit http://localhost:8000/docs
```

---

## Architecture

**Specification-first design**: Every plot starts as a Markdown spec (library-agnostic), then AI generates implementations for all major libraries.

```
specs/scatter-basic-001.md  → plots/matplotlib/scatter/scatter-basic-001/default.py
                            → plots/seaborn/scatterplot/scatter-basic-001/default.py
                            → plots/plotly/scatter/scatter-basic-001/default.py
```

**Issue-based workflow**: GitHub Issues as state machine for plot lifecycle. All quality feedback documented as bot comments - no clutter in repo.

**Multi-LLM quality checks**: Claude + Gemini + GPT evaluate generated plots. Score ≥ 85 required (median). Automatic feedback loops (max 3 attempts).

See [docs/architecture/](docs/architecture/) for details.

---

## Tech Stack

**Backend**: FastAPI • PostgreSQL • SQLAlchemy • Python 3.10+

**Frontend**: Next.js 14 • TypeScript • Tailwind CSS

**Plotting**: matplotlib • seaborn • plotly (more coming)

**Infrastructure**: Google Cloud Run • Cloud SQL • Cloud Storage

**Automation**: GitHub Actions • n8n Cloud Pro

**AI**: Claude (Code Max) • Vertex AI (Multi-LLM)

---

## Project Structure

```
pyplots/
├── specs/              # Plot specifications (Markdown)
├── plots/              # Library-specific implementations
│   ├── matplotlib/
│   ├── seaborn/
│   └── plotly/
├── core/               # Shared business logic
├── api/                # FastAPI backend
├── app/                # Next.js frontend
├── automation/         # AI code generation
├── tests/              # Test suite (pytest)
└── docs/               # Documentation
    ├── architecture/   # System design
    ├── development.md  # Developer guide
    └── deployment.md   # Cloud deployment
```

---

## Documentation

- **[Vision](docs/vision.md)** - Product vision and mission
- **[Workflow](docs/workflow.md)** - 7 automation flows (Discovery → Deployment → Social Media)
- **[Architecture](docs/architecture/)** - System design, database, API, automation
- **[Development](docs/development.md)** - Local setup, code standards, contributing
- **[Deployment](docs/deployment.md)** - GCP setup, CI/CD, cost optimization

---

## Contributing

We welcome contributions! **All code is AI-generated** - you propose ideas, AI implements them.

**How to contribute**:

1. **Propose plot ideas** - Create GitHub Issue with plot description (what you want to visualize)
2. **Improve specs** - Suggest better descriptions for existing plots
3. **Report issues** - Found bugs or quality problems? Open an Issue
4. **Improve docs** - Help others understand the project

**The workflow**:
- You create Issue with plot idea → AI generates spec → AI generates code for all libraries → Multi-LLM quality check → Deployed

**Important**: Don't submit code directly! If a plot has quality issues, it means the spec needs improvement, not the code.

See [development.md](docs/development.md) for details.

---

## Development

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Type check (optional)
uv sync --extra typecheck
uv run mypy .

# Start backend
uv run uvicorn api.main:app --reload

# Start frontend
cd app && npm run dev
```

**Coverage target**: 90%+

**Python versions**: 3.10, 3.11, 3.12, 3.13

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Links

- **Website**: [pyplots.ai](https://pyplots.ai)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/MarkusNeusinger/pyplots/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MarkusNeusinger/pyplots/discussions)

---

<div align="center">

**Made with ❤️ by the data science community**

[⭐ Star us on GitHub](https://github.com/MarkusNeusinger/pyplots) • [🐛 Report Bug](https://github.com/MarkusNeusinger/pyplots/issues) • [💡 Request Feature](https://github.com/MarkusNeusinger/pyplots/issues)

</div>
