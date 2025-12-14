"""
parallel-basic: Basic Parallel Coordinates Plot
Library: plotly
"""

import pandas as pd
import plotly.graph_objects as go


# Data - Iris dataset for multivariate demonstration
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

# Map species to numeric for color scale
species_map = {"setosa": 0, "versicolor": 1, "virginica": 2}
df["species_code"] = df["species"].map(species_map)

# Create parallel coordinates plot using graph_objects for more control
fig = go.Figure(
    data=go.Parcoords(
        line={
            "color": df["species_code"],
            "colorscale": [[0, "#306998"], [0.5, "#FFD43B"], [1, "#4CAF50"]],
            "showscale": True,
            "colorbar": {
                "title": {"text": "Species", "font": {"size": 20}},
                "tickvals": [0, 1, 2],
                "ticktext": ["setosa", "versicolor", "virginica"],
                "tickfont": {"size": 18},
            },
        },
        dimensions=[
            {"label": "Sepal Length (cm)", "values": df["sepal_length"]},
            {"label": "Sepal Width (cm)", "values": df["sepal_width"]},
            {"label": "Petal Length (cm)", "values": df["petal_length"]},
            {"label": "Petal Width (cm)", "values": df["petal_width"]},
        ],
        labelfont={"size": 20},
        tickfont={"size": 16},
    )
)

# Layout - sized for 4800x2700 px output
fig.update_layout(
    title={"text": "parallel-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    template="plotly_white",
    margin={"l": 100, "r": 150, "t": 100, "b": 80},
)

# Save as PNG (4800x2700 px) and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
