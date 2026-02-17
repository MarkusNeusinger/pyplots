"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: altair | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import altair as alt
import numpy as np
import pandas as pd
from scipy import stats


# Data - Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
good_scores = np.random.normal(loc=620, scale=80, size=300)
bad_scores = np.random.normal(loc=480, scale=90, size=300)

# Compute ECDFs
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# K-S test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Find the point of maximum divergence
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_ecdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_ecdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
diffs = np.abs(good_ecdf_at_all - bad_ecdf_at_all)
max_idx = np.argmax(diffs)
ks_x = all_values[max_idx]
ks_y_good = good_ecdf_at_all[max_idx]
ks_y_bad = bad_ecdf_at_all[max_idx]

# ECDF DataFrames
good_df = pd.DataFrame({"Score": good_sorted, "ECDF": good_ecdf, "Group": "Good Customers"})
bad_df = pd.DataFrame({"Score": bad_sorted, "ECDF": bad_ecdf, "Group": "Bad Customers"})
ecdf_df = pd.concat([good_df, bad_df], ignore_index=True)

# K-S distance line
ks_line_df = pd.DataFrame({"Score": [ks_x, ks_x], "ECDF": [ks_y_bad, ks_y_good]})

# K-S annotation point (midpoint of the distance line)
ks_mid_y = (ks_y_good + ks_y_bad) / 2
ks_label_df = pd.DataFrame({"Score": [ks_x + 15], "ECDF": [ks_mid_y], "label": [f"D = {ks_stat:.3f}"]})

# ECDF step lines
color_scale = alt.Scale(domain=["Good Customers", "Bad Customers"], range=["#306998", "#E8833A"])

ecdf_lines = (
    alt.Chart(ecdf_df)
    .mark_line(interpolate="step-after", strokeWidth=3)
    .encode(
        x=alt.X("Score:Q", title="Credit Score"),
        y=alt.Y("ECDF:Q", title="Cumulative Proportion", scale=alt.Scale(domain=[0, 1])),
        color=alt.Color("Group:N", scale=color_scale, title=""),
        tooltip=["Group:N", "Score:Q", "ECDF:Q"],
    )
)

# K-S distance vertical line
ks_distance = (
    alt.Chart(ks_line_df).mark_line(color="#D62728", strokeWidth=3.5, strokeDash=[6, 4]).encode(x="Score:Q", y="ECDF:Q")
)

# K-S statistic label
ks_label = (
    alt.Chart(ks_label_df)
    .mark_text(align="left", fontSize=20, fontWeight="bold", color="#D62728")
    .encode(x="Score:Q", y="ECDF:Q", text="label:N")
)

# P-value subtitle
p_text = "p < 0.001" if p_value < 0.001 else f"p = {p_value:.4f}"
subtitle_text = f"K-S Statistic: {ks_stat:.3f} | {p_text}"

# Combine layers
chart = (
    alt.layer(ecdf_lines, ks_distance, ks_label)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "ks-test-comparison · altair · pyplots.ai", subtitle=subtitle_text, fontSize=28, subtitleFontSize=20
        ),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.2)
    .configure_legend(titleFontSize=18, labelFontSize=18, symbolSize=300, symbolStrokeWidth=3, orient="top-right")
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
