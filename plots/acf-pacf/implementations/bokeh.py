""" pyplots.ai
acf-pacf: Autocorrelation and Partial Autocorrelation (ACF/PACF) Plot
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-14
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Span
from bokeh.plotting import figure
from statsmodels.tsa.stattools import acf, pacf


# Data - Simulated AR(2) process (monthly airline-like seasonal data)
np.random.seed(42)
n_obs = 200
series = np.zeros(n_obs)
for i in range(2, n_obs):
    series[i] = 0.6 * series[i - 1] - 0.3 * series[i - 2] + np.random.randn()

# Compute ACF and PACF
n_lags = 35
acf_values = acf(series, nlags=n_lags, fft=True)
pacf_values = pacf(series, nlags=n_lags, method="ywm")
conf_bound = 1.96 / np.sqrt(n_obs)

# ACF plot (top)
acf_lags = np.arange(len(acf_values))
acf_source = ColumnDataSource(data={"x": acf_lags, "y": acf_values})
acf_stem_source = ColumnDataSource(
    data={"x0": acf_lags, "y0": np.zeros(len(acf_lags)), "x1": acf_lags, "y1": acf_values}
)

p_acf = figure(width=4800, height=1300, title="acf-pacf · bokeh · pyplots.ai", x_axis_label="Lag", y_axis_label="ACF")

p_acf.segment(x0="x0", y0="y0", x1="x1", y1="y1", source=acf_stem_source, line_width=5, color="#306998", alpha=0.85)
p_acf.scatter(x="x", y="y", source=acf_source, size=18, color="#306998", alpha=0.9)

p_acf.add_layout(
    Span(location=conf_bound, dimension="width", line_dash="dashed", line_width=3, line_color="#D04437", line_alpha=0.7)
)
p_acf.add_layout(
    Span(
        location=-conf_bound, dimension="width", line_dash="dashed", line_width=3, line_color="#D04437", line_alpha=0.7
    )
)
p_acf.add_layout(Span(location=0, dimension="width", line_width=2, line_color="#999999", line_alpha=0.5))

# PACF plot (bottom)
pacf_lags = np.arange(1, len(pacf_values))
pacf_vals = pacf_values[1:]
pacf_source = ColumnDataSource(data={"x": pacf_lags, "y": pacf_vals})
pacf_stem_source = ColumnDataSource(
    data={"x0": pacf_lags, "y0": np.zeros(len(pacf_lags)), "x1": pacf_lags, "y1": pacf_vals}
)

p_pacf = figure(width=4800, height=1300, x_axis_label="Lag", y_axis_label="PACF", x_range=p_acf.x_range)

p_pacf.segment(x0="x0", y0="y0", x1="x1", y1="y1", source=pacf_stem_source, line_width=5, color="#306998", alpha=0.85)
p_pacf.scatter(x="x", y="y", source=pacf_source, size=18, color="#306998", alpha=0.9)

p_pacf.add_layout(
    Span(location=conf_bound, dimension="width", line_dash="dashed", line_width=3, line_color="#D04437", line_alpha=0.7)
)
p_pacf.add_layout(
    Span(
        location=-conf_bound, dimension="width", line_dash="dashed", line_width=3, line_color="#D04437", line_alpha=0.7
    )
)
p_pacf.add_layout(Span(location=0, dimension="width", line_width=2, line_color="#999999", line_alpha=0.5))

# Style both plots
for p in [p_acf, p_pacf]:
    p.title.text_font_size = "36pt"
    p.xaxis.axis_label_text_font_size = "28pt"
    p.yaxis.axis_label_text_font_size = "28pt"
    p.xaxis.major_label_text_font_size = "22pt"
    p.yaxis.major_label_text_font_size = "22pt"
    p.xgrid.grid_line_alpha = 0
    p.ygrid.grid_line_alpha = 0.2
    p.ygrid.grid_line_dash = "dashed"
    p.outline_line_color = None
    p.toolbar_location = None

# Layout
layout = column(p_acf, p_pacf)

# Save
export_png(layout, filename="plot.png")
output_file("plot.html")
save(layout)
