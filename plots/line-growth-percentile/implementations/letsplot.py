""" pyplots.ai
line-growth-percentile: Pediatric Growth Chart with Percentile Curves
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-19
"""
# ruff: noqa: F405

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403, F405


LetsPlot.setup_html()

# Data - WHO-style weight-for-age reference for boys (0-36 months)
np.random.seed(42)
age_months = np.arange(0, 37, 1)
n = len(age_months)

# WHO-approximated weight-for-age 50th percentile for boys 0-36 months (kg)
# Key reference points: ~3.3kg at birth, ~10.2kg at 12mo, ~12.2kg at 24mo, ~14.3kg at 36mo
percentile_50 = 3.3 + 3.8 * np.log1p(age_months * 0.6)

# Spread increases with age (SD widens)
spread = 0.25 + 0.03 * age_months
percentile_3 = percentile_50 - 1.88 * spread
percentile_10 = percentile_50 - 1.28 * spread
percentile_25 = percentile_50 - 0.67 * spread
percentile_75 = percentile_50 + 0.67 * spread
percentile_90 = percentile_50 + 1.28 * spread
percentile_97 = percentile_50 + 1.88 * spread

# Individual patient data - a healthy boy tracking around 55th-65th percentile
patient_ages = np.array([0, 1, 2, 4, 6, 9, 12, 15, 18, 24, 30, 36])
patient_weights = np.array([3.5, 4.5, 5.6, 7.0, 7.9, 9.2, 10.2, 10.9, 11.5, 12.7, 13.8, 14.8])

# Build percentile band dataframes
df_bands = pd.DataFrame(
    {
        "age": age_months,
        "p3": percentile_3,
        "p10": percentile_10,
        "p25": percentile_25,
        "p50": percentile_50,
        "p75": percentile_75,
        "p90": percentile_90,
        "p97": percentile_97,
    }
)

# Patient data
df_patient = pd.DataFrame({"age": patient_ages, "weight": patient_weights})

# Percentile label data (at right edge of chart)
label_age = 36.5
df_labels = pd.DataFrame(
    {
        "age": [label_age] * 7,
        "weight": [
            percentile_3[-1],
            percentile_10[-1],
            percentile_25[-1],
            percentile_50[-1],
            percentile_75[-1],
            percentile_90[-1],
            percentile_97[-1],
        ],
        "label": ["P3", "P10", "P25", "P50", "P75", "P90", "P97"],
    }
)

# Blue-toned palette for boys (graduated: darker at extremes, lighter near median)
blue_outer = "#1A4C7A"
blue_mid = "#4A8DBF"
blue_inner = "#A3C9E8"

# Plot
plot = (
    ggplot()
    # Outermost band: P3-P10 and P90-P97
    + geom_ribbon(aes(x="age", ymin="p3", ymax="p10"), data=df_bands, fill=blue_outer, alpha=0.35)
    + geom_ribbon(aes(x="age", ymin="p90", ymax="p97"), data=df_bands, fill=blue_outer, alpha=0.35)
    # Middle band: P10-P25 and P75-P90
    + geom_ribbon(aes(x="age", ymin="p10", ymax="p25"), data=df_bands, fill=blue_mid, alpha=0.3)
    + geom_ribbon(aes(x="age", ymin="p75", ymax="p90"), data=df_bands, fill=blue_mid, alpha=0.3)
    # Inner band: P25-P75
    + geom_ribbon(aes(x="age", ymin="p25", ymax="p75"), data=df_bands, fill=blue_inner, alpha=0.3)
    # Percentile lines
    + geom_line(aes(x="age", y="p3"), data=df_bands, color=blue_outer, size=0.5, alpha=0.6)
    + geom_line(aes(x="age", y="p10"), data=df_bands, color=blue_mid, size=0.5, alpha=0.6)
    + geom_line(aes(x="age", y="p25"), data=df_bands, color=blue_inner, size=0.5, alpha=0.6)
    + geom_line(aes(x="age", y="p50"), data=df_bands, color="#306998", size=1.8)
    + geom_line(aes(x="age", y="p75"), data=df_bands, color=blue_inner, size=0.5, alpha=0.6)
    + geom_line(aes(x="age", y="p90"), data=df_bands, color=blue_mid, size=0.5, alpha=0.6)
    + geom_line(aes(x="age", y="p97"), data=df_bands, color=blue_outer, size=0.5, alpha=0.6)
    # Patient trajectory
    + geom_line(aes(x="age", y="weight"), data=df_patient, color="#E63946", size=1.5)
    + geom_point(aes(x="age", y="weight"), data=df_patient, color="#E63946", size=4, fill="#E63946", shape=21)
    # Percentile labels on right margin
    + geom_text(aes(x="age", y="weight", label="label"), data=df_labels, size=10, color="#555555", hjust=0)
    # Scales and labels
    + scale_x_continuous(breaks=list(range(0, 37, 6)), labels=[str(m) for m in range(0, 37, 6)], limits=[0, 39])
    + labs(
        title="Boys Weight-for-Age · line-growth-percentile · letsplot · pyplots.ai", x="Age (months)", y="Weight (kg)"
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_position="none",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
