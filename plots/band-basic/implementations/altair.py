""" pyplots.ai
band-basic: Basic Band Plot
Library: altair 6.0.0 | Python 3.14
Quality: 88/100 | Updated: 2026-02-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_center = 2 * np.sin(x) + 0.5 * x  # Central trend (sinusoidal + linear growth)

# Confidence band widens over time (realistic uncertainty growth)
uncertainty = 0.5 + 0.15 * x
y_lower = y_center - 1.96 * uncertainty
y_upper = y_center + 1.96 * uncertainty
y_inner_lower = y_center - 0.674 * uncertainty  # 50% CI inner band
y_inner_upper = y_center + 0.674 * uncertainty

df = pd.DataFrame(
    {
        "x": x,
        "y_center": y_center,
        "y_lower": y_lower,
        "y_upper": y_upper,
        "y_inner_lower": y_inner_lower,
        "y_inner_upper": y_inner_upper,
    }
)

# Nearest-point selection for interactive HTML export
nearest = alt.selection_point(nearest=True, on="pointerover", fields=["x"], empty=False)

# 95% confidence band (outer, lighter)
band_outer = (
    alt.Chart(df)
    .mark_area(opacity=0.2, color="#306998", interpolate="monotone")
    .encode(
        x=alt.X("x:Q", title="Time (s)"), y=alt.Y("y_lower:Q", title="Signal Amplitude (mV)"), y2=alt.Y2("y_upper:Q")
    )
)

# 50% confidence band (inner, creates gradient depth)
band_inner = (
    alt.Chart(df)
    .mark_area(opacity=0.2, color="#306998", interpolate="monotone")
    .encode(x="x:Q", y="y_inner_lower:Q", y2="y_inner_upper:Q")
)

# Central trend line (darker navy for strong contrast)
line = alt.Chart(df).mark_line(strokeWidth=2.5, color="#1a3a5c", interpolate="monotone").encode(x="x:Q", y="y_center:Q")

# Interactive tooltip points (visible only on hover in HTML)
tooltip_points = (
    alt.Chart(df)
    .mark_point(color="#1a3a5c", size=80)
    .encode(
        x="x:Q",
        y="y_center:Q",
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=[
            alt.Tooltip("x:Q", title="Time (s)", format=".1f"),
            alt.Tooltip("y_center:Q", title="Signal (mV)", format=".2f"),
            alt.Tooltip("y_lower:Q", title="95% CI Lower", format=".2f"),
            alt.Tooltip("y_upper:Q", title="95% CI Upper", format=".2f"),
        ],
    )
    .add_params(nearest)
)

# Vertical guide rule (visible only on hover in HTML)
guide_rule = (
    alt.Chart(df)
    .mark_rule(color="#999999", strokeDash=[4, 4])
    .encode(x="x:Q", opacity=alt.condition(nearest, alt.value(0.5), alt.value(0)))
)

# Combine layers
chart = (
    (band_outer + band_inner + line + tooltip_points + guide_rule)
    .properties(width=1600, height=900, title=alt.Title("band-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.2)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
