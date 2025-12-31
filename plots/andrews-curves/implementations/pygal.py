""" pyplots.ai
andrews-curves: Andrews Curves for Multivariate Data
Library: pygal 3.1.0 | Python 3.13.11
Quality: 76/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Generate synthetic Iris-like data (4 features, 3 species)
np.random.seed(42)

# Simulate sepal length, sepal width, petal length, petal width for 3 species
# Species 1: Setosa - small petals, medium sepals
setosa = np.column_stack(
    [
        np.random.normal(5.0, 0.35, 50),  # sepal length
        np.random.normal(3.4, 0.38, 50),  # sepal width
        np.random.normal(1.5, 0.17, 50),  # petal length
        np.random.normal(0.2, 0.10, 50),  # petal width
    ]
)

# Species 2: Versicolor - medium petals and sepals
versicolor = np.column_stack(
    [
        np.random.normal(5.9, 0.52, 50),  # sepal length
        np.random.normal(2.8, 0.31, 50),  # sepal width
        np.random.normal(4.3, 0.47, 50),  # petal length
        np.random.normal(1.3, 0.20, 50),  # petal width
    ]
)

# Species 3: Virginica - large petals and sepals
virginica = np.column_stack(
    [
        np.random.normal(6.6, 0.64, 50),  # sepal length
        np.random.normal(3.0, 0.32, 50),  # sepal width
        np.random.normal(5.5, 0.55, 50),  # petal length
        np.random.normal(2.0, 0.27, 50),  # petal width
    ]
)

# Combine data
X = np.vstack([setosa, versicolor, virginica])
y = np.array([0] * 50 + [1] * 50 + [2] * 50)
species_names = ["Setosa", "Versicolor", "Virginica"]

# Normalize variables (z-score standardization)
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std

# Andrews curve function: f(t) = x1/sqrt(2) + x2*sin(t) + x3*cos(t) + x4*sin(2t) + ...
t_values = np.linspace(-np.pi, np.pi, 100)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C"),  # Blue, Yellow, Red for 3 species
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=2,
    opacity=0.4,
    opacity_hover=0.6,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="andrews-curves · pygal · pyplots.ai",
    x_title="t (radians)",
    y_title="f(t)",
    show_dots=False,
    stroke_style={"width": 2},
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    truncate_legend=-1,
)

# Plot curves for each species (sample 15 per species for clarity)
for species_idx in range(3):
    species_mask = y == species_idx
    species_data = X_scaled[species_mask]

    # Sample 15 observations per species
    n_samples = 15
    indices = np.random.choice(len(species_data), n_samples, replace=False)

    for i, idx in enumerate(indices):
        row = species_data[idx]
        # Andrews transform: f(t) = x1/sqrt(2) + x2*sin(t) + x3*cos(t) + x4*sin(2t)
        curve_values = (
            row[0] / np.sqrt(2) + row[1] * np.sin(t_values) + row[2] * np.cos(t_values) + row[3] * np.sin(2 * t_values)
        )
        points = [(float(t), float(v)) for t, v in zip(t_values, curve_values, strict=True)]

        # Add series name only for first curve of each species
        if i == 0:
            chart.add(species_names[species_idx], points, show_dots=False)
        else:
            chart.add(None, points, show_dots=False, stroke=custom_style.colors[species_idx])

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
