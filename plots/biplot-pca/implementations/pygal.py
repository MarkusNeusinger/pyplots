""" pyplots.ai
biplot-pca: PCA Biplot with Scores and Loading Vectors
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-09
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

# Use correlation biplot scaling - loadings are already unit vectors in correlation biplot
# Scale to fit nicely within score range but maintain relative proportions
score_range = max(scores[:, 0].max() - scores[:, 0].min(), scores[:, 1].max() - scores[:, 1].min())
loading_scale = score_range * 0.35  # Smaller scale for better balance
unit_circle_radius = loading_scale  # Unit circle matches loading scale

# Custom style for 4800x2700 px canvas
# Colors in order of series added: 3 species, unit circle, 4 loading vectors
species_colors = ["#306998", "#FFD43B", "#2ECC71"]  # Blue, Yellow, Green
unit_circle_color = "#CC6666"  # Muted red for dashed circle (4th series)
vector_colors = ["#C0392B", "#8E44AD", "#E67E22", "#16A085"]  # Dark Red, Purple, Orange, Teal

custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(species_colors + [unit_circle_color] + vector_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
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
    legend_at_bottom=False,
    legend_box_size=36,
    dots_size=14,
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

# Create unit circle for loading magnitude reference
circle_points = []
for angle in range(0, 361, 5):
    rad = math.radians(angle)
    cx = unit_circle_radius * math.cos(rad)
    cy = unit_circle_radius * math.sin(rad)
    circle_points.append((cx, cy))

chart.add("Unit Circle", circle_points, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "15,10"})

# Shorten feature names for display
short_names = ["Sepal L.", "Sepal W.", "Petal L.", "Petal W."]


# Helper function to create arrowhead points
def create_arrow_points(x1, y1, x2, y2, head_length=0.12, head_width=0.08):
    """Create line with arrowhead as series of connected points."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return [(x1, y1)]

    # Unit vector along arrow direction
    ux = dx / length
    uy = dy / length

    # Perpendicular vector
    px = -uy
    py = ux

    # Arrowhead points (create a triangular head)
    head_base_x = x2 - ux * head_length * loading_scale
    head_base_y = y2 - uy * head_length * loading_scale
    head_side = head_width * loading_scale

    # Arrow as connected segments: origin -> head_base -> left wing -> tip -> right wing -> head_base
    points = [
        (x1, y1),  # Start at origin
        (head_base_x, head_base_y),  # Line to base of arrowhead
        (head_base_x + px * head_side, head_base_y + py * head_side),  # Left wing
        (x2, y2),  # Tip
        (head_base_x - px * head_side, head_base_y - py * head_side),  # Right wing
        (head_base_x, head_base_y),  # Back to base
    ]
    return points


# Add loading vectors with arrowheads
for i, short_name in enumerate(short_names):
    load_x = float(loadings[i, 0] * loading_scale)
    load_y = float(loadings[i, 1] * loading_scale)

    # Create arrow with visible arrowhead
    arrow_pts = create_arrow_points(0.0, 0.0, load_x, load_y)

    chart.add(f"{short_name}", arrow_pts, stroke=True, show_dots=False, fill=True, stroke_style={"width": 6})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
