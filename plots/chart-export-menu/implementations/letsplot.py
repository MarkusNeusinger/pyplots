"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Monthly sales data over time
np.random.seed(42)
months = pd.date_range("2024-01-01", periods=12, freq="MS")
electronics = np.cumsum(np.random.normal(50, 15, 12)) + 200
clothing = np.cumsum(np.random.normal(40, 12, 12)) + 150
home_goods = np.cumsum(np.random.normal(35, 10, 12)) + 120

df = pd.DataFrame(
    {
        "Month": list(months) * 3,
        "Sales": np.concatenate([electronics, clothing, home_goods]),
        "Category": ["Electronics"] * 12 + ["Clothing"] * 12 + ["Home Goods"] * 12,
    }
)
df["Month_Label"] = df["Month"].dt.strftime("%b")

# Create plot with export menu (lets-plot includes built-in export via ggtb)
plot = (
    ggplot(df, aes(x="Month_Label", y="Sales", group="Category", color="Category"))  # noqa: F405
    + geom_line(size=2)  # noqa: F405
    + geom_point(size=5, alpha=0.8)  # noqa: F405
    + scale_color_manual(values=["#306998", "#FFD43B", "#DC2626"])  # noqa: F405
    + labs(  # noqa: F405
        x="Month", y="Sales (thousands)", title="chart-export-menu · letsplot · pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        legend_title=element_text(size=18),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="right",
    )
)

# Add toolbar for interactive export menu (PNG, SVG export buttons)
plot = plot + ggtb()  # noqa: F405

# Save PNG (scale 3x for 4800 × 2700 px) and HTML
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
