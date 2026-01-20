"""pyplots.ai
drawdown-basic: Drawdown Chart
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Generate sample price data (simulating ~2 years of daily data)
np.random.seed(42)
n_days = 500
dates = pd.date_range(start="2022-01-01", periods=n_days, freq="B")

# Simulate price movement with trends and volatility
returns = np.random.normal(0.0003, 0.015, n_days)
# Add a few drawdown periods
returns[50:80] = np.random.normal(-0.01, 0.02, 30)
returns[200:260] = np.random.normal(-0.008, 0.025, 60)
returns[350:400] = np.random.normal(-0.005, 0.018, 50)

price = 100 * np.cumprod(1 + returns)

# Calculate drawdown
running_max = np.maximum.accumulate(price)
drawdown = (price - running_max) / running_max * 100

# Create DataFrame
df = pd.DataFrame({"date": dates, "price": price, "drawdown": drawdown, "day_num": np.arange(n_days)})

# Find maximum drawdown point
max_dd_idx = int(np.argmin(drawdown))
max_dd_value = drawdown[max_dd_idx]

# Find recovery points (where drawdown returns to zero after being negative)
recovery_mask = (drawdown == 0) & (np.roll(drawdown, 1) < 0)
recovery_points = df[recovery_mask].copy()

# DataFrame for maximum drawdown point
max_dd_df = df.iloc[[max_dd_idx]].copy()

# Create the drawdown chart
plot = (
    ggplot(df, aes(x="day_num", y="drawdown"))  # noqa: F405
    + geom_area(fill="#DC2626", alpha=0.4)  # noqa: F405
    + geom_line(color="#DC2626", size=1.5)  # noqa: F405
    + geom_hline(yintercept=0, color="#333333", size=1.0, linetype="dashed")  # noqa: F405
    + geom_point(  # noqa: F405
        data=max_dd_df,
        mapping=aes(x="day_num", y="drawdown"),  # noqa: F405
        color="#991B1B",
        size=6,
        shape=18,
    )
    + geom_point(  # noqa: F405
        data=recovery_points,
        mapping=aes(x="day_num", y="drawdown"),  # noqa: F405
        color="#16A34A",
        size=4,
    )
    + labs(  # noqa: F405
        x="Trading Days",
        y="Drawdown (%)",
        title="drawdown-basic \u00b7 letsplot \u00b7 pyplots.ai",
        caption="Max Drawdown: {:.1f}% on Day {}".format(max_dd_value, max_dd_idx),
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        plot_caption=element_text(size=14),  # noqa: F405
        panel_grid=element_line(color="#E5E5E5", size=0.5, linetype="dashed"),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
