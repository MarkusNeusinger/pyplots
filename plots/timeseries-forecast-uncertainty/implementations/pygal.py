"""pyplots.ai
timeseries-forecast-uncertainty: Time Series Forecast with Uncertainty Band
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Generate time series data: 36 months historical + 12 months forecast
n_historical = 36
n_forecast = 12

# Create date range
dates = pd.date_range(start="2022-01-01", periods=n_historical + n_forecast, freq="MS")
date_labels = [d.strftime("%b %Y") for d in dates]

# Generate historical data with trend and seasonality
t_hist = np.arange(n_historical)
trend = 100 + t_hist * 1.5
seasonality = 15 * np.sin(2 * np.pi * t_hist / 12)
noise = np.random.normal(0, 5, n_historical)
historical = trend + seasonality + noise

# Generate forecast starting from last historical value
t_forecast = np.arange(n_forecast)
last_trend = 100 + (n_historical - 1) * 1.5
forecast_trend = last_trend + (t_forecast + 1) * 1.5
forecast_seasonality = 15 * np.sin(2 * np.pi * (n_historical + t_forecast) / 12)
forecast = forecast_trend + forecast_seasonality

# Calculate confidence intervals (widening over time)
uncertainty_growth = np.sqrt(t_forecast + 1)
std_80 = 8 * uncertainty_growth
std_95 = 15 * uncertainty_growth

lower_80 = forecast - std_80
upper_80 = forecast + std_80
lower_95 = forecast - std_95
upper_95 = forecast + std_95

# Custom style for large canvas with all colors defined
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#306998",  # Historical - Python Blue
        "#E67E22",  # Forecast - Orange
        "#F5B041",  # 95% CI Upper - Light orange
        "#F5B041",  # 95% CI Lower - Light orange
        "#D35400",  # 80% CI Upper - Dark orange
        "#D35400",  # 80% CI Lower - Dark orange
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=6,
    font_family="sans-serif",
)

# Create chart
chart = pygal.Line(
    width=4800,
    height=2700,
    title="timeseries-forecast-uncertainty · pygal · pyplots.ai",
    x_title="Date",
    y_title="Monthly Sales (Units)",
    style=custom_style,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=45,
    show_dots=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    fill=False,
    margin=50,
    spacing=30,
)

# Set x-axis labels (show every 6 months for readability)
chart.x_labels = date_labels
chart.x_labels_major_count = 9

# Prepare data series
# Historical data: values for historical period, None for forecast period
historical_series = list(historical) + [None] * n_forecast

# Forecast data: None for historical period, values for forecast period
# Include last historical point for continuity
forecast_series = [None] * (n_historical - 1) + [historical[-1]] + list(forecast)

# 95% confidence band (upper and lower)
upper_95_series = [None] * (n_historical - 1) + [historical[-1]] + list(upper_95)
lower_95_series = [None] * (n_historical - 1) + [historical[-1]] + list(lower_95)

# 80% confidence band (upper and lower)
upper_80_series = [None] * (n_historical - 1) + [historical[-1]] + list(upper_80)
lower_80_series = [None] * (n_historical - 1) + [historical[-1]] + list(lower_80)

# Add series to chart in proper order
chart.add("Historical", historical_series, stroke_style={"width": 6})
chart.add("Forecast", forecast_series, stroke_style={"width": 6, "dasharray": "15, 10"})
chart.add("95% CI Upper", upper_95_series, stroke_style={"width": 2, "dasharray": "5, 5"})
chart.add("95% CI Lower", lower_95_series, stroke_style={"width": 2, "dasharray": "5, 5"})
chart.add("80% CI Upper", upper_80_series, stroke_style={"width": 3, "dasharray": "3, 3"})
chart.add("80% CI Lower", lower_80_series, stroke_style={"width": 3, "dasharray": "3, 3"})

# Save as PNG
chart.render_to_png("plot.png")

# Save as HTML (interactive)
chart.render_to_file("plot.html")
