"""pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-15
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Data - 200 samples with slight skew to show deviation from normality
np.random.seed(42)
observed = np.concatenate([np.random.normal(50, 10, 160), np.random.exponential(8, 40) + 45])
observed = np.sort(observed)
n = len(observed)

# Fit normal parameters from the data
mu = np.mean(observed)
sigma = np.std(observed, ddof=1)

# Compute empirical CDF using plotting position i/(n+1)
empirical_cdf = np.arange(1, n + 1) / (n + 1)

# Compute theoretical CDF using normal distribution: Phi((x - mu) / sigma)
theoretical_cdf = np.array([0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2)))) for x in observed])

# Custom style for 3600x3600 px (square aspect ratio)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#cccccc",
    colors=("#306998", "#888888"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=3,
)

# Create XY chart with square dimensions
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="pp-basic · pygal · pyplots.ai",
    x_title="Theoretical CDF",
    y_title="Empirical CDF",
    show_legend=True,
    legend_at_bottom=True,
    dots_size=10,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    xrange=(0, 1),
    range=(0, 1),
)

# P-P data points (theoretical CDF vs empirical CDF)
pp_points = list(zip(theoretical_cdf, empirical_cdf, strict=True))
chart.add("Observed vs Normal", pp_points)

# 45-degree reference line (perfect fit)
reference_line = [(0, 0), (1, 1)]
chart.add("Perfect Fit", reference_line, stroke=True, show_dots=False, dots_size=0)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
