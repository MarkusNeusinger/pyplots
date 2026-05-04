"""anyplot.ai
sunburst-basic: Basic Sunburst Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2026-05-04
"""

import os

import plotly.graph_objects as go


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data - Company budget breakdown by department and team (in $ millions)
labels = [
    # Level 1 - Root (innermost)
    "Company",
    # Level 2 - Departments
    "Engineering",
    "Sales",
    "Marketing",
    "Operations",
    # Level 3 - Teams (outer ring)
    "Backend",
    "Frontend",
    "DevOps",
    "Enterprise",
    "SMB",
    "Digital",
    "Brand",
    "HR",
    "Finance",
]

parents = [
    "",
    "Company",
    "Company",
    "Company",
    "Company",
    "Engineering",
    "Engineering",
    "Engineering",
    "Sales",
    "Sales",
    "Marketing",
    "Marketing",
    "Operations",
    "Operations",
]

# Values in $M — branchvalues="total" so each parent value equals sum of its children
values = [
    48,  # Company
    18,  # Engineering
    15,  # Sales
    7,  # Marketing
    8,  # Operations
    8,  # Backend
    6,  # Frontend
    4,  # DevOps
    10,  # Enterprise
    5,  # SMB
    4,  # Digital
    3,  # Brand
    3,  # HR
    5,  # Finance
]

# Okabe-Ito palette — departments get canonical positions 1-4,
# teams get lighter/darker variants to preserve family grouping
colors = [
    INK_SOFT,  # Company (root) — neutral
    "#009E73",  # Engineering — Okabe-Ito #1
    "#D55E00",  # Sales — Okabe-Ito #2
    "#0072B2",  # Marketing — Okabe-Ito #3
    "#CC79A7",  # Operations — Okabe-Ito #4
    # Engineering teams (green family)
    "#00B589",  # Backend — lighter green
    "#009E73",  # Frontend — base green
    "#007A58",  # DevOps — darker green
    # Sales teams (vermillion family)
    "#F07030",  # Enterprise — lighter vermillion
    "#D55E00",  # SMB — base vermillion
    # Marketing teams (blue family)
    "#2090CC",  # Digital — lighter blue
    "#0072B2",  # Brand — base blue
    # Operations teams (pink/purple family)
    "#DD99C0",  # HR — lighter pink
    "#CC79A7",  # Finance — base pink
]

# Plot
fig = go.Figure(
    go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker={"colors": colors, "line": {"color": PAGE_BG, "width": 2}},
        textfont={"size": 22},
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Budget: $%{value}M<extra></extra>",
    )
)

fig.update_layout(
    title={
        "text": "sunburst-basic · plotly · anyplot.ai",
        "font": {"size": 36, "color": INK},
        "x": 0.5,
        "xanchor": "center",
    },
    paper_bgcolor=PAGE_BG,
    plot_bgcolor=PAGE_BG,
    font={"color": INK},
    margin={"t": 120, "l": 40, "r": 40, "b": 40},
)

# Save
fig.write_image(f"plot-{THEME}.png", width=1600, height=900, scale=3)
fig.write_html(f"plot-{THEME}.html", include_plotlyjs="cdn")
