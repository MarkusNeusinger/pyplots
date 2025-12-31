""" pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

# Time series data for main chart (spanning 2 columns)
dates = pd.date_range("2024-01-01", periods=120, freq="D")
base_price = 100 + np.cumsum(np.random.randn(120) * 2)
price_df = pd.DataFrame({"date": dates, "price": base_price})

# Volume data for bar chart
volume_df = pd.DataFrame({"date": dates, "volume": np.random.randint(500, 2000, 120)})

# Daily returns for histogram
returns = np.diff(base_price) / base_price[:-1] * 100
returns_df = pd.DataFrame({"returns": returns})

# Correlation scatter data
scatter_df = pd.DataFrame({"feature_a": np.random.randn(80) * 15 + 50, "feature_b": np.random.randn(80) * 10 + 40})
scatter_df["feature_b"] = scatter_df["feature_a"] * 0.6 + scatter_df["feature_b"]

# Category breakdown for pie-like (arc) chart
category_df = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D"], "value": [35, 28, 22, 15]}
)

# Main time series chart (spans full width - equivalent to colspan=2)
main_chart = (
    alt.Chart(price_df)
    .mark_line(strokeWidth=4, color="#306998")
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(labelFontSize=16, titleFontSize=18)),
        y=alt.Y("price:Q", title="Price ($)", axis=alt.Axis(labelFontSize=16, titleFontSize=18)),
    )
    .properties(width=900, height=350, title=alt.Title("Daily Price Trend (Main View)", fontSize=22))
)

# Volume bar chart
volume_chart = (
    alt.Chart(volume_df)
    .mark_bar(color="#FFD43B", opacity=0.85)
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        y=alt.Y("volume:Q", title="Volume", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    )
    .properties(width=440, height=200, title=alt.Title("Trading Volume", fontSize=18))
)

# Returns histogram
histogram_chart = (
    alt.Chart(returns_df)
    .mark_bar(color="#306998", opacity=0.75)
    .encode(
        x=alt.X(
            "returns:Q",
            bin=alt.Bin(maxbins=20),
            title="Daily Return (%)",
            axis=alt.Axis(labelFontSize=14, titleFontSize=16),
        ),
        y=alt.Y("count():Q", title="Frequency", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    )
    .properties(width=440, height=200, title=alt.Title("Return Distribution", fontSize=18))
)

# Scatter plot for correlation
scatter_chart = (
    alt.Chart(scatter_df)
    .mark_circle(size=120, color="#306998", opacity=0.65)
    .encode(
        x=alt.X("feature_a:Q", title="Feature A", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        y=alt.Y("feature_b:Q", title="Feature B", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    )
    .properties(width=440, height=200, title=alt.Title("Feature Correlation", fontSize=18))
)

# Category breakdown using arc chart (donut)
arc_chart = (
    alt.Chart(category_df)
    .mark_arc(innerRadius=50, outerRadius=90)
    .encode(
        theta=alt.Theta("value:Q"),
        color=alt.Color(
            "category:N",
            scale=alt.Scale(
                domain=["Product A", "Product B", "Product C", "Product D"],
                range=["#306998", "#FFD43B", "#4B8BBE", "#E6B800"],
            ),
            legend=alt.Legend(labelFontSize=14, titleFontSize=16, orient="right", title="Category"),
        ),
    )
    .properties(width=440, height=200, title=alt.Title("Category Breakdown", fontSize=18))
)

# Create custom grid layout using vconcat and hconcat
# Row 1: Main chart spanning full width (equivalent to colspan=2)
# Row 2: Volume and Histogram side by side
# Row 3: Scatter and Arc chart side by side

top_row = main_chart

middle_row = alt.hconcat(volume_chart, histogram_chart).resolve_scale(x="independent", y="independent")

bottom_row = alt.hconcat(scatter_chart, arc_chart).resolve_scale(x="independent", y="independent")

# Combine all rows vertically with main title
combined = (
    alt.vconcat(top_row, middle_row, bottom_row)
    .resolve_scale(x="independent", y="independent")
    .configure(background="white")
    .configure_title(anchor="start", fontSize=24, offset=10)
    .configure_concat(spacing=25)
    .properties(title=alt.Title("subplot-grid-custom · altair · pyplots.ai", fontSize=30, anchor="middle", offset=15))
)

# Save outputs
combined.save("plot.png", scale_factor=3.0)
combined.save("plot.html")
