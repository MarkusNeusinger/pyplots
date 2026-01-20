""" pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-20
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seaborn style
sns.set_theme(style="whitegrid")

# Generate 2 years of daily data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
n_days = len(dates)

# Create realistic time series with trend and seasonality
trend = np.linspace(100, 180, n_days)
seasonality = 15 * np.sin(np.linspace(0, 4 * np.pi, n_days))
noise = np.random.normal(0, 5, n_days)
values = trend + seasonality + noise

df = pd.DataFrame({"date": dates, "value": values})

# Filter to show 1Y range (as the "active" selection)
end_date = dates[-1]
start_date = end_date - pd.DateOffset(years=1)
df_filtered = df[df["date"] >= start_date].copy()

# Create figure with extra space at top for buttons
fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(top=0.85)

# Plot line chart
sns.lineplot(data=df_filtered, x="date", y="value", ax=ax, linewidth=2.5, color="#306998")

# Style the plot
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("line-range-buttons · seaborn · pyplots.ai", fontsize=24, pad=60)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Fill area under the line (from y-axis minimum for better visual)
y_min = df_filtered["value"].min() - 5
ax.fill_between(df_filtered["date"], y_min, df_filtered["value"], alpha=0.2, color="#306998")
ax.set_ylim(bottom=y_min)

# Add range selector buttons as visual elements
buttons = ["1M", "3M", "6M", "YTD", "1Y", "All"]
active_button = "1Y"

# Button positioning
button_y = 0.92
button_width = 0.08
button_height = 0.05
button_spacing = 0.02
total_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
start_x = 0.5 - total_width / 2

for i, btn_text in enumerate(buttons):
    x_pos = start_x + i * (button_width + button_spacing)

    # Determine button style
    if btn_text == active_button:
        facecolor = "#306998"
        textcolor = "white"
        edgecolor = "#306998"
    else:
        facecolor = "#f0f0f0"
        textcolor = "#333333"
        edgecolor = "#cccccc"

    # Create button rectangle
    btn = mpatches.FancyBboxPatch(
        (x_pos, button_y - button_height / 2),
        button_width,
        button_height,
        boxstyle="round,pad=0.01,rounding_size=0.01",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=2,
        transform=fig.transFigure,
    )
    fig.patches.append(btn)

    # Add button text
    fig.text(
        x_pos + button_width / 2,
        button_y,
        btn_text,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=textcolor,
    )

# Format x-axis dates
ax.xaxis.set_major_locator(plt.MaxNLocator(8))
fig.autofmt_xdate(rotation=30)

plt.tight_layout(rect=[0, 0, 1, 0.88])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
