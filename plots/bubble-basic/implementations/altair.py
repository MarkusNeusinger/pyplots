"""pyplots.ai
bubble-basic: Basic Bubble Chart
Library: altair 6.0.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import altair as alt
import numpy as np
import pandas as pd


# Data — tech startup metrics: funding vs revenue, sized by employees, colored by stage
np.random.seed(42)
n = 40

stages = np.random.choice(["Seed", "Series A", "Series B", "Growth"], size=n, p=[0.3, 0.3, 0.25, 0.15])

# Base funding depends on stage for realistic clustering
stage_funding = {"Seed": (5, 8), "Series A": (15, 12), "Series B": (30, 15), "Growth": (50, 20)}
funding_m = np.array([np.random.normal(*stage_funding[s]) for s in stages])
funding_m = np.clip(funding_m, 1, 80)

# Revenue correlates with funding plus noise
revenue_m = funding_m * np.random.uniform(0.6, 1.6, size=n) + np.random.normal(3, 2, size=n)
revenue_m = np.clip(revenue_m, 1, 100)

# Employees scale with funding
stage_emp = {"Seed": (15, 5), "Series A": (60, 30), "Series B": (200, 80), "Growth": (500, 200)}
employees = np.array([int(np.clip(np.random.normal(*stage_emp[s]), 10, 900)) for s in stages])

df = pd.DataFrame(
    {
        "Funding ($M)": np.round(funding_m, 1),
        "Revenue ($M)": np.round(revenue_m, 1),
        "Employees": employees,
        "Stage": pd.Categorical(stages, categories=["Seed", "Series A", "Series B", "Growth"], ordered=True),
    }
)

# Color palette starting with Python Blue
stage_colors = ["#306998", "#4B8BBE", "#FFD43B", "#E5792A"]

# Chart
chart = (
    alt.Chart(df)
    .mark_circle(opacity=0.65, stroke="white", strokeWidth=1.5)
    .encode(
        x=alt.X("Funding ($M):Q", scale=alt.Scale(domain=[0, 85]), axis=alt.Axis(gridDash=[3, 3], gridColor="#e0e0e0")),
        y=alt.Y(
            "Revenue ($M):Q", scale=alt.Scale(domain=[0, 110]), axis=alt.Axis(gridDash=[3, 3], gridColor="#e0e0e0")
        ),
        size=alt.Size(
            "Employees:Q",
            scale=alt.Scale(range=[60, 2800], domain=[10, 900]),
            legend=alt.Legend(
                titleFontSize=18,
                labelFontSize=16,
                values=[50, 200, 500, 900],
                symbolFillColor="#306998",
                symbolStrokeColor="white",
            ),
        ),
        color=alt.Color(
            "Stage:N",
            scale=alt.Scale(domain=["Seed", "Series A", "Series B", "Growth"], range=stage_colors),
            legend=alt.Legend(
                titleFontSize=18, labelFontSize=16, symbolType="circle", symbolSize=300, symbolStrokeWidth=0
            ),
        ),
        tooltip=["Stage:N", "Funding ($M):Q", "Revenue ($M):Q", "Employees:Q"],
    )
    .properties(width=1600, height=900, title="bubble-basic · altair · pyplots.ai")
    .configure_title(fontSize=28, anchor="middle", fontWeight="bold")
    .configure_axis(labelFontSize=18, titleFontSize=22, domainColor="#999999", domainWidth=0.5, tickColor="#cccccc")
    .configure_view(strokeWidth=0)
    .configure_legend(orient="right", padding=10)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
