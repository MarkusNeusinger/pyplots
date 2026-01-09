"""pyplots.ai
scatter-text: Scatter Plot with Text Labels Instead of Points
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Programming languages positioned by popularity vs age
np.random.seed(42)

languages = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "Ruby",
    "Go",
    "Rust",
    "Swift",
    "Kotlin",
    "TypeScript",
    "Scala",
    "R",
    "Julia",
    "Perl",
    "PHP",
    "C#",
    "Haskell",
    "Elixir",
    "Clojure",
    "Dart",
    "Lua",
    "MATLAB",
    "Fortran",
    "COBOL",
    "Lisp",
    "Erlang",
    "F#",
    "Groovy",
    "Crystal",
    "Nim",
]

# Simulated: x = language age (years), y = relative popularity score
ages = np.array(
    [
        33,
        29,
        29,
        41,
        29,
        15,
        13,
        10,
        13,
        12,
        20,
        31,
        12,
        37,
        30,
        24,
        34,
        13,
        17,
        13,
        31,
        40,
        68,
        65,
        66,
        38,
        19,
        21,
        10,
        15,
    ]
)
popularity = np.array(
    [95, 97, 85, 70, 45, 65, 55, 60, 52, 75, 35, 48, 30, 20, 55, 68, 15, 18, 12, 28, 25, 40, 10, 5, 8, 14, 20, 22, 8, 6]
)

# Add some jitter to avoid overlap
ages = ages + np.random.uniform(-1, 1, len(ages))
popularity = popularity + np.random.uniform(-2, 2, len(ages))

df = pd.DataFrame({"Age (Years)": ages, "Popularity Score": popularity, "Language": languages})

# Create scatter text plot using mark_text
chart = (
    alt.Chart(df)
    .mark_text(fontSize=16, fontWeight="bold")
    .encode(
        x=alt.X("Age (Years):Q", title="Language Age (Years Since Creation)", scale=alt.Scale(domain=[0, 75])),
        y=alt.Y("Popularity Score:Q", title="Relative Popularity Score", scale=alt.Scale(domain=[0, 105])),
        text="Language:N",
        color=alt.Color("Popularity Score:Q", scale=alt.Scale(scheme="viridis"), legend=alt.Legend(title="Popularity")),
    )
    .properties(
        width=1600, height=900, title=alt.Title(text="scatter-text · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=18, labelFontSize=16)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
