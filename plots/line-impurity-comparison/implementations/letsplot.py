"""pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data
p = np.linspace(0, 1, 200)

# Gini impurity: 2 * p * (1 - p)
gini = 2 * p * (1 - p)

# Entropy: -p * log2(p) - (1-p) * log2(1-p), normalized to [0, 1]
# Handle edge cases at p=0 and p=1
with np.errstate(divide="ignore", invalid="ignore"):
    entropy_raw = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
entropy_raw = np.nan_to_num(entropy_raw, nan=0.0)
entropy = entropy_raw  # max is 1.0 at p=0.5, already in [0, 1]

df = pd.DataFrame(
    {
        "p": np.tile(p, 2),
        "impurity": np.concatenate([gini, entropy]),
        "metric": ["Gini: 2p(1\u2212p)"] * len(p)
        + ["Entropy: \u2212p log\u2082p \u2212 (1\u2212p) log\u2082(1\u2212p)"] * len(p),
    }
)

# Annotation markers for maxima at p=0.5
max_points_df = pd.DataFrame({"p": [0.5, 0.5], "impurity": [1.0, 0.5]})
max_label_df = pd.DataFrame({"p": [0.5], "impurity": [1.0], "label": ["Both maxima at p = 0.5"]})

# Plot
plot = (
    ggplot(df, aes(x="p", y="impurity", color="metric"))  # noqa: F405
    + geom_line(size=2.5)  # noqa: F405
    + geom_point(  # noqa: F405
        data=max_points_df,
        mapping=aes(x="p", y="impurity"),  # noqa: F405
        inherit_aes=False,
        size=7,
        color="#333333",
        shape=21,
        fill="white",
        stroke=2.5,
    )
    + geom_vline(xintercept=0.5, color="#cccccc", size=0.6, linetype="dotted")  # noqa: F405
    + geom_text(  # noqa: F405
        data=max_label_df,
        mapping=aes(x="p", y="impurity", label="label"),  # noqa: F405
        inherit_aes=False,
        nudge_x=0.15,
        nudge_y=-0.03,
        size=13,
        color="#333333",
    )
    + scale_color_manual(values=["#306998", "#e07a2f"])  # noqa: F405
    + scale_x_continuous(  # noqa: F405
        breaks=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    )
    + scale_y_continuous(breaks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])  # noqa: F405
    + labs(  # noqa: F405
        x="Probability (p)",
        y="Impurity Measure",
        title="line-impurity-comparison \u00b7 letsplot \u00b7 pyplots.ai",
        color="",
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        legend_text=element_text(size=15),  # noqa: F405
        legend_position="bottom",
        panel_grid_major=element_line(color="#e5e5e5", size=0.4),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
)

# Save
export_ggsave(plot, "plot.png", path=".", scale=3)
export_ggsave(plot, "plot.html", path=".")
