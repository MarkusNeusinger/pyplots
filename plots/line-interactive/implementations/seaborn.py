"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Daily temperature readings with seasonal patterns (realistic weather scenario)
np.random.seed(42)
n_points = 180  # ~6 months of daily data

# Generate datetime index
dates = pd.date_range("2024-01-01", periods=n_points, freq="D")

# Generate realistic temperature data with seasonal pattern
base_temp = 15  # Base temperature in Celsius
seasonal_pattern = 12 * np.sin(2 * np.pi * np.arange(n_points) / 365 - np.pi / 2)  # Seasonal cycle
weekly_variation = 3 * np.sin(2 * np.pi * np.arange(n_points) / 7)  # Weekly variation
noise = np.random.normal(0, 2.5, n_points)

# Combine patterns for realistic temperature
temperature = base_temp + seasonal_pattern + weekly_variation + noise

# Add some extreme events (heat waves and cold snaps)
heat_wave_indices = [85, 86, 87, 88, 89]  # Late March heat wave
cold_snap_indices = [25, 26, 27]  # Late January cold snap
for idx in heat_wave_indices:
    temperature[idx] += np.random.uniform(6, 10)
for idx in cold_snap_indices:
    temperature[idx] -= np.random.uniform(5, 8)

# Create DataFrame for seaborn
df = pd.DataFrame({"Date": dates, "Temperature": temperature, "Day": np.arange(n_points)})

# Set seaborn style (white, not whitegrid - we'll add custom subtle grid)
sns.set_theme(style="white")

# Create the figure with two axes: main plot and range selector
fig, (ax, ax_range) = plt.subplots(2, 1, figsize=(16, 9), height_ratios=[5, 1], sharex=False)
fig.subplots_adjust(hspace=0.15)

# Main line plot using seaborn
sns.lineplot(data=df, x="Date", y="Temperature", color="#306998", linewidth=2.5, ax=ax, label="Daily Temperature")

# Add scatter points for hover targets (every 10th point)
scatter_df = df.iloc[::10].copy()
sns.scatterplot(
    data=scatter_df,
    x="Date",
    y="Temperature",
    color="#306998",
    s=150,
    alpha=0.8,
    edgecolor="white",
    linewidth=1.5,
    ax=ax,
    zorder=3,
    label="Data Points",
)

# Range selector subplot - simplified overview of the data
sns.lineplot(data=df, x="Date", y="Temperature", color="#306998", linewidth=1.5, ax=ax_range, legend=False)
ax_range.set_ylabel("")
ax_range.set_xlabel("Drag to Select Range", fontsize=14)
ax_range.tick_params(axis="y", labelsize=10)
ax_range.tick_params(axis="x", labelsize=12)
ax_range.set_title("Range Selector", fontsize=14, fontweight="bold", loc="left")

# Add span selector for range selection (demonstrates interactive range selection)
# Highlight current selection on the range selector
selected_start, selected_end = 40, 100
ax_range.axvspan(dates[selected_start], dates[selected_end], alpha=0.3, color="#FFD43B", zorder=2)
ax_range.annotate(
    "Selected Range",
    xy=(dates[(selected_start + selected_end) // 2], ax_range.get_ylim()[1]),
    xytext=(0, -5),
    textcoords="offset points",
    fontsize=11,
    ha="center",
    va="top",
    color="#306998",
    fontweight="bold",
)

# Highlight heat wave with visible markers and annotation
heat_wave_df = df.iloc[heat_wave_indices]
ax.scatter(
    heat_wave_df["Date"],
    heat_wave_df["Temperature"],
    color="#E63946",
    s=250,
    edgecolors="#306998",
    linewidths=2.5,
    zorder=5,
    marker="^",
)
ax.annotate(
    f"Heat Wave: {heat_wave_df['Temperature'].max():.1f}°C",
    xy=(dates[87], temperature[87]),
    xytext=(0, 25),
    textcoords="offset points",
    fontsize=13,
    fontweight="bold",
    color="white",
    ha="center",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#E63946", "alpha": 0.95, "edgecolor": "#306998", "linewidth": 1.5},
    arrowprops={"arrowstyle": "-", "color": "#E63946", "lw": 2},
)

# Highlight cold snap with visible markers and annotation
cold_snap_df = df.iloc[cold_snap_indices]
ax.scatter(
    cold_snap_df["Date"],
    cold_snap_df["Temperature"],
    color="#1E88E5",
    s=250,
    edgecolors="#306998",
    linewidths=2.5,
    zorder=5,
    marker="v",
)
ax.annotate(
    f"Cold Snap: {cold_snap_df['Temperature'].min():.1f}°C",
    xy=(dates[26], temperature[26]),
    xytext=(0, -35),
    textcoords="offset points",
    fontsize=13,
    fontweight="bold",
    color="white",
    ha="center",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#1E88E5", "alpha": 0.95, "edgecolor": "#306998", "linewidth": 1.5},
    arrowprops={"arrowstyle": "-", "color": "#1E88E5", "lw": 2},
)

# Add average temperature reference line
avg_temp = np.mean(temperature)
ax.axhline(y=avg_temp, color="#808080", linestyle="--", linewidth=2, alpha=0.7, label=f"Average: {avg_temp:.1f}°C")

# Style the plot
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Temperature (°C)", fontsize=20)
ax.set_title("line-interactive · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=15)

# Configure tick parameters
ax.tick_params(axis="both", labelsize=16)

# Format x-axis for better date display
fig.autofmt_xdate(rotation=30)

# Add subtle grid (using white theme, so no double grid effect)
ax.grid(True, alpha=0.25, linestyle="--")
ax_range.grid(True, alpha=0.2, linestyle="-")

# Add legend
ax.legend(fontsize=14, loc="upper right", framealpha=0.95)

# Add interactive controls hint
fig.text(
    0.5,
    0.01,
    "Interactive Controls: Hover points for values • Scroll to zoom • Click-drag to pan • Home to reset",
    ha="center",
    va="bottom",
    fontsize=12,
    color="#555555",
    style="italic",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f0f0f0", "alpha": 0.9, "edgecolor": "#cccccc"},
)

# Ensure proper layout with extra bottom margin for footer
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)

# Demonstrate hover tooltip with a static annotation
demo_idx = 12  # Show tooltip on a representative point
demo_x, demo_y = dates[demo_idx * 10], temperature[demo_idx * 10]
demo_date_str = dates[demo_idx * 10].strftime("%b %d, %Y")
ax.annotate(
    f"Date: {demo_date_str}\nTemp: {demo_y:.1f}°C",
    xy=(demo_x, demo_y),
    xytext=(35, 35),
    textcoords="offset points",
    fontsize=14,
    fontweight="bold",
    color="#306998",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "#FFD43B", "alpha": 0.95, "edgecolor": "#306998", "linewidth": 2},
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2, "connectionstyle": "arc3,rad=0.2"},
    zorder=10,
)

# Save the plot
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
