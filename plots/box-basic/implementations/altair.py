""" pyplots.ai
box-basic: Basic Box Plot
Library: altair 6.0.0 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - salary distributions across departments
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
params = {
    "Engineering": (95000, 15000, 80),
    "Marketing": (72000, 12000, 65),
    "Sales": (68000, 18000, 90),
    "HR": (63000, 9000, 55),
    "Finance": (85000, 13000, 70),
}

records = []
for dept, (mean, std, n) in params.items():
    salaries = np.random.normal(mean, std, n)
    salaries = np.clip(salaries, 25000, None)
    for s in salaries:
        records.append({"Department": dept, "Salary": round(s, -2)})

df = pd.DataFrame(records)

# Color palette - Python Blue first, then cohesive colorblind-safe tones
colors = ["#306998", "#E5A835", "#4B8BBE", "#7B6D8D", "#2A9D8F"]

# Plot
chart = (
    alt.Chart(df)
    .mark_boxplot(
        size=80,
        median={"stroke": "white", "strokeWidth": 2.5},
        outliers={"size": 120, "strokeWidth": 1.5, "filled": True, "opacity": 0.7},
    )
    .encode(
        x=alt.X(
            "Department:N",
            title="Department",
            sort=departments,
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=0),
        ),
        y=alt.Y(
            "Salary:Q",
            title="Salary ($)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format="$,.0f", gridOpacity=0.2),
        ),
        color=alt.Color("Department:N", scale=alt.Scale(domain=departments, range=colors), legend=None),
        tooltip=[
            alt.Tooltip("Department:N"),
            alt.Tooltip("median(Salary):Q", title="Median Salary", format="$,.0f"),
            alt.Tooltip("q1(Salary):Q", title="Q1", format="$,.0f"),
            alt.Tooltip("q3(Salary):Q", title="Q3", format="$,.0f"),
        ],
    )
    .properties(width=1600, height=900, title=alt.Title("box-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(grid=True, gridOpacity=0.2, gridColor="#CCCCCC")
    .configure_view(strokeWidth=0)
    .interactive()
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
