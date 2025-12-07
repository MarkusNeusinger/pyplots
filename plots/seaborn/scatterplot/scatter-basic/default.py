"""
scatter-basic: Basic Scatter Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

data = pd.DataFrame({"x": x, "y": y})

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.scatterplot(data=data, x="x", y="y", s=50, alpha=0.7, color="#306998", ax=ax)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("Basic Scatter Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
