""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 82/100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Monthly performance metrics across departments
np.random.seed(42)
departments = ["Sales", "Marketing", "Engineering", "Support", "Finance", "HR", "Operations"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate performance data (values 0-100)
data = np.random.randn(len(departments), len(months)) * 20 + 50
# Add patterns to demonstrate heatmap capabilities
data[0, :6] += 20  # Sales strong first half
data[2, 6:] += 25  # Engineering strong second half
data[4, :] = data[4, :] * 0.3 + 70  # Finance consistently stable
data[5, 3:9] -= 15  # HR dip mid-year
# Clip to valid performance range
data = np.clip(data, 5, 95)

# Plot - clustermap groups similar departments via hierarchical clustering
cmap = sns.diverging_palette(240, 10, as_cmap=True)
g = sns.clustermap(
    data,
    annot=True,
    fmt=".0f",
    cmap=cmap,
    center=50,
    xticklabels=months,
    yticklabels=departments,
    linewidths=1,
    linecolor="white",
    annot_kws={"fontsize": 14},
    figsize=(16, 10),
    row_cluster=True,
    col_cluster=False,
    dendrogram_ratio=0.08,
    cbar_pos=None,
    vmin=0,
    vmax=100,
)

# Colorbar with proper placement
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 100))
cbar = g.fig.colorbar(sm, ax=g.ax_heatmap, location="right", shrink=0.7, pad=0.12)
cbar.set_label("Performance Score", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Style
g.ax_heatmap.set_xlabel("Month", fontsize=20)
g.ax_heatmap.set_ylabel("")
g.ax_heatmap.tick_params(axis="x", labelsize=16)
g.ax_heatmap.tick_params(axis="y", labelsize=16, rotation=0)
g.fig.suptitle("heatmap-basic · seaborn · pyplots.ai", fontsize=24, y=1.02)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
