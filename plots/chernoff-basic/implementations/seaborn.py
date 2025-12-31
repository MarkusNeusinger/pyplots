""" pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
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

# Select subset of samples (5 per species = 15 total faces)
np.random.seed(42)
indices = []
for species in range(3):
    species_indices = np.where(target == species)[0]
    selected = np.random.choice(species_indices, 5, replace=False)
    indices.extend(selected)
indices = np.array(indices)

subset_data = data[indices]
subset_target = target[indices]
species_names = ["Setosa", "Versicolor", "Virginica"]

# Normalize data to 0-1 range for facial feature mapping
data_min = subset_data.min(axis=0)
data_max = subset_data.max(axis=0)
normalized_data = (subset_data - data_min) / (data_max - data_min + 1e-8)

# Set seaborn style (no grid for cleaner face display)
sns.set_style("white")
sns.set_context("poster", font_scale=0.9)

# Color palette for species (using seaborn palette)
palette = sns.color_palette("Set2", 3)
face_colors = [palette[t] for t in subset_target]

# Create figure with grid layout (3 rows x 5 cols for 15 faces)
# Using square format for better face display
fig = plt.figure(figsize=(12, 12))

# Create a main axes for the heatmap showing feature values
gs = fig.add_gridspec(4, 5, height_ratios=[0.8, 1, 1, 1], hspace=0.3, wspace=0.15)

# Add heatmap showing raw feature values at top using seaborn
ax_heatmap = fig.add_subplot(gs[0, :])
heatmap_data = normalized_data.T  # Features x Samples
sns.heatmap(
    heatmap_data,
    ax=ax_heatmap,
    cmap="YlOrRd",
    cbar_kws={"label": "Normalized Value", "shrink": 0.8},
    xticklabels=[f"{species_names[subset_target[i]][0]}{(i % 5) + 1}" for i in range(15)],
    yticklabels=["Sepal L.", "Sepal W.", "Petal L.", "Petal W."],
    linewidths=0.5,
    linecolor="white",
)
ax_heatmap.set_title("Feature Values (mapped to faces below)", fontsize=14, pad=10)
ax_heatmap.tick_params(axis="x", labelsize=10, rotation=0)
ax_heatmap.tick_params(axis="y", labelsize=11)

# Draw Chernoff faces in grid below heatmap
for idx in range(15):
    row = idx // 5 + 1  # Rows 1, 2, 3 (0 is heatmap)
    col = idx % 5
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
fig.suptitle("chernoff-basic · seaborn · pyplots.ai", fontsize=22, fontweight="bold", y=0.98)

# Add legend for species
legend_handles = [mpatches.Patch(color=palette[i], label=species_names[i], ec="black", lw=1) for i in range(3)]
fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=14, frameon=True, bbox_to_anchor=(0.5, 0.01))

# Add feature mapping explanation
feature_text = (
    "Face Width ← Sepal Length  |  Face Height ← Sepal Width  |  Eye Size ← Petal Length  |  Mouth Curve ← Petal Width"
)
fig.text(0.5, 0.045, feature_text, ha="center", fontsize=11, style="italic")

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
