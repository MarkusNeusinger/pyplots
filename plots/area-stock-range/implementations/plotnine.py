""" pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_label,
    geom_line,
    geom_rect,
    geom_ribbon,
    geom_vline,
    ggplot,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - 2 years of simulated stock price data
np.random.seed(42)
n_days = 500  # ~2 years of trading days
dates = pd.date_range("2022-01-03", periods=n_days, freq="B")  # Business days

# Generate realistic stock price with trends and volatility
initial_price = 150.0
daily_returns = np.random.normal(0.0003, 0.015, n_days)

# Add some trend changes for interesting patterns
trend = np.zeros(n_days)
trend[0:100] = 0.001  # Bull run
trend[100:200] = -0.0008  # Correction
trend[200:350] = 0.0005  # Recovery
trend[350:420] = -0.0003  # Sideways/slight decline
trend[420:] = 0.0008  # Late rally

# Add volatility clusters
volatility_multiplier = np.ones(n_days)
volatility_multiplier[80:120] = 1.8  # High volatility period
volatility_multiplier[280:310] = 1.5  # Another volatile period
volatility_multiplier[400:430] = 2.0  # Major volatility

adjusted_returns = daily_returns * volatility_multiplier + trend
price = initial_price * np.cumprod(1 + adjusted_returns)

df = pd.DataFrame({"date": dates, "price": price})

# Define selected range for main view (simulating 6-month preset selection)
range_start = pd.Timestamp("2023-04-01")
range_end = pd.Timestamp("2023-10-01")

# Create two panels: Main view shows selected 6M range, Overview shows full history
df_main = df[(df["date"] >= range_start) & (df["date"] <= range_end)].copy()
df_main["panel"] = "Selected Range: Apr-Oct 2023 (6M)"

df_overview = df.copy()
df_overview["panel"] = "Range Selector · Full History"

df_combined = pd.concat([df_main, df_overview], ignore_index=True)

# Calculate y_min for ribbon baseline (for proper area fill without starting at 0)
# Use per-panel minimums for better y-axis utilization
df_combined["y_min"] = df_combined.groupby("panel")["price"].transform("min") * 0.95

# Ensure proper panel ordering (main view first, then overview)
df_combined["panel"] = pd.Categorical(
    df_combined["panel"],
    categories=["Selected Range: Apr-Oct 2023 (6M)", "Range Selector · Full History"],
    ordered=True,
)

# Create range highlight for overview panel
range_highlight = pd.DataFrame({"xmin": [range_start], "xmax": [range_end], "panel": ["Range Selector · Full History"]})
range_highlight["panel"] = pd.Categorical(
    range_highlight["panel"],
    categories=["Selected Range: Apr-Oct 2023 (6M)", "Range Selector · Full History"],
    ordered=True,
)

# Create annotation label for explaining the selection in the overview panel
selection_midpoint = range_start + (range_end - range_start) / 2
overview_price_range = df["price"].max() - df["price"].min()
annotation_y = df["price"].max() - overview_price_range * 0.15
annotation_df = pd.DataFrame(
    {
        "x": [selection_midpoint],
        "y": [annotation_y],
        "label": ["Selected\nTimeframe"],
        "panel": ["Range Selector · Full History"],
    }
)
annotation_df["panel"] = pd.Categorical(
    annotation_df["panel"],
    categories=["Selected Range: Apr-Oct 2023 (6M)", "Range Selector · Full History"],
    ordered=True,
)

# Plot - Stock area chart with faceted range selector
plot = (
    ggplot(df_combined, aes(x="date", y="price"))
    + geom_rect(
        data=range_highlight,
        mapping=aes(xmin="xmin", xmax="xmax"),
        ymin=-np.inf,
        ymax=np.inf,
        fill="#306998",
        alpha=0.2,
        inherit_aes=False,
    )
    + geom_vline(data=range_highlight, mapping=aes(xintercept="xmin"), color="#1a4971", size=1.2, linetype="dashed")
    + geom_vline(data=range_highlight, mapping=aes(xintercept="xmax"), color="#1a4971", size=1.2, linetype="dashed")
    + geom_label(
        data=annotation_df,
        mapping=aes(x="x", y="y", label="label"),
        fill="#ffffff",
        color="#1a4971",
        size=12,
        alpha=0.9,
        inherit_aes=False,
    )
    + geom_ribbon(aes(ymin="y_min", ymax="price"), fill="#306998", alpha=0.4)
    + geom_line(color="#306998", size=1.2)
    + facet_wrap("~panel", ncol=1, scales="free")
    + scale_x_datetime(date_labels="%b %Y", date_breaks="2 months")
    + scale_y_continuous(labels=lambda x: [f"${v:.0f}" for v in x])
    + labs(x="Date", y="Stock Price (USD)", title="area-stock-range · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(angle=45, ha="right"),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", size=0.5, alpha=0.3),
        panel_grid_minor=element_blank(),
        strip_text=element_text(size=16, weight="bold"),
        strip_background=element_rect(fill="#e8e8e8", color=None),
        panel_spacing=0.12,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
