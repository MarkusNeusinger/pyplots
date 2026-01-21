# pyplots - Project Overview

## Purpose
**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples across 9 major libraries.

## Core Principle
Community proposes plot ideas via GitHub Issues → AI generates code → AI quality review → Deployed

## Supported Libraries (9 total)
- **matplotlib** - The classic standard, maximum flexibility
- **seaborn** - Statistical visualizations, beautiful defaults
- **plotly** - Interactive web plots, dashboards, 3D
- **bokeh** - Interactive, streaming data, large datasets
- **altair** - Declarative/Vega-Lite, elegant exploration
- **plotnine** - ggplot2 syntax for R users
- **pygal** - Minimalistic SVG charts
- **highcharts** - Interactive web charts (requires license for commercial use)
- **lets-plot** - ggplot2 grammar by JetBrains, interactive

## Tech Stack
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy async, asyncpg, PostgreSQL
- **Frontend**: React 19, Vite, TypeScript, MUI 7
- **Package Manager**: uv (fast Python installer)
- **Infrastructure**: Google Cloud Run, Cloud SQL, Cloud Storage
- **AI**: Claude (code generation + quality review)
- **CI/CD**: GitHub Actions with label-driven triggers

## Key Architecture
- Plot-centric design: Everything for one plot lives in `plots/{spec-id}/`
- Specification-driven: Every plot starts as a library-agnostic Markdown spec
- Per-library metadata files (no merge conflicts)
- Quality scores: ≥90 auto-merge, <90 repair loop, ≥50 minimum after 3 attempts
