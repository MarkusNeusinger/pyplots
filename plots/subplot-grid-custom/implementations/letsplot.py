# ruff: noqa: F405
"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()

# Set seed for reproducibility
np.random.seed(42)

# Generate sample data - Financial dashboard theme
n_days = 100
dates = pd.date_range("2024-01-01", periods=n_days, freq="D")

# Main time series - stock price
price_start = 100
returns = np.random.normal(0.001, 0.02, n_days)
price = price_start * np.cumprod(1 + returns)
volume = np.random.uniform(1e6, 5e6, n_days) * (1 + 0.5 * np.abs(returns))

# Daily returns for histogram
daily_returns = np.diff(price) / price[:-1] * 100

# Sector performance for bar chart
sectors = ["Tech", "Health", "Finance", "Energy"]
sector_returns = [12.5, 8.3, 5.1, -2.4]

# Correlation data for heatmap
assets = ["A", "B", "C", "D"]
corr_data = np.array(
    [[1.0, 0.65, 0.32, -0.15], [0.65, 1.0, 0.48, 0.22], [0.32, 0.48, 1.0, 0.55], [-0.15, 0.22, 0.55, 1.0]]
)

# Prepare DataFrames
df_price = pd.DataFrame({"Day": range(n_days), "Price": price})

df_volume = pd.DataFrame({"Day": range(n_days), "Volume": volume / 1e6})

df_returns = pd.DataFrame({"Return": daily_returns})

df_sectors = pd.DataFrame({"Sector": sectors, "Return": sector_returns})

# Heatmap data (long format)
heatmap_rows = []
for i, asset1 in enumerate(assets):
    for j, asset2 in enumerate(assets):
        heatmap_rows.append({"Asset1": asset1, "Asset2": asset2, "Correlation": corr_data[i, j]})
df_corr = pd.DataFrame(heatmap_rows)

# Theme settings for consistent styling
base_theme = theme_minimal() + theme(
    panel_grid_major=element_line(color="#E0E0E0", size=0.5), panel_grid_minor=element_blank()
)

# Main plot: Price time series (will span 2x2 in grid)
plot_main = (
    ggplot(df_price, aes(x="Day", y="Price"))
    + geom_line(color="#306998", size=2)
    + geom_area(fill="#306998", alpha=0.15)
    + labs(x="Trading Day", y="Price ($)", title="Stock Price")
    + base_theme
    + theme(
        axis_title=element_text(size=22), axis_text=element_text(size=18), plot_title=element_text(size=24, face="bold")
    )
    + ggsize(800, 500)
)

# Volume bar chart (spans 2 columns)
plot_volume = (
    ggplot(df_volume, aes(x="Day", y="Volume"))
    + geom_bar(stat="identity", fill="#FFD43B", alpha=0.8, width=1)
    + labs(x="Trading Day", y="Volume (M)", title="Trading Volume")
    + base_theme
    + theme(
        axis_title=element_text(size=18), axis_text=element_text(size=14), plot_title=element_text(size=20, face="bold")
    )
    + ggsize(800, 280)
)

# Returns histogram
plot_histogram = (
    ggplot(df_returns, aes(x="Return"))
    + geom_histogram(bins=20, fill="#306998", color="white", alpha=0.85)
    + labs(x="Daily Return (%)", y="Count", title="Returns")
    + base_theme
    + theme(
        axis_title=element_text(size=16), axis_text=element_text(size=13), plot_title=element_text(size=18, face="bold")
    )
    + ggsize(400, 350)
)

# Sector performance bar chart
plot_sectors = (
    ggplot(df_sectors, aes(x="Sector", y="Return", fill="Return"))
    + geom_bar(stat="identity", width=0.7)
    + scale_fill_gradient2(low="#DC2626", mid="#F5F5F5", high="#16A34A", midpoint=0)
    + labs(x="Sector", y="Return (%)", title="Sectors")
    + base_theme
    + theme(
        axis_title=element_text(size=16),
        axis_text=element_text(size=13),
        plot_title=element_text(size=18, face="bold"),
        legend_position="none",
    )
    + ggsize(400, 350)
)

# Correlation heatmap
plot_heatmap = (
    ggplot(df_corr, aes(x="Asset1", y="Asset2", fill="Correlation"))
    + geom_tile(color="white", size=1)
    + geom_text(aes(label="Correlation"), size=12, format=".2f", color="black")
    + scale_fill_gradient2(low="#DC2626", mid="white", high="#306998", midpoint=0, limits=[-1, 1])
    + labs(x="", y="", title="Correlations")
    + theme_minimal()
    + theme(
        axis_text=element_text(size=14),
        plot_title=element_text(size=18, face="bold"),
        panel_grid=element_blank(),
        legend_position="none",
    )
    + coord_fixed()
    + ggsize(350, 350)
)

# Create custom grid layout using ggbunch for precise positioning
# Layout demonstrates non-uniform cells with row/column spanning:
# - Main price chart: larger area (spans equivalent of 2x2)
# - Volume: wide chart below price
# - Histogram, Sectors, Heatmap: smaller panels on right side

# ggbunch regions: (x, y, width, height) in relative coordinates [0-1]
# x,y = position of top-left corner, width/height = size relative to container

plots = [
    plot_main,  # Large left panel
    plot_volume,  # Wide panel below main
    plot_histogram,  # Top right
    plot_sectors,  # Middle right
    plot_heatmap,  # Bottom right
]

regions = [
    (0.0, 0.1, 0.6, 0.5),  # Main: top-left, 60% wide, 50% tall
    (0.0, 0.6, 0.6, 0.4),  # Volume: below main, 60% wide, 40% tall
    (0.6, 0.1, 0.4, 0.3),  # Histogram: top-right, 40% wide, 30% tall
    (0.6, 0.4, 0.4, 0.3),  # Sectors: mid-right, 40% wide, 30% tall
    (0.6, 0.7, 0.4, 0.3),  # Heatmap: bottom-right, 40% wide, 30% tall
]

# Create the bunch with custom layout
bunch = ggbunch(plots, regions)

# Add size and title
final_plot = bunch + ggtitle("subplot-grid-custom · lets-plot · pyplots.ai") + ggsize(1600, 900)

# Save as PNG with scale for high resolution (target ~4800x2700)
ggsave(final_plot, "plot.png", path=".", scale=3)

# Save as HTML for interactivity
ggsave(final_plot, "plot.html", path=".")
