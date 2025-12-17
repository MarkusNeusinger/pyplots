"""
errorbar-basic: Basic Error Bar Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="whitegrid")

# Data - experimental measurements with associated uncertainties
np.random.seed(42)
categories = ["Control", "Treatment A", "Treatment B", "Treatment C", "Treatment D", "Treatment E"]
x = np.arange(len(categories))
y = np.array([25.3, 38.7, 42.1, 35.8, 48.2, 31.5])  # Mean values

# Asymmetric errors: Treatment C and D have notably different lower/upper bounds
asymmetric_lower = np.array([2.1, 3.5, 2.8, 6.5, 4.8, 2.5])
asymmetric_upper = np.array([2.1, 3.5, 2.8, 2.8, 2.2, 2.5])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.errorbar(
    x,
    y,
    yerr=[asymmetric_lower, asymmetric_upper],
    fmt="o",
    markersize=15,
    color="#306998",
    ecolor="#306998",
    elinewidth=3,
    capsize=10,
    capthick=3,
    alpha=0.9,
)

# Styling
ax.set_xlabel("Experimental Group", fontsize=20)
ax.set_ylabel("Response Value (units)", fontsize=20)
ax.set_title("errorbar-basic · seaborn · pyplots.ai", fontsize=24)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=16)
ax.tick_params(axis="y", labelsize=16)

# Add some vertical padding
ax.set_ylim(0, max(y + asymmetric_upper) * 1.15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
