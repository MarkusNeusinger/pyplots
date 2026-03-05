"""pyplots.ai
histogram-epidemic: Epidemic Curve (Epi Curve)
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-03-05
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_col,
    geom_text,
    geom_vline,
    ggplot,
    labs,
    scale_fill_manual,
    scale_x_date,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)

start_date = pd.Timestamp("2024-01-15")
dates = pd.date_range(start_date, periods=90, freq="D")

# Simulate a point-source outbreak with propagated secondary wave
days = np.arange(90)
confirmed_rate = (
    45 * np.exp(-0.5 * ((days - 18) / 5) ** 2) + 25 * np.exp(-0.5 * ((days - 55) / 10) ** 2) + np.random.poisson(2, 90)
)
probable_rate = (
    15 * np.exp(-0.5 * ((days - 20) / 6) ** 2) + 10 * np.exp(-0.5 * ((days - 57) / 11) ** 2) + np.random.poisson(1, 90)
)
suspect_rate = (
    8 * np.exp(-0.5 * ((days - 22) / 7) ** 2) + 5 * np.exp(-0.5 * ((days - 60) / 12) ** 2) + np.random.poisson(1, 90)
)

confirmed = np.maximum(confirmed_rate.astype(int), 0)
probable = np.maximum(probable_rate.astype(int), 0)
suspect = np.maximum(suspect_rate.astype(int), 0)

df = pd.DataFrame(
    {
        "onset_date": np.tile(dates, 3),
        "case_count": np.concatenate([confirmed, probable, suspect]),
        "case_type": (["Confirmed"] * 90 + ["Probable"] * 90 + ["Suspect"] * 90),
    }
)
df["case_type"] = pd.Categorical(df["case_type"], categories=["Suspect", "Probable", "Confirmed"], ordered=True)

# Intervention dates
lockdown_date = pd.Timestamp("2024-02-10")
vaccination_date = pd.Timestamp("2024-03-01")

interventions = pd.DataFrame(
    {"date": [lockdown_date, vaccination_date], "label": ["Lockdown", "Vaccination\ncampaign"]}
)

# Plot
plot = (
    ggplot(df, aes(x="onset_date", y="case_count"))
    + geom_col(aes(fill="case_type"), width=0.85)
    + geom_vline(
        data=interventions, mapping=aes(xintercept="date"), linetype="dashed", color="#333333", size=0.7, alpha=0.8
    )
    + geom_text(
        data=interventions, mapping=aes(x="date", label="label"), y=52, ha="left", nudge_x=1.5, size=11, color="#333333"
    )
    + scale_fill_manual(values={"Confirmed": "#306998", "Probable": "#F0A030", "Suspect": "#B0B0B0"})
    + scale_x_date(date_breaks="2 weeks", date_labels="%b %d")
    + labs(
        x="Date of Symptom Onset",
        y="Number of New Cases",
        fill="Case Classification",
        title="histogram-epidemic \u00b7 plotnine \u00b7 pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=45, ha="right"),
        plot_title=element_text(size=24, weight="bold"),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="top",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        axis_line_x=element_line(color="#333333", size=0.5),
        axis_line_y=element_line(color="#333333", size=0.5),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
