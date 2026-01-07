"""pyplots.ai
indicator-bollinger: Bollinger Bands Indicator Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Generate realistic stock price data with Bollinger Bands
np.random.seed(42)

# Generate 120 trading days of price data
n_periods = 120
dates = pd.date_range("2024-01-02", periods=n_periods, freq="B")  # Business days

# Generate realistic price movement (random walk with drift)
returns = np.random.normal(0.001, 0.02, n_periods)  # Small positive drift, 2% daily volatility
price_base = 150.0
close_prices = price_base * np.cumprod(1 + returns)

# Calculate Bollinger Bands (20-period SMA, 2 standard deviations)
window = 20
df = pd.DataFrame({"date": dates, "close": close_prices})
df["sma"] = df["close"].rolling(window=window).mean()
df["std"] = df["close"].rolling(window=window).std()
df["upper_band"] = df["sma"] + 2 * df["std"]
df["lower_band"] = df["sma"] - 2 * df["std"]

# Drop NaN values from rolling calculation
df = df.dropna().reset_index(drop=True)

# Create base chart
base = alt.Chart(df).encode(x=alt.X("date:T", title="Date", axis=alt.Axis(format="%b %Y", labelAngle=-45)))

# Upper band line
upper_line = base.mark_line(strokeWidth=2, color="#306998", opacity=0.7).encode(
    y=alt.Y("upper_band:Q", title="Price ($)", scale=alt.Scale(zero=False))
)

# Lower band line
lower_line = base.mark_line(strokeWidth=2, color="#306998", opacity=0.7).encode(
    y=alt.Y("lower_band:Q", scale=alt.Scale(zero=False))
)

# Band fill area (between upper and lower bands)
band_area = (
    alt.Chart(df)
    .mark_area(opacity=0.15, color="#306998")
    .encode(x=alt.X("date:T"), y=alt.Y("upper_band:Q", scale=alt.Scale(zero=False)), y2="lower_band:Q")
)

# Middle band (SMA) - dashed line
sma_line = base.mark_line(strokeWidth=2.5, strokeDash=[8, 4], color="#306998", opacity=0.9).encode(
    y=alt.Y("sma:Q", scale=alt.Scale(zero=False))
)

# Close price line - prominent
price_line = base.mark_line(strokeWidth=3, color="#FFD43B").encode(y=alt.Y("close:Q", scale=alt.Scale(zero=False)))

# Combine all layers
chart = (
    alt.layer(band_area, upper_line, lower_line, sma_line, price_line)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="indicator-bollinger · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=18, labelFontSize=16)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
