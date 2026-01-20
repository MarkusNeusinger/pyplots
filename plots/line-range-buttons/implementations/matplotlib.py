"""pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Generate 2 years of daily data
np.random.seed(42)
dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
n_points = len(dates)

# Create realistic price-like data with trend and volatility
trend = np.linspace(100, 150, n_points)
noise = np.cumsum(np.random.randn(n_points) * 0.5)
seasonal = 10 * np.sin(np.linspace(0, 4 * np.pi, n_points))
values = trend + noise + seasonal

# Create DataFrame
df = pd.DataFrame({"date": dates, "value": values})

# Define range buttons and their date ranges
buttons_config = [
    ("1M", pd.Timedelta(days=30)),
    ("3M", pd.Timedelta(days=90)),
    ("6M", pd.Timedelta(days=180)),
    ("YTD", "ytd"),
    ("1Y", pd.Timedelta(days=365)),
    ("All", "all"),
]

# Select active button (3M for demonstration)
active_button = "3M"

# Calculate date range based on active button
end_date = df["date"].max()
if active_button == "YTD":
    start_date = pd.Timestamp(f"{end_date.year}-01-01")
elif active_button == "All":
    start_date = df["date"].min()
else:
    delta = [b[1] for b in buttons_config if b[0] == active_button][0]
    start_date = end_date - delta

# Filter data to selected range
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_filtered = df[mask]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot the line chart
ax.plot(df_filtered["date"], df_filtered["value"], color="#306998", linewidth=3, solid_capstyle="round")

# Fill under the line for visual appeal
ax.fill_between(df_filtered["date"], df_filtered["value"], alpha=0.15, color="#306998")

# Style the main plot
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("line-range-buttons · matplotlib · pyplots.ai", fontsize=24, pad=50)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Set y-axis to start from a reasonable value (not 0)
y_min = df_filtered["value"].min()
y_max = df_filtered["value"].max()
y_margin = (y_max - y_min) * 0.1
ax.set_ylim(y_min - y_margin, y_max + y_margin)

# Format x-axis dates
fig.autofmt_xdate(rotation=30)

# Add range selector buttons at the top
button_y = 0.94  # Position buttons near the top
button_width = 0.08
button_height = 0.05
button_spacing = 0.01
start_x = 0.15

for i, (label, _) in enumerate(buttons_config):
    x_pos = start_x + i * (button_width + button_spacing)

    # Determine button style based on whether it's active
    if label == active_button:
        facecolor = "#306998"
        edgecolor = "#306998"
        textcolor = "white"
        linewidth = 2
    else:
        facecolor = "#f0f0f0"
        edgecolor = "#cccccc"
        textcolor = "#666666"
        linewidth = 1

    # Create button-like rectangle using figure coordinates
    rect = mpatches.FancyBboxPatch(
        (x_pos, button_y),
        button_width,
        button_height,
        boxstyle="round,pad=0.01,rounding_size=0.015",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        transform=fig.transFigure,
        clip_on=False,
    )
    fig.patches.append(rect)

    # Add button text
    fig.text(
        x_pos + button_width / 2,
        button_y + button_height / 2,
        label,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=textcolor,
        transform=fig.transFigure,
    )

# Add a subtitle showing current range
range_text = f"Showing: {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"
fig.text(0.5, 0.88, range_text, ha="center", va="center", fontsize=14, color="#666666", transform=fig.transFigure)

# Adjust layout to make room for buttons
plt.subplots_adjust(top=0.84)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
