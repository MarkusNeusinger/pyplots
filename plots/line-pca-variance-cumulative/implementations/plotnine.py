""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 80/100 | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_hline,
    geom_line,
    geom_point,
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

# Threshold reference lines
thresholds = pd.DataFrame({"yintercept": [90.0, 95.0], "label": ["90%", "95%"]})

# Plot
plot = (
    ggplot(df, aes(x="component", y="cumulative_variance"))
    + geom_hline(data=thresholds, mapping=aes(yintercept="yintercept"), linetype="dashed", color="#999999", size=0.8)
    + geom_line(color="#306998", size=1.5)
    + geom_point(color="#306998", size=4, fill="white", stroke=1.5)
    + scale_x_continuous(breaks=n_components, labels=[str(i) for i in n_components])
    + scale_y_continuous(
        limits=(0, 105),
        breaks=[0, 20, 40, 60, 80, 90, 95, 100],
        labels=["0%", "20%", "40%", "60%", "80%", "90%", "95%", "100%"],
    )
    + labs(
        x="Number of Principal Components",
        y="Cumulative Explained Variance",
        title="line-pca-variance-cumulative · plotnine · pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#CCCCCC", size=0.5, alpha=0.25),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
