""" pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-15
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, save
from bokeh.resources import CDN
from scipy import stats


# Data
np.random.seed(42)
observed = np.random.normal(loc=50, scale=12, size=200) + np.random.exponential(scale=3, size=200)

observed_sorted = np.sort(observed)
n = len(observed_sorted)

mu, sigma = stats.norm.fit(observed_sorted)
empirical_cdf = np.arange(1, n + 1) / (n + 1)
theoretical_cdf = stats.norm.cdf(observed_sorted, loc=mu, scale=sigma)

source = ColumnDataSource(data={"theoretical": theoretical_cdf, "empirical": empirical_cdf})

# Plot
p = figure(
    width=3600,
    height=3600,
    title="pp-basic · bokeh · pyplots.ai",
    x_axis_label="Theoretical Cumulative Probability",
    y_axis_label="Empirical Cumulative Probability",
    x_range=(0, 1),
    y_range=(0, 1),
)

p.line([0, 1], [0, 1], line_color="#AAAAAA", line_width=3, line_dash="dashed")

p.scatter(
    x="theoretical", y="empirical", source=source, size=18, color="#306998", alpha=0.7, line_color="white", line_width=1
)

# Style
p.title.text_font_size = "48pt"
p.title.text_font_style = "normal"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.major_tick_line_color = None
p.yaxis.major_tick_line_color = None

p.xaxis.axis_line_color = "#333333"
p.yaxis.axis_line_color = "#333333"
p.xaxis[0].ticker.desired_num_ticks = 6
p.yaxis[0].ticker.desired_num_ticks = 6

p.outline_line_color = None
p.xgrid.grid_line_alpha = 0.2
p.ygrid.grid_line_alpha = 0.2
p.xgrid.grid_line_width = 1
p.ygrid.grid_line_width = 1

p.toolbar_location = None
p.background_fill_color = "#FFFFFF"
p.border_fill_color = "#FFFFFF"
p.min_border_left = 180
p.min_border_bottom = 150
p.min_border_top = 100
p.min_border_right = 60

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="pp-basic · bokeh · pyplots.ai")
