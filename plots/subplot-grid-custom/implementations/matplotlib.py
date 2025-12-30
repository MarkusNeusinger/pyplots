"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

# Time series data for main plot (spanning 2 columns)
dates = pd.date_range("2024-01-01", periods=120, freq="D")
base_price = 100
returns = np.random.randn(120) * 0.02
prices = base_price * np.cumprod(1 + returns)

# Volume data for bar chart
volume = np.random.uniform(1e6, 5e6, 120)

# Returns distribution for histogram
daily_returns = np.diff(prices) / prices[:-1] * 100

# Scatter data for correlation plot
x_corr = np.random.randn(50) * 10 + 50
y_corr = x_corr * 0.7 + np.random.randn(50) * 5

# Category data for bar chart
categories = ["A", "B", "C", "D"]
values = [85, 72, 93, 67]

# Create figure with GridSpec (custom layout)
fig = plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[2, 1, 1], wspace=0.35, hspace=0.5)

# Main plot: Time series spanning 2 columns and 2 rows (top-left)
ax_main = fig.add_subplot(gs[0:2, 0:2])
ax_main.plot(dates, prices, color="#306998", linewidth=2.5, label="Price")
ax_main.fill_between(dates, prices.min() * 0.95, prices, alpha=0.2, color="#306998")
ax_main.set_xlabel("Date", fontsize=18)
ax_main.set_ylabel("Price ($)", fontsize=18)
ax_main.set_title("Price Trend (Main View)", fontsize=20, fontweight="bold")
ax_main.tick_params(axis="both", labelsize=14)
ax_main.grid(True, alpha=0.3, linestyle="--")
ax_main.legend(fontsize=14, loc="upper left")
# Format date labels to avoid overlap
ax_main.xaxis.set_major_locator(mdates.MonthLocator())
ax_main.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

# Top right: Correlation scatter plot
ax_scatter = fig.add_subplot(gs[0, 2])
ax_scatter.scatter(x_corr, y_corr, s=150, alpha=0.7, color="#FFD43B", edgecolor="#306998", linewidth=1.5)
ax_scatter.set_xlabel("Variable X", fontsize=16)
ax_scatter.set_ylabel("Variable Y", fontsize=16)
ax_scatter.set_title("Correlation", fontsize=18, fontweight="bold")
ax_scatter.tick_params(axis="both", labelsize=12)
ax_scatter.grid(True, alpha=0.3, linestyle="--")

# Middle right: Category bar chart
ax_bar = fig.add_subplot(gs[1, 2])
bars = ax_bar.bar(
    categories, values, color=["#306998", "#FFD43B", "#306998", "#FFD43B"], edgecolor="white", linewidth=2
)
ax_bar.set_xlabel("Product", fontsize=16)
ax_bar.set_ylabel("Score", fontsize=16)
ax_bar.set_title("Performance", fontsize=18, fontweight="bold")
ax_bar.tick_params(axis="both", labelsize=12)
ax_bar.set_ylim(0, 110)
for bar, val in zip(bars, values, strict=True):
    ax_bar.text(bar.get_x() + bar.get_width() / 2, val + 3, str(val), ha="center", fontsize=12, fontweight="bold")

# Bottom left: Volume bar chart
ax_volume = fig.add_subplot(gs[2, 0])
ax_volume.bar(range(len(volume)), volume / 1e6, color="#306998", alpha=0.7, width=1.0)
ax_volume.set_xlabel("Days", fontsize=16)
ax_volume.set_ylabel("Volume (M)", fontsize=16)
ax_volume.set_title("Daily Volume", fontsize=18, fontweight="bold")
ax_volume.tick_params(axis="both", labelsize=12)
ax_volume.set_xlim(0, len(volume))

# Bottom middle: Returns histogram
ax_hist = fig.add_subplot(gs[2, 1])
ax_hist.hist(daily_returns, bins=25, color="#FFD43B", edgecolor="#306998", linewidth=1.5, alpha=0.8)
ax_hist.axvline(0, color="#306998", linestyle="--", linewidth=2)
ax_hist.set_xlabel("Daily Return (%)", fontsize=16)
ax_hist.set_ylabel("Frequency", fontsize=16)
ax_hist.set_title("Return Distribution", fontsize=18, fontweight="bold")
ax_hist.tick_params(axis="both", labelsize=12)

# Bottom right: Summary statistics text box
ax_stats = fig.add_subplot(gs[2, 2])
ax_stats.axis("off")
stats_text = (
    f"Start Price: ${base_price:.2f}\n"
    f"End Price: ${prices[-1]:.2f}\n"
    f"Total Return: {(prices[-1] / base_price - 1) * 100:.1f}%\n"
    f"Avg Daily Vol: {np.mean(volume) / 1e6:.1f}M\n"
    f"Volatility: {np.std(daily_returns):.2f}%"
)
ax_stats.text(
    0.5,
    0.45,
    stats_text,
    transform=ax_stats.transAxes,
    fontsize=15,
    verticalalignment="center",
    horizontalalignment="center",
    bbox={"boxstyle": "round,pad=0.6", "facecolor": "#306998", "alpha": 0.1, "edgecolor": "#306998", "linewidth": 2},
    family="monospace",
    linespacing=1.8,
)
ax_stats.set_title("Summary Stats", fontsize=18, fontweight="bold")

# Overall title
fig.suptitle("subplot-grid-custom · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.99)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
