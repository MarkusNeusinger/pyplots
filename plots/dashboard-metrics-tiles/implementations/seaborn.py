"""pyplots.ai
dashboard-metrics-tiles: Real-Time Dashboard Tiles
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import matplotlib.pyplot as plt
import numpy as np


np.random.seed(42)

# Metric data - 6 tiles in 3x2 grid
metrics = [
    {
        "name": "CPU Usage",
        "value": 45,
        "unit": "%",
        "history": np.cumsum(np.random.randn(30)) + 50,
        "change": -5.2,
        "status": "good",
    },
    {
        "name": "Memory",
        "value": 72,
        "unit": "%",
        "history": np.cumsum(np.random.randn(30)) + 70,
        "change": 8.1,
        "status": "warning",
    },
    {
        "name": "Response Time",
        "value": 120,
        "unit": "ms",
        "history": np.cumsum(np.random.randn(30)) + 130,
        "change": -15.3,
        "status": "good",
    },
    {
        "name": "Active Users",
        "value": 1847,
        "unit": "",
        "history": np.cumsum(np.random.randn(30)) * 50 + 1800,
        "change": 12.7,
        "status": "good",
    },
    {
        "name": "Error Rate",
        "value": 2.3,
        "unit": "%",
        "history": np.cumsum(np.random.randn(30)) * 0.5 + 2,
        "change": 45.0,
        "status": "critical",
    },
    {
        "name": "Throughput",
        "value": 892,
        "unit": "req/s",
        "history": np.cumsum(np.random.randn(30)) * 30 + 850,
        "change": -3.4,
        "status": "good",
    },
]

# Status colors
status_colors = {"good": "#28a745", "warning": "#ffc107", "critical": "#dc3545"}

# Create figure with 3x2 grid
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

for ax, metric in zip(axes, metrics, strict=True):
    # Tile background
    ax.set_facecolor("#f8f9fa")
    for spine in ax.spines.values():
        spine.set_color("#dee2e6")
        spine.set_linewidth(2)

    # Clear axis ticks for clean tile look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Metric name (top)
    ax.text(0.5, 9.2, metric["name"], fontsize=18, fontweight="bold", color="#495057", ha="center", va="top")

    # Main value (center, large)
    value_text = f"{metric['value']:,}{metric['unit']}" if metric["unit"] else f"{metric['value']:,}"
    ax.text(
        5,
        6.0,
        value_text,
        fontsize=42,
        fontweight="bold",
        color=status_colors[metric["status"]],
        ha="center",
        va="center",
    )

    # Change indicator with arrow
    change = metric["change"]
    arrow = "▲" if change >= 0 else "▼"

    # Determine if change is favorable based on metric type
    # For CPU, Memory, Response Time, Error Rate: lower is better (decrease = green)
    # For Active Users, Throughput: higher is better (increase = green)
    decrease_is_good = metric["name"] in ["CPU Usage", "Memory", "Response Time", "Error Rate"]

    if decrease_is_good:
        change_color = "#28a745" if change < 0 else "#dc3545"
    else:
        change_color = "#28a745" if change >= 0 else "#dc3545"

    change_text = f"{arrow} {abs(change):.1f}%"
    ax.text(5, 3.8, change_text, fontsize=18, fontweight="bold", color=change_color, ha="center", va="center")

    # Sparkline at bottom
    history = metric["history"]
    history_norm = (history - history.min()) / (history.max() - history.min() + 1e-9)
    x_spark = np.linspace(1, 9, len(history))
    y_spark = history_norm * 1.8 + 0.8

    ax.plot(x_spark, y_spark, color=status_colors[metric["status"]], linewidth=2.5, alpha=0.8)
    ax.fill_between(x_spark, 0.5, y_spark, color=status_colors[metric["status"]], alpha=0.15)

# Main title
fig.suptitle("dashboard-metrics-tiles · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
