""" pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: plotly 6.5.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-31
"""

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris


# Data - use Iris dataset with 4 measurements per flower
np.random.seed(42)
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# Select subset for clear visualization (5 samples per species = 15 faces)
indices = []
for species in range(3):
    species_indices = np.where(y == species)[0][:5]
    indices.extend(species_indices)
X_subset = X[indices]
y_subset = y[indices]

# Normalize data to 0-1 range
X_norm = (X_subset - X_subset.min(axis=0)) / (X_subset.max(axis=0) - X_subset.min(axis=0))

# Colors for each species
colors = ["#306998", "#FFD43B", "#2CA02C"]  # Python Blue, Python Yellow, Green


def create_face_shape(cx, cy, radius, data, color):
    """
    Create a Chernoff face at position (cx, cy) with given radius.
    data: normalized values [0-1] for 4 features
    Feature mapping:
      - sepal_length -> face width
      - sepal_width -> face height
      - petal_length -> eye size
      - petal_width -> mouth curvature
    """
    shapes = []

    # Unpack features
    face_width_factor = 0.7 + data[0] * 0.6  # 0.7-1.3
    face_height_factor = 0.8 + data[1] * 0.4  # 0.8-1.2
    eye_size = 0.08 + data[2] * 0.12  # 0.08-0.2
    mouth_curve = data[3] * 0.15  # 0-0.15 (smile amount)

    # Face outline (ellipse approximated by path)
    face_w = radius * face_width_factor
    face_h = radius * face_height_factor

    # Create ellipse path for face
    theta = np.linspace(0, 2 * np.pi, 50)
    face_x = cx + face_w * np.cos(theta)
    face_y = cy + face_h * np.sin(theta)

    shapes.append(
        dict(
            type="path",
            path="M " + " L ".join([f"{x},{y}" for x, y in zip(face_x, face_y)]) + " Z",
            fillcolor=color,
            line=dict(color="#333333", width=2),
            opacity=0.3,
        )
    )

    # Eyes
    eye_offset_x = face_w * 0.35
    eye_offset_y = face_h * 0.2
    eye_r = radius * eye_size

    # Left eye
    eye_theta = np.linspace(0, 2 * np.pi, 30)
    left_eye_x = (cx - eye_offset_x) + eye_r * np.cos(eye_theta)
    left_eye_y = (cy + eye_offset_y) + eye_r * 0.7 * np.sin(eye_theta)
    shapes.append(
        dict(
            type="path",
            path="M " + " L ".join([f"{x},{y}" for x, y in zip(left_eye_x, left_eye_y)]) + " Z",
            fillcolor="white",
            line=dict(color="#333333", width=2),
        )
    )

    # Left pupil
    pupil_r = eye_r * 0.5
    pupil_x = (cx - eye_offset_x) + pupil_r * np.cos(eye_theta)
    pupil_y = (cy + eye_offset_y) + pupil_r * np.sin(eye_theta)
    shapes.append(
        dict(
            type="path",
            path="M " + " L ".join([f"{x},{y}" for x, y in zip(pupil_x, pupil_y)]) + " Z",
            fillcolor="#333333",
            line=dict(color="#333333", width=1),
        )
    )

    # Right eye
    right_eye_x = (cx + eye_offset_x) + eye_r * np.cos(eye_theta)
    right_eye_y = (cy + eye_offset_y) + eye_r * 0.7 * np.sin(eye_theta)
    shapes.append(
        dict(
            type="path",
            path="M " + " L ".join([f"{x},{y}" for x, y in zip(right_eye_x, right_eye_y)]) + " Z",
            fillcolor="white",
            line=dict(color="#333333", width=2),
        )
    )

    # Right pupil
    pupil_x = (cx + eye_offset_x) + pupil_r * np.cos(eye_theta)
    pupil_y = (cy + eye_offset_y) + pupil_r * np.sin(eye_theta)
    shapes.append(
        dict(
            type="path",
            path="M " + " L ".join([f"{x},{y}" for x, y in zip(pupil_x, pupil_y)]) + " Z",
            fillcolor="#333333",
            line=dict(color="#333333", width=1),
        )
    )

    # Nose (simple triangle)
    nose_h = face_h * 0.15
    nose_w = face_w * 0.1
    nose_y_center = cy
    nose_top = f"M {cx},{nose_y_center + nose_h * 0.5}"
    nose_left = f"L {cx - nose_w},{nose_y_center - nose_h * 0.5}"
    nose_right = f"L {cx + nose_w},{nose_y_center - nose_h * 0.5}"
    shapes.append(
        dict(
            type="path",
            path=f"{nose_top} {nose_left} {nose_right} Z",
            fillcolor="#333333",
            line=dict(color="#333333", width=1),
            opacity=0.5,
        )
    )

    # Mouth (curved line based on mouth_curve)
    mouth_y = cy - face_h * 0.35
    mouth_width = face_w * 0.5
    mouth_points = 20
    mouth_x_vals = np.linspace(cx - mouth_width, cx + mouth_width, mouth_points)
    # Parabolic curve for smile - positive curve = smile, negative = frown
    # Map from 0-1 to -0.15 to +0.15 for frown to smile
    smile_amount = (mouth_curve - 0.075) * 2  # Center around neutral
    mouth_y_vals = mouth_y + smile_amount * (1 - ((mouth_x_vals - cx) / mouth_width) ** 2) * radius * 0.3

    # Create mouth as a thick line using path
    mouth_path = "M " + " L ".join([f"{x},{y}" for x, y in zip(mouth_x_vals, mouth_y_vals)])
    shapes.append(dict(type="path", path=mouth_path, line=dict(color="#333333", width=3)))

    # Eyebrows (angled based on features)
    brow_offset_y = eye_offset_y + eye_r + face_h * 0.1
    brow_width = eye_r * 1.2
    brow_angle = (data[0] - 0.5) * 0.15  # Slight angle variation

    # Left eyebrow
    shapes.append(
        dict(
            type="line",
            x0=cx - eye_offset_x - brow_width,
            y0=cy + brow_offset_y - brow_angle * radius,
            x1=cx - eye_offset_x + brow_width,
            y1=cy + brow_offset_y + brow_angle * radius,
            line=dict(color="#333333", width=3),
        )
    )

    # Right eyebrow
    shapes.append(
        dict(
            type="line",
            x0=cx + eye_offset_x - brow_width,
            y0=cy + brow_offset_y + brow_angle * radius,
            x1=cx + eye_offset_x + brow_width,
            y1=cy + brow_offset_y - brow_angle * radius,
            line=dict(color="#333333", width=3),
        )
    )

    return shapes


# Create figure
fig = go.Figure()

# Grid layout: 3 rows (species) x 5 columns (samples)
n_cols = 5
n_rows = 3
spacing = 2.5
radius = 0.9

all_shapes = []

for i, (data, species) in enumerate(zip(X_norm, y_subset)):
    row = i // n_cols
    col = i % n_cols

    cx = col * spacing + spacing / 2
    cy = (n_rows - 1 - row) * spacing + spacing / 2  # Invert row for top-to-bottom

    color = colors[species]
    face_shapes = create_face_shape(cx, cy, radius, data, color)
    all_shapes.extend(face_shapes)

# Add invisible scatter for axis setup
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(opacity=0), showlegend=False))

# Add legend entries for species
for i, (name, color) in enumerate(zip(target_names, colors)):
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=20, color=color, opacity=0.5, line=dict(color="#333333", width=2)),
            name=name.capitalize(),
            showlegend=True,
        )
    )

# Row labels (species names)
for i, name in enumerate(target_names):
    row_y = (n_rows - 1 - i) * spacing + spacing / 2
    fig.add_annotation(
        x=-0.8,
        y=row_y,
        text=f"<b>{name.capitalize()}</b>",
        showarrow=False,
        font=dict(size=18, color="#333333"),
        xanchor="right",
    )

# Column labels (sample numbers)
for col in range(n_cols):
    col_x = col * spacing + spacing / 2
    fig.add_annotation(
        x=col_x,
        y=n_rows * spacing + 0.3,
        text=f"Sample {col + 1}",
        showarrow=False,
        font=dict(size=16, color="#666666"),
    )

# Feature mapping legend
mapping_text = (
    "<b>Feature Mapping:</b><br>"
    "Face Width: Sepal Length<br>"
    "Face Height: Sepal Width<br>"
    "Eye Size: Petal Length<br>"
    "Smile: Petal Width"
)
fig.add_annotation(
    x=n_cols * spacing + 0.5,
    y=n_rows * spacing / 2,
    text=mapping_text,
    showarrow=False,
    font=dict(size=14, color="#333333"),
    align="left",
    xanchor="left",
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="#cccccc",
    borderwidth=1,
    borderpad=10,
)

# Update layout
fig.update_layout(
    title=dict(
        text="Iris Dataset · chernoff-basic · plotly · pyplots.ai",
        font=dict(size=28, color="#333333"),
        x=0.5,
        xanchor="center",
    ),
    shapes=all_shapes,
    xaxis=dict(range=[-1.5, n_cols * spacing + 3.5], showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(
        range=[-0.5, n_rows * spacing + 1],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        title="",
        scaleanchor="x",
        scaleratio=1,
    ),
    template="plotly_white",
    legend=dict(
        title=dict(text="<b>Species</b>", font=dict(size=18)),
        font=dict(size=16),
        x=1.02,
        y=0.98,
        xanchor="left",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#cccccc",
        borderwidth=1,
    ),
    margin=dict(l=120, r=200, t=100, b=50),
    plot_bgcolor="white",
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
