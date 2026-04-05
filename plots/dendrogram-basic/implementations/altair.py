"""pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: altair 6.0.0 | Python 3.14.3
Quality: /100 | Updated: 2026-04-05
"""

import altair as alt
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import load_iris


# Data - Iris flower measurements (15 samples, 3 species)
iris = load_iris()
indices = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
features = iris.data[indices]
species_names = ["Setosa", "Versicolor", "Virginica"]
labels = [f"{species_names[iris.target[i]]}-{i}" for i in indices]

# Compute hierarchical clustering using Ward's method
Z = linkage(features, method="ward")
dendro = dendrogram(Z, labels=labels, no_plot=True)

# Extract line segments from scipy's dendrogram output
# Each merge produces a U-shape: left vertical + horizontal + right vertical
segments = []
for xpts, ypts in zip(dendro["icoord"], dendro["dcoord"], strict=True):
    for i in range(3):
        segments.append({"x": xpts[i], "y": ypts[i], "x2": xpts[i + 1], "y2": ypts[i + 1]})

segments_df = pd.DataFrame(segments)

# Leaf label positions from scipy (positioned at 5, 15, 25, ...)
leaf_labels = dendro["ivl"]
leaf_df = pd.DataFrame(
    {
        "x": [5 + 10 * i for i in range(len(leaf_labels))],
        "y_base": [0.0] * len(leaf_labels),
        "label": leaf_labels,
        "species": [lbl.rsplit("-", 1)[0] for lbl in leaf_labels],
    }
)

# Species color palette starting with Python Blue
species_palette = {"Setosa": "#306998", "Versicolor": "#D4A017", "Virginica": "#7B68AE"}

# Axis domain
x_min = min(s["x"] for s in segments) - 5
x_max = max(s["x2"] for s in segments) + 5
y_max = Z[:, 2].max() * 1.08

# Dendrogram branches
branches = (
    alt.Chart(segments_df)
    .mark_rule(strokeWidth=2.5, color="#4A7FA5")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[x_min, x_max]), axis=None),
        x2="x2:Q",
        y=alt.Y("y:Q", title="Distance (Ward's method)", scale=alt.Scale(domain=[0, y_max])),
        y2="y2:Q",
    )
)

# Leaf markers at base of dendrogram colored by species
leaf_dots = (
    alt.Chart(leaf_df)
    .mark_point(size=120, filled=True, strokeWidth=1.5, stroke="white")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[x_min, x_max]), axis=None),
        y=alt.Y("y_base:Q", scale=alt.Scale(domain=[0, y_max])),
        color=alt.Color(
            "species:N",
            scale=alt.Scale(domain=list(species_palette.keys()), range=list(species_palette.values())),
            legend=alt.Legend(
                title="Species", titleFontSize=18, labelFontSize=16, symbolSize=200, orient="right", offset=10
            ),
        ),
    )
)

# Leaf labels colored by species
leaf_text = (
    alt.Chart(leaf_df)
    .mark_text(angle=315, align="right", baseline="top", fontSize=14, fontWeight="bold")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[x_min, x_max]), axis=None),
        y=alt.value(870),
        text="label:N",
        color=alt.Color(
            "species:N",
            scale=alt.Scale(domain=list(species_palette.keys()), range=list(species_palette.values())),
            legend=None,
        ),
    )
)

# Combine layers
chart = (
    alt.layer(branches, leaf_dots, leaf_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("dendrogram-basic · altair · pyplots.ai", fontSize=28, anchor="start", offset=20),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.2, gridDash=[4, 4], domainColor="#888888")
    .configure_view(strokeWidth=0)
    .configure_legend(padding=20, cornerRadius=4, strokeColor="#dddddd")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
