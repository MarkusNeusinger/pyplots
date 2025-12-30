"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Daily temperature readings over a year (365 days)
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")

# Generate realistic temperature pattern: seasonal trend + noise
day_of_year = np.arange(365)
seasonal = 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Peak in summer
baseline = 12  # Average temperature
noise = np.random.normal(0, 3, 365)
temperature = baseline + seasonal + noise

df = pd.DataFrame({"Date": dates, "Temperature (°C)": temperature})

# Create plot (4800x2700 px at 300 dpi = 16x9 inches)
sns.set_context("talk", font_scale=1.2)
sns.set_style("whitegrid")

fig, ax = plt.subplots(figsize=(16, 9))

# Line plot with seaborn
sns.lineplot(data=df, x="Date", y="Temperature (°C)", ax=ax, color="#306998", linewidth=2.5)

# Add markers at monthly intervals to show data point density
monthly_idx = np.arange(0, 365, 30)
ax.scatter(
    df["Date"].iloc[monthly_idx],
    df["Temperature (°C)"].iloc[monthly_idx],
    color="#FFD43B",
    s=150,
    zorder=5,
    edgecolor="#306998",
    linewidth=2,
    label="Monthly Markers",
)

# Highlight a zoom region with annotation to simulate interactive focus
zoom_start = 150  # June
zoom_end = 210  # Late July
ax.axvspan(
    df["Date"].iloc[zoom_start], df["Date"].iloc[zoom_end], alpha=0.15, color="#FFD43B", label="Example Focus Region"
)

# Add annotation to show what hover would reveal
peak_idx = df["Temperature (°C)"].idxmax()
peak_date = df["Date"].iloc[peak_idx]
peak_temp = df["Temperature (°C)"].iloc[peak_idx]
ax.annotate(
    f"{peak_date.strftime('%b %d')}: {peak_temp:.1f}°C",
    xy=(peak_date, peak_temp),
    xytext=(peak_date + pd.Timedelta(days=30), peak_temp + 5),
    fontsize=14,
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2},
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "#306998", "alpha": 0.9},
)

# Styling
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Temperature (°C)", fontsize=20)
ax.set_title("line-interactive · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=14, loc="lower right")

# Format x-axis dates
fig.autofmt_xdate(rotation=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
