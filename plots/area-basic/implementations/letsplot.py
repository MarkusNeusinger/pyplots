""" pyplots.ai
area-basic: Basic Area Chart
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - daily website visitors over a month
np.random.seed(42)
days = pd.date_range(start="2024-01-01", periods=30, freq="D")
base_visitors = 5000
trend = np.linspace(0, 1500, 30)
weekly_pattern = 800 * np.sin(np.arange(30) * 2 * np.pi / 7)
noise = np.random.randn(30) * 400
visitors = base_visitors + trend + weekly_pattern + noise
visitors = np.clip(visitors, 2000, None).astype(int)

df = pd.DataFrame({"date": days, "visitors": visitors})
df["day_num"] = np.arange(len(df))

# Plot
plot = (
    ggplot(df, aes(x="day_num", y="visitors"))  # noqa: F405
    + geom_area(fill="#306998", alpha=0.4)  # noqa: F405
    + geom_line(color="#306998", size=2)  # noqa: F405
    + labs(  # noqa: F405
        x="Day of Month", y="Daily Visitors", title="area-basic \u00b7 lets-plot \u00b7 pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
