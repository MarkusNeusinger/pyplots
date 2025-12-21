""" pyplots.ai
streamgraph-basic: Basic Stream Graph
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Monthly streaming hours by music genre over 2 years
np.random.seed(42)

months = pd.date_range(start="2022-01", periods=24, freq="ME")
genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz"]

# Generate smooth streaming data with trends
data = {}
for i, genre in enumerate(genres):
    base = 50 + i * 10
    trend = np.linspace(0, 20 * (1 - 0.3 * i), 24)
    seasonal = 15 * np.sin(np.linspace(0, 4 * np.pi, 24) + i * np.pi / 3)
    noise = np.random.randn(24) * 5
    data[genre] = np.maximum(base + trend + seasonal + noise, 10)

df = pd.DataFrame(data, index=months)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Prepare data for stackplot
x = np.arange(len(months))
y_data = [df[genre].values for genre in genres]

# Create streamgraph with symmetric baseline ("wiggle" creates centered baseline)
colors = ["#306998", "#FFD43B", "#E07A5F", "#81B29A", "#F2CC8F"]
ax.stackplot(
    x,
    *y_data,
    labels=genres,
    colors=colors,
    baseline="wiggle",  # Centers the baseline symmetrically
    alpha=0.9,
)

# Style
ax.set_title("streamgraph-basic · seaborn · pyplots.ai", fontsize=24)
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Streaming Hours (millions)", fontsize=20)
ax.tick_params(axis="both", labelsize=16)

# X-axis formatting with month labels
tick_positions = np.arange(0, len(months), 3)
tick_labels = [months[i].strftime("%b %Y") for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha="right")

# Remove spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)

# Remove y-axis ticks (streamgraphs emphasize shape over exact values)
ax.set_yticks([])

# Legend
ax.legend(loc="upper right", fontsize=16, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
