"""pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: plotly | Python 3.13
Quality: pending | Created: 2026-02-18
"""

import numpy as np
import plotly.graph_objects as go


np.random.seed(42)

# Data - Technology innovation items across sectors and time horizons
sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech"]
rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_radii = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

innovations = [
    # AI & ML sector
    {"name": "LLM Agents", "sector": "AI & ML", "ring": "Adopt"},
    {"name": "RAG Pipelines", "sector": "AI & ML", "ring": "Adopt"},
    {"name": "Multimodal Models", "sector": "AI & ML", "ring": "Trial"},
    {"name": "AI Code Review", "sector": "AI & ML", "ring": "Trial"},
    {"name": "Neuromorphic Chips", "sector": "AI & ML", "ring": "Assess"},
    {"name": "Autonomous Research", "sector": "AI & ML", "ring": "Hold"},
    {"name": "Quantum ML", "sector": "AI & ML", "ring": "Hold"},
    # Cloud & Infra sector
    {"name": "Platform Engineering", "sector": "Cloud & Infra", "ring": "Adopt"},
    {"name": "FinOps", "sector": "Cloud & Infra", "ring": "Adopt"},
    {"name": "WebAssembly", "sector": "Cloud & Infra", "ring": "Trial"},
    {"name": "Edge Computing", "sector": "Cloud & Infra", "ring": "Trial"},
    {"name": "Confidential Computing", "sector": "Cloud & Infra", "ring": "Assess"},
    {"name": "Serverless GPUs", "sector": "Cloud & Infra", "ring": "Assess"},
    {"name": "Decentralized Cloud", "sector": "Cloud & Infra", "ring": "Hold"},
    # Sustainability sector
    {"name": "Carbon Tracking APIs", "sector": "Sustainability", "ring": "Adopt"},
    {"name": "Green Software", "sector": "Sustainability", "ring": "Trial"},
    {"name": "Digital Product Passports", "sector": "Sustainability", "ring": "Trial"},
    {"name": "Circular Economy Platforms", "sector": "Sustainability", "ring": "Assess"},
    {"name": "Fusion Energy Tech", "sector": "Sustainability", "ring": "Hold"},
    {"name": "Climate AI", "sector": "Sustainability", "ring": "Assess"},
    # Biotech sector
    {"name": "mRNA Therapeutics", "sector": "Biotech", "ring": "Adopt"},
    {"name": "CRISPR Diagnostics", "sector": "Biotech", "ring": "Trial"},
    {"name": "Digital Twins (Health)", "sector": "Biotech", "ring": "Assess"},
    {"name": "Synthetic Biology", "sector": "Biotech", "ring": "Assess"},
    {"name": "Brain-Computer Interfaces", "sector": "Biotech", "ring": "Hold"},
    {"name": "Longevity Engineering", "sector": "Biotech", "ring": "Hold"},
]

# Sector angular ranges (270-degree layout, leaving bottom-right for legend/title area)
sector_count = len(sectors)
sector_span = 270 / sector_count
sector_starts = {sector: i * sector_span for i, sector in enumerate(sectors)}

# Color palette per sector (starting with Python Blue, colorblind-safe)
sector_colors = {"AI & ML": "#306998", "Cloud & Infra": "#E0872B", "Sustainability": "#2A9D8F", "Biotech": "#8E4585"}

# Compute angular positions with jitter within each sector
item_angles = []
item_radii = []
item_names = []
item_sectors = []

for sector in sectors:
    sector_items = [inn for inn in innovations if inn["sector"] == sector]
    start_angle = sector_starts[sector]

    # Group by ring within each sector
    for ring in rings:
        ring_items = [item for item in sector_items if item["ring"] == ring]
        if not ring_items:
            continue
        n = len(ring_items)
        # Spread items evenly within the sector span, with padding
        padding = sector_span * 0.12
        usable_span = sector_span - 2 * padding
        for idx, item in enumerate(ring_items):
            if n == 1:
                angle = start_angle + sector_span / 2
            else:
                angle = start_angle + padding + usable_span * idx / (n - 1)

            # Add small radial jitter for readability
            base_r = ring_radii[ring]
            jitter = np.random.uniform(-0.25, 0.25)
            r = base_r + jitter

            item_angles.append(angle)
            item_radii.append(r)
            item_names.append(item["name"])
            item_sectors.append(item["sector"])

# Create figure
fig = go.Figure()

# Draw subtle ring background fills for visual separation
ring_fills = [
    (0, 1.5, "rgba(48, 105, 152, 0.04)"),
    (1.5, 2.5, "rgba(48, 105, 152, 0.03)"),
    (2.5, 3.5, "rgba(48, 105, 152, 0.02)"),
    (3.5, 4.5, "rgba(48, 105, 152, 0.01)"),
]
theta_fill = np.linspace(0, 270, 200).tolist()
for r_inner, r_outer, fill_color in ring_fills:
    r_vals = [r_outer] * len(theta_fill) + [r_inner] * len(theta_fill)
    t_vals = theta_fill + theta_fill[::-1]
    fig.add_trace(
        go.Scatterpolar(
            r=r_vals,
            theta=t_vals,
            fill="toself",
            fillcolor=fill_color,
            line={"width": 0},
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Draw ring boundary circles (concentric rings)
for radius in [1.5, 2.5, 3.5, 4.5]:
    theta_circle = np.linspace(0, 270, 200)
    r_circle = np.full_like(theta_circle, radius)
    fig.add_trace(
        go.Scatterpolar(
            r=r_circle.tolist(),
            theta=theta_circle.tolist(),
            mode="lines",
            line={"color": "rgba(0, 0, 0, 0.12)", "width": 1.5},
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Draw sector divider lines
for sector in sectors:
    angle = sector_starts[sector]
    fig.add_trace(
        go.Scatterpolar(
            r=[0, 4.7],
            theta=[angle, angle],
            mode="lines",
            line={"color": "rgba(0, 0, 0, 0.2)", "width": 1, "dash": "dot"},
            showlegend=False,
            hoverinfo="skip",
        )
    )
# Closing line at 270 degrees
fig.add_trace(
    go.Scatterpolar(
        r=[0, 4.7],
        theta=[270, 270],
        mode="lines",
        line={"color": "rgba(0, 0, 0, 0.2)", "width": 1, "dash": "dot"},
        showlegend=False,
        hoverinfo="skip",
    )
)

# Add innovation items per sector (for legend grouping)
for sector in sectors:
    mask = [i for i, s in enumerate(item_sectors) if s == sector]
    sector_r = [item_radii[i] for i in mask]
    sector_theta = [item_angles[i] for i in mask]
    sector_names = [item_names[i] for i in mask]

    fig.add_trace(
        go.Scatterpolar(
            r=sector_r,
            theta=sector_theta,
            mode="markers+text",
            marker={
                "size": 16,
                "color": sector_colors[sector],
                "line": {"color": "white", "width": 2},
                "symbol": "circle",
            },
            text=sector_names,
            textposition="top center",
            textfont={"size": 12, "color": sector_colors[sector]},
            name=sector,
            legendgroup=sector,
            hovertemplate="%{text}<extra>" + sector + "</extra>",
        )
    )

# Add ring labels along a radial line
for ring_name, radius in ring_radii.items():
    fig.add_trace(
        go.Scatterpolar(
            r=[radius],
            theta=[278],
            mode="text",
            text=[f"<b>{ring_name}</b>"],
            textfont={"size": 15, "color": "rgba(80, 80, 80, 0.9)"},
            textposition="middle right",
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Add sector header labels along the outer edge
for sector in sectors:
    mid_angle = sector_starts[sector] + sector_span / 2
    fig.add_trace(
        go.Scatterpolar(
            r=[5.0],
            theta=[mid_angle],
            mode="text",
            text=[f"<b>{sector}</b>"],
            textfont={"size": 18, "color": sector_colors[sector]},
            textposition="top center",
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Layout
fig.update_layout(
    title={
        "text": "radar-innovation-timeline · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.97,
    },
    polar={
        "radialaxis": {"visible": False, "range": [0, 5.5]},
        "angularaxis": {"visible": False, "direction": "clockwise", "rotation": 90},
        "bgcolor": "rgba(250, 250, 250, 0.3)",
    },
    legend={
        "font": {"size": 16},
        "x": 0.92,
        "y": 0.08,
        "xanchor": "left",
        "yanchor": "bottom",
        "bgcolor": "rgba(255, 255, 255, 0.95)",
        "bordercolor": "rgba(0, 0, 0, 0.15)",
        "borderwidth": 1,
        "title": {"text": "Sectors", "font": {"size": 18}},
    },
    template="plotly_white",
    margin={"l": 80, "r": 120, "t": 80, "b": 80},
    paper_bgcolor="white",
    width=1200,
    height=1200,
)

# Save
fig.write_image("plot.png", width=1200, height=1200, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
