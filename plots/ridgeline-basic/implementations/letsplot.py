"""
ridgeline-basic: Ridgeline Plot
Library: letsplot
"""

import os
import shutil

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - monthly temperature distributions
np.random.seed(42)
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Generate realistic temperature data with seasonal pattern
data = []
for i, month in enumerate(months):
    # Seasonal temperature pattern (Northern Hemisphere)
    base_temp = 5 + 15 * np.sin((i - 3) * np.pi / 6)
    temps = np.random.normal(base_temp, 4, 200)
    for temp in temps:
        data.append({"month": month, "temperature": temp})

df = pd.DataFrame(data)

# Create ordered categorical for proper month ordering
df["month"] = pd.Categorical(df["month"], categories=months, ordered=True)

# Color palette gradient from cool to warm
colors = [
    "#306998",  # Python Blue (winter)
    "#3B82F6",  # Blue
    "#06B6D4",  # Cyan
    "#10B981",  # Emerald
    "#22C55E",  # Green
    "#84CC16",  # Lime
    "#FFD43B",  # Python Yellow (summer)
    "#F97316",  # Orange
    "#EF4444",  # Red
    "#F97316",  # Orange
    "#8B5CF6",  # Violet
    "#306998",  # Python Blue
]

# Create ridgeline plot using geom_area_ridges
plot = (
    ggplot(df, aes(x="temperature", y="month", fill="month"))
    + geom_area_ridges(alpha=0.7, scale=1.5, color="white", size=0.5)
    + scale_fill_manual(values=colors)
    + labs(x="Temperature (°C)", y="Month", title="Monthly Temperature Distribution")
    + theme_minimal()
    + theme(
        axis_text=element_text(size=16),
        axis_title=element_text(size=20),
        plot_title=element_text(size=20),
        legend_position="none",
    )
    + ggsize(1600, 900)
)

# Save as PNG and HTML
# Note: lets_plot saves to lets-plot-images/ subdirectory by default
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")

# Move files from lets-plot-images to current directory
if os.path.exists("lets-plot-images/plot.png"):
    shutil.move("lets-plot-images/plot.png", "plot.png")
if os.path.exists("lets-plot-images/plot.html"):
    shutil.move("lets-plot-images/plot.html", "plot.html")
if os.path.exists("lets-plot-images") and not os.listdir("lets-plot-images"):
    os.rmdir("lets-plot-images")
