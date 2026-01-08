"""pyplots.ai
renko-basic: Basic Renko Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Generate sample price data (simulating stock prices)
np.random.seed(42)
n_days = 200
dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
# Simulate price with random walk
returns = np.random.normal(0.001, 0.02, n_days)
prices = 100 * np.cumprod(1 + returns)

# Renko chart parameters
brick_size = 2.0  # $2 brick size

# Calculate Renko bricks
bricks = []
current_price = prices[0]
brick_start = (current_price // brick_size) * brick_size
direction = None  # 1 for up, -1 for down

for price in prices:
    while True:
        if direction is None:
            # Initial direction
            if price >= brick_start + brick_size:
                bricks.append({"bottom": brick_start, "top": brick_start + brick_size, "direction": 1})
                brick_start += brick_size
                direction = 1
            elif price <= brick_start - brick_size:
                bricks.append({"bottom": brick_start - brick_size, "top": brick_start, "direction": -1})
                brick_start -= brick_size
                direction = -1
            else:
                break
        elif direction == 1:
            # Currently in uptrend
            if price >= brick_start + brick_size:
                bricks.append({"bottom": brick_start, "top": brick_start + brick_size, "direction": 1})
                brick_start += brick_size
            elif price <= brick_start - 2 * brick_size:
                # Reversal requires 2 bricks in opposite direction
                brick_start -= brick_size
                bricks.append({"bottom": brick_start - brick_size, "top": brick_start, "direction": -1})
                brick_start -= brick_size
                direction = -1
            else:
                break
        else:
            # Currently in downtrend
            if price <= brick_start - brick_size:
                bricks.append({"bottom": brick_start - brick_size, "top": brick_start, "direction": -1})
                brick_start -= brick_size
            elif price >= brick_start + 2 * brick_size:
                # Reversal requires 2 bricks in opposite direction
                brick_start += brick_size
                bricks.append({"bottom": brick_start, "top": brick_start + brick_size, "direction": 1})
                brick_start += brick_size
                direction = 1
            else:
                break

# Create DataFrame for plotting
brick_df = pd.DataFrame(bricks)
brick_df["x"] = range(len(brick_df))
brick_df["color"] = brick_df["direction"].map({1: "Bullish", -1: "Bearish"})
# Add small gap between bricks
gap = 0.1
brick_df["xmin"] = brick_df["x"] - 0.4 + gap / 2
brick_df["xmax"] = brick_df["x"] + 0.4 - gap / 2

# Create the plot
plot = (
    ggplot(brick_df)
    + geom_rect(aes(xmin="xmin", xmax="xmax", ymin="bottom", ymax="top", fill="color"), color="white", size=0.5)
    + scale_fill_manual(values={"Bullish": "#22C55E", "Bearish": "#EF4444"})
    + labs(title="renko-basic · letsplot · pyplots.ai", x="Brick Index", y="Price ($)", fill="Direction")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        panel_grid_major=element_line(color="#E5E5E5", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactivity
ggsave(plot, "plot.html", path=".")
