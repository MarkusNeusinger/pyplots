""" pyplots.ai
area-basic: Basic Area Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

# Simulate realistic web traffic with weekly pattern and trend
base_visitors = 5000
trend = np.linspace(0, 1500, 30)
weekly_pattern = np.array([1.0, 1.1, 1.15, 1.2, 1.1, 0.7, 0.65] * 5)[:30]
noise = np.random.randn(30) * 300
visitors = (base_visitors + trend) * weekly_pattern + noise
visitors = np.maximum(visitors, 1000)  # Ensure positive values

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Area fill with semi-transparent Python Blue
ax.fill_between(df["date"], df["visitors"], alpha=0.4, color="#306998")

# Line on top using seaborn
sns.lineplot(data=df, x="date", y="visitors", ax=ax, color="#306998", linewidth=3)

# Style
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Visitors (count)", fontsize=20)
ax.set_title("area-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Set y-axis to start at 0 to emphasize area magnitude
ax.set_ylim(bottom=0)

# Format x-axis dates
fig.autofmt_xdate(rotation=45)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
