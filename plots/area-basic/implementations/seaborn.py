"""pyplots.ai
area-basic: Basic Area Chart
Library: seaborn 0.13.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-12
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

# Simulate realistic web traffic with weekly pattern, trend, and a traffic spike
base_visitors = 5000
trend = np.linspace(0, 1500, 30)
weekly_pattern = np.array([1.0, 1.1, 1.15, 1.2, 1.1, 0.7, 0.65] * 5)[:30]
noise = np.random.randn(30) * 300
visitors = (base_visitors + trend) * weekly_pattern + noise
visitors[17] *= 1.45  # Traffic spike from a viral post on day 18
visitors = np.maximum(visitors, 1000)

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Plot
sns.set_theme(style="white", context="talk", font_scale=1.2)

fig, ax = plt.subplots(figsize=(16, 9))

sns.lineplot(data=df, x="date", y="visitors", ax=ax, color="#306998", linewidth=3)
ax.fill_between(df["date"], df["visitors"], alpha=0.4, color="#306998")

# Annotate the traffic spike
spike_idx = 17
ax.annotate(
    "Viral post",
    xy=(df["date"].iloc[spike_idx], df["visitors"].iloc[spike_idx]),
    xytext=(df["date"].iloc[spike_idx - 6], df["visitors"].iloc[spike_idx] * 1.0),
    fontsize=16,
    color="#1a3a5c",
    arrowprops={"arrowstyle": "->", "color": "#1a3a5c", "lw": 2},
    ha="center",
)

# Style
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Visitors (count)", fontsize=20)
ax.set_title("area-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)

# Set y-axis to start at 0, cap top to reduce whitespace
ax.set_ylim(bottom=0, top=df["visitors"].max() * 1.12)

# Format x-axis dates
fig.autofmt_xdate(rotation=45)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
