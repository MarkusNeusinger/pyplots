"""pyplots.ai
shap-summary: SHAP Summary Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulate SHAP values for a trained model
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
# Features with higher importance have larger SHAP value magnitudes
importance = np.array([1.0, 0.85, 0.72, 0.65, 0.55, 0.48, 0.40, 0.35, 0.28, 0.20])
shap_values = np.zeros((n_samples, n_features))
feature_values = np.zeros((n_samples, n_features))

for i in range(n_features):
    # Feature values normalized 0-1
    feature_values[:, i] = np.random.beta(2, 2, n_samples)
    # SHAP values correlate with feature values (with noise)
    base_shap = (feature_values[:, i] - 0.5) * importance[i] * 2
    noise = np.random.normal(0, 0.15 * importance[i], n_samples)
    shap_values[:, i] = base_shap + noise

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C", "#27AE60", "#9B59B6", "#F39C12"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=2,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create horizontal bar chart showing mean absolute SHAP values
# Pygal doesn't support true scatter with color gradients, so we'll show
# feature importance as bars with annotations for SHAP distribution
chart = pygal.HorizontalBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="shap-summary · pygal · pyplots.ai",
    x_title="Mean |SHAP Value| (Impact on Model Output)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: f"{x:.3f}",
    show_y_guides=True,
    show_x_guides=True,
    margin=50,
    spacing=30,
    truncate_legend=50,
)

# Calculate mean absolute SHAP for each feature
mean_abs_shap_per_feature = np.mean(np.abs(shap_values), axis=0)

# Also calculate positive and negative contributions
mean_positive = np.zeros(n_features)
mean_negative = np.zeros(n_features)
for i in range(n_features):
    pos_mask = shap_values[:, i] > 0
    neg_mask = shap_values[:, i] < 0
    if np.any(pos_mask):
        mean_positive[i] = np.mean(shap_values[pos_mask, i])
    if np.any(neg_mask):
        mean_negative[i] = np.mean(np.abs(shap_values[neg_mask, i]))

# Sort by importance (ascending so most important appears at top in horizontal bar)
sorted_indices = np.argsort(mean_abs_shap_per_feature)
sorted_names = [feature_names[i] for i in sorted_indices]
sorted_importance = mean_abs_shap_per_feature[sorted_indices]
sorted_positive = mean_positive[sorted_indices]
sorted_negative = mean_negative[sorted_indices]

# Add data series - Main bars showing overall importance
chart.add("Mean |SHAP|", sorted_importance.tolist())

# Show positive and negative contributions as separate series
chart.add("Positive Impact", sorted_positive.tolist())
chart.add("Negative Impact", sorted_negative.tolist())

# Set feature names as x labels
chart.x_labels = sorted_names

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
