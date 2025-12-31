"""pyplots.ai
contour-decision-boundary: Decision Boundary Classifier Visualization
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import altair as alt
import numpy as np
import pandas as pd
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier


# Data - generate two-moon classification dataset
np.random.seed(42)
X, y = make_moons(n_samples=150, noise=0.25, random_state=42)

# Train a KNN classifier
clf = KNeighborsClassifier(n_neighbors=5)
clf.fit(X, y)

# Create mesh grid for decision boundary
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 150), np.linspace(y_min, y_max, 150))

# Predict on mesh grid
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Create DataFrame for background regions (decision boundary)
mesh_df = pd.DataFrame(
    {"X1": xx.ravel(), "X2": yy.ravel(), "Predicted Class": ["Class A" if z == 0 else "Class B" for z in Z.ravel()]}
)

# Create DataFrame for training points
train_df = pd.DataFrame(
    {"X1": X[:, 0], "X2": X[:, 1], "Class": ["Class A" if label == 0 else "Class B" for label in y]}
)

# Add prediction for training points to show misclassified
train_predictions = clf.predict(X)
train_df["Correctly Classified"] = [
    "Correct" if p == t else "Incorrect" for p, t in zip(train_predictions, y, strict=True)
]

# Decision boundary background using rect marks
background = (
    alt.Chart(mesh_df)
    .mark_rect(opacity=0.4)
    .encode(
        x=alt.X("X1:Q", bin=alt.Bin(maxbins=150), title="Feature X1"),
        y=alt.Y("X2:Q", bin=alt.Bin(maxbins=150), title="Feature X2"),
        color=alt.Color(
            "Predicted Class:N",
            scale=alt.Scale(domain=["Class A", "Class B"], range=["#306998", "#FFD43B"]),
            legend=alt.Legend(title="Decision Region", titleFontSize=18, labelFontSize=16, orient="right"),
        ),
    )
)

# Training points with outline to show classification status
points = (
    alt.Chart(train_df)
    .mark_circle(size=250, strokeWidth=3)
    .encode(
        x=alt.X("X1:Q"),
        y=alt.Y("X2:Q"),
        fill=alt.Color(
            "Class:N",
            scale=alt.Scale(domain=["Class A", "Class B"], range=["#306998", "#FFD43B"]),
            legend=alt.Legend(title="True Class", titleFontSize=18, labelFontSize=16, orient="right"),
        ),
        stroke=alt.Stroke(
            "Correctly Classified:N",
            scale=alt.Scale(domain=["Correct", "Incorrect"], range=["#333333", "#E63946"]),
            legend=alt.Legend(title="Classification", titleFontSize=18, labelFontSize=16, orient="right"),
        ),
        tooltip=["X1:Q", "X2:Q", "Class:N", "Correctly Classified:N"],
    )
)

# Combine layers
chart = (
    alt.layer(background, points)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("contour-decision-boundary · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .resolve_scale(color="independent")
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
