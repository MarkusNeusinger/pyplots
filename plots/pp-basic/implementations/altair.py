"""pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: altair 6.0.0 | Python 3.14.3
"""

from statistics import NormalDist

import altair as alt
import numpy as np
import pandas as pd


# Data — clinical trial: blood pressure measurements vs normal reference
np.random.seed(42)
observed = np.concatenate([np.random.normal(50, 10, 160), np.random.exponential(5, 40) + 55])
observed_sorted = np.sort(observed)
n = len(observed_sorted)

mu = float(observed_sorted.mean())
sigma = float(observed_sorted.std())
dist = NormalDist(mu, sigma)
empirical_cdf = np.arange(1, n + 1) / (n + 1)
theoretical_cdf = np.array([dist.cdf(x) for x in observed_sorted])
deviation = np.abs(empirical_cdf - theoretical_cdf)

df = pd.DataFrame({"Theoretical CDF (Normal)": theoretical_cdf, "Empirical CDF": empirical_cdf, "Deviation": deviation})

ref_df = pd.DataFrame({"x": [0, 1], "y": [0, 1]})

# Confidence band around diagonal (± ~1.36/√n Kolmogorov-Smirnov bound)
ks_bound = 1.36 / np.sqrt(n)
band_x = np.linspace(0, 1, 50)
band_df = pd.DataFrame(
    {"x": band_x, "y_lo": np.clip(band_x - ks_bound, 0, 1), "y_hi": np.clip(band_x + ks_bound, 0, 1)}
)

# Plot
band = (
    alt.Chart(band_df).mark_area(opacity=0.08, color="#306998").encode(x=alt.X("x:Q"), y=alt.Y("y_lo:Q"), y2="y_hi:Q")
)

reference_line = (
    alt.Chart(ref_df).mark_line(strokeDash=[8, 6], strokeWidth=2.5, color="#999999").encode(x="x:Q", y="y:Q")
)

points = (
    alt.Chart(df)
    .mark_circle(stroke="#1a3a5c", strokeWidth=0.8)
    .encode(
        x=alt.X("Theoretical CDF (Normal):Q", scale=alt.Scale(domain=[0, 1]), title="Theoretical CDF (Normal)"),
        y=alt.Y("Empirical CDF:Q", scale=alt.Scale(domain=[0, 1]), title="Empirical CDF"),
        color=alt.Color(
            "Deviation:Q",
            scale=alt.Scale(scheme="blues", domain=[0, float(deviation.max())]),
            legend=alt.Legend(
                title="Deviation",
                titleFontSize=16,
                labelFontSize=14,
                orient="bottom-right",
                direction="vertical",
                gradientLength=150,
            ),
        ),
        size=alt.Size("Deviation:Q", scale=alt.Scale(range=[60, 220]), legend=None),
        opacity=alt.value(0.8),
        tooltip=[
            alt.Tooltip("Theoretical CDF (Normal):Q", format=".3f"),
            alt.Tooltip("Empirical CDF:Q", format=".3f"),
            alt.Tooltip("Deviation:Q", format=".4f", title="Abs. Deviation"),
        ],
    )
)

chart = (
    (band + reference_line + points)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title(
            "pp-basic · altair · pyplots.ai",
            fontSize=28,
            fontWeight="bold",
            subtitle="Normality check — points colored by deviation from perfect fit",
            subtitleFontSize=18,
            subtitleColor="#666666",
        ),
    )
    .configure_axis(
        labelFontSize=18,
        titleFontSize=22,
        titleColor="#333333",
        labelColor="#555555",
        grid=True,
        gridOpacity=0.15,
        gridColor="#cccccc",
        domainColor="#888888",
        tickColor="#888888",
    )
    .configure_view(strokeWidth=0)
    .configure_legend(strokeColor="#dddddd", padding=10, cornerRadius=4, fillColor="#fafafa")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
