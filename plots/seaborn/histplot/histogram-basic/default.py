"""
histogram-basic: Basic Histogram
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)
data = pd.DataFrame({"value": np.random.normal(100, 15, 500)})

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.histplot(data=data, x="value", bins=30, color="#306998", alpha=0.8, edgecolor="white", ax=ax)

# Labels and styling
ax.set_xlabel("Value", fontsize=20)
ax.set_ylabel("Frequency", fontsize=20)
ax.set_title("Basic Histogram", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
