"""pyplots.ai
shap-summary: SHAP Summary Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 35/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulate SHAP values for credit risk model
np.random.seed(42)
n_samples = 200
n_features = 10

feature_names = [
    "Income",
    "Age",
    "Credit Score",
    "Loan Amount",
    "Employment Years",
    "Debt Ratio",
    "Num Accounts",
    "Late Payments",
    "Credit Util",
    "Loan Term",
]

# Generate synthetic SHAP values with realistic patterns
importance = np.array([1.0, 0.85, 0.72, 0.65, 0.55, 0.48, 0.40, 0.35, 0.28, 0.20])
shap_values = np.zeros((n_samples, n_features))
feature_values = np.zeros((n_samples, n_features))

for i in range(n_features):
    feature_values[:, i] = np.random.beta(2, 2, n_samples)
    base_shap = (feature_values[:, i] - 0.5) * importance[i] * 2
    noise = np.random.normal(0, 0.15 * importance[i], n_samples)
    shap_values[:, i] = base_shap + noise

# Sort features by mean absolute SHAP value (most important at top)
mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
sorted_indices = np.argsort(mean_abs_shap)[::-1]  # Descending
sorted_names = [feature_names[i] for i in sorted_indices]

# Define color bins for feature values (blue=low, purple=mid, red=high)
# Since pygal can't do per-point gradients, we'll use discrete series
n_color_bins = 5
color_palette = [
    "#3B4CC0",  # Blue (low)
    "#7B9FD4",  # Light blue
    "#C0C0C0",  # Gray (mid)
    "#E87D72",  # Light red
    "#B40426",  # Red (high)
]
bin_labels = ["Low", "Low-Mid", "Mid", "Mid-High", "High"]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(color_palette),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=0,
    opacity=0.65,
    opacity_hover=0.9,
)

# Create XY scatter chart for beeswarm-like visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="shap-summary · pygal · pyplots.ai",
    x_title="SHAP Value (Impact on Model Output)",
    y_title="Feature",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    dots_size=8,
    stroke=False,
    show_y_guides=True,
    show_x_guides=True,
    margin=50,
    x_label_rotation=0,
    range=(0.5, n_features + 0.5),
)

# Prepare data points for each color bin
# Each series = one color bin (representing feature value range)
series_data = [[] for _ in range(n_color_bins)]

# Add jitter to y-positions to create beeswarm effect
for feat_idx, orig_idx in enumerate(sorted_indices):
    y_base = n_features - feat_idx  # Higher importance = higher y position

    for sample_idx in range(n_samples):
        shap_val = shap_values[sample_idx, orig_idx]
        feat_val = feature_values[sample_idx, orig_idx]

        # Determine color bin based on feature value
        bin_idx = min(int(feat_val * n_color_bins), n_color_bins - 1)

        # Add vertical jitter to spread points (beeswarm style)
        jitter = np.random.uniform(-0.35, 0.35)
        y_pos = y_base + jitter

        series_data[bin_idx].append((shap_val, y_pos))

# Add each color bin as a series
for bin_idx in range(n_color_bins):
    chart.add(f"Feature Value: {bin_labels[bin_idx]}", series_data[bin_idx])

# Set y-axis labels to feature names (reversed so most important at top)
chart.y_labels = [{"value": n_features - i, "label": sorted_names[i]} for i in range(n_features)]

# Add reference line at x=0 using a separate series
zero_line_points = [(0, 0.3), (0, n_features + 0.7)]
chart.add("x=0 (Reference)", zero_line_points, stroke=True, dots_size=0, stroke_style={"width": 4, "dasharray": "10,5"})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
