"""pyplots.ai
calibration-curve: Calibration Curve
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-26
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: Generate synthetic binary classification with realistic calibration
np.random.seed(42)
n_samples = 2000
n_bins = 10

# Generate true probabilities spread across 0-1 range
true_prob = np.random.beta(2, 2, n_samples)
y_true = (np.random.random(n_samples) < true_prob).astype(int)

# Model 1: Well-calibrated model (Logistic Regression style)
noise1 = np.random.randn(n_samples) * 0.08
y_prob_model1 = np.clip(true_prob + noise1, 0.01, 0.99)

# Model 2: Overconfident model (Random Forest / Neural Network style)
# More extreme S-curve to make miscalibration pattern more visible
y_prob_model2 = 1 / (1 + np.exp(-12 * (true_prob - 0.5)))
y_prob_model2 = np.clip(y_prob_model2 + np.random.randn(n_samples) * 0.02, 0.02, 0.98)

# Compute calibration data inline (KISS principle - no helper functions)
bin_edges = np.linspace(0, 1, n_bins + 1)

# Model 1 calibration
bin_indices1 = np.digitize(y_prob_model1, bin_edges[1:-1])
mean_pred1 = []
frac_pos1 = []
for i in range(n_bins):
    mask = bin_indices1 == i
    if mask.sum() > 0:
        mean_pred1.append(np.mean(y_prob_model1[mask]))
        frac_pos1.append(np.mean(y_true[mask]))

# Model 2 calibration
bin_indices2 = np.digitize(y_prob_model2, bin_edges[1:-1])
mean_pred2 = []
frac_pos2 = []
for i in range(n_bins):
    mask = bin_indices2 == i
    if mask.sum() > 0:
        mean_pred2.append(np.mean(y_prob_model2[mask]))
        frac_pos2.append(np.mean(y_true[mask]))

# Compute Brier scores inline
brier1 = np.mean((y_prob_model1 - y_true) ** 2)
brier2 = np.mean((y_prob_model2 - y_true) ** 2)

# Custom style for 4800 x 2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#888888", "#306998", "#D62728"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=6,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart for calibration curve
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="calibration-curve · pygal · pyplots.ai",
    x_title="Mean Predicted Probability",
    y_title="Fraction of Positives",
    show_dots=True,
    dots_size=14,
    stroke_style={"width": 5},
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:.1f}",
    range=(0, 1),
    xrange=(0, 1),
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
    margin=50,
    margin_bottom=150,
)

# Perfect calibration line (diagonal reference) - first in gray, dashed, no dots
perfect_calibration = [(0, 0), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75), (1.0, 1.0)]
chart.add("Perfect Calibration", perfect_calibration, stroke_dasharray="15,8", dots_size=0, stroke_style={"width": 4})

# Model 1 calibration curve - well-calibrated (blue)
model1_points = list(zip(mean_pred1, frac_pos1, strict=False))
chart.add(f"Logistic Regression (Brier: {brier1:.3f})", model1_points)

# Model 2 calibration curve - overconfident (red for contrast)
model2_points = list(zip(mean_pred2, frac_pos2, strict=False))
chart.add(f"Overconfident Model (Brier: {brier2:.3f})", model2_points)

# Save as PNG only
chart.render_to_png("plot.png")
