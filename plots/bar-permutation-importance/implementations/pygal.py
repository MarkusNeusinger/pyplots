""" pyplots.ai
bar-permutation-importance: Permutation Feature Importance Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


# Data - Using Wine dataset with permutation importance
np.random.seed(42)
wine = load_wine()
X, y = wine.data, wine.target
feature_names = wine.feature_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model and compute permutation importance
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)

# Sort by mean importance (ascending for bottom-to-top display in horizontal bar)
sorted_idx = result.importances_mean.argsort()
importance_mean = result.importances_mean[sorted_idx]
importance_std = result.importances_std[sorted_idx]
features = [feature_names[i].replace("_", " ").title() for i in sorted_idx]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#646464"),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=2,
    font_family="sans-serif",
)

# Create horizontal bar chart
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
    truncate_label=-1,
    spacing=20,
    margin=60,
    margin_left=350,
    margin_bottom=120,
)

# Set x-axis labels (feature names) - in pygal HorizontalBar these become y-axis labels
chart.x_labels = features

# Add all importance values as a single series with tooltips showing ± std
data_points = []
for imp, std in zip(importance_mean, importance_std, strict=True):
    data_points.append({"value": imp, "label": f"Importance: {imp:.4f} ± {std:.4f}"})

chart.add("Feature Importance", data_points)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
