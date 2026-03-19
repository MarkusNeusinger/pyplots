"""pyplots.ai
spc-xbar-r: Statistical Process Control Chart (X-bar/R)
Library: plotly | Python 3.13
Quality: pending | Created: 2026-03-19
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data
np.random.seed(42)
n_samples = 30
subgroup_size = 5

# Control chart constants for subgroup size 5
A2 = 0.577
D3 = 0.0
D4 = 2.114

# Generate realistic shaft diameter measurements (mm) from CNC machining
process_mean = 25.0
process_std = 0.05
measurements = np.random.normal(process_mean, process_std, (n_samples, subgroup_size))

# Inject out-of-control points
measurements[7] += 0.15
measurements[18] -= 0.12
measurements[24] += 0.18

# Calculate X-bar and R for each sample
sample_means = measurements.mean(axis=1)
sample_ranges = measurements.max(axis=1) - measurements.min(axis=1)

# Control limits for X-bar chart
x_bar_bar = sample_means.mean()
r_bar = sample_ranges.mean()
ucl_xbar = x_bar_bar + A2 * r_bar
lcl_xbar = x_bar_bar - A2 * r_bar
upper_warn_xbar = x_bar_bar + (2 / 3) * A2 * r_bar
lower_warn_xbar = x_bar_bar - (2 / 3) * A2 * r_bar

# Control limits for R chart
ucl_r = D4 * r_bar
lcl_r = D3 * r_bar
upper_warn_r = r_bar + (2 / 3) * (ucl_r - r_bar)
lower_warn_r = max(0, r_bar - (2 / 3) * (r_bar - lcl_r))

sample_ids = np.arange(1, n_samples + 1)

# Identify out-of-control points
ooc_xbar = (sample_means > ucl_xbar) | (sample_means < lcl_xbar)
ooc_r = (sample_ranges > ucl_r) | (sample_ranges < lcl_r)

# Plot
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    subplot_titles=["X-bar Chart (Sample Means)", "R Chart (Sample Ranges)"],
)

# --- X-bar Chart ---
fig.add_trace(
    go.Scatter(
        x=sample_ids,
        y=sample_means,
        mode="lines+markers",
        marker={"size": 9, "color": "#306998"},
        line={"width": 2.5, "color": "#306998"},
        name="X-bar",
    ),
    row=1,
    col=1,
)

# Out-of-control points (X-bar)
fig.add_trace(
    go.Scatter(
        x=sample_ids[ooc_xbar],
        y=sample_means[ooc_xbar],
        mode="markers",
        marker={"size": 14, "color": "#D62728", "symbol": "diamond", "line": {"width": 2, "color": "white"}},
        name="Out of Control",
    ),
    row=1,
    col=1,
)

# X-bar control limits
fig.add_hline(y=x_bar_bar, line={"color": "#2ca02c", "width": 2.5}, row=1, col=1)
fig.add_hline(y=ucl_xbar, line={"color": "#D62728", "width": 2, "dash": "dash"}, row=1, col=1)
fig.add_hline(y=lcl_xbar, line={"color": "#D62728", "width": 2, "dash": "dash"}, row=1, col=1)
fig.add_hline(y=upper_warn_xbar, line={"color": "#FF7F0E", "width": 1.5, "dash": "dot"}, row=1, col=1)
fig.add_hline(y=lower_warn_xbar, line={"color": "#FF7F0E", "width": 1.5, "dash": "dot"}, row=1, col=1)

# X-bar limit annotations
fig.add_annotation(
    x=n_samples + 0.8,
    y=ucl_xbar,
    text="UCL",
    font={"size": 14, "color": "#D62728"},
    showarrow=False,
    xref="x",
    yref="y",
)
fig.add_annotation(
    x=n_samples + 0.8,
    y=lcl_xbar,
    text="LCL",
    font={"size": 14, "color": "#D62728"},
    showarrow=False,
    xref="x",
    yref="y",
)
fig.add_annotation(
    x=n_samples + 0.8,
    y=x_bar_bar,
    text="CL",
    font={"size": 14, "color": "#2ca02c"},
    showarrow=False,
    xref="x",
    yref="y",
)

# --- R Chart ---
fig.add_trace(
    go.Scatter(
        x=sample_ids,
        y=sample_ranges,
        mode="lines+markers",
        marker={"size": 9, "color": "#306998"},
        line={"width": 2.5, "color": "#306998"},
        name="Range",
        showlegend=False,
    ),
    row=2,
    col=1,
)

# Out-of-control points (R)
if ooc_r.any():
    fig.add_trace(
        go.Scatter(
            x=sample_ids[ooc_r],
            y=sample_ranges[ooc_r],
            mode="markers",
            marker={"size": 14, "color": "#D62728", "symbol": "diamond", "line": {"width": 2, "color": "white"}},
            name="Out of Control (R)",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

# R chart control limits
fig.add_hline(y=r_bar, line={"color": "#2ca02c", "width": 2.5}, row=2, col=1)
fig.add_hline(y=ucl_r, line={"color": "#D62728", "width": 2, "dash": "dash"}, row=2, col=1)
fig.add_hline(y=lcl_r, line={"color": "#D62728", "width": 2, "dash": "dash"}, row=2, col=1)
fig.add_hline(y=upper_warn_r, line={"color": "#FF7F0E", "width": 1.5, "dash": "dot"}, row=2, col=1)
fig.add_hline(y=lower_warn_r, line={"color": "#FF7F0E", "width": 1.5, "dash": "dot"}, row=2, col=1)

# R chart limit annotations
fig.add_annotation(
    x=n_samples + 0.8, y=ucl_r, text="UCL", font={"size": 14, "color": "#D62728"}, showarrow=False, xref="x2", yref="y2"
)
fig.add_annotation(
    x=n_samples + 0.8, y=lcl_r, text="LCL", font={"size": 14, "color": "#D62728"}, showarrow=False, xref="x2", yref="y2"
)
fig.add_annotation(
    x=n_samples + 0.8, y=r_bar, text="CL", font={"size": 14, "color": "#2ca02c"}, showarrow=False, xref="x2", yref="y2"
)

# Style
fig.update_layout(
    title={"text": "CNC Shaft Diameter Monitoring · spc-xbar-r · plotly · pyplots.ai", "font": {"size": 28}},
    template="plotly_white",
    showlegend=True,
    legend={"font": {"size": 16}, "x": 0.01, "y": 0.98},
    margin={"r": 80},
)

fig.update_annotations(font={"size": 18}, selector={"text": "X-bar Chart (Sample Means)"})
fig.update_annotations(font={"size": 18}, selector={"text": "R Chart (Sample Ranges)"})

fig.update_xaxes(title={"text": "Sample Number", "font": {"size": 22}}, tickfont={"size": 18}, row=2, col=1)
fig.update_yaxes(title={"text": "Sample Mean (mm)", "font": {"size": 22}}, tickfont={"size": 18}, row=1, col=1)
fig.update_yaxes(title={"text": "Sample Range (mm)", "font": {"size": 22}}, tickfont={"size": 18}, row=2, col=1)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
