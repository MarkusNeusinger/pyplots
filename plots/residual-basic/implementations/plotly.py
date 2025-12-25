"""pyplots.ai
residual-basic: Residual Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import plotly.graph_objects as go


# Data - Simulate a linear regression with some heteroscedasticity
np.random.seed(42)
n = 150

# Generate fitted values (predictions from a model)
fitted = np.linspace(10, 100, n)

# Generate residuals with slight heteroscedasticity pattern (variance increases with fitted)
# Some points show clear patterns, others are random - mimics real regression diagnostics
base_residuals = np.random.randn(n) * (3 + 0.03 * fitted)
# Add a subtle non-linear pattern to make diagnostics interesting
slight_pattern = 0.5 * np.sin(fitted / 15)
residuals = base_residuals + slight_pattern

# Sort for trend line calculation
sort_idx = np.argsort(fitted)
fitted_sorted = fitted[sort_idx]
residuals_sorted = residuals[sort_idx]

# Compute smoothed trend line using numpy convolution (moving average)
window_size = 15
kernel = np.ones(window_size) / window_size
smoothed = np.convolve(residuals_sorted, kernel, mode="same")
# Fix edge effects by using edge values
smoothed[: window_size // 2] = smoothed[window_size // 2]
smoothed[-(window_size // 2) :] = smoothed[-(window_size // 2) - 1]

# Create figure
fig = go.Figure()

# Add scatter points for residuals
fig.add_trace(
    go.Scatter(
        x=fitted,
        y=residuals,
        mode="markers",
        marker=dict(
            size=14,
            color="#306998",  # Python Blue
            opacity=0.6,
            line=dict(width=1, color="#1a3d5c"),
        ),
        name="Residuals",
        hovertemplate="Fitted: %{x:.1f}<br>Residual: %{y:.2f}<extra></extra>",
    )
)

# Add horizontal reference line at y=0 (as a trace for legend visibility)
fig.add_trace(
    go.Scatter(
        x=[fitted.min(), fitted.max()],
        y=[0, 0],
        mode="lines",
        line=dict(color="#FFD43B", width=3, dash="dash"),
        name="Zero Reference",
        hoverinfo="skip",
    )
)

# Add smoothed trend line
fig.add_trace(
    go.Scatter(
        x=fitted_sorted,
        y=smoothed,
        mode="lines",
        line=dict(color="#c44e52", width=4),
        name="Trend (Smoothed)",
        hovertemplate="Fitted: %{x:.1f}<br>Smoothed: %{y:.2f}<extra></extra>",
    )
)

# Update layout for large canvas
fig.update_layout(
    title=dict(
        text="residual-basic \u00b7 plotly \u00b7 pyplots.ai",
        font=dict(size=32, color="#2d2d2d"),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Fitted Values", font=dict(size=24)),
        tickfont=dict(size=18),
        gridcolor="rgba(128, 128, 128, 0.3)",
        gridwidth=1,
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Residuals", font=dict(size=24)),
        tickfont=dict(size=18),
        gridcolor="rgba(128, 128, 128, 0.3)",
        gridwidth=1,
        zeroline=False,
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(
        font=dict(size=18),
        x=0.98,
        y=0.98,
        xanchor="right",
        yanchor="top",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="rgba(128, 128, 128, 0.3)",
        borderwidth=1,
    ),
    margin=dict(l=100, r=80, t=100, b=100),
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
