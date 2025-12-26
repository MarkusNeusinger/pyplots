""" pyplots.ai
line-confidence: Line Plot with Confidence Interval
Library: altair 6.0.0 | Python 3.13.11
Quality: 84/100 | Created: 2025-12-26
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Simulating a time series forecast with 95% confidence interval
np.random.seed(42)

# Generate time points (50 days of daily data)
n_points = 50
days = np.arange(n_points)

# Create a trend with some curvature (e.g., a model prediction)
trend = 100 + 0.5 * days + 0.02 * days**2 + np.sin(days / 5) * 5

# Add noise for the central line
noise = np.random.normal(0, 3, n_points)
y_mean = trend + noise

# Confidence interval that widens over time (typical for forecasts)
uncertainty = 5 + 0.15 * days  # Uncertainty grows with time
y_lower = y_mean - 1.96 * uncertainty / 2
y_upper = y_mean + 1.96 * uncertainty / 2

# Create DataFrame with legend columns for proper legend display
df = pd.DataFrame(
    {
        "Day": days,
        "Value": y_mean,
        "Lower": y_lower,
        "Upper": y_upper,
        "Line": "Predicted Mean",
        "Band": "95% Confidence Interval",
    }
)

# Calculate appropriate y-axis domain with padding (avoid unnecessary whitespace from 0)
y_min = df["Lower"].min()
y_max = df["Upper"].max()
y_padding = (y_max - y_min) * 0.1
y_domain = [y_min - y_padding, y_max + y_padding]

# Define color scale for legend
color_scale = alt.Scale(domain=["Predicted Mean", "95% Confidence Interval"], range=["#306998", "#306998"])

# Create the confidence band (area) with legend entry
band = (
    alt.Chart(df)
    .mark_area(opacity=0.3)
    .encode(
        x=alt.X("Day:Q", title="Day", axis=alt.Axis(values=list(range(0, 51, 5)))),
        y=alt.Y("Lower:Q", title="Predicted Value", scale=alt.Scale(domain=y_domain)),
        y2="Upper:Q",
        fill=alt.Fill("Band:N", scale=color_scale, legend=alt.Legend(title="Legend", symbolType="square")),
    )
)

# Create the central line with legend entry
line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4)
    .encode(
        x="Day:Q",
        y=alt.Y("Value:Q"),
        color=alt.Color("Line:N", scale=color_scale, legend=alt.Legend(title="Legend", symbolStrokeWidth=4)),
    )
)

# Add point markers on the line for clarity
points = alt.Chart(df).mark_point(size=60, filled=True, color="#306998").encode(x="Day:Q", y=alt.Y("Value:Q"))

# Combine band, line, and points
chart = (
    alt.layer(band, line, points)
    .properties(
        width=1600, height=900, title=alt.Title("line-confidence · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .configure_legend(labelFontSize=16, titleFontSize=18, symbolSize=200, orient="top-right")
)

# Save as PNG (scale_factor=3 gives 4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save as HTML for interactivity
interactive_band = (
    alt.Chart(df)
    .mark_area(opacity=0.3, color="#306998")
    .encode(
        x=alt.X("Day:Q", title="Day"),
        y=alt.Y("Lower:Q", title="Predicted Value", scale=alt.Scale(domain=y_domain)),
        y2="Upper:Q",
        tooltip=[
            alt.Tooltip("Day:Q", title="Day"),
            alt.Tooltip("Lower:Q", title="Lower Bound", format=".1f"),
            alt.Tooltip("Upper:Q", title="Upper Bound", format=".1f"),
        ],
    )
)

interactive_line = alt.Chart(df).mark_line(strokeWidth=3, color="#306998").encode(x="Day:Q", y=alt.Y("Value:Q"))

interactive_points = (
    alt.Chart(df)
    .mark_point(size=40, filled=True, color="#306998")
    .encode(
        x="Day:Q",
        y=alt.Y("Value:Q"),
        tooltip=[alt.Tooltip("Day:Q", title="Day"), alt.Tooltip("Value:Q", title="Predicted Value", format=".1f")],
    )
)

interactive_chart = (
    alt.layer(interactive_band, interactive_line, interactive_points)
    .properties(
        width=800, height=450, title=alt.Title("line-confidence · altair · pyplots.ai", fontSize=20, anchor="middle")
    )
    .configure_axis(labelFontSize=14, titleFontSize=16, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .interactive()
)

interactive_chart.save("plot.html")
