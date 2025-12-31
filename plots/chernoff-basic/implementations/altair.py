""" pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: altair 6.0.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-31
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Iris dataset features for 12 representative flowers
np.random.seed(42)
# Diverse samples from iris-like measurements (normalized 0-1)
data = pd.DataFrame(
    {
        "observation": [f"Sample {i + 1}" for i in range(12)],
        "sepal_length": [0.22, 0.83, 0.45, 0.12, 0.91, 0.67, 0.33, 0.78, 0.55, 0.95, 0.28, 0.61],
        "sepal_width": [0.63, 0.45, 0.78, 0.89, 0.32, 0.56, 0.71, 0.41, 0.65, 0.25, 0.82, 0.48],
        "petal_length": [0.07, 0.69, 0.42, 0.05, 0.83, 0.55, 0.18, 0.76, 0.38, 0.95, 0.11, 0.62],
        "petal_width": [0.04, 0.54, 0.33, 0.02, 0.79, 0.48, 0.12, 0.67, 0.29, 0.88, 0.08, 0.52],
        "species": [
            "setosa",
            "virginica",
            "versicolor",
            "setosa",
            "virginica",
            "versicolor",
            "setosa",
            "virginica",
            "versicolor",
            "virginica",
            "setosa",
            "versicolor",
        ],
    }
)

# Map species to colors
species_colors = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#4B8BBE"}
data["color"] = data["species"].map(species_colors)

# Grid positions for 12 faces (3 columns x 4 rows for larger faces)
data["col"] = [i % 3 for i in range(12)]
data["row"] = [i // 3 for i in range(12)]
data["x_center"] = data["col"] * 250 + 180
data["y_center"] = (3 - data["row"]) * 180 + 80

# Calculate face feature dimensions based on variables
# face_width: sepal_length, face_height: sepal_width
# eye_size: petal_length, mouth_width: petal_width
# eyebrow_slant: derived from petal_length (maps to eyebrow angle)
data["face_width"] = 50 + data["sepal_length"] * 45  # 50-95
data["face_height"] = 60 + data["sepal_width"] * 45  # 60-105
data["eye_size"] = 8 + data["petal_length"] * 18  # 8-26
data["mouth_width"] = 18 + data["petal_width"] * 28  # 18-46
data["eyebrow_slant"] = -12 + data["petal_length"] * 24  # -12 to 12 (angle offset)

# Build face components using layered shapes
face_records = []
for _, r in data.iterrows():
    xc, yc = r["x_center"], r["y_center"]
    fw, fh = r["face_width"], r["face_height"]
    es = r["eye_size"]
    mw = r["mouth_width"]
    eb_slant = r["eyebrow_slant"]

    # Face border (slightly larger, darker)
    face_records.append(
        {
            "x": xc,
            "y": yc,
            "size": fw * fh * 3.2,
            "color": "#2C3E50",
            "part": "border",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.2,
        }
    )
    # Face outline (large point)
    face_records.append(
        {
            "x": xc,
            "y": yc,
            "size": fw * fh * 3.0,
            "color": r["color"],
            "part": "face",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.45,
        }
    )
    # Left eyebrow (line represented by two points)
    face_records.append(
        {
            "x": xc - fw * 0.38,
            "y": yc + fh * 0.32 + eb_slant * 0.3,
            "size": 120,
            "color": "#2C3E50",
            "part": "eyebrow",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
        }
    )
    face_records.append(
        {
            "x": xc - fw * 0.22,
            "y": yc + fh * 0.32 - eb_slant * 0.3,
            "size": 120,
            "color": "#2C3E50",
            "part": "eyebrow",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
        }
    )
    # Right eyebrow
    face_records.append(
        {
            "x": xc + fw * 0.22,
            "y": yc + fh * 0.32 - eb_slant * 0.3,
            "size": 120,
            "color": "#2C3E50",
            "part": "eyebrow",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
        }
    )
    face_records.append(
        {
            "x": xc + fw * 0.38,
            "y": yc + fh * 0.32 + eb_slant * 0.3,
            "size": 120,
            "color": "#2C3E50",
            "part": "eyebrow",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
        }
    )
    # Left eye
    face_records.append(
        {
            "x": xc - fw * 0.30,
            "y": yc + fh * 0.15,
            "size": es * 45,
            "color": "#1A252F",
            "part": "eye",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 1.0,
        }
    )
    # Right eye
    face_records.append(
        {
            "x": xc + fw * 0.30,
            "y": yc + fh * 0.15,
            "size": es * 45,
            "color": "#1A252F",
            "part": "eye",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 1.0,
        }
    )
    # Left pupil (white highlight)
    face_records.append(
        {
            "x": xc - fw * 0.30 + 3,
            "y": yc + fh * 0.15 + 3,
            "size": es * 12,
            "color": "#FFFFFF",
            "part": "pupil",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.95,
        }
    )
    # Right pupil (white highlight)
    face_records.append(
        {
            "x": xc + fw * 0.30 + 3,
            "y": yc + fh * 0.15 + 3,
            "size": es * 12,
            "color": "#FFFFFF",
            "part": "pupil",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.95,
        }
    )
    # Nose
    face_records.append(
        {
            "x": xc,
            "y": yc - fh * 0.05,
            "size": 90,
            "color": "#5D6D7E",
            "part": "nose",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.7,
        }
    )
    # Mouth - using horizontal ellipse shape for better representation
    # Create mouth with multiple points to simulate elliptical shape
    mouth_y = yc - fh * 0.30
    for dx in np.linspace(-mw * 0.4, mw * 0.4, 7):
        # Parabolic curve for mouth (smiling effect based on width)
        dy = -(dx**2) / (mw * 1.2) + mw * 0.08
        face_records.append(
            {
                "x": xc + dx,
                "y": mouth_y + dy,
                "size": 80 if abs(dx) < mw * 0.3 else 50,
                "color": "#C0392B",
                "part": "mouth",
                "observation": r["observation"],
                "species": r["species"],
                "opacity": 0.9,
            }
        )

face_df = pd.DataFrame(face_records)

# Reorder so borders draw first, then faces, then features
part_order = {"border": 0, "face": 1, "eyebrow": 2, "nose": 3, "mouth": 4, "eye": 5, "pupil": 6}
face_df["order"] = face_df["part"].map(part_order)
face_df = face_df.sort_values("order")

# Create labels for each face - positioned below faces
label_df = data[["x_center", "y_center", "observation", "face_height"]].copy()
label_df["y_label"] = label_df["y_center"] - label_df["face_height"] * 0.6 - 25

# Face components chart
faces = (
    alt.Chart(face_df)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[0, 900])),
        y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[0, 850])),
        size=alt.Size("size:Q", legend=None, scale=alt.Scale(range=[40, 18000])),
        color=alt.Color("color:N", legend=None, scale=None),
        opacity=alt.Opacity("opacity:Q", legend=None),
        order="order:O",
        tooltip=["observation:N", "species:N"],
    )
)

# Labels
labels = (
    alt.Chart(label_df)
    .mark_text(fontSize=15, fontWeight="bold", color="#2C3E50")
    .encode(x=alt.X("x_center:Q", axis=None), y=alt.Y("y_label:Q", axis=None), text="observation:N")
)

# Legend for species (positioned in top right corner to avoid overlap)
legend_data = pd.DataFrame(
    {
        "species": ["setosa", "versicolor", "virginica"],
        "x": [830, 830, 830],
        "y": [800, 760, 720],
        "color": ["#306998", "#FFD43B", "#4B8BBE"],
    }
)

# Legend with matching face-like appearance (translucent, larger)
legend_points = (
    alt.Chart(legend_data)
    .mark_point(filled=True, size=800, opacity=0.45)
    .encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None), color=alt.Color("color:N", scale=None, legend=None))
)

legend_text = (
    alt.Chart(legend_data)
    .mark_text(align="right", fontSize=14, dx=-30, fontWeight="bold")
    .encode(x="x:Q", y="y:Q", text="species:N")
)

# Feature mapping explanation (moved to bottom left to avoid label overlap)
mapping_data = pd.DataFrame(
    {
        "text": [
            "Feature Mapping:",
            "Face width ← sepal length",
            "Face height ← sepal width",
            "Eye size ← petal length",
            "Mouth width ← petal width",
            "Eyebrow slant ← petal length",
        ],
        "x": [50, 50, 50, 50, 50, 50],
        "y": [95, 75, 55, 35, 15, -5],
    }
)

mapping_text = (
    alt.Chart(mapping_data)
    .mark_text(align="left", fontSize=12, color="#34495E")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Combine all layers
chart = (
    (faces + labels + legend_points + legend_text + mapping_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "chernoff-basic · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            subtitle="Iris Dataset: Each face represents a flower sample with features encoding measurements",
            subtitleFontSize=16,
        ),
    )
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
