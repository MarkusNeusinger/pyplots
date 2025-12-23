"""pyplots.ai
sparkline-basic: Basic Sparkline
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - simulated daily stock prices over 50 trading days
np.random.seed(42)
n_points = 50
returns = np.random.randn(n_points) * 0.015  # Daily returns ~1.5% volatility
prices = 100 * np.cumprod(1 + returns)  # Cumulative price series starting at 100

df = pd.DataFrame({"day": range(n_points), "price": prices})

# Find min/max points for highlighting
min_idx = int(np.argmin(prices))
max_idx = int(np.argmax(prices))
first_idx = 0
last_idx = n_points - 1

highlight_df = pd.DataFrame(
    {
        "day": [min_idx, max_idx, first_idx, last_idx],
        "price": [prices[min_idx], prices[max_idx], prices[first_idx], prices[last_idx]],
        "type": ["min", "max", "first", "last"],
    }
)

# Plot - minimal sparkline with highlighted points
# Using wider aspect ratio typical for sparklines (approximately 5:1)
plot = (
    ggplot(df, aes(x="day", y="price"))  # noqa: F405
    + geom_area(fill="#306998", alpha=0.15)  # noqa: F405
    + geom_line(color="#306998", size=2.0)  # noqa: F405
    + geom_point(  # noqa: F405
        data=highlight_df[highlight_df["type"] == "min"],
        mapping=aes(x="day", y="price"),  # noqa: F405
        color="#DC2626",
        size=8,
    )  # Min point (red)
    + geom_point(  # noqa: F405
        data=highlight_df[highlight_df["type"] == "max"],
        mapping=aes(x="day", y="price"),  # noqa: F405
        color="#16A34A",
        size=8,
    )  # Max point (green)
    + geom_point(  # noqa: F405
        data=highlight_df[highlight_df["type"].isin(["first", "last"])],
        mapping=aes(x="day", y="price"),  # noqa: F405
        color="#FFD43B",
        size=6,
    )  # First/last points (yellow)
    + labs(title="sparkline-basic · lets-plot · pyplots.ai")  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + theme_void()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=28, hjust=0.5),  # noqa: F405
        plot_margin=[80, 60, 60, 60],
    )
)

# Save PNG (scale 3x for 4800x2700) and HTML to current directory
export_ggsave(plot, "plot.png", path=".", scale=3)
export_ggsave(plot, "plot.html", path=".")
