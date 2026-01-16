"""pyplots.ai
histogram-returns-distribution: Returns Distribution Histogram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate 252 daily returns (1 year of trading data)
np.random.seed(42)
returns = np.random.normal(loc=0.0005, scale=0.015, size=252) * 100  # Convert to percentage

# Calculate statistics
n = len(returns)
mean_return = np.mean(returns)
std_return = np.std(returns, ddof=1)

# Skewness calculation
skewness = (n / ((n - 1) * (n - 2))) * np.sum(((returns - mean_return) / std_return) ** 3)

# Kurtosis calculation (excess kurtosis)
kurtosis = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * np.sum(((returns - mean_return) / std_return) ** 4) - (
    3 * (n - 1) ** 2
) / ((n - 2) * (n - 3))

# Create histogram bins with density normalization
n_bins = 30
counts, bin_edges = np.histogram(returns, bins=n_bins, density=True)

# Identify tail regions (beyond 2 standard deviations)
lower_tail = mean_return - 2 * std_return
upper_tail = mean_return + 2 * std_return

# Create histogram as step-like XY path with separate series for normal and tail regions
hist_normal = [(float(bin_edges[0]), 0.0)]
hist_tails = [(float(bin_edges[0]), 0.0)]

for i, count in enumerate(counts):
    left = float(bin_edges[i])
    right = float(bin_edges[i + 1])
    center = (left + right) / 2
    height = float(count)

    # Assign to normal or tail based on bin center
    if center < lower_tail or center > upper_tail:
        # Tail region
        hist_tails.append((left, height))
        hist_tails.append((right, height))
        hist_normal.append((left, 0.0))
        hist_normal.append((right, 0.0))
    else:
        # Normal region
        hist_normal.append((left, height))
        hist_normal.append((right, height))
        hist_tails.append((left, 0.0))
        hist_tails.append((right, 0.0))

hist_normal.append((float(bin_edges[-1]), 0.0))
hist_tails.append((float(bin_edges[-1]), 0.0))

# Generate normal distribution curve for overlay
x_curve = np.linspace(returns.min() - 0.5, returns.max() + 0.5, 200)
normal_pdf = (1 / (std_return * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - mean_return) / std_return) ** 2)
normal_curve = [(float(x), float(y)) for x, y in zip(x_curve, normal_pdf, strict=True)]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#E74C3C", "#2ECC71"),  # Blue for normal, red for tails, green for curve
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=40,
    value_font_size=28,
    opacity=0.7,
)

# Create XY chart for histogram with normal distribution overlay
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="histogram-returns-distribution · pygal · pyplots.ai",
    x_title="Returns (%)",
    y_title="Probability Density",
    show_dots=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=30,
    show_y_guides=True,
    show_x_guides=False,
    margin_bottom=120,
)

# Add histogram series as filled step areas
chart.add("Returns (within 2σ)", hist_normal, fill=True, stroke_style={"width": 2})
chart.add("Tails (beyond 2σ)", hist_tails, fill=True, stroke_style={"width": 2})

# Add normal distribution overlay curve
chart.add("Normal Distribution", normal_curve, fill=False, stroke_style={"width": 6})

# Add statistics as secondary title using a text annotation approach
stats_text = (
    f"Mean: {mean_return:.3f}%  |  Std: {std_return:.3f}%  |  Skew: {skewness:.2f}  |  Kurtosis: {kurtosis:.2f}"
)
chart.config.show_minor_x_labels = True
chart.config.x_labels = [{"label": "", "value": mean_return}]

# Add custom annotation for statistics box by updating the title
chart.title = f"histogram-returns-distribution · pygal · pyplots.ai\n{stats_text}"

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
