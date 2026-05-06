""" anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: altair 6.1.0 | Python 3.13.13
Quality: 88/100 | Updated: 2026-05-06
"""

import os

import altair as alt
import numpy as np
import pandas as pd


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data: Create a correlation matrix with better representation of positive/negative correlations
np.random.seed(42)

# Business metrics with meaningful correlations
metrics = ["Revenue", "Marketing", "R&D", "Support", "Profit", "Growth", "Efficiency"]
n_metrics = len(metrics)

# Generate base data with controlled correlations
base_data = np.random.randn(150, n_metrics)

# Introduce realistic correlations
base_data[:, 1] = base_data[:, 0] * 0.7 + np.random.randn(150) * 0.3  # Marketing ↔ Revenue
base_data[:, 2] = base_data[:, 0] * 0.6 + np.random.randn(150) * 0.4  # R&D ↔ Revenue
base_data[:, 3] = -base_data[:, 1] * 0.5 + np.random.randn(150) * 0.5  # Support ↔ Marketing (inverse)
base_data[:, 4] = base_data[:, 0] * 0.8 - base_data[:, 3] * 0.3 + np.random.randn(150) * 0.2  # Profit
base_data[:, 5] = base_data[:, 2] * 0.65 + np.random.randn(150) * 0.35  # Growth ↔ R&D
base_data[:, 6] = -base_data[:, 1] * 0.4 + base_data[:, 0] * 0.3 + np.random.randn(150) * 0.5  # Efficiency

# Calculate correlation matrix
corr_matrix = np.corrcoef(base_data.T)

# Create long-format DataFrame for Altair
rows = []
for i, row_metric in enumerate(metrics):
    for j, col_metric in enumerate(metrics):
        rows.append({"x": col_metric, "y": row_metric, "correlation": round(corr_matrix[i, j], 2)})

df = pd.DataFrame(rows)

# Create base heatmap with rectangles
base_chart = (
    alt.Chart(df)
    .mark_rect(stroke="white", strokeWidth=2)
    .encode(
        x=alt.X(
            "x:N",
            title="Business Metrics",
            sort=metrics,
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=-45),
        ),
        y=alt.Y("y:N", title="Business Metrics", sort=metrics, axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        color=alt.Color(
            "correlation:Q",
            scale=alt.Scale(scheme="brownbluegreen", domain=[-1, 1]),
            legend=alt.Legend(
                title="Correlation", titleFontSize=18, labelFontSize=16, fillColor=ELEVATED_BG, strokeColor=INK_SOFT
            ),
        ),
        tooltip=[
            alt.Tooltip("x:N", title="Column"),
            alt.Tooltip("y:N", title="Row"),
            alt.Tooltip("correlation:Q", title="Correlation", format=".2f"),
        ],
    )
)

# Create text layer for annotations with conditional color
text = (
    alt.Chart(df)
    .mark_text(fontSize=20, fontWeight="bold")
    .encode(
        x=alt.X("x:N", sort=metrics),
        y=alt.Y("y:N", sort=metrics),
        text=alt.Text("correlation:Q", format=".2f"),
        color=alt.condition(
            (alt.datum.correlation > 0.5) | (alt.datum.correlation < -0.5), alt.value("white"), alt.value(INK_SOFT)
        ),
    )
)

# Combine heatmap and text
chart = (
    (base_chart + text)
    .properties(
        width=1600,
        height=1600,
        title=alt.Title("heatmap-annotated · altair · anyplot.ai", fontSize=28, anchor="middle"),
        background=PAGE_BG,
    )
    .configure_view(fill=PAGE_BG, stroke=INK_SOFT, strokeWidth=0)
    .configure_axis(
        domainColor=INK_SOFT,
        tickColor=INK_SOFT,
        gridColor=INK_SOFT,
        gridOpacity=0.0,
        labelColor=INK_SOFT,
        titleColor=INK,
    )
    .configure_title(color=INK, fontSize=28, anchor="middle")
    .configure_legend(
        fillColor=ELEVATED_BG,
        strokeColor=INK_SOFT,
        labelColor=INK_SOFT,
        titleColor=INK,
        titleFontSize=18,
        labelFontSize=16,
    )
)

# Save as PNG (scale_factor=3 for high resolution: 1600x1600 * 3 = 4800x4800, scaled to 3600x3600)
chart.save(f"plot-{THEME}.png", scale_factor=2.25)

# Save as HTML for interactive version
chart.save(f"plot-{THEME}.html")
