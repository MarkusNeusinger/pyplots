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

# Create base encoding for x-axis
x_encoding = alt.X("date:T", title="Date", axis=alt.Axis(format="%b %Y", labelAngle=-45, labelFontSize=18))

# Calculate scale domain for y-axis
y_min = df["lower_band"].min() * 0.98
y_max = df["upper_band"].max() * 1.02
y_scale = alt.Scale(domain=[y_min, y_max], zero=False)

# Band fill area (between upper and lower bands)
band_area = (
    alt.Chart(df)
    .mark_area(opacity=0.2, color="#306998")
    .encode(x=alt.X("date:T"), y=alt.Y("upper_band:Q", scale=y_scale), y2="lower_band:Q")
)

# Upper band line
upper_line = (
    alt.Chart(df)
    .mark_line(strokeWidth=2.5, color="#306998", opacity=0.7)
    .encode(x=x_encoding, y=alt.Y("upper_band:Q", scale=y_scale))
)

# Lower band line
lower_line = (
    alt.Chart(df)
    .mark_line(strokeWidth=2.5, color="#306998", opacity=0.7)
    .encode(x=x_encoding, y=alt.Y("lower_band:Q", scale=y_scale))
)

# Middle band (SMA) - dashed line
sma_line = (
    alt.Chart(df)
    .mark_line(strokeWidth=3, strokeDash=[10, 5], color="#306998", opacity=0.9)
    .encode(x=x_encoding, y=alt.Y("sma:Q", scale=y_scale))
)

# Close price line - prominent
price_line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4, color="#FFD43B")
    .encode(x=x_encoding, y=alt.Y("close:Q", title="Price ($)", scale=y_scale))
)

# Combine all layers
chart = (
    alt.layer(band_area, upper_line, lower_line, sma_line, price_line)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="indicator-bollinger · altair · pyplots.ai",
            subtitle="20-period SMA with 2 standard deviation bands",
            fontSize=28,
            subtitleFontSize=20,
            anchor="middle",
        ),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
