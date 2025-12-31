""" pyplots.ai
bar-permutation-importance: Permutation Feature Importance Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
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

# Generate sequential color gradient (viridis-inspired) inline
min_imp = importance_mean.min()
max_imp = importance_mean.max()
imp_range = max_imp - min_imp if max_imp != min_imp else 1.0

# Viridis color stops: purple (0) -> teal (0.5) -> yellow (1)
viridis_stops = [(0.0, 68, 1, 84), (0.25, 58, 82, 139), (0.5, 32, 144, 140), (0.75, 94, 201, 97), (1.0, 253, 231, 36)]

bar_colors = []
for imp in importance_mean:
    t = (imp - min_imp) / imp_range
    for j in range(len(viridis_stops) - 1):
        t0, r0, g0, b0 = viridis_stops[j]
        t1, r1, g1, b1 = viridis_stops[j + 1]
        if t0 <= t <= t1:
            seg_t = (t - t0) / (t1 - t0)
            r = int(r0 + (r1 - r0) * seg_t)
            g = int(g0 + (g1 - g0) * seg_t)
            b = int(b0 + (b1 - b0) * seg_t)
            bar_colors.append(f"#{r:02x}{g:02x}{b:02x}")
            break
    else:
        bar_colors.append("#fde724")

# Custom style with larger fonts for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(bar_colors),
    title_font_size=84,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=44,
    value_font_size=44,
    stroke_width=2,
    font_family="sans-serif",
)

# Pre-compute formatted value labels with error bars (mean ± std)
value_labels = [f"{imp:.3f} ± {std:.3f}" for imp, std in zip(importance_mean, importance_std, strict=True)]

# Create horizontal bar chart
# Range includes negative values to ensure x=0 reference line is visible
chart = pygal.HorizontalBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-permutation-importance · pygal · pyplots.ai",
    x_title="Mean Decrease in Accuracy",
    show_legend=False,
    print_values=True,
    print_values_position="top",
    show_y_guides=True,
    show_x_guides=True,
    truncate_label=-1,
    spacing=24,
    margin=60,
    margin_left=420,
    margin_bottom=140,
    range=(-0.03, importance_mean.max() + importance_std.max() + 0.03),
    zero=0,
)

# Set feature labels on y-axis
chart.x_labels = features

# Add each bar with individual color and value label showing error bar info
for i, (feat, imp, _std, color, label) in enumerate(
    zip(features, importance_mean, importance_std, bar_colors, value_labels, strict=True)
):
    data = [None] * len(features)
    data[i] = {"value": imp, "label": f"{feat}: {label}"}
    chart.add(feat, data, color=color, formatter=lambda x, lbl=label: lbl)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
