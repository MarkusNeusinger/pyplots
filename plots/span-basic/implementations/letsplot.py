"""
span-basic: Basic Span Plot (Highlighted Region)
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_line,
    geom_point,
    geom_rect,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Simulated economic indicator over time
np.random.seed(42)
months = pd.date_range("2006-01", periods=72, freq="ME")
base = np.linspace(100, 85, 36).tolist() + np.linspace(85, 120, 36).tolist()
noise = np.random.randn(72) * 3
values = np.array(base) + noise

df = pd.DataFrame({"date": months, "index": values})
df["date_num"] = np.arange(len(df))

# Span regions (recession period 2008-2009)
spans = pd.DataFrame(
    {
        "xmin": [24],  # Start of recession (Jan 2008)
        "xmax": [42],  # End of recession (Jun 2009)
        "ymin": [df["index"].min() - 5],
        "ymax": [df["index"].max() + 5],
        "label": ["Recession Period"],
    }
)

# Plot
plot = (
    ggplot()
    # Vertical span for recession period
    + geom_rect(data=spans, mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="label"), alpha=0.25)
    # Economic indicator line
    + geom_line(data=df, mapping=aes(x="date_num", y="index"), color="#306998", size=1.5)
    + geom_point(data=df, mapping=aes(x="date_num", y="index"), color="#306998", size=3, alpha=0.6)
    # Labels and styling
    + labs(x="Months (2006-2011)", y="Economic Index", title="span-basic · letsplot · pyplots.ai")
    + scale_fill_manual(values=["#FFD43B"], name="Highlighted Region")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale 3x gives 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")
