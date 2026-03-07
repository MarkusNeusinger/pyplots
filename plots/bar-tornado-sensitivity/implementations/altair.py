"""pyplots.ai
bar-tornado-sensitivity: Tornado Diagram for Sensitivity Analysis
Library: altair 6.0.0 | Python 3.14.3
Quality: 78/100 | Created: 2026-03-07
"""

import altair as alt
import pandas as pd


# Data - NPV sensitivity analysis for a capital investment project
base_npv = 250.0  # Base case NPV in $M

parameters = [
    ("Discount Rate", 195.0, 320.0),
    ("Revenue Growth", 200.0, 310.0),
    ("Operating Costs", 210.0, 305.0),
    ("Terminal Value", 215.0, 295.0),
    ("CapEx Estimate", 218.0, 288.0),
    ("Tax Rate", 225.0, 280.0),
    ("Working Capital", 232.0, 272.0),
    ("Inflation Rate", 238.0, 265.0),
]

records = []
for param, low, high in parameters:
    span = abs(high - low)
    records.append({"parameter": param, "value": low, "side": "Low Scenario", "span": span, "base": base_npv})
    records.append({"parameter": param, "value": high, "side": "High Scenario", "span": span, "base": base_npv})

df = pd.DataFrame(records)

# Sort by span descending — widest at top means highest sort_rank at top
y_sort = alt.EncodingSortField(field="span", order="descending")

# Bars
bars = (
    alt.Chart(df)
    .mark_bar(cornerRadius=3, height=38)
    .encode(
        x=alt.X("value:Q", title="Net Present Value ($M)", scale=alt.Scale(domain=[185, 325])),
        x2="base:Q",
        y=alt.Y("parameter:N", sort=y_sort, title=None, axis=alt.Axis(grid=False)),
        color=alt.Color(
            "side:N",
            scale=alt.Scale(domain=["Low Scenario", "High Scenario"], range=["#306998", "#E8853A"]),
            title=None,
        ),
        tooltip=[
            alt.Tooltip("parameter:N", title="Parameter"),
            alt.Tooltip("side:N", title="Scenario"),
            alt.Tooltip("value:Q", title="NPV ($M)", format=",.0f"),
        ],
    )
)

# Value labels — low scenario (left side)
low_labels = (
    alt.Chart(df)
    .transform_filter(alt.datum.side == "Low Scenario")
    .mark_text(fontSize=14, fontWeight="bold", dx=-18, align="right", color="#306998")
    .encode(x="value:Q", y=alt.Y("parameter:N", sort=y_sort), text=alt.Text("value:Q", format="$,.0f"))
)

# Value labels — high scenario (right side)
high_labels = (
    alt.Chart(df)
    .transform_filter(alt.datum.side == "High Scenario")
    .mark_text(fontSize=14, fontWeight="bold", dx=18, align="left", color="#C06A2B")
    .encode(x="value:Q", y=alt.Y("parameter:N", sort=y_sort), text=alt.Text("value:Q", format="$,.0f"))
)

# Base case reference line
rule = (
    alt.Chart(pd.DataFrame({"x": [base_npv]}))
    .mark_rule(strokeDash=[6, 4], strokeWidth=2, color="#333333")
    .encode(x="x:Q")
)

# Base case label anchored to top parameter
sort_order = [p for p, _, _ in sorted(parameters, key=lambda x: abs(x[2] - x[1]), reverse=True)]
base_label_df = pd.DataFrame(
    {
        "x": [base_npv],
        "y": [sort_order[0]],
        "label": [f"Base Case: ${base_npv:.0f}M"],
        "span": [max(abs(high - low) for _, low, high in parameters)],
    }
)
label = (
    alt.Chart(base_label_df)
    .mark_text(align="left", dx=8, dy=-28, fontSize=16, fontWeight="bold", color="#333333")
    .encode(x="x:Q", y=alt.Y("y:N", sort=y_sort), text="label:N")
)

chart = (
    (bars + low_labels + high_labels + rule + label)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("bar-tornado-sensitivity \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="start"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridColor="#e8e8e8", gridDash=[3, 3])
    .configure_legend(labelFontSize=16, symbolSize=300, orient="bottom", direction="horizontal")
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
