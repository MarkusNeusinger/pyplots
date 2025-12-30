"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: matplotlib 3.10.8 | Python 3.13
Quality: 88/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import mplcursors
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

# Create the figure with interactive backend capabilities
fig, ax = plt.subplots(figsize=(16, 9))

# Main line plot
(line,) = ax.plot(dates, response_times, color="#306998", linewidth=2.5, label="Response Time", zorder=2)

# Add scatter points for hover targets (every 5th point for better interactivity)
scatter = ax.scatter(
    dates[::5],
    response_times[::5],
    color="#306998",
    s=100,
    alpha=0.8,
    edgecolors="white",
    linewidths=1.5,
    zorder=3,
    label="Data Points",
)

# Setup mplcursors for interactive hover tooltips on scatter points
cursor = mplcursors.cursor(scatter, hover=True)


@cursor.connect("add")
def on_add(sel):
    """Format hover tooltip with datetime and value."""
    idx = sel.index * 5  # Map back to original index
    date_str = dates[idx].strftime("%Y-%m-%d %H:%M")
    val = response_times[idx]
    sel.annotation.set_text(f"Time: {date_str}\nResponse: {val:.1f} ms")
    sel.annotation.get_bbox_patch().set(facecolor="#FFD43B", alpha=0.95)
    sel.annotation.set_fontsize(14)
    sel.annotation.set_fontweight("bold")


# Highlight anomaly spikes with visible annotations
for i, idx in enumerate(spike_indices):
    ax.scatter(
        dates[idx],
        response_times[idx],
        color="#E63946",
        s=250,
        edgecolors="#306998",
        linewidths=2.5,
        zorder=5,
        marker="^",
    )
    offset_y = 20 if i % 2 == 0 else -35
    ax.annotate(
        f"Anomaly: {response_times[idx]:.0f} ms",
        xy=(dates[idx], response_times[idx]),
        xytext=(0, offset_y),
        textcoords="offset points",
        fontsize=13,
        fontweight="bold",
        color="white",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#E63946", alpha=0.95, edgecolor="#306998", linewidth=1.5),
        arrowprops=dict(arrowstyle="-", color="#E63946", lw=2),
    )

# Add a reference line for average response time
avg_response = np.mean(response_times)
ax.axhline(
    y=avg_response, color="#808080", linestyle="--", linewidth=2, alpha=0.7, label=f"Average: {avg_response:.0f} ms"
)

# Highlight zoom region to demonstrate range selection capability
zoom_start, zoom_end = 70, 100
ax.axvspan(dates[zoom_start], dates[zoom_end], alpha=0.2, color="#2A9D8F", zorder=1)
ax.annotate(
    "Zoom Region\n(use scroll/drag)",
    xy=(dates[85], ax.get_ylim()[0] + 10),
    fontsize=12,
    ha="center",
    va="bottom",
    color="#2A9D8F",
    fontweight="bold",
)

# Style the plot
ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Response Time (ms)", fontsize=20)
ax.set_title("line-interactive · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=15)

# Configure tick parameters
ax.tick_params(axis="both", labelsize=16)

# Format x-axis for better date display
fig.autofmt_xdate(rotation=30)

# Add subtle grid (reduced alpha for busy chart)
ax.grid(True, alpha=0.2, linestyle="--", zorder=1)

# Add compact legend
ax.legend(fontsize=14, loc="upper left", framealpha=0.95)

# Add toolbar hint for navigation
fig.text(
    0.5,
    0.01,
    "Interactive Controls: Hover points for values • Scroll to zoom • Click-drag to pan • Home to reset",
    ha="center",
    va="bottom",
    fontsize=12,
    color="#555555",
    style="italic",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f0f0", alpha=0.9, edgecolor="#cccccc"),
)

# Ensure proper layout with extra bottom margin for footer
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)

# Simulate a hover state by programmatically adding an annotation at one point
# This demonstrates the hover tooltip that mplcursors provides
demo_idx = 15  # Show tooltip on a representative point
demo_x, demo_y = dates[demo_idx * 5], response_times[demo_idx * 5]
demo_date_str = dates[demo_idx * 5].strftime("%Y-%m-%d %H:%M")
ax.annotate(
    f"Time: {demo_date_str}\nResponse: {demo_y:.1f} ms",
    xy=(demo_x, demo_y),
    xytext=(30, 30),
    textcoords="offset points",
    fontsize=14,
    fontweight="bold",
    color="#306998",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFD43B", alpha=0.95, edgecolor="#306998", linewidth=2),
    arrowprops=dict(arrowstyle="->", color="#306998", lw=2, connectionstyle="arc3,rad=0.2"),
    zorder=10,
)

# Save the plot
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
