"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import altair as alt
import pandas as pd


# Data - KPI metrics with actual values, targets, and qualitative range thresholds
# Each metric shows: current performance, target goal, and bands for poor/satisfactory/good
metrics = [
    {"metric": "Revenue ($K)", "actual": 275, "target": 250, "poor": 150, "satisfactory": 200, "good": 300},
    {"metric": "Profit ($K)", "actual": 85, "target": 100, "poor": 50, "satisfactory": 75, "good": 125},
    {"metric": "New Customers", "actual": 320, "target": 300, "poor": 200, "satisfactory": 275, "good": 350},
    {"metric": "Satisfaction (1-5)", "actual": 4.2, "target": 4.5, "poor": 3.0, "satisfactory": 4.0, "good": 5.0},
]

# Normalize all values to percentage of maximum (good value) for common scale
range_data = []
for m in metrics:
    max_val = m["good"]
    poor_pct = (m["poor"] / max_val) * 100
    sat_pct = (m["satisfactory"] / max_val) * 100
    # Build qualitative bands: Poor (0 to poor), Satisfactory (poor to sat), Good (sat to 100%)
    range_data.append({"metric": m["metric"], "range_start": 0, "range_end": poor_pct, "band": "Poor"})
    range_data.append({"metric": m["metric"], "range_start": poor_pct, "range_end": sat_pct, "band": "Satisfactory"})
    range_data.append({"metric": m["metric"], "range_start": sat_pct, "range_end": 100, "band": "Good"})

df_ranges = pd.DataFrame(range_data)

# Build dataframe for actual values (normalized to percentage)
df_actual = pd.DataFrame([{"metric": m["metric"], "actual": (m["actual"] / m["good"]) * 100} for m in metrics])

# Build dataframe for target markers (normalized to percentage)
df_target = pd.DataFrame([{"metric": m["metric"], "target": (m["target"] / m["good"]) * 100} for m in metrics])

# Background qualitative ranges (grayscale bands as per specification)
ranges_chart = (
    alt.Chart(df_ranges)
    .mark_bar(height=55)
    .encode(
        y=alt.Y("metric:N", title=None, sort=[m["metric"] for m in metrics]),
        x=alt.X("range_start:Q", title="% of Maximum", scale=alt.Scale(domain=[0, 110])),
        x2=alt.X2("range_end:Q"),
        color=alt.Color(
            "band:N",
            scale=alt.Scale(domain=["Poor", "Satisfactory", "Good"], range=["#d9d9d9", "#bdbdbd", "#969696"]),
            legend=alt.Legend(title="Performance Band", orient="bottom", titleFontSize=18, labelFontSize=16),
        ),
    )
)

# Actual value bar (Python Blue - primary measure)
actual_chart = (
    alt.Chart(df_actual)
    .mark_bar(color="#306998", height=22)
    .encode(
        y=alt.Y("metric:N", title=None, sort=[m["metric"] for m in metrics]),
        x=alt.X("actual:Q", title="% of Maximum", scale=alt.Scale(domain=[0, 110])),
    )
)

# Target marker (thin black vertical line perpendicular to bar)
target_chart = (
    alt.Chart(df_target)
    .mark_tick(color="black", thickness=4, size=55)
    .encode(
        y=alt.Y("metric:N", title=None, sort=[m["metric"] for m in metrics]),
        x=alt.X("target:Q", title="% of Maximum", scale=alt.Scale(domain=[0, 110])),
    )
)

# Layer all components: ranges (background), actual bar, target marker
chart = (
    alt.layer(ranges_chart, actual_chart, target_chart)
    .properties(
        width=1400, height=700, title=alt.Title("bullet-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
