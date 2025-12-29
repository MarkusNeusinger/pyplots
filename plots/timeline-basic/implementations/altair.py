""" pyplots.ai
timeline-basic: Event Timeline
Library: altair 6.0.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-29
"""

import altair as alt
import pandas as pd


# Data: Software project milestones
data = pd.DataFrame(
    {
        "date": pd.to_datetime(
            [
                "2024-01-15",
                "2024-02-20",
                "2024-03-10",
                "2024-04-05",
                "2024-05-01",
                "2024-06-15",
                "2024-07-20",
                "2024-08-30",
                "2024-09-15",
                "2024-10-25",
                "2024-11-10",
                "2024-12-01",
            ]
        ),
        "event": [
            "Project Kickoff",
            "Requirements Complete",
            "Design Review",
            "Development Start",
            "Alpha Release",
            "Beta Testing",
            "Security Audit",
            "Performance Testing",
            "User Acceptance",
            "Release Candidate",
            "Documentation",
            "Production Launch",
        ],
        "category": [
            "Planning",
            "Planning",
            "Planning",
            "Development",
            "Development",
            "Testing",
            "Testing",
            "Testing",
            "Testing",
            "Release",
            "Release",
            "Release",
        ],
    }
)

# Alternate label positions to prevent overlap (above/below axis)
data["y_offset"] = [1.5 if i % 2 == 0 else -1.5 for i in range(len(data))]
data["y_zero"] = 0
data["y_label"] = [2.3 if i % 2 == 0 else -2.3 for i in range(len(data))]

# Color palette for categories (Python Blue and complementary colors)
category_colors = {"Planning": "#306998", "Development": "#FFD43B", "Testing": "#4ECDC4", "Release": "#E8575A"}

# Shared y scale
y_scale = alt.Scale(domain=[-3.5, 3.5])

# Color scale for consistency
color_scale = alt.Scale(domain=list(category_colors.keys()), range=list(category_colors.values()))

# Vertical connector lines from axis to points
connectors = (
    alt.Chart(data)
    .mark_rule(strokeWidth=3, opacity=0.7)
    .encode(
        x="date:T",
        y=alt.Y("y_zero:Q", scale=y_scale),
        y2="y_offset:Q",
        color=alt.Color("category:N", scale=color_scale, legend=None),
    )
)

# Event markers on the timeline
points = (
    alt.Chart(data)
    .mark_circle(size=600, stroke="white", strokeWidth=3)
    .encode(
        x=alt.X(
            "date:T",
            axis=alt.Axis(title="Date", format="%b %Y", labelFontSize=18, titleFontSize=22, labelAngle=-45, grid=False),
        ),
        y=alt.Y("y_offset:Q", scale=y_scale),
        color=alt.Color(
            "category:N",
            scale=color_scale,
            legend=alt.Legend(
                title="Phase",
                titleFontSize=20,
                labelFontSize=18,
                orient="top-right",
                direction="vertical",
                symbolSize=400,
            ),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%B %d, %Y"),
            alt.Tooltip("event:N", title="Event"),
            alt.Tooltip("category:N", title="Phase"),
        ],
    )
)

# Central timeline axis line using rule from min to max date
timeline_line = alt.Chart(data).mark_rule(color="#666666", strokeWidth=4).encode(y=alt.Y("y_zero:Q", scale=y_scale))

# Event labels positioned above/below points
labels = (
    alt.Chart(data)
    .mark_text(align="center", fontSize=16, fontWeight="bold")
    .encode(x="date:T", y=alt.Y("y_label:Q", scale=y_scale), text="event:N", color=alt.value("#333333"))
)

# Combine all layers
chart = (
    (timeline_line + connectors + points + labels)
    .properties(
        width=1600, height=900, title=alt.Title("timeline-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_view(strokeWidth=0)
    .configure_axisY(disable=True)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
