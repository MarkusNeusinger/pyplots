"""pyplots.ai
timeseries-forecast-uncertainty: Time Series Forecast with Uncertainty Band
Library: altair | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Monthly sales with 36 months history + 12 months forecast
np.random.seed(42)

# Historical period (36 months)
historical_dates = pd.date_range("2021-01-01", periods=36, freq="MS")
trend = np.linspace(100, 180, 36)
seasonal = 15 * np.sin(np.linspace(0, 6 * np.pi, 36))
noise = np.random.normal(0, 8, 36)
historical_values = trend + seasonal + noise

# Forecast period (12 months)
forecast_dates = pd.date_range("2024-01-01", periods=12, freq="MS")
forecast_trend = np.linspace(180, 210, 12)
forecast_seasonal = 15 * np.sin(np.linspace(6 * np.pi, 8 * np.pi, 12))
forecast_values = forecast_trend + forecast_seasonal

# Confidence intervals - widening over forecast horizon
forecast_std = np.linspace(5, 20, 12)
lower_80 = forecast_values - 1.28 * forecast_std
upper_80 = forecast_values + 1.28 * forecast_std
lower_95 = forecast_values - 1.96 * forecast_std
upper_95 = forecast_values + 1.96 * forecast_std

# Create DataFrames
historical_df = pd.DataFrame({"date": historical_dates, "actual": historical_values, "type": "Historical"})

forecast_df = pd.DataFrame(
    {
        "date": forecast_dates,
        "forecast": forecast_values,
        "lower_80": lower_80,
        "upper_80": upper_80,
        "lower_95": lower_95,
        "upper_95": upper_95,
        "type": "Forecast",
    }
)

# Historical line chart
historical_line = (
    alt.Chart(historical_df)
    .mark_line(strokeWidth=3, color="#306998")
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("actual:Q", title="Sales (thousands USD)", scale=alt.Scale(domain=[50, 270])),
    )
)

# 95% confidence band (lighter)
band_95 = (
    alt.Chart(forecast_df)
    .mark_area(opacity=0.2, color="#FFD43B")
    .encode(x=alt.X("date:T"), y=alt.Y("lower_95:Q"), y2=alt.Y2("upper_95:Q"))
)

# 80% confidence band (darker)
band_80 = (
    alt.Chart(forecast_df)
    .mark_area(opacity=0.35, color="#FFD43B")
    .encode(x=alt.X("date:T"), y=alt.Y("lower_80:Q"), y2=alt.Y2("upper_80:Q"))
)

# Forecast line (dashed)
forecast_line = (
    alt.Chart(forecast_df)
    .mark_line(strokeWidth=3, strokeDash=[8, 4], color="#E67E22")
    .encode(x=alt.X("date:T"), y=alt.Y("forecast:Q"))
)

# Vertical line at forecast start
forecast_start = pd.DataFrame({"date": [pd.Timestamp("2024-01-01")]})
vertical_rule = (
    alt.Chart(forecast_start).mark_rule(strokeWidth=2, strokeDash=[6, 3], color="#555555").encode(x="date:T")
)

# Legend data for manual legend
legend_data = pd.DataFrame(
    {
        "label": ["Historical", "Forecast", "80% CI", "95% CI"],
        "color": ["#306998", "#E67E22", "#FFD43B", "#FFD43B"],
        "opacity": [1.0, 1.0, 0.5, 0.25],
    }
)

# Combine all layers
chart = (
    alt.layer(band_95, band_80, historical_line, forecast_line, vertical_rule)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "timeseries-forecast-uncertainty · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            subtitle="Monthly Sales with 80% and 95% Confidence Intervals",
            subtitleFontSize=20,
        ),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
