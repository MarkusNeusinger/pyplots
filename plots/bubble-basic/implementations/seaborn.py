""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)
n_points = 50

x = np.random.randn(n_points) * 15 + 50
y = x * 0.6 + np.random.randn(n_points) * 10 + 20
size_values = np.random.rand(n_points) * 80 + 20  # Range 20-100

df = pd.DataFrame({"x": x, "y": y, "size": size_values})

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Scale sizes for visibility at 4800x2700 - map to area range 100-2000
size_scaled = (df["size"] - df["size"].min()) / (df["size"].max() - df["size"].min())
sizes = size_scaled * 1900 + 100

sns.scatterplot(data=df, x="x", y="y", size=sizes, sizes=(100, 2000), alpha=0.6, color="#306998", legend=False, ax=ax)

# Size legend - create proxy bubbles for legend
legend_sizes = [20, 50, 80]
legend_markers = []
for s in legend_sizes:
    scaled = (s - df["size"].min()) / (df["size"].max() - df["size"].min())
    marker_size = scaled * 1900 + 100
    marker = ax.scatter([], [], s=marker_size, c="#306998", alpha=0.6)
    legend_markers.append(marker)

ax.legend(
    legend_markers,
    [f"Size: {s}" for s in legend_sizes],
    title="Bubble Size",
    loc="upper left",
    fontsize=14,
    title_fontsize=16,
    framealpha=0.9,
)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("bubble-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
