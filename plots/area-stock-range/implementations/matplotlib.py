"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Generate 3 years of synthetic stock price data
np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=750, freq="B")  # Business days
returns = np.random.normal(0.0003, 0.015, len(dates))  # Daily returns
price = 100 * np.cumprod(1 + returns)  # Starting price $100

# Create figure with GridSpec for better layout control
fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.15)
ax_main = fig.add_subplot(gs[0])
ax_range = fig.add_subplot(gs[1])

# Main chart - Area plot with semi-transparent fill
ax_main.fill_between(dates, price, alpha=0.4, color="#306998", label="Price Range")
ax_main.plot(dates, price, color="#306998", linewidth=2.5, label="Closing Price")

# Styling for main chart
ax_main.set_ylabel("Price ($)", fontsize=20)
ax_main.set_title("Stock Price History · area-stock-range · matplotlib · pyplots.ai", fontsize=24)
ax_main.tick_params(axis="both", labelsize=16)
ax_main.grid(True, alpha=0.3, linestyle="--")
ax_main.legend(fontsize=16, loc="upper left")

# Format x-axis dates for main chart
ax_main.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax_main.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.setp(ax_main.xaxis.get_majorticklabels(), rotation=0)

# Calculate y-axis limits with padding
y_min, y_max = price.min(), price.max()
y_padding = (y_max - y_min) * 0.1
ax_main.set_ylim(y_min - y_padding, y_max + y_padding)

# Range selector subplot (navigator view showing full history)
ax_range.fill_between(dates, price, alpha=0.5, color="#306998")
ax_range.plot(dates, price, color="#306998", linewidth=1.5)

# Highlight a selected range (example: last 6 months)
selected_start = dates[-130]  # Approximately 6 months
selected_end = dates[-1]
ax_range.axvspan(selected_start, selected_end, alpha=0.25, color="#FFD43B")
ax_range.axvline(selected_start, color="#FFD43B", linewidth=3, linestyle="-")
ax_range.axvline(selected_end, color="#FFD43B", linewidth=3, linestyle="-")

# Styling for range selector
ax_range.set_xlabel("Date", fontsize=20)
ax_range.set_ylabel("Price", fontsize=14)
ax_range.tick_params(axis="both", labelsize=14)
ax_range.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax_range.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax_range.set_ylim(y_min - y_padding, y_max + y_padding)

# Add range selector label
ax_range.text(
    0.02,
    0.82,
    "Range Selector",
    transform=ax_range.transAxes,
    fontsize=14,
    fontweight="bold",
    color="#333333",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8},
)

# Add preset range indicators as text
preset_text = "1M  3M  6M  1Y  YTD  All"
ax_range.text(
    0.98,
    0.82,
    preset_text,
    transform=ax_range.transAxes,
    fontsize=12,
    ha="right",
    color="#555555",
    family="monospace",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8},
)

# Set x-axis limits: main chart shows selected range, range selector shows all
ax_main.set_xlim(selected_start, selected_end)
ax_range.set_xlim(dates[0], dates[-1])

# Remove top/right spines for cleaner look
for ax in [ax_main, ax_range]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
