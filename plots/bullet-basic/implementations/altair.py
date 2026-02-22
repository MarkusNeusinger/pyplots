"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: altair 6.0.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-22
"""

import altair as alt
import pandas as pd


# Data - KPI metrics with actual values, targets, and qualitative range thresholds
metrics = [
    {"metric": "Revenue ($K)", "actual": 275, "target": 250, "poor": 150, "satisfactory": 200, "good": 300},
    {"metric": "Profit ($K)", "actual": 85, "target": 100, "poor": 50, "satisfactory": 75, "good": 125},
    {"metric": "New Customers", "actual": 320, "target": 300, "poor": 200, "satisfactory": 275, "good": 350},
    {"metric": "Satisfaction", "actual": 4.2, "target": 4.5, "poor": 3.0, "satisfactory": 4.0, "good": 5.0},
]
metric_order = [m["metric"] for m in metrics]

# Normalize to percentage of maximum and build dataframes
range_data = []
for m in metrics:
    max_val = m["good"]
    poor_pct = (m["poor"] / max_val) * 100
    sat_pct = (m["satisfactory"] / max_val) * 100
    range_data.append({"metric": m["metric"], "start": 0, "end": poor_pct, "band": "Poor"})
    range_data.append({"metric": m["metric"], "start": poor_pct, "end": sat_pct, "band": "Satisfactory"})
    range_data.append({"metric": m["metric"], "start": sat_pct, "end": 100, "band": "Good"})

df_ranges = pd.DataFrame(range_data)

df_actual = pd.DataFrame(
    [{"metric": m["metric"], "actual_pct": (m["actual"] / m["good"]) * 100, "actual_raw": m["actual"]} for m in metrics]
)

df_target = pd.DataFrame(
    [{"metric": m["metric"], "target_pct": (m["target"] / m["good"]) * 100, "target_raw": m["target"]} for m in metrics]
)

# Background qualitative ranges (grayscale bands)
ranges_chart = (
    alt.Chart(df_ranges)
    .mark_bar(height=50)
    .encode(
        y=alt.Y("metric:N", title=None, sort=metric_order, axis=alt.Axis(labelFontSize=18)),
        x=alt.X(
            "start:Q",
            title="Performance (% of Goal)",
            scale=alt.Scale(domain=[0, 105]),
            axis=alt.Axis(titleFontSize=22, labelFontSize=16, tickCount=6),
        ),
        x2="end:Q",
        color=alt.Color(
            "band:N",
            scale=alt.Scale(domain=["Poor", "Satisfactory", "Good"], range=["#e0e0e0", "#c0c0c0", "#9e9e9e"]),
            legend=alt.Legend(
                title="Performance Band", orient="bottom", titleFontSize=18, labelFontSize=16, direction="horizontal"
            ),
        ),
        tooltip=[alt.Tooltip("metric:N", title="Metric"), alt.Tooltip("band:N", title="Band")],
    )
)

# Actual value bar (Python Blue)
actual_chart = (
    alt.Chart(df_actual)
    .mark_bar(color="#306998", height=20)
    .encode(
        y=alt.Y("metric:N", sort=metric_order),
        x=alt.X("actual_pct:Q"),
        tooltip=[
            alt.Tooltip("metric:N", title="Metric"),
            alt.Tooltip("actual_raw:Q", title="Actual"),
            alt.Tooltip("actual_pct:Q", title="% of Goal", format=".1f"),
        ],
    )
)

# Target marker (thin black vertical tick)
target_chart = (
    alt.Chart(df_target)
    .mark_tick(color="#222222", thickness=4, size=50)
    .encode(
        y=alt.Y("metric:N", sort=metric_order),
        x=alt.X("target_pct:Q"),
        tooltip=[alt.Tooltip("metric:N", title="Metric"), alt.Tooltip("target_raw:Q", title="Target")],
    )
)

# Actual value text labels on bars
value_labels = (
    alt.Chart(df_actual)
    .mark_text(align="left", dx=6, fontSize=16, fontWeight="bold", color="#1a3a5c")
    .encode(y=alt.Y("metric:N", sort=metric_order), x=alt.X("actual_pct:Q"), text=alt.Text("actual_raw:Q"))
)

# Layer all components and configure
chart = (
    alt.layer(ranges_chart, actual_chart, target_chart, value_labels)
    .properties(
        width=1400, height=400, title=alt.Title("bullet-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
