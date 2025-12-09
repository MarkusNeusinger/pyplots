"""
area-basic: Basic Area Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - monthly sales over a year
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Set seaborn style
sns.set_theme(style="whitegrid")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot line and filled area (seaborn doesn't have native area chart, use matplotlib)
ax.plot(data["month"], data["sales"], color="#306998", linewidth=2)
ax.fill_between(data["month"], data["sales"], alpha=0.4, color="#306998")

# Labels and styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Sales", fontsize=20)
ax.set_title("Basic Area Chart", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Set y-axis to start from 0 for proper area representation
ax.set_ylim(0, max(data["sales"]) * 1.1)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
