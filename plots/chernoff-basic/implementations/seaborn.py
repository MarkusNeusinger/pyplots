"""pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_iris


# Load and prepare data (Iris dataset - 4 measurements per flower)
iris = load_iris()
data = iris.data
target = iris.target
feature_names = iris.feature_names

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

# Set seaborn style
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Color palette for species (using seaborn palette)
palette = sns.color_palette("Set2", 3)
face_colors = [palette[t] for t in subset_target]


def draw_chernoff_face(ax, features, color, label=""):
    """Draw a Chernoff face based on normalized features (0-1)."""
    # Map features to facial characteristics
    # Feature 0: sepal_length -> face width (0.6 to 1.0)
    # Feature 1: sepal_width -> face height (0.7 to 1.1)
    # Feature 2: petal_length -> eye size (0.04 to 0.12)
    # Feature 3: petal_width -> mouth curvature (-0.3 to 0.3)

    face_width = 0.6 + features[0] * 0.4
    face_height = 0.7 + features[1] * 0.4
    eye_size = 0.04 + features[2] * 0.08
    mouth_curve = -0.3 + features[3] * 0.6

    # Draw face outline (ellipse)
    face = mpatches.Ellipse((0.5, 0.5), face_width, face_height, facecolor=color, edgecolor="black", linewidth=2)
    ax.add_patch(face)

    # Draw eyes
    eye_y = 0.58
    eye_spacing = 0.12 + features[1] * 0.06  # sepal_width affects eye spacing

    # Left eye
    left_eye = mpatches.Ellipse(
        (0.5 - eye_spacing, eye_y), eye_size * 1.5, eye_size, facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(left_eye)

    # Left pupil
    left_pupil = mpatches.Circle((0.5 - eye_spacing, eye_y), eye_size * 0.4, facecolor="black")
    ax.add_patch(left_pupil)

    # Right eye
    right_eye = mpatches.Ellipse(
        (0.5 + eye_spacing, eye_y), eye_size * 1.5, eye_size, facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(right_eye)

    # Right pupil
    right_pupil = mpatches.Circle((0.5 + eye_spacing, eye_y), eye_size * 0.4, facecolor="black")
    ax.add_patch(right_pupil)

    # Draw eyebrows (petal_length affects eyebrow angle)
    eyebrow_angle = -0.15 + features[2] * 0.3
    eyebrow_y = eye_y + eye_size + 0.04

    # Left eyebrow
    ax.plot(
        [0.5 - eye_spacing - 0.06, 0.5 - eye_spacing + 0.06],
        [eyebrow_y + eyebrow_angle, eyebrow_y - eyebrow_angle],
        color="black",
        linewidth=3,
    )

    # Right eyebrow
    ax.plot(
        [0.5 + eye_spacing - 0.06, 0.5 + eye_spacing + 0.06],
        [eyebrow_y - eyebrow_angle, eyebrow_y + eyebrow_angle],
        color="black",
        linewidth=3,
    )

    # Draw nose (sepal_length affects nose size)
    nose_size = 0.03 + features[0] * 0.03
    nose = mpatches.Polygon(
        [[0.5, 0.52], [0.5 - nose_size, 0.42], [0.5 + nose_size, 0.42]],
        facecolor=tuple(c * 0.85 for c in color[:3]),
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(nose)

    # Draw mouth (curved line based on petal_width)
    mouth_width = 0.08 + features[0] * 0.06
    mouth_x = np.linspace(0.5 - mouth_width, 0.5 + mouth_width, 20)
    mouth_y = 0.32 + mouth_curve * ((mouth_x - 0.5) ** 2) * 15

    ax.plot(mouth_x, mouth_y, color="darkred", linewidth=3)

    # Set axis properties
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    if label:
        ax.set_title(label, fontsize=14, fontweight="bold", pad=5)


# Create figure with grid layout (3 rows x 5 cols for 15 faces)
fig, axes = plt.subplots(3, 5, figsize=(16, 9))

# Draw each face
for idx, (ax, features, color) in enumerate(zip(axes.flatten(), normalized_data, face_colors, strict=True)):
    species_idx = subset_target[idx]
    sample_num = (idx % 5) + 1
    label = f"{species_names[species_idx]} #{sample_num}"
    draw_chernoff_face(ax, features, color, label)

# Add overall title
fig.suptitle("chernoff-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

# Add legend for species
legend_handles = [mpatches.Patch(color=palette[i], label=species_names[i]) for i in range(3)]
fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=16, frameon=True, bbox_to_anchor=(0.5, -0.02))

# Add feature mapping explanation
feature_text = (
    "Feature Mapping: "
    "Face Width ← Sepal Length | "
    "Face Height ← Sepal Width | "
    "Eye Size ← Petal Length | "
    "Mouth Curve ← Petal Width"
)
fig.text(0.5, -0.06, feature_text, ha="center", fontsize=12, style="italic")

plt.tight_layout(rect=[0, 0.08, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
