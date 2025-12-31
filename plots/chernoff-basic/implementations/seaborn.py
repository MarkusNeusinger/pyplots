""" pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 81/100 | Created: 2025-12-31
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Load and prepare data (Iris dataset - 4 measurements per flower)
iris_df = sns.load_dataset("iris")
feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
data = iris_df[feature_cols].values
species_map = {"setosa": 0, "versicolor": 1, "virginica": 2}
target = iris_df["species"].map(species_map).values

# Select subset of samples with MORE variation within species (5 per species = 15 total faces)
# Choose samples that span the full range of variation within each species
np.random.seed(42)
indices = []
for species in range(3):
    species_indices = np.where(target == species)[0]
    species_data = data[species_indices]
    # Compute distance from mean to select diverse samples
    mean_vals = species_data.mean(axis=0)
    distances = np.sum((species_data - mean_vals) ** 2, axis=1)
    # Select: 1 closest to mean, 2 with smallest values, 2 with largest values
    sorted_by_dist = species_indices[np.argsort(distances)]
    sorted_by_sum = species_indices[np.argsort(species_data.sum(axis=1))]
    selected = list({sorted_by_dist[0], sorted_by_sum[0], sorted_by_sum[1], sorted_by_sum[-1], sorted_by_sum[-2]})
    while len(selected) < 5:
        for idx in species_indices:
            if idx not in selected:
                selected.append(idx)
                break
    indices.extend(selected[:5])
indices = np.array(indices)

subset_data = data[indices]
subset_target = target[indices]
species_names = ["Setosa", "Versicolor", "Virginica"]

# Normalize data to 0-1 range using GLOBAL min/max for better within-species variation
data_min = data.min(axis=0)
data_max = data.max(axis=0)
normalized_data = (subset_data - data_min) / (data_max - data_min + 1e-8)

# Set seaborn style
sns.set_style("white")
sns.set_context("poster", font_scale=1.0)

# Color palette for species (using seaborn palette)
palette = sns.color_palette("Set2", 3)
face_colors = [palette[t] for t in subset_target]

# Create figure - 16:9 aspect ratio for 4800x2700 at 300dpi
fig = plt.figure(figsize=(16, 9))

# Create grid layout: heatmap on left, faces on right
gs = fig.add_gridspec(3, 7, width_ratios=[1.5, 1, 1, 1, 1, 1, 0.1], hspace=0.25, wspace=0.15)

# Add heatmap showing feature values on left side using seaborn
ax_heatmap = fig.add_subplot(gs[:, 0])
heatmap_data = normalized_data  # Samples x Features (15 x 4)
sns.heatmap(
    heatmap_data,
    ax=ax_heatmap,
    cmap="YlOrRd",
    cbar=False,
    xticklabels=["Sepal\nLength", "Sepal\nWidth", "Petal\nLength", "Petal\nWidth"],
    yticklabels=[f"{species_names[subset_target[i]][0]}{(i % 5) + 1}" for i in range(15)],
    linewidths=1,
    linecolor="white",
    annot=True,
    fmt=".2f",
    annot_kws={"size": 9},
)
ax_heatmap.set_title("Feature Values\n(Normalized)", fontsize=16, fontweight="bold", pad=10)
ax_heatmap.tick_params(axis="x", labelsize=12, rotation=0)
ax_heatmap.tick_params(axis="y", labelsize=11)

# Draw Chernoff faces in grid (3 rows x 5 cols on the right side)
for idx in range(15):
    row = idx // 5  # Rows 0, 1, 2
    col = idx % 5 + 1  # Columns 1-5 (column 0 is heatmap)
    ax = fig.add_subplot(gs[row, col])

    features = normalized_data[idx]
    color = face_colors[idx]

    # Map features to facial characteristics
    # Feature 0: sepal_length -> face width (0.6 to 1.0)
    # Feature 1: sepal_width -> face height (0.7 to 1.1)
    # Feature 2: petal_length -> eye size (0.06 to 0.14)
    # Feature 3: petal_width -> mouth curvature (-0.25 to 0.25)

    face_width = 0.55 + features[0] * 0.4
    face_height = 0.65 + features[1] * 0.4
    eye_size = 0.06 + features[2] * 0.08
    mouth_curve = -0.25 + features[3] * 0.5

    # Draw face outline (ellipse)
    face = mpatches.Ellipse((0.5, 0.5), face_width, face_height, facecolor=color, edgecolor="black", linewidth=2.5)
    ax.add_patch(face)

    # Draw eyes
    eye_y = 0.58
    eye_spacing = 0.11 + features[1] * 0.05

    # Left eye
    left_eye = mpatches.Ellipse(
        (0.5 - eye_spacing, eye_y), eye_size * 1.6, eye_size, facecolor="white", edgecolor="black", linewidth=2
    )
    ax.add_patch(left_eye)
    left_pupil = mpatches.Circle((0.5 - eye_spacing, eye_y), eye_size * 0.35, facecolor="black")
    ax.add_patch(left_pupil)

    # Right eye
    right_eye = mpatches.Ellipse(
        (0.5 + eye_spacing, eye_y), eye_size * 1.6, eye_size, facecolor="white", edgecolor="black", linewidth=2
    )
    ax.add_patch(right_eye)
    right_pupil = mpatches.Circle((0.5 + eye_spacing, eye_y), eye_size * 0.35, facecolor="black")
    ax.add_patch(right_pupil)

    # Draw eyebrows
    eyebrow_angle = -0.12 + features[2] * 0.24
    eyebrow_y = eye_y + eye_size + 0.05

    ax.plot(
        [0.5 - eye_spacing - 0.05, 0.5 - eye_spacing + 0.05],
        [eyebrow_y + eyebrow_angle, eyebrow_y - eyebrow_angle],
        color="black",
        linewidth=3.5,
        solid_capstyle="round",
    )
    ax.plot(
        [0.5 + eye_spacing - 0.05, 0.5 + eye_spacing + 0.05],
        [eyebrow_y - eyebrow_angle, eyebrow_y + eyebrow_angle],
        color="black",
        linewidth=3.5,
        solid_capstyle="round",
    )

    # Draw nose
    nose_size = 0.03 + features[0] * 0.025
    nose = mpatches.Polygon(
        [[0.5, 0.50], [0.5 - nose_size, 0.40], [0.5 + nose_size, 0.40]],
        facecolor=tuple(c * 0.85 for c in color[:3]),
        edgecolor="black",
        linewidth=1.5,
    )
    ax.add_patch(nose)

    # Draw mouth
    mouth_width = 0.08 + features[0] * 0.05
    mouth_x = np.linspace(0.5 - mouth_width, 0.5 + mouth_width, 25)
    mouth_y = 0.30 + mouth_curve * ((mouth_x - 0.5) ** 2) * 18
    ax.plot(mouth_x, mouth_y, color="#8B0000", linewidth=3.5, solid_capstyle="round")

    # Set axis properties
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Add label below face
    species_idx = subset_target[idx]
    sample_num = (idx % 5) + 1
    ax.text(
        0.5, -0.02, f"{species_names[species_idx]} #{sample_num}", ha="center", va="top", fontsize=11, fontweight="bold"
    )

# Add overall title
fig.suptitle("chernoff-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

# Add legend for species (positioned to the right)
legend_handles = [mpatches.Patch(color=palette[i], label=species_names[i], ec="black", lw=1.5) for i in range(3)]
fig.legend(
    handles=legend_handles, loc="center right", fontsize=14, frameon=True, bbox_to_anchor=(0.99, 0.5), title="Species"
)

# Add feature mapping explanation at bottom
feature_text = (
    "Face Width ← Sepal Length  |  Face Height ← Sepal Width  |  Eye Size ← Petal Length  |  Mouth Curve ← Petal Width"
)
fig.text(0.55, 0.02, feature_text, ha="center", fontsize=12, style="italic")

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
