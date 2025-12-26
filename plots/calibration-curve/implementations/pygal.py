"""pyplots.ai
calibration-curve: Calibration Curve
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-26
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: Generate synthetic binary classification with realistic calibration
np.random.seed(42)
n_samples = 2000

# Generate true probabilities spread across 0-1 range
true_prob = np.random.beta(2, 2, n_samples)
y_true = (np.random.random(n_samples) < true_prob).astype(int)

# Model 1: Well-calibrated model (Logistic Regression style)
# Predictions closely match true probabilities
noise1 = np.random.randn(n_samples) * 0.08
y_prob_model1 = np.clip(true_prob + noise1, 0.01, 0.99)

# Model 2: Overconfident model (Random Forest / Neural Network style)
# Pushes predictions toward extremes - classic S-curve miscalibration
# Above diagonal for low probs, below diagonal for high probs
y_prob_model2 = 1 / (1 + np.exp(-8 * (true_prob - 0.5)))
y_prob_model2 = np.clip(y_prob_model2 + np.random.randn(n_samples) * 0.03, 0.02, 0.98)


# Compute calibration curve data using equal-width bins
def compute_calibration(y_true, y_prob, n_bins=10):
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bin_edges[1:-1])

    mean_predicted = []
    fraction_positive = []

    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            mean_predicted.append(np.mean(y_prob[mask]))
            fraction_positive.append(np.mean(y_true[mask]))

    return mean_predicted, fraction_positive


# Compute Brier score (lower is better)
def brier_score(y_true, y_prob):
    return np.mean((y_prob - y_true) ** 2)


# Get calibration data for both models
mean_pred1, frac_pos1 = compute_calibration(y_true, y_prob_model1)
mean_pred2, frac_pos2 = compute_calibration(y_true, y_prob_model2)

brier1 = brier_score(y_true, y_prob_model1)
brier2 = brier_score(y_true, y_prob_model2)

# Custom style for 4800 x 2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#888888"),
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
    dots_size=12,
    stroke_style={"width": 5},
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:.1f}",
    range=(0, 1),
    xrange=(0, 1),
    legend_at_bottom=False,
    truncate_legend=-1,
    margin=50,
    margin_right=80,
)

# Perfect calibration line (diagonal reference)
perfect_calibration = [
    (0, 0),
    (0.1, 0.1),
    (0.2, 0.2),
    (0.3, 0.3),
    (0.4, 0.4),
    (0.5, 0.5),
    (0.6, 0.6),
    (0.7, 0.7),
    (0.8, 0.8),
    (0.9, 0.9),
    (1.0, 1.0),
]
chart.add("Perfect Calibration", perfect_calibration, stroke_dasharray="10,5", dots_size=0, stroke_style={"width": 3})

# Model 1 calibration curve
model1_points = list(zip(mean_pred1, frac_pos1, strict=True))
chart.add(f"Logistic Regression (Brier: {brier1:.3f})", model1_points)

# Model 2 calibration curve
model2_points = list(zip(mean_pred2, frac_pos2, strict=True))
chart.add(f"Overconfident Model (Brier: {brier2:.3f})", model2_points)

# Save as SVG and PNG
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
