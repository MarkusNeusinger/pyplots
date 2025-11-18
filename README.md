# 🎨 pyplots

**AI-powered Python plotting examples that work with YOUR data.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

# Start the development server
make serve

# Open http://localhost:3000
```

## 🎯 Features

### Available Now
- 📚 **500+ plot specifications** across all major libraries
- 🔄 **Multi-library comparison** - See any plot in 5+ libraries
- 📤 **"Try with your data"** - Upload CSV/Excel and visualize instantly  
- 🏷️ **AI-powered tagging** - Natural language search
- ⚡ **Specification-driven** - Every plot guaranteed to work
- 🐍 **Multi-Python support** - Tests on Python 3.10, 3.11, 3.12

### Coming Soon
- 🌐 Natural language to visualization
- 🎨 Auto-styling with your brand colors
- 📊 Data-adaptive plots (auto-adjusts to your data structure)
- 🔌 IDE plugins for real-time suggestions
- 🚀 pip install pyplots

## 📁 Project Structure

```
pyplots/
├── plots/                  # All plot specifications and implementations
│   └── {plot-id}/
│       ├── spec.yaml      # What the plot should do
│       ├── plot.py        # Implementation
│       └── preview.png    # Visual preview
├── website/               # Next.js gallery interface
├── api/                   # FastAPI backend
├── automation/            # n8n workflows and AI tools
└── packages/              # Shared utilities
```

## 💡 Example: Try with Your Data

```python
# 1. Upload your data
import pyplots as pp

data = pp.load("your_sales_data.csv")

# 2. Choose a plot
plot = pp.get("timeseries-multi-line")

# 3. Apply to your data
result = plot.apply(data, 
    x="date", 
    y=["revenue", "profit"],
    title="Company Performance"
)

# 4. Get customized code for YOUR columns
code = result.get_code(library="plotly")
```

## 🔍 Natural Language Search

```python
# Find plots using natural language
results = pp.search("""
    I need to show correlation between multiple variables 
    that handles missing data and looks good in publications
""")

# AI understands: correlation + missing data + publication quality
# Returns relevant plots regardless of library
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to contribute:
- 📝 Add new plot specifications
- 🐛 Report bugs
- 💡 Suggest features
- 📚 Improve documentation
- ⭐ Star the repository

## 🛠️ Development

```bash
# Install dependencies
uv sync --all-extras

# Run tests
make test

# Run specific Python version tests
uv run --python 3.11 pytest

# Add a new plot
./scripts/new-plot.sh "My Amazing Plot"

# Start development server
make serve
```

## 📊 Supported Libraries

- **matplotlib** - The classic, publication-ready plots
- **seaborn** - Statistical data visualization
- **plotly** - Interactive web-based plots
- **bokeh** - Interactive visualization for browsers
- **altair** - Declarative visualization
- **holoviews** - Data analysis and visualization
- More coming soon...

## 🏗️ Architecture

- **Specification-first**: Every plot starts with a clear spec
- **AI-powered tagging**: Dynamic, contextual categorization
- **Multi-version testing**: Ensures compatibility across Python versions
- **Mono-repo structure**: Everything in one place
- **UV package manager**: 10-100x faster than pip

## 📈 Roadmap

- [x] Core plot collection (500+ plots)
- [x] Multi-library comparison
- [x] "Try with your data" feature
- [x] AI-powered tagging
- [ ] Natural language to visualization
- [ ] Real-time collaboration
- [ ] pip package release
- [ ] IDE plugins

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All visualization library maintainers
- The Python data science community
- Contributors and early adopters

---

<div align="center">
<b>Stop adapting examples to your data. Start visualizing your data directly.</b>

🌟 Star us on GitHub | 🌐 [pyplots.ai](https://pyplots.ai) | 📧 hello@pyplots.ai
</div>