"""
radar-basic: Basic Radar Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")

# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 70, 90, 65, 80]
athlete_b = [70, 85, 75, 80, 70]

# Number of variables
n_vars = len(categories)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()

# Close the polygon by appending the first value
athlete_a += athlete_a[:1]
athlete_b += athlete_b[:1]
angles += angles[:1]

# Create figure with polar projection
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"polar": True})

# Use seaborn color palette
palette = sns.color_palette("colorblind")
color_a = palette[0]
color_b = palette[3]

# Plot data
ax.plot(angles, athlete_a, "o-", linewidth=2, color=color_a, label="Athlete A", markersize=8)
ax.fill(angles, athlete_a, alpha=0.25, color=color_a)

ax.plot(angles, athlete_b, "o-", linewidth=2, color=color_b, label="Athlete B", markersize=8)
ax.fill(angles, athlete_b, alpha=0.25, color=color_b)

# Set category labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=16)

# Configure radial axis
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=14)
ax.set_rlabel_position(30)

# Title and legend
ax.set_title("Athlete Performance Comparison", fontsize=20, pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), fontsize=14)

# Grid styling
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
