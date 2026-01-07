"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Monthly temperature readings over 2 years
np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=24, freq="ME")
base_temp = 15 + 10 * np.sin(np.linspace(0, 2 * np.pi, 24))  # Seasonal pattern
noise = np.random.normal(0, 2, 24)
temperatures = base_temp + noise + np.linspace(0, 3, 24)  # Slight warming trend

df = pd.DataFrame({"date": dates, "temperature": temperatures})
df["month_num"] = range(len(df))

# Create small multiples showing progressive reveal (6 stages)
stages = [4, 8, 12, 16, 20, 24]  # Show at 4, 8, 12, 16, 20, 24 months
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

sns.set_style("whitegrid")

# Python colors for the line
line_color = "#306998"
highlight_color = "#FFD43B"

for ax, stage in zip(axes, stages, strict=True):
    # Subset data up to this stage
    df_subset = df.iloc[:stage].copy()

    # Plot the line using seaborn
    sns.lineplot(data=df_subset, x="month_num", y="temperature", ax=ax, color=line_color, linewidth=3)

    # Add markers at each point
    sns.scatterplot(
        data=df_subset, x="month_num", y="temperature", ax=ax, color=line_color, s=100, zorder=5, legend=False
    )

    # Highlight the most recent point (current position)
    ax.scatter(
        df_subset["month_num"].iloc[-1],
        df_subset["temperature"].iloc[-1],
        color=highlight_color,
        s=300,
        zorder=6,
        edgecolors=line_color,
        linewidths=2,
    )

    # Keep consistent axis limits across all panels
    ax.set_xlim(-1, 25)
    ax.set_ylim(0, 35)

    # Styling
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Temperature (°C)", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
    ax.grid(True, alpha=0.3, linestyle="--")

    # Stage label
    ax.set_title(f"Month {stage}", fontsize=16, fontweight="bold")

# Main title
fig.suptitle("line-animated-progressive · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
