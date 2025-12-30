""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Server response time metrics (realistic monitoring scenario)
np.random.seed(42)
n_points = 200

# Generate datetime index for one week of hourly data
dates = pd.date_range("2024-01-01", periods=n_points, freq="h")

# Generate realistic server response times with patterns
base_response = 120  # Base response time in ms
daily_pattern = 30 * np.sin(2 * np.pi * np.arange(n_points) / 24)  # Daily cycle
weekly_pattern = 15 * np.sin(2 * np.pi * np.arange(n_points) / 168)  # Weekly cycle
noise = np.random.normal(0, 10, n_points)
trend = np.linspace(0, 20, n_points)  # Slight upward trend

# Add some spike anomalies
response_times = base_response + daily_pattern + weekly_pattern + noise + trend
spike_indices = [45, 120, 175]
for idx in spike_indices:
    response_times[idx] += np.random.uniform(50, 100)

# Create the plot
fig, ax = plt.subplots(figsize=(16, 9))

# Main line plot with markers for data point visibility
ax.plot(dates, response_times, color="#306998", linewidth=2.5, label="Response Time", zorder=2)

# Add scatter points to show data density (smaller markers for large dataset)
ax.scatter(
    dates[::10], response_times[::10], color="#306998", s=80, alpha=0.7, edgecolors="white", linewidths=1.5, zorder=3
)

# Highlight anomaly spikes
for idx in spike_indices:
    ax.scatter(dates[idx], response_times[idx], color="#FFD43B", s=200, edgecolors="#306998", linewidths=2, zorder=4)
    ax.annotate(
        f"{response_times[idx]:.0f} ms",
        xy=(dates[idx], response_times[idx]),
        xytext=(10, 15),
        textcoords="offset points",
        fontsize=14,
        fontweight="bold",
        color="#306998",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFD43B", alpha=0.9),
        arrowprops=dict(arrowstyle="->", color="#306998", lw=1.5),
    )

# Add a reference line for average response time
avg_response = np.mean(response_times)
ax.axhline(
    y=avg_response, color="#808080", linestyle="--", linewidth=2, alpha=0.6, label=f"Average ({avg_response:.0f} ms)"
)

# Fill area to highlight a zoomed region concept
zoom_start, zoom_end = 70, 100
ax.axvspan(dates[zoom_start], dates[zoom_end], alpha=0.15, color="#FFD43B", label="Focus Region")

# Style the plot
ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Response Time (ms)", fontsize=20)
ax.set_title("line-interactive · matplotlib · pyplots.ai", fontsize=24, fontweight="bold")

# Configure tick parameters
ax.tick_params(axis="both", labelsize=16)

# Format x-axis for better date display
fig.autofmt_xdate(rotation=30)

# Add grid
ax.grid(True, alpha=0.3, linestyle="--", zorder=1)

# Add legend
ax.legend(fontsize=16, loc="upper left", framealpha=0.95)

# Add interactive hint annotation
ax.annotate(
    "Interactive: Hover for values, scroll to zoom, drag to pan",
    xy=(0.5, 0.02),
    xycoords="axes fraction",
    fontsize=14,
    ha="center",
    va="bottom",
    color="#555555",
    style="italic",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8, edgecolor="#cccccc"),
)

# Ensure proper layout
plt.tight_layout()

# Save the plot
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
