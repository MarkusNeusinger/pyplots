"""pyplots.ai
area-basic: Basic Area Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - daily website visitors over a month
np.random.seed(42)
days = np.arange(1, 31)
base_visitors = 5000 + np.linspace(0, 2000, 30)  # Upward trend
noise = np.random.randn(30) * 500
visitors = base_visitors + noise
visitors = np.clip(visitors, 3000, 10000)  # Realistic bounds

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Area chart with semi-transparent fill
ax.fill_between(days, visitors, alpha=0.4, color="#306998")
ax.plot(days, visitors, color="#306998", linewidth=3)

# Labels and styling
ax.set_xlabel("Day of Month", fontsize=20)
ax.set_ylabel("Daily Visitors", fontsize=20)
ax.set_title("area-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Set axis limits for better presentation
ax.set_xlim(1, 30)
ax.set_ylim(0, ax.get_ylim()[1] * 1.1)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
