""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: altair 6.0.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import altair as alt
import numpy as np
import pandas as pd


# Data — tech startup metrics: funding vs revenue with employee count as bubble size
np.random.seed(42)
n = 40

funding_m = np.random.lognormal(mean=2.5, sigma=0.8, size=n)
revenue_m = funding_m * np.random.uniform(0.3, 1.8, size=n) + np.random.exponential(2, size=n)
employees = np.clip(funding_m * np.random.uniform(8, 25, size=n), 20, 800).astype(int)

df = pd.DataFrame(
    {"Funding ($M)": np.round(funding_m, 1), "Revenue ($M)": np.round(revenue_m, 1), "Employees": employees}
)

# Chart
chart = (
    alt.Chart(df)
    .mark_circle(opacity=0.6, color="#306998", stroke="white", strokeWidth=0.5)
    .encode(
        x=alt.X("Funding ($M):Q", scale=alt.Scale(zero=False)),
        y=alt.Y("Revenue ($M):Q", scale=alt.Scale(zero=False)),
        size=alt.Size(
            "Employees:Q", scale=alt.Scale(range=[80, 2500]), legend=alt.Legend(titleFontSize=18, labelFontSize=16)
        ),
        tooltip=["Funding ($M):Q", "Revenue ($M):Q", "Employees:Q"],
    )
    .properties(width=1600, height=900, title="bubble-basic · altair · pyplots.ai")
    .configure_title(fontSize=28, anchor="middle")
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.2)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
