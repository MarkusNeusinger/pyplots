""" pyplots.ai
line-yield-curve: Yield Curve (Interest Rate Term Structure)
Library: plotly 6.6.0 | Python 3.14.3
Quality: 89/100 | Created: 2026-03-14
"""

import numpy as np
import plotly.graph_objects as go


# Data - U.S. Treasury yield curves on three dates showing normal, flat, and inverted shapes
maturity_labels = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
maturity_years = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])

# Normal upward-sloping curve (Jan 2022)
yields_normal = np.array([0.08, 0.21, 0.44, 0.78, 1.18, 1.42, 1.72, 1.90, 1.98, 2.32, 2.27])

# Flat curve (Jun 2023)
yields_flat = np.array([5.27, 5.40, 5.47, 5.40, 4.87, 4.49, 4.13, 4.03, 3.84, 4.09, 3.91])

# Inverted curve (Oct 2023)
yields_inverted = np.array([5.54, 5.55, 5.56, 5.46, 5.05, 4.80, 4.62, 4.65, 4.62, 4.98, 4.81])

# Colors
colors = ["#306998", "#E8833A", "#C74C4C"]

# Plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=maturity_years,
        y=yields_normal,
        name="Jan 2022 (Normal)",
        mode="lines+markers",
        line={"color": colors[0], "width": 4},
        marker={"size": 12},
        hovertemplate="%{text}<br>Yield: %{y:.2f}%<extra>Jan 2022</extra>",
        text=maturity_labels,
    )
)

fig.add_trace(
    go.Scatter(
        x=maturity_years,
        y=yields_flat,
        name="Jun 2023 (Flat)",
        mode="lines+markers",
        line={"color": colors[1], "width": 4},
        marker={"size": 12},
        hovertemplate="%{text}<br>Yield: %{y:.2f}%<extra>Jun 2023</extra>",
        text=maturity_labels,
    )
)

fig.add_trace(
    go.Scatter(
        x=maturity_years,
        y=yields_inverted,
        name="Oct 2023 (Inverted)",
        mode="lines+markers",
        line={"color": colors[2], "width": 4},
        marker={"size": 12},
        hovertemplate="%{text}<br>Yield: %{y:.2f}%<extra>Oct 2023</extra>",
        text=maturity_labels,
    )
)

# Inversion shading - highlight region where short-term > long-term for inverted curve
short_term_max = max(yields_inverted[:4])
long_term_min = min(yields_inverted[6:])
fig.add_hrect(
    y0=long_term_min,
    y1=short_term_max,
    fillcolor="rgba(199, 76, 76, 0.08)",
    line_width=0,
    annotation_text="Inversion Zone",
    annotation_position="top right",
    annotation_font={"size": 18, "color": "rgba(199, 76, 76, 0.7)"},
)

# Layout
fig.update_layout(
    title={
        "text": "U.S. Treasury Yield Curves · line-yield-curve · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Maturity", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "tickvals": maturity_years,
        "ticktext": maturity_labels,
        "type": "log",
        "showgrid": False,
    },
    yaxis={
        "title": {"text": "Yield (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "ticksuffix": "%",
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.15)",
    },
    legend={
        "font": {"size": 20},
        "x": 0.02,
        "y": 0.98,
        "xanchor": "left",
        "yanchor": "top",
        "bgcolor": "rgba(255, 255, 255, 0.8)",
        "bordercolor": "rgba(128, 128, 128, 0.3)",
        "borderwidth": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 80, "t": 120, "b": 100},
    hovermode="x unified",
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
