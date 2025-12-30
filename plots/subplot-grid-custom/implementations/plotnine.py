"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    geom_bar,
    geom_histogram,
    geom_line,
    geom_point,
    ggplot,
    labs,
    scale_fill_manual,
    stat_smooth,
    theme,
    theme_minimal,
)


# Data - Investment Portfolio Dashboard
np.random.seed(42)

# Main time series: Daily portfolio value over 60 days
n_days = 60
dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
portfolio_value = 100000 + np.cumsum(np.random.randn(n_days) * 500 + 50)
df_portfolio = pd.DataFrame({"day": range(n_days), "value": portfolio_value, "date": dates})

# Volume/Activity data - Trading volume per day
volume = np.abs(np.random.randn(n_days) * 1000 + 3000)
df_volume = pd.DataFrame({"day": range(n_days), "volume": volume})

# Asset allocation (pie chart equivalent - bar chart for plotnine)
assets = ["Stocks", "Bonds", "Real Estate", "Cash"]
allocations = [55, 25, 12, 8]
df_allocation = pd.DataFrame(
    {"asset": pd.Categorical(assets, categories=assets, ordered=True), "allocation": allocations}
)

# Daily returns distribution
returns = np.diff(portfolio_value) / portfolio_value[:-1] * 100
df_returns = pd.DataFrame({"returns": returns})

# Colors
colors = ["#306998", "#FFD43B", "#4A8BBF", "#E07A5F"]

# Shared theme - sized for 4800x2700 canvas
base_theme = theme_minimal() + theme(
    plot_title=element_text(size=18, face="bold", ha="center", margin={"b": 8}),
    axis_title=element_text(size=16),
    axis_text=element_text(size=13),
    legend_text=element_text(size=13),
    legend_title=element_text(size=14, face="bold"),
    panel_grid_major=element_line(color="#cccccc", alpha=0.3),
    panel_grid_minor=element_line(color="#eeeeee", alpha=0.2),
    panel_background=element_rect(fill="white"),
    plot_margin=0.01,
)

# Small theme for right-side panels (more compact titles)
small_theme = base_theme + theme(
    plot_title=element_text(size=16, face="bold", margin={"b": 5, "t": 5}),
    axis_title=element_text(size=14),
    axis_text=element_text(size=11),
)

# Main Plot (spans full left side): Portfolio Value Over Time
p_main = (
    ggplot(df_portfolio, aes(x="day", y="value"))
    + geom_line(size=1.8, color="#306998")
    + geom_point(size=2.5, color="#306998", alpha=0.6)
    + stat_smooth(method="lm", se=True, color="#FFD43B", fill="#FFD43B", alpha=0.2, size=1.2)
    + labs(title="Portfolio Value Trend", x="Trading Day", y="Portfolio Value ($)")
    + base_theme
    + theme(plot_title=element_text(size=22, margin={"b": 10, "t": 40}))
)

# Top Right: Asset Allocation (horizontal bar chart)
p_allocation = (
    ggplot(df_allocation, aes(x="asset", y="allocation", fill="asset"))
    + geom_bar(stat="identity", width=0.7, show_legend=False)
    + scale_fill_manual(values=colors)
    + labs(title="Asset Allocation", x="", y="Allocation (%)")
    + small_theme
    + theme(axis_text_x=element_text(size=11, angle=0))
)

# Middle Right: Trading Volume
p_volume = (
    ggplot(df_volume, aes(x="day", y="volume"))
    + geom_bar(stat="identity", fill="#306998", alpha=0.7, width=0.8)
    + labs(title="Daily Trading Volume", x="Trading Day", y="Volume (Units)")
    + small_theme
)

# Bottom Right: Returns Distribution
p_returns = (
    ggplot(df_returns, aes(x="returns"))
    + geom_histogram(bins=15, fill="#FFD43B", color="#306998", alpha=0.8, size=0.5)
    + labs(title="Returns Distribution", x="Daily Return (%)", y="Frequency")
    + small_theme
)

# Create custom grid layout using plotnine composition operators
# Layout: Main plot (full height left) | 3 stacked smaller plots (right column)
# This creates a dashboard with main visualization and supporting detail panels
right_column = p_allocation / p_volume / p_returns
custom_grid = p_main | right_column

# Draw and customize the figure
fig = custom_grid.draw()

# Set figure size for 4800x2700 px at 300 DPI
fig.set_size_inches(16, 9)

# Adjust subplot spacing for clean layout with main title
fig.subplots_adjust(top=0.88, bottom=0.08, left=0.06, right=0.98, hspace=0.35, wspace=0.18)

# Add main title positioned above all subplot titles
fig.suptitle("subplot-grid-custom · plotnine · pyplots.ai", fontsize=28, fontweight="bold", y=0.98)

# Save
fig.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
