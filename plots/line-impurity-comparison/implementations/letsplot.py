""" pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 88/100 | Created: 2026-02-17
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
with np.errstate(divide="ignore", invalid="ignore"):
    entropy = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
entropy = np.nan_to_num(entropy, nan=0.0)

# Main curves data
df = pd.DataFrame(
    {
        "p": np.tile(p, 2),
        "impurity": np.concatenate([gini, entropy]),
        "metric": ["Gini: 2p(1\u2212p)"] * len(p) + ["Entropy (normalized)"] * len(p),
    }
)

# Shaded region between curves to highlight their difference
ribbon_df = pd.DataFrame({"p": p, "gini": gini, "entropy": entropy})

# Annotation markers for maxima at p=0.5
max_gini_df = pd.DataFrame({"p": [0.5], "impurity": [0.5]})
max_entropy_df = pd.DataFrame({"p": [0.5], "impurity": [1.0]})
max_label_df = pd.DataFrame({"p": [0.5], "impurity": [1.05], "label": ["Maximum uncertainty\nat p = 0.5"]})

# Difference annotation
diff_label_df = pd.DataFrame({"p": [0.72], "impurity": [0.6], "label": ["Shaded region:\ndifference between metrics"]})

# Plot
plot = (
    ggplot()  # noqa: F405
    # Shaded ribbon between curves (distinctive lets-plot feature)
    + geom_ribbon(  # noqa: F405
        data=ribbon_df,
        mapping=aes(x="p", ymin="gini", ymax="entropy"),  # noqa: F405
        fill="#306998",
        alpha=0.08,
    )
    # Main curves
    + geom_line(  # noqa: F405
        data=df,
        mapping=aes(x="p", y="impurity", color="metric"),  # noqa: F405
        size=2.5,
        tooltips=layer_tooltips()  # noqa: F405
        .line("@metric")
        .line("p = @p")
        .line("impurity = @impurity"),
    )
    # Vertical guide at p=0.5
    + geom_vline(xintercept=0.5, color="#bbbbbb", size=0.5, linetype="dashed")  # noqa: F405
    # Open circle markers at maxima
    + geom_point(  # noqa: F405
        data=max_entropy_df,
        mapping=aes(x="p", y="impurity"),  # noqa: F405
        size=8,
        color="#e07a2f",
        shape=21,
        fill="white",
        stroke=2.5,
    )
    + geom_point(  # noqa: F405
        data=max_gini_df,
        mapping=aes(x="p", y="impurity"),  # noqa: F405
        size=8,
        color="#306998",
        shape=21,
        fill="white",
        stroke=2.5,
    )
    # Annotation for maximum uncertainty
    + geom_text(  # noqa: F405
        data=max_label_df,
        mapping=aes(x="p", y="impurity", label="label"),  # noqa: F405
        size=12,
        color="#444444",
        fontface="italic",
    )
    # Annotation for shaded difference region
    + geom_text(  # noqa: F405
        data=diff_label_df,
        mapping=aes(x="p", y="impurity", label="label"),  # noqa: F405
        size=10,
        color="#6a8fb2",
        fontface="italic",
    )
    # Scales
    + scale_color_manual(values=["#306998", "#e07a2f"])  # noqa: F405
    + scale_x_continuous(  # noqa: F405
        breaks=list(np.arange(0, 1.1, 0.1))
    )
    + scale_y_continuous(  # noqa: F405
        breaks=list(np.arange(0, 1.1, 0.2))
    )
    # Labels
    + labs(  # noqa: F405
        x="Probability of class 1 (p)",
        y="Impurity measure (normalized)",
        title="line-impurity-comparison \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle="Both criteria peak at maximum uncertainty (p = 0.5), explaining why Gini and entropy yield similar tree structures",
        color="",
    )
    + ggsize(1600, 900)  # noqa: F405
    # Theme: refined minimal with careful whitespace
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16, color="#555555"),  # noqa: F405
        axis_title=element_text(size=20, color="#333333"),  # noqa: F405
        plot_title=element_text(size=24, face="bold", color="#222222"),  # noqa: F405
        plot_subtitle=element_text(size=15, color="#666666", face="italic"),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="bottom",
        panel_grid_major=element_line(color="#eeeeee", size=0.3),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
        axis_line=element_line(color="#cccccc", size=0.5),  # noqa: F405
        plot_margin=[40, 20, 20, 20],
    )
)

# Save
export_ggsave(plot, "plot.png", path=".", scale=3)
export_ggsave(plot, "plot.html", path=".")
