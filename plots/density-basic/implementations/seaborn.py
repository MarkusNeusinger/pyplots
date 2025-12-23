"""pyplots.ai
density-basic: Basic Density Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - create a realistic bimodal distribution of test scores
np.random.seed(42)
test_scores = np.concatenate(
    [
        np.random.normal(72, 10, 300),  # Main group centered at 72
        np.random.normal(88, 5, 100),  # High achievers group
    ]
)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot density curve with fill
sns.kdeplot(data=test_scores, ax=ax, fill=True, alpha=0.6, color="#306998", linewidth=3)

# Add rug plot to show individual observations
sns.rugplot(data=test_scores, ax=ax, color="#306998", alpha=0.3, height=0.03)

# Style
ax.set_xlabel("Test Score (points)", fontsize=20)
ax.set_ylabel("Density", fontsize=20)
ax.set_title("density-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
