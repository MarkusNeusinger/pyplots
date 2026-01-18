""" pyplots.ai
histogram-returns-distribution: Returns Distribution Histogram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-16
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

# Prepare bar chart data - use bin centers as x-labels
bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(counts))]
normal_heights = []
tail_heights = []

for i, count in enumerate(counts):
    center = bin_centers[i]
    if center < lower_tail or center > upper_tail:
        tail_heights.append(count)
        normal_heights.append(0)
    else:
        normal_heights.append(count)
        tail_heights.append(0)

# Generate normal distribution curve points for overlay using XY chart
x_curve = np.linspace(returns.min() - 0.5, returns.max() + 0.5, 100)
normal_pdf = (1 / (std_return * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - mean_return) / std_return) ** 2)

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
    legend_font_size=36,
    value_font_size=28,
    stroke_width=4,
    opacity=0.85,
    opacity_hover=1.0,
)

# Create stats subtitle
stats_text = (
    f"Mean: {mean_return:.3f}%  |  Std Dev: {std_return:.3f}%  |  Skewness: {skewness:.2f}  |  Kurtosis: {kurtosis:.2f}"
)

# Create Bar chart for histogram
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"histogram-returns-distribution · pygal · pyplots.ai\n{stats_text}",
    x_title="Returns (%)",
    y_title="Probability Density",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=28,
    show_y_guides=True,
    show_x_guides=False,
    margin_bottom=160,
    margin_left=100,
    x_label_rotation=0,
    truncate_label=-1,
    print_values=False,
)

# Set x-axis labels (show fewer labels to avoid crowding)
x_labels = [f"{c:.1f}" if i % 5 == 0 else "" for i, c in enumerate(bin_centers)]
chart.x_labels = x_labels

# Add histogram bars
chart.add("Returns (within 2σ)", normal_heights)
chart.add("Tails (beyond ±2σ)", tail_heights)

# Create separate XY chart for the normal curve overlay
curve_chart = pygal.XY(
    width=4800,
    height=2700,
    style=Style(
        background="transparent",
        plot_background="transparent",
        foreground="#333",
        foreground_strong="#333",
        colors=("#1a472a",),  # Dark green for curve visibility
        stroke_width=8,
        opacity=1.0,
    ),
    show_dots=False,
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    show_x_guides=False,
    show_y_guides=False,
)

# Add normal distribution curve
normal_curve_data = [(float(x), float(y)) for x, y in zip(x_curve, normal_pdf, strict=True)]
curve_chart.add("Normal Distribution", normal_curve_data, stroke_style={"width": 8})

# Since pygal cannot overlay charts directly, we add the curve as a secondary series
# Create a combined XY chart that shows both histogram and curve
combined_chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"histogram-returns-distribution · pygal · pyplots.ai\n{stats_text}",
    x_title="Returns (%)",
    y_title="Probability Density",
    show_dots=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=28,
    show_y_guides=True,
    show_x_guides=False,
    margin_bottom=160,
    margin_left=100,
    explicit_size=True,
    print_values=False,
)

# Build histogram as filled step polygons for XY chart
hist_normal_xy = []
hist_tails_xy = []

for i, count in enumerate(counts):
    left = float(bin_edges[i])
    right = float(bin_edges[i + 1])
    center = (left + right) / 2
    height = float(count)

    if center < lower_tail or center > upper_tail:
        # Add to tails, zeros to normal
        hist_tails_xy.extend([(left, 0), (left, height), (right, height), (right, 0)])
        hist_normal_xy.extend([(left, 0), (left, 0), (right, 0), (right, 0)])
    else:
        # Add to normal, zeros to tails
        hist_normal_xy.extend([(left, 0), (left, height), (right, height), (right, 0)])
        hist_tails_xy.extend([(left, 0), (left, 0), (right, 0), (right, 0)])

# Add histogram series
combined_chart.add("Returns (within 2σ)", hist_normal_xy, fill=True, stroke_style={"width": 1})
combined_chart.add("Tails (beyond ±2σ)", hist_tails_xy, fill=True, stroke_style={"width": 1})

# Add normal distribution curve - make it prominent with thick stroke
combined_chart.add("Normal Distribution", normal_curve_data, fill=False, stroke_style={"width": 8, "dasharray": "0"})

# Save outputs
combined_chart.render_to_file("plot.html")
combined_chart.render_to_png("plot.png")
