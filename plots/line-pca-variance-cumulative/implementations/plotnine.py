""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 85/100 | Created: 2026-02-17
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

df = pd.DataFrame({"component": n_components, "cumulative_variance": cumulative_variance})

# Detect elbow point using maximum second derivative (discrete differences)
diffs = np.diff(cumulative_variance)
second_diffs = np.diff(diffs)
elbow_idx = int(np.argmax(np.abs(second_diffs))) + 1  # +1 for 0-indexing offset
elbow_component = int(n_components[elbow_idx])
elbow_variance = cumulative_variance[elbow_idx]

# Threshold annotation data
thresh_labels = pd.DataFrame({"x": [13.4, 13.4], "y": [90.0, 95.0], "label": ["90%", "95%"]})

# Elbow point data
elbow_df = pd.DataFrame({"component": [elbow_component], "cumulative_variance": [elbow_variance]})

# Plot
plot = (
    ggplot(df, aes(x="component", y="cumulative_variance"))
    # Shaded region between 90% and 95% thresholds
    + annotate("rect", xmin=0.5, xmax=13.5, ymin=90, ymax=95, fill="#E8F5E9", alpha=0.4)
    # Shaded region above 95%
    + annotate("rect", xmin=0.5, xmax=13.5, ymin=95, ymax=102, fill="#C8E6C9", alpha=0.3)
    # Threshold lines with distinct amber/green colors
    + geom_hline(yintercept=90.0, linetype="dashed", color="#E65100", size=0.8, alpha=0.7)
    + geom_hline(yintercept=95.0, linetype="dashed", color="#2E7D32", size=0.8, alpha=0.7)
    # Threshold labels on right side
    + geom_text(
        data=thresh_labels,
        mapping=aes(x="x", y="y", label="label"),
        ha="left",
        va="bottom",
        size=11,
        color="#555555",
        fontweight="bold",
        nudge_y=0.6,
    )
    # Vertical drop-line from elbow to x-axis
    + geom_segment(
        data=elbow_df,
        mapping=aes(x="component", xend="component", y=28, yend="cumulative_variance"),
        linetype="dotted",
        color="#306998",
        size=0.7,
        alpha=0.5,
    )
    # Main cumulative line
    + geom_line(color="#306998", size=1.5)
    # Data points with white fill
    + geom_point(color="#306998", size=4, fill="white", stroke=1.5)
    # Highlighted elbow point
    + geom_point(
        data=elbow_df,
        mapping=aes(x="component", y="cumulative_variance"),
        color="#D84315",
        size=6,
        fill="#FF8A65",
        stroke=2,
    )
    # Elbow annotation
    + geom_text(
        data=elbow_df,
        mapping=aes(
            x="component",
            y="cumulative_variance",
            label=[f"Elbow at {elbow_component} components\n({elbow_variance:.1f}%)"],
        ),
        ha="left",
        va="bottom",
        size=10,
        color="#D84315",
        fontweight="bold",
        nudge_x=0.3,
        nudge_y=1.5,
    )
    # Scales
    + scale_x_continuous(breaks=n_components, labels=[str(i) for i in n_components], expand=(0.02, 0.5))
    + scale_y_continuous(
        limits=(28, 102),
        breaks=[30, 40, 50, 60, 70, 80, 90, 95, 100],
        labels=["30%", "40%", "50%", "60%", "70%", "80%", "90%", "95%", "100%"],
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
        axis_title=element_text(size=20, color="#333333", face="bold"),
        axis_text=element_text(size=16, color="#555555"),
        plot_title=element_text(size=24, color="#222222", face="bold"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.3, alpha=0.5),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="#FAFAFA", color="white"),
        axis_line_x=element_line(color="#BBBBBB", size=0.5),
        axis_ticks_major_x=element_line(color="#BBBBBB", size=0.5),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
