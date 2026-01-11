"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave


LetsPlot.setup_html()  # noqa: F405

# Generate realistic stock price data (2 years of daily prices)
np.random.seed(42)
n_days = 504  # ~2 years of trading days
dates = pd.date_range(start="2024-01-01", periods=n_days, freq="B")  # Business days

# Generate realistic price movements using geometric Brownian motion
initial_price = 150.0
drift = 0.0003
volatility = 0.018
returns = np.random.normal(drift, volatility, n_days)
prices = initial_price * np.cumprod(1 + returns)

# Add trend and seasonal patterns
trend = np.linspace(0, 30, n_days)
seasonal = 10 * np.sin(np.linspace(0, 4 * np.pi, n_days))
prices = prices + trend + seasonal

# Create main DataFrame with full price history
df_full = pd.DataFrame({"date": dates, "price": prices})
df_full["date_num"] = range(len(df_full))  # Numeric dates for positioning

# Define preset ranges for the range selector
preset_ranges = {
    "1M": 21,  # ~1 month trading days
    "3M": 63,  # ~3 months
    "6M": 126,  # ~6 months (current selection)
    "1Y": 252,  # ~1 year
    "YTD": None,  # Calculated below
    "All": n_days,
}

# Calculate YTD (days from Jan 1 of current year in data)
ytd_start = pd.Timestamp("2025-01-01")
ytd_days = len(df_full[df_full["date"] >= ytd_start])
preset_ranges["YTD"] = ytd_days

# Current selection: 6 months
selected_days = 126
range_start_idx = len(df_full) - selected_days
df_selected = df_full.iloc[range_start_idx:].copy()

# Y-axis limits with padding for main chart
price_min = df_selected["price"].min()
price_max = df_selected["price"].max()
price_range = price_max - price_min
y_min = price_min - price_range * 0.05
y_max = price_max + price_range * 0.1

# Tooltips for interactive exploration (HTML)
main_tooltips = (
    layer_tooltips()  # noqa: F405
    .title("Stock Price")
    .line("Date: @date")
    .line("Price: $@{price}")
    .format("price", ".2f")
)

# Create gradient effect data - multiple ribbons with decreasing alpha from top to bottom
# This simulates a gradient fill effect by layering ribbons
n_gradient_bands = 5
gradient_dfs = []
for i in range(n_gradient_bands):
    band_df = df_selected.copy()
    # Each band covers a portion of the area from bottom (y_min) to price
    band_df["y_lower"] = y_min + (band_df["price"] - y_min) * (i / n_gradient_bands)
    band_df["y_upper"] = y_min + (band_df["price"] - y_min) * ((i + 1) / n_gradient_bands)
    band_df["alpha_level"] = i  # Track which band for alpha assignment
    gradient_dfs.append(band_df)
df_gradient = pd.concat(gradient_dfs, ignore_index=True)

# Main area chart - selected range with gradient effect
main_chart = (
    ggplot(df_selected, aes(x="date", y="price"))  # noqa: F405
    # Gradient bands - bottom bands lighter (lower alpha), top bands darker
    + geom_ribbon(  # noqa: F405
        aes(x="date", ymin="y_lower", ymax="y_upper"),  # noqa: F405
        data=gradient_dfs[0],
        fill="#306998",
        alpha=0.10,
        inherit_aes=False,
    )
    + geom_ribbon(  # noqa: F405
        aes(x="date", ymin="y_lower", ymax="y_upper"),  # noqa: F405
        data=gradient_dfs[1],
        fill="#306998",
        alpha=0.18,
        inherit_aes=False,
    )
    + geom_ribbon(  # noqa: F405
        aes(x="date", ymin="y_lower", ymax="y_upper"),  # noqa: F405
        data=gradient_dfs[2],
        fill="#306998",
        alpha=0.26,
        inherit_aes=False,
    )
    + geom_ribbon(  # noqa: F405
        aes(x="date", ymin="y_lower", ymax="y_upper"),  # noqa: F405
        data=gradient_dfs[3],
        fill="#306998",
        alpha=0.34,
        inherit_aes=False,
    )
    + geom_ribbon(  # noqa: F405
        aes(x="date", ymin="y_lower", ymax="y_upper"),  # noqa: F405
        data=gradient_dfs[4],
        fill="#306998",
        alpha=0.42,
        inherit_aes=False,
    )
    + geom_line(color="#306998", size=1.5, tooltips=main_tooltips)  # noqa: F405
    + labs(x="", y="Price (USD)")  # noqa: F405
    + scale_x_datetime()  # noqa: F405
    + scale_y_continuous(limits=[y_min, y_max])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        panel_grid_major=element_line(color="#D8D8D8", size=0.4),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 600)  # noqa: F405
)

# Navigator/mini chart showing full data range with selection highlight
# Create selection rectangle data
select_xmin = df_full["date"].iloc[range_start_idx]
select_xmax = df_full["date"].iloc[-1]
nav_y_min = df_full["price"].min() - 5
nav_y_max = df_full["price"].max() + 5

selection_rect = pd.DataFrame({"xmin": [select_xmin], "xmax": [select_xmax], "ymin": [nav_y_min], "ymax": [nav_y_max]})

# Navigator chart - full data range with selection rectangle
navigator = (
    ggplot(df_full, aes(x="date", y="price"))  # noqa: F405
    # Selection rectangle (highlight selected region)
    + geom_rect(  # noqa: F405
        aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),  # noqa: F405
        data=selection_rect,
        inherit_aes=False,
        fill="#306998",
        alpha=0.15,
        color="#306998",
        linetype="solid",
        size=1,
    )
    # Full price area
    + geom_area(fill="#306998", alpha=0.25, tooltips="none")  # noqa: F405
    + geom_line(color="#306998", size=0.8, tooltips="none")  # noqa: F405
    + labs(x="Date", y="Price")  # noqa: F405
    + scale_x_datetime()  # noqa: F405
    + scale_y_continuous(limits=[nav_y_min, nav_y_max])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title_x=element_text(size=16),  # noqa: F405
        axis_title_y=element_text(size=12),  # noqa: F405
        axis_text=element_text(size=11),  # noqa: F405
        panel_grid=element_line(color="#E8E8E8", size=0.3),  # noqa: F405
    )
    + ggsize(1600, 150)  # noqa: F405
)

# Preset range buttons panel - styled as UI buttons
button_labels = ["1M", "3M", "6M", "1Y", "YTD", "All"]
buttons_df = pd.DataFrame(
    {
        "x": list(range(len(button_labels))),
        "y": [1] * len(button_labels),
        "label": button_labels,
        "selected": [label == "6M" for label in button_labels],  # 6M is currently active
    }
)

# Button styling: selected button is highlighted with border, others have subtle fill
buttons_df["fill_color"] = buttons_df["selected"].map({True: "#306998", False: "#F5F5F5"})
buttons_df["text_color"] = buttons_df["selected"].map({True: "white", False: "#444444"})
buttons_df["border_color"] = buttons_df["selected"].map({True: "#1E4A6E", False: "#CCCCCC"})

buttons_panel = (
    ggplot(buttons_df, aes(x="x", y="y"))  # noqa: F405
    # Button backgrounds - compact, UI-like appearance
    + geom_tile(  # noqa: F405
        aes(fill="fill_color", color="border_color"),  # noqa: F405
        width=0.75,
        height=0.5,
        size=1.0,
    )
    # Button labels
    + geom_text(  # noqa: F405
        aes(label="label", color="text_color"),  # noqa: F405
        size=12,
        fontface="bold",  # noqa: F405
    )
    + scale_fill_identity()  # noqa: F405
    + scale_color_identity()  # noqa: F405
    + scale_x_continuous(limits=[-0.6, len(button_labels) - 0.4])  # noqa: F405
    + scale_y_continuous(limits=[0.6, 1.4])  # noqa: F405
    + labs(title="Range Selection")  # noqa: F405
    + theme_void()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=12, color="#888888", hjust=0.5)  # noqa: F405
    )
    + ggsize(1600, 70)  # noqa: F405
)

# Combine all panels using gggrid
combined = gggrid(  # noqa: F405
    [main_chart, navigator, buttons_panel], ncol=1, heights=[6, 1.5, 0.8], align=True
)

# Add overall title
combined = (
    combined
    + ggtitle("area-stock-range · letsplot · pyplots.ai")  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + theme(plot_title=element_text(size=26, face="bold"))  # noqa: F405
)

# Save PNG (scale 3x for 4800x2700 px output)
ggsave(combined, "plot.png", path=".", scale=3)

# Save interactive HTML (pan, zoom, tooltips available in HTML viewer)
ggsave(combined, "plot.html", path=".")
