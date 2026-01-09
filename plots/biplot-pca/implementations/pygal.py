""" pyplots.ai
biplot-pca: PCA Biplot with Scores and Loading Vectors
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-09
"""

import math

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

# Use correlation biplot scaling
score_range = max(scores[:, 0].max() - scores[:, 0].min(), scores[:, 1].max() - scores[:, 1].min())
loading_scale = score_range * 0.4
unit_circle_radius = loading_scale

# Custom style for 4800x2700 px canvas
species_colors = ["#306998", "#FFD43B", "#2ECC71"]  # Blue, Yellow, Green for species
unit_circle_color = "#999999"  # Gray for unit circle reference
# Distinct colors for each loading vector (colorblind-friendly)
loading_colors = ["#E41A1C", "#984EA3", "#FF7F00", "#377EB8"]  # Red, Purple, Orange, Blue

custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(species_colors + [unit_circle_color] + loading_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=38,
    tooltip_font_size=36,
    stroke_width=4,
    opacity=0.85,
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
    legend_at_bottom=True,
    legend_box_size=32,
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
    chart.add(name.capitalize(), points, stroke=False, dots_size=12)

# Create unit circle for loading magnitude reference (subtle, no legend text)
circle_points = []
for angle in range(0, 361, 3):
    rad = math.radians(angle)
    circle_points.append((unit_circle_radius * math.cos(rad), unit_circle_radius * math.sin(rad)))
chart.add("Reference", circle_points, stroke=True, show_dots=False, stroke_style={"width": 2, "dasharray": "8,6"})

# Shorten feature names for legend and labels
short_names = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]

# Add each loading vector as separate series (name in legend acts as label)
for i, short_name in enumerate(short_names):
    tip_x = float(loadings[i, 0] * loading_scale)
    tip_y = float(loadings[i, 1] * loading_scale)

    # Calculate arrow geometry inline (no helper function)
    dx, dy = tip_x, tip_y
    length = math.sqrt(dx * dx + dy * dy)
    ux = dx / length if length > 0 else 0
    uy = dy / length if length > 0 else 0
    px, py = -uy, ux  # Perpendicular vector

    head_len = 0.12 * loading_scale
    head_wid = 0.07 * loading_scale
    hb_x = tip_x - ux * head_len
    hb_y = tip_y - uy * head_len

    # Arrow path: origin -> shaft -> arrowhead wings -> tip -> back
    arrow = [
        (0.0, 0.0),
        (hb_x, hb_y),
        (hb_x + px * head_wid, hb_y + py * head_wid),
        (tip_x, tip_y),
        (hb_x - px * head_wid, hb_y - py * head_wid),
        (hb_x, hb_y),
    ]
    chart.add(short_name, arrow, stroke=True, show_dots=False, fill=True, stroke_style={"width": 4})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
