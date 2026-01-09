""" pyplots.ai
biplot-pca: PCA Biplot with Scores and Loading Vectors
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-09
"""

import pygal
from pygal.style import Style
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Load and prepare data
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# Standardize features
X_scaled = StandardScaler().fit_transform(X)

# Perform PCA
pca = PCA(n_components=2)
scores = pca.fit_transform(X_scaled)
loadings = pca.components_.T  # Shape: (n_features, n_components)
variance_explained = pca.explained_variance_ratio_ * 100

# Scale loadings for visibility relative to scores
# Use a scaling factor based on score range
score_range = max(scores[:, 0].max() - scores[:, 0].min(), scores[:, 1].max() - scores[:, 1].min())
loading_scale = score_range * 0.8

# Custom style for 4800x2700 px canvas
# Colors: 3 for species (scatter points) + 4 for loading vectors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#306998",  # Blue - Setosa
        "#FFD43B",  # Yellow - Versicolor
        "#2ECC71",  # Green - Virginica
        "#C0392B",  # Dark Red - Sepal Length
        "#8E44AD",  # Purple - Sepal Width
        "#E67E22",  # Orange - Petal Length
        "#16A085",  # Teal - Petal Width
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    tooltip_font_size=36,
    stroke_width=3,
    opacity=0.8,
    opacity_hover=0.95,
)

# Create XY chart for biplot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="biplot-pca · pygal · pyplots.ai",
    x_title=f"PC1 ({variance_explained[0]:.1f}%)",
    y_title=f"PC2 ({variance_explained[1]:.1f}%)",
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=36,
    dots_size=12,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    truncate_legend=-1,
    explicit_size=True,
)

# Add score points for each species (class)
for i, name in enumerate(target_names):
    mask = y == i
    points = [(float(scores[j, 0]), float(scores[j, 1])) for j in range(len(y)) if mask[j]]
    chart.add(name.capitalize(), points, stroke=False, dots_size=14)

# Shorten feature names for display
short_names = ["Sepal L.", "Sepal W.", "Petal L.", "Petal W."]

# Add loading vectors as lines from origin to scaled loading endpoints
# Each loading shown as a stroke line with arrow-like dot at endpoint
for i, (_fname, short_name) in enumerate(zip(feature_names, short_names, strict=True)):
    load_x = loadings[i, 0] * loading_scale
    load_y = loadings[i, 1] * loading_scale
    # Create line from origin to loading point
    vector_points = [(0.0, 0.0), (float(load_x), float(load_y))]
    chart.add(f"→ {short_name}", vector_points, stroke=True, show_dots=True, dots_size=16, stroke_style={"width": 8})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
