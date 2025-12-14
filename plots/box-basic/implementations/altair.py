"""
box-basic: Basic Box Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - simulating salary distributions across departments
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
data = []

for dept in departments:
    if dept == "Engineering":
        values = np.random.normal(95000, 15000, 80)
    elif dept == "Marketing":
        values = np.random.normal(75000, 12000, 60)
    elif dept == "Sales":
        values = np.random.normal(70000, 20000, 100)
    elif dept == "HR":
        values = np.random.normal(65000, 10000, 50)
    else:  # Finance
        values = np.random.normal(85000, 14000, 70)

    # Add some outliers
    outliers = np.random.uniform(values.min() - 20000, values.max() + 25000, 3)
    values = np.concatenate([values, outliers])

    for v in values:
        data.append({"Department": dept, "Salary": v})

df = pd.DataFrame(data)

# Color palette - Python colors first, then colorblind-safe additions
colors = ["#306998", "#FFD43B", "#4B8BBE", "#646464", "#2ECC71"]

# Create box plot
chart = (
    alt.Chart(df)
    .mark_boxplot(size=80, median={"stroke": "white", "strokeWidth": 3}, outliers={"size": 100, "strokeWidth": 2})
    .encode(
        x=alt.X("Department:N", title="Department", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y("Salary:Q", title="Salary ($)", axis=alt.Axis(labelFontSize=18, titleFontSize=22, format="$,.0f")),
        color=alt.Color("Department:N", scale=alt.Scale(range=colors), legend=None),
    )
    .properties(width=1600, height=900, title=alt.Title("box-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
