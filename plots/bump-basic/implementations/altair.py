"""
bump-basic: Basic Bump Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data - Sports league standings over 6 matchweeks
data = {
    "Team": (
        ["Arsenal"] * 6
        + ["Chelsea"] * 6
        + ["Liverpool"] * 6
        + ["Man City"] * 6
        + ["Man United"] * 6
        + ["Tottenham"] * 6
    ),
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"] * 6,
    "Rank": [
        # Arsenal: Starts 3rd, rises to 1st, stays competitive
        3,
        2,
        1,
        1,
        2,
        1,
        # Chelsea: Mid-table consistency
        4,
        4,
        3,
        4,
        3,
        3,
        # Liverpool: Starts 1st, drops mid-season, recovers
        1,
        1,
        2,
        3,
        1,
        2,
        # Man City: Slow start, climbs steadily
        5,
        5,
        4,
        2,
        4,
        4,
        # Man United: Volatile rankings
        2,
        3,
        5,
        5,
        5,
        5,
        # Tottenham: Bottom position, occasional rise
        6,
        6,
        6,
        6,
        6,
        6,
    ],
}

df = pd.DataFrame(data)

# Define color palette (Python Blue first, then colorblind-safe colors)
colors = ["#306998", "#FFD43B", "#E15759", "#59A14F", "#9C755F", "#BAB0AC"]

# Create bump chart
lines = (
    alt.Chart(df)
    .mark_line(strokeWidth=4, opacity=0.8)
    .encode(
        x=alt.X("Week:O", title="Match Week", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y(
            "Rank:Q",
            title="League Position",
            scale=alt.Scale(domain=[1, 6], reverse=True),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickMinStep=1),
        ),
        color=alt.Color(
            "Team:N",
            title="Team",
            scale=alt.Scale(domain=df["Team"].unique().tolist(), range=colors),
            legend=alt.Legend(labelFontSize=16, titleFontSize=18),
        ),
    )
)

points = (
    alt.Chart(df)
    .mark_point(size=250, filled=True, opacity=1)
    .encode(
        x=alt.X("Week:O"),
        y=alt.Y("Rank:Q", scale=alt.Scale(domain=[1, 6], reverse=True)),
        color=alt.Color("Team:N", scale=alt.Scale(domain=df["Team"].unique().tolist(), range=colors)),
        tooltip=["Team:N", "Week:O", "Rank:Q"],
    )
)

chart = (
    (lines + points)
    .properties(width=1600, height=900, title=alt.Title("bump-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save as PNG (1600 × 900 × 3 = 4800 × 2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.interactive().save("plot.html")
