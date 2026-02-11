""" pyplots.ai
area-basic: Basic Area Chart
Library: letsplot 4.8.2 | Python 3.14.2
Quality: 95/100 | Created: 2025-12-23
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
trend = np.linspace(0, 2000, 30)
weekly_pattern = 1000 * np.sin(np.arange(30) * 2 * np.pi / 7)
noise = np.random.randn(30) * 300
visitors = base_visitors + trend + weekly_pattern + noise
visitors = np.clip(visitors, 2000, None).astype(int)

df = pd.DataFrame({"date": days, "visitors": visitors})

# Plot
plot = (
    ggplot(df, aes(x="date", y="visitors"))  # noqa: F405
    + geom_area(  # noqa: F405
        fill="#306998",
        alpha=0.4,
        tooltips=layer_tooltips()  # noqa: F405
        .line("@visitors visitors")
        .format("date", "%b %d, %Y")
        .line("@date"),
    )
    + geom_line(color="#306998", size=2)  # noqa: F405
    + scale_x_datetime(format="%b %d")  # noqa: F405
    + scale_y_continuous(limits=[0, None])  # noqa: F405
    + labs(  # noqa: F405
        x="Date", y="Daily Visitors", title="area-basic · letsplot · pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid=element_line(color="#CCCCCC", size=0.3, linetype="dashed"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
