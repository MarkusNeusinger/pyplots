"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: altair 6.0.0 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
study_hours = np.random.normal(5, 1.5, 100).clip(1, 10)
exam_scores = study_hours * 8 + np.random.normal(0, 6, 100) + 30

df = pd.DataFrame({"Study Hours per Day": study_hours, "Exam Score (%)": exam_scores})

# Plot
chart = (
    alt.Chart(df)
    .mark_point(filled=True, size=150, opacity=0.7, color="#306998", stroke="white", strokeWidth=0.5)
    .encode(
        x=alt.X("Study Hours per Day:Q", scale=alt.Scale(zero=False)),
        y=alt.Y("Exam Score (%):Q", scale=alt.Scale(zero=False)),
        tooltip=["Study Hours per Day:Q", "Exam Score (%):Q"],
    )
    .properties(width=1600, height=900, title=alt.Title("scatter-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.2)
    .configure_view(strokeWidth=0)
    .interactive()
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
