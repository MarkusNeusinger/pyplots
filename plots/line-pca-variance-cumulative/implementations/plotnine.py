""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 89/100 | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_hline,
    geom_line,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data - PCA on the Wine dataset (13 features)
wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(X_scaled)

n_components = np.arange(1, len(pca.explained_variance_ratio_) + 1)
cumulative_variance = np.cumsum(pca.explained_variance_ratio_) * 100
individual_variance = pca.explained_variance_ratio_ * 100

df = pd.DataFrame(
    {"component": n_components, "cumulative_variance": cumulative_variance, "individual_variance": individual_variance}
)

# Detect elbow point via maximum curvature (second derivative)
diffs = np.diff(cumulative_variance)
elbow_idx = int(np.argmax(np.abs(np.diff(diffs)))) + 1
elbow_component = int(n_components[elbow_idx])
elbow_variance = cumulative_variance[elbow_idx]

elbow_df = pd.DataFrame({"component": [elbow_component], "cumulative_variance": [elbow_variance]})

# Threshold labels positioned in open space left of data
thresholds = pd.DataFrame(
    {
        "y": [90.0, 95.0, 99.0],
        "label": ["90% threshold", "95% threshold", "99% threshold"],
        "color": ["#E65100", "#2E7D32", "#1565C0"],
        "x": [5.5, 5.5, 5.5],
    }
)

# Plot
plot = (
    ggplot(df, aes(x="component", y="cumulative_variance"))
    # Shaded threshold bands
    + annotate("rect", xmin=0.3, xmax=13.7, ymin=90, ymax=95, fill="#FFF3E0", alpha=0.3)
    + annotate("rect", xmin=0.3, xmax=13.7, ymin=95, ymax=99, fill="#E8F5E9", alpha=0.3)
    + annotate("rect", xmin=0.3, xmax=13.7, ymin=99, ymax=102, fill="#E3F2FD", alpha=0.25)
    # Threshold dashed lines at 90%, 95%, 99%
    + geom_hline(yintercept=90.0, linetype="dashed", color="#E65100", size=0.7, alpha=0.55)
    + geom_hline(yintercept=95.0, linetype="dashed", color="#2E7D32", size=0.7, alpha=0.55)
    + geom_hline(yintercept=99.0, linetype="dashed", color="#1565C0", size=0.7, alpha=0.55)
    # Individual variance as subtle square markers (secondary data layer)
    + geom_point(aes(y="individual_variance"), shape="s", color="#306998", fill="#306998", size=2.5, alpha=0.15)
    # Vertical drop-line from elbow to x-axis
    + geom_segment(
        data=elbow_df,
        mapping=aes(x="component", xend="component", y=0, yend="cumulative_variance"),
        linetype="dotted",
        color="#D84315",
        size=0.6,
        alpha=0.4,
    )
    # Main cumulative line
    + geom_line(color="#306998", size=1.5)
    # Data points with white fill
    + geom_point(color="#306998", size=4, fill="white", stroke=1.5, shape="o")
    # Highlighted elbow point
    + geom_point(
        data=elbow_df,
        mapping=aes(x="component", y="cumulative_variance"),
        color="#D84315",
        size=7,
        fill="#FF8A65",
        stroke=2.2,
        shape="o",
    )
    # Elbow annotation - offset to upper-right to avoid crowding nearby points
    + geom_text(
        data=elbow_df,
        mapping=aes(
            x="component",
            y="cumulative_variance",
            label=[f"Elbow: {elbow_component} components ({elbow_variance:.1f}%)"],
        ),
        ha="left",
        va="bottom",
        size=10,
        color="#D84315",
        fontweight="bold",
        nudge_x=0.6,
        nudge_y=3.5,
    )
    # Threshold labels positioned in open space above the line
    + geom_text(
        data=thresholds,
        mapping=aes(x="x", y="y", label="label", color="color"),
        ha="center",
        va="bottom",
        size=9,
        fontweight="bold",
        nudge_y=0.4,
        show_legend=False,
    )
    + scale_color_identity()
    # Scales
    + scale_x_continuous(breaks=n_components, labels=[str(i) for i in n_components], expand=(0.02, 0.4))
    + scale_y_continuous(
        limits=(0, 102), breaks=[0, 20, 40, 60, 80, 100], labels=["0%", "20%", "40%", "60%", "80%", "100%"]
    )
    + labs(
        x="Number of Principal Components",
        y="Cumulative Explained Variance (%)",
        title="line-pca-variance-cumulative · plotnine · pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color="#333333"),
        axis_title=element_text(size=20, color="#444444", face="bold"),
        axis_text=element_text(size=16, color="#555555"),
        plot_title=element_text(size=24, color="#222222", face="bold", ha="left"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.3, alpha=0.4),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="#FAFAFA", color="#EEEEEE", size=0.3),
        axis_line_x=element_line(color="#BBBBBB", size=0.5),
        axis_ticks_major_x=element_line(color="#BBBBBB", size=0.4),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
