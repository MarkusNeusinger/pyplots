"""pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-31
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

# Grid positions for 12 faces (4 columns x 3 rows)
data["col"] = [i % 4 for i in range(12)]
data["row"] = [i // 4 for i in range(12)]
data["x_center"] = data["col"] * 180 + 100
data["y_center"] = (2 - data["row"]) * 200 + 150  # Invert row for top-to-bottom

# Calculate face feature dimensions based on variables
# face_width: sepal_length, face_height: sepal_width
# eye_size: petal_length, mouth_width: petal_width
data["face_width"] = 35 + data["sepal_length"] * 35  # 35-70
data["face_height"] = 45 + data["sepal_width"] * 35  # 45-80
data["eye_size"] = 6 + data["petal_length"] * 14  # 6-20
data["mouth_width"] = 12 + data["petal_width"] * 20  # 12-32

# Build face components using layered shapes
face_records = []
for _, r in data.iterrows():
    xc, yc = r["x_center"], r["y_center"]
    fw, fh = r["face_width"], r["face_height"]
    es = r["eye_size"]
    mw = r["mouth_width"]

    # Face outline (large point)
    face_records.append(
        {
            "x": xc,
            "y": yc,
            "size": fw * fh * 2.5,
            "color": r["color"],
            "part": "face",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.35,
            "shape": "circle",
        }
    )
    # Face border (slightly larger, darker)
    face_records.append(
        {
            "x": xc,
            "y": yc,
            "size": fw * fh * 2.8,
            "color": "#2C3E50",
            "part": "border",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.15,
            "shape": "circle",
        }
    )
    # Left eye
    face_records.append(
        {
            "x": xc - fw * 0.32,
            "y": yc + fh * 0.18,
            "size": es * 30,
            "color": "#1A252F",
            "part": "eye",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 1.0,
            "shape": "circle",
        }
    )
    # Right eye
    face_records.append(
        {
            "x": xc + fw * 0.32,
            "y": yc + fh * 0.18,
            "size": es * 30,
            "color": "#1A252F",
            "part": "eye",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 1.0,
            "shape": "circle",
        }
    )
    # Left pupil (white highlight)
    face_records.append(
        {
            "x": xc - fw * 0.32 + 2,
            "y": yc + fh * 0.18 + 2,
            "size": es * 8,
            "color": "#FFFFFF",
            "part": "pupil",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
            "shape": "circle",
        }
    )
    # Right pupil (white highlight)
    face_records.append(
        {
            "x": xc + fw * 0.32 + 2,
            "y": yc + fh * 0.18 + 2,
            "size": es * 8,
            "color": "#FFFFFF",
            "part": "pupil",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.9,
            "shape": "circle",
        }
    )
    # Nose
    face_records.append(
        {
            "x": xc,
            "y": yc - fh * 0.05,
            "size": 60,
            "color": "#5D6D7E",
            "part": "nose",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.6,
            "shape": "circle",
        }
    )
    # Mouth (ellipse approximated by a point)
    face_records.append(
        {
            "x": xc,
            "y": yc - fh * 0.32,
            "size": mw * 12,
            "color": "#C0392B",
            "part": "mouth",
            "observation": r["observation"],
            "species": r["species"],
            "opacity": 0.85,
            "shape": "circle",
        }
    )

face_df = pd.DataFrame(face_records)

# Reorder so borders draw first, then faces, then features
part_order = {"border": 0, "face": 1, "nose": 2, "mouth": 3, "eye": 4, "pupil": 5}
face_df["order"] = face_df["part"].map(part_order)
face_df = face_df.sort_values("order")

# Create labels for each face
label_df = data[["x_center", "y_center", "observation", "face_height"]].copy()
label_df["y_label"] = label_df["y_center"] - 65

# Face components chart
faces = (
    alt.Chart(face_df)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[0, 850])),
        y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[0, 750])),
        size=alt.Size("size:Q", legend=None, scale=alt.Scale(range=[30, 12000])),
        color=alt.Color("color:N", legend=None, scale=None),
        opacity=alt.Opacity("opacity:Q", legend=None),
        order="order:O",
        tooltip=["observation:N", "species:N"],
    )
)

# Labels
labels = (
    alt.Chart(label_df)
    .mark_text(fontSize=14, fontWeight="bold", color="#2C3E50")
    .encode(x=alt.X("x_center:Q", axis=None), y=alt.Y("y_label:Q", axis=None), text="observation:N")
)

# Legend for species (positioned in lower right)
legend_data = pd.DataFrame(
    {
        "species": ["setosa", "versicolor", "virginica"],
        "x": [780, 780, 780],
        "y": [120, 80, 40],
        "color": ["#306998", "#FFD43B", "#4B8BBE"],
    }
)

legend_points = (
    alt.Chart(legend_data)
    .mark_point(filled=True, size=250)
    .encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None), color=alt.Color("color:N", scale=None, legend=None))
)

legend_text = (
    alt.Chart(legend_data).mark_text(align="right", fontSize=13, dx=-15).encode(x="x:Q", y="y:Q", text="species:N")
)

# Feature mapping explanation
mapping_data = pd.DataFrame(
    {
        "text": [
            "Face width: sepal length",
            "Face height: sepal width",
            "Eye size: petal length",
            "Mouth width: petal width",
        ],
        "x": [65, 65, 65, 65],
        "y": [120, 95, 70, 45],
    }
)

mapping_text = (
    alt.Chart(mapping_data)
    .mark_text(align="left", fontSize=11, color="#5D6D7E")
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
