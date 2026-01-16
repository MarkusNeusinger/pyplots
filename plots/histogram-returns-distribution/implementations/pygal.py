"""pyplots.ai
histogram-returns-distribution: Returns Distribution Histogram
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate 252 daily returns (1 year of trading data)
np.random.seed(42)
returns = np.random.normal(loc=0.0005, scale=0.015, size=252) * 100  # Convert to percentage

# Calculate statistics manually
n = len(returns)
mean_return = np.mean(returns)
std_return = np.std(returns, ddof=1)

# Skewness calculation
skewness = (n / ((n - 1) * (n - 2))) * np.sum(((returns - mean_return) / std_return) ** 3)

# Kurtosis calculation (excess kurtosis)
kurtosis = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * np.sum(((returns - mean_return) / std_return) ** 4) - (
    3 * (n - 1) ** 2
) / ((n - 2) * (n - 3))

# Create histogram bins
n_bins = 30
counts, bin_edges = np.histogram(returns, bins=n_bins, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
bin_width = bin_edges[1] - bin_edges[0]

# Scale counts for display
counts_scaled = counts * 100  # Scale for better visualization

# Identify tail regions (beyond 2 standard deviations)
lower_tail = mean_return - 2 * std_return
upper_tail = mean_return + 2 * std_return

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#E74C3C"),  # Blue for normal, red for tails
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    tooltip_font_size=20,
)

# Create histogram chart
stats_text = f"Mean: {mean_return:.3f}% | Std: {std_return:.3f}% | Skew: {skewness:.2f} | Kurt: {kurtosis:.2f}"
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"Daily Returns Distribution ({stats_text}) · histogram-returns-distribution · pygal · pyplots.ai",
    x_title="Returns (%)",
    y_title="Frequency (Density × 100)",
    show_legend=True,
    legend_at_bottom=True,
    show_x_guides=False,
    show_y_guides=True,
    spacing=0,
    margin=50,
    x_label_rotation=45,
)

# Create bin labels - show every 5th for clarity
chart.x_labels = [f"{bin_centers[i]:.2f}" if i % 5 == 0 else "" for i in range(len(bin_centers))]

# Separate histogram data into normal and tail regions
normal_bars = []
tail_bars = []

for center, count in zip(bin_centers, counts_scaled, strict=True):
    if center < lower_tail or center > upper_tail:
        normal_bars.append(None)
        tail_bars.append({"value": count, "label": f"{center:.2f}%"})
    else:
        normal_bars.append({"value": count, "label": f"{center:.2f}%"})
        tail_bars.append(None)

# Add histogram series
chart.add("Returns", normal_bars)
chart.add("Tails (>2σ)", tail_bars)

# Save plot
chart.render_to_png("plot.png")

# Also save HTML for interactive version
chart.render_to_file("plot.html")
