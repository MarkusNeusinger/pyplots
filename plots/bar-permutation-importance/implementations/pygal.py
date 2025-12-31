""" pyplots.ai
bar-permutation-importance: Permutation Feature Importance Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated permutation importance results (realistic ML feature importance)
np.random.seed(42)

# Feature names representing typical ML model features (sorted by importance, ascending)
features = [
    "Year Built",
    "Bathrooms",
    "Garage Size",
    "Lot Area",
    "Bedrooms",
    "Basement Area",
    "Total Rooms",
    "Living Area",
    "Neighborhood",
    "Overall Quality",
]

# Mean importance values (mean decrease in R² score from permutation)
# Sorted ascending for bottom-to-top display in horizontal bar
importance_mean = np.array([0.002, 0.008, 0.015, 0.024, 0.032, 0.048, 0.067, 0.095, 0.128, 0.185])

# Standard deviation across 10 permutation repetitions
importance_std = np.array([0.003, 0.005, 0.008, 0.011, 0.014, 0.018, 0.022, 0.028, 0.035, 0.042])

# Generate sequential color gradient based on importance values (viridis-like)
# Colors from low (purple) to high (yellow) importance
min_imp = importance_mean.min()
max_imp = importance_mean.max()
imp_range = max_imp - min_imp if max_imp != min_imp else 1.0


def importance_to_color(imp):
    """Map importance value to a viridis-like color gradient."""
    t = (imp - min_imp) / imp_range
    # Viridis-inspired gradient: purple -> blue -> teal -> green -> yellow
    if t < 0.25:
        r = int(68 + (58 - 68) * (t / 0.25))
        g = int(1 + (82 - 1) * (t / 0.25))
        b = int(84 + (139 - 84) * (t / 0.25))
    elif t < 0.5:
        t2 = (t - 0.25) / 0.25
        r = int(58 + (32 - 58) * t2)
        g = int(82 + (144 - 82) * t2)
        b = int(139 + (140 - 139) * t2)
    elif t < 0.75:
        t2 = (t - 0.5) / 0.25
        r = int(32 + (94 - 32) * t2)
        g = int(144 + (201 - 144) * t2)
        b = int(140 + (97 - 140) * t2)
    else:
        t2 = (t - 0.75) / 0.25
        r = int(94 + (253 - 94) * t2)
        g = int(201 + (231 - 201) * t2)
        b = int(97 + (36 - 97) * t2)
    return f"#{r:02x}{g:02x}{b:02x}"


bar_colors = [importance_to_color(imp) for imp in importance_mean]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(bar_colors),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=2,
    font_family="sans-serif",
)

# Create horizontal bar chart
# Set x_range to include 0 to ensure x=0 reference line is visible
chart = pygal.HorizontalBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-permutation-importance · pygal · pyplots.ai",
    x_title="Mean Decrease in Accuracy",
    show_legend=False,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: f"{x:.4f}",
    show_y_guides=True,
    show_x_guides=True,
    truncate_label=-1,
    spacing=20,
    margin=60,
    margin_left=350,
    margin_bottom=120,
    range=(min(0, importance_mean.min() - 0.01), importance_mean.max() + 0.02),
    zero=0,
)

# Set x-axis labels (feature names) - in pygal HorizontalBar these become y-axis labels
chart.x_labels = features

# Add each bar as a separate series to apply individual colors
# Tooltips show mean ± std to represent error bar information
for i, (feat, imp, std, color) in enumerate(zip(features, importance_mean, importance_std, bar_colors, strict=True)):
    # Create data with None for other positions to align bars
    data = [None] * len(features)
    data[i] = {"value": imp, "label": f"{feat}: {imp:.4f} ± {std:.4f} (std)"}
    chart.add(feat, data, color=color)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
