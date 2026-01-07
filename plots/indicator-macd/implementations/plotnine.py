"""pyplots.ai
indicator-macd: MACD Technical Indicator Chart
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_bar,
    geom_hline,
    geom_line,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
)


# Data - Generate realistic MACD data from simulated price movement
np.random.seed(42)
n_periods = 120

# Generate random walk price data
returns = np.random.normal(0.0005, 0.02, n_periods + 50)
price = 100 * np.cumprod(1 + returns)

# Calculate EMAs (inline calculation)
price_series = pd.Series(price)
ema_12 = price_series.ewm(span=12, adjust=False).mean().values
ema_26 = price_series.ewm(span=26, adjust=False).mean().values

# Calculate MACD components (skip warmup period)
macd_line = ema_12 - ema_26
signal_line = pd.Series(macd_line).ewm(span=9, adjust=False).mean().values
histogram = macd_line - signal_line

# Create DataFrame with last n_periods
df = pd.DataFrame(
    {
        "date": pd.date_range("2024-01-01", periods=n_periods, freq="D"),
        "macd": macd_line[-n_periods:],
        "signal": signal_line[-n_periods:],
        "histogram": histogram[-n_periods:],
    }
)
df["bar_color"] = np.where(df["histogram"] >= 0, "Positive", "Negative")

# Reshape data for lines
df_lines = pd.melt(df[["date", "macd", "signal"]], id_vars=["date"], var_name="line_type", value_name="value")

# Plot
plot = (
    ggplot()
    + geom_bar(data=df, mapping=aes(x="date", y="histogram", fill="bar_color"), stat="identity", width=0.8)
    + geom_hline(yintercept=0, color="#888888", size=0.5, linetype="solid")
    + geom_line(data=df_lines, mapping=aes(x="date", y="value", color="line_type"), size=1.5)
    + scale_fill_manual(values={"Positive": "#2E7D32", "Negative": "#C62828"}, name="Histogram")
    + scale_color_manual(
        values={"macd": "#306998", "signal": "#FFD43B"},
        labels={"macd": "MACD (12,26)", "signal": "Signal (9)"},
        name="Lines",
    )
    + labs(title="indicator-macd · plotnine · pyplots.ai", x="Date", y="MACD Value")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=45, ha="right"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="right",
        legend_background=element_rect(fill="white", alpha=0.9),
        panel_background=element_rect(fill="white"),
        panel_grid_major=element_line(color="#DDDDDD", size=0.5),
        panel_grid_minor=element_blank(),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
