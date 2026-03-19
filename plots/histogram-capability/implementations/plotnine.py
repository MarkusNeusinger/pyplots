""" pyplots.ai
histogram-capability: Process Capability Plot with Specification Limits
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-19
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    after_stat,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_histogram,
    geom_vline,
    ggplot,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    stat_function,
    theme,
    theme_minimal,
)
from scipy import stats


# Data - shaft diameter measurements (mm)
np.random.seed(42)
target = 10.00
lsl = 9.95
usl = 10.05
# Mean slightly above target to demonstrate Cp vs Cpk difference
measurements = np.random.normal(loc=10.008, scale=0.012, size=200)

# Capability indices
mean = np.mean(measurements)
sigma = np.std(measurements, ddof=1)
cp = (usl - lsl) / (6 * sigma)
cpk = min((usl - mean) / (3 * sigma), (mean - lsl) / (3 * sigma))

df = pd.DataFrame({"diameter": measurements})


# Normal PDF function for stat_function layer
def norm_pdf(x):
    return stats.norm.pdf(x, mean, sigma)


peak_density = norm_pdf(mean)

# Colorblind-safe palette: blue for limits, dark orange for target
limit_color = "#c0392b"
target_color = "#e67e22"
bar_color = "#306998"
curve_color = "#1a3d5c"
text_color = "#2c3e50"

# Plot using plotnine's stat_function for the normal curve overlay
plot = (
    ggplot(df, aes(x="diameter"))
    + geom_histogram(aes(y=after_stat("density")), bins=25, fill=bar_color, color="white", alpha=0.75)
    + stat_function(fun=norm_pdf, color=curve_color, size=2, n=300)
    + geom_vline(xintercept=lsl, linetype="dashed", color=limit_color, size=1.2)
    + geom_vline(xintercept=usl, linetype="dashed", color=limit_color, size=1.2)
    + geom_vline(xintercept=target, linetype="dotted", color=target_color, size=1.0)
    + annotate("text", x=lsl - 0.003, y=peak_density * 0.95, label="LSL", size=13, color=limit_color, fontweight="bold")
    + annotate("text", x=usl + 0.003, y=peak_density * 0.95, label="USL", size=13, color=limit_color, fontweight="bold")
    + annotate(
        "text", x=target + 0.004, y=peak_density * 0.82, label="Target", size=12, color=target_color, fontweight="bold"
    )
    + annotate(
        "label",
        x=mean + 3.5 * sigma,
        y=peak_density * 0.72,
        label=f"Cp  = {cp:.2f}\nCpk = {cpk:.2f}\n\u03bc    = {mean:.4f}\n\u03c3    = {sigma:.4f}",
        size=13,
        color=text_color,
        ha="left",
        fill="#f8f9fa",
        alpha=0.85,
        label_padding=0.6,
    )
    + labs(x="Shaft Diameter (mm)", y="Density", title="histogram-capability \u00b7 plotnine \u00b7 pyplots.ai")
    + scale_x_continuous(breaks=np.round(np.arange(9.94, 10.07, 0.01), 2).tolist())
    + scale_y_continuous(expand=(0, 0, 0.08, 0))
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color=text_color),
        axis_title=element_text(size=20, margin={"t": 12, "r": 12}),
        axis_text=element_text(size=16, color="#555555"),
        plot_title=element_text(size=24, weight="bold", margin={"b": 16}),
        plot_background=element_rect(fill="white", color="white"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#dddddd", size=0.4),
        plot_margin=0.04,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
