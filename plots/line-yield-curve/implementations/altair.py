""" pyplots.ai
line-yield-curve: Yield Curve (Interest Rate Term Structure)
Library: altair 6.0.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-14
"""

import altair as alt
import pandas as pd


# Data - U.S. Treasury yield curves on three dates showing normal, flat, and inverted shapes
maturities = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
maturity_years = [1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]

# Jan 2022 - Normal upward-sloping curve (pre-tightening)
yields_normal = [0.08, 0.21, 0.47, 0.78, 1.18, 1.42, 1.63, 1.78, 1.78, 2.11, 2.07]

# Jul 2023 - Inverted curve (peak inversion)
yields_inverted = [5.40, 5.49, 5.52, 5.40, 4.87, 4.56, 4.18, 4.06, 3.96, 4.22, 4.03]

# Jan 2025 - Normalizing curve (post-pivot)
yields_normalizing = [4.34, 4.35, 4.30, 4.16, 4.20, 4.25, 4.38, 4.49, 4.58, 4.87, 4.81]

records = []
for i, mat in enumerate(maturities):
    records.append(
        {
            "maturity": mat,
            "maturity_years": maturity_years[i],
            "yield_pct": yields_normal[i],
            "date": "Jan 2022 (Normal)",
        }
    )
    records.append(
        {
            "maturity": mat,
            "maturity_years": maturity_years[i],
            "yield_pct": yields_inverted[i],
            "date": "Jul 2023 (Inverted)",
        }
    )
    records.append(
        {
            "maturity": mat,
            "maturity_years": maturity_years[i],
            "yield_pct": yields_normalizing[i],
            "date": "Jan 2025 (Normalizing)",
        }
    )

df = pd.DataFrame(records)

# Color palette - professional finance style
colors = ["#306998", "#E15759", "#59A14F"]

# Plot - line chart with points
line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4)
    .encode(
        x=alt.X(
            "maturity_years:Q",
            title="Maturity (Years)",
            scale=alt.Scale(type="log", domain=[0.08, 35]),
            axis=alt.Axis(
                labelFontSize=18,
                titleFontSize=22,
                values=[1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30],
                labelExpr="datum.value < 0.09 ? '1M' : datum.value < 0.3 ? '3M' : datum.value < 0.6 ? '6M' : datum.value + 'Y'",
            ),
        ),
        y=alt.Y(
            "yield_pct:Q",
            title="Yield (%)",
            scale=alt.Scale(domain=[0, 6]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
        color=alt.Color(
            "date:N",
            scale=alt.Scale(range=colors),
            legend=alt.Legend(
                title=None, labelFontSize=18, labelLimit=300, orient="top-right", symbolStrokeWidth=4, symbolSize=200
            ),
        ),
        tooltip=["maturity:N", "yield_pct:Q", "date:N"],
        order="maturity_years:Q",
    )
)

points = (
    alt.Chart(df)
    .mark_point(size=150, filled=True)
    .encode(
        x="maturity_years:Q",
        y="yield_pct:Q",
        color=alt.Color("date:N", scale=alt.Scale(range=colors), legend=None),
        tooltip=["maturity:N", "yield_pct:Q", "date:N"],
    )
)

chart = (
    (line + points)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "U.S. Treasury Yield Curves · line-yield-curve · altair · pyplots.ai", fontSize=28, anchor="middle"
        ),
    )
    .configure_axis(gridOpacity=0.2, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.interactive().save("plot.html")
