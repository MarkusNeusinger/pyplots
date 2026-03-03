"""pyplots.ai
heatmap-mandelbrot: Mandelbrot Set Fractal Visualization
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-03-03
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    geom_raster,
    ggplot,
    labs,
    scale_fill_cmap,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Compute Mandelbrot set escape times with smooth coloring
x_min, x_max = -2.5, 1.0
y_min, y_max = -1.25, 1.25
max_iter = 100
nx, ny = 600, 429

real = np.linspace(x_min, x_max, nx)
imag = np.linspace(y_min, y_max, ny)
real_grid, imag_grid = np.meshgrid(real, imag)
c = real_grid + 1j * imag_grid

# Vectorized Mandelbrot iteration with smooth escape-time coloring
z = np.zeros_like(c)
escape_time = np.zeros(c.shape, dtype=float)
active = np.ones(c.shape, dtype=bool)

for i in range(max_iter):
    z[active] = z[active] ** 2 + c[active]
    escaped = active & (np.abs(z) > 2)
    escape_time[escaped] = i + 1 - np.log2(np.log2(np.abs(z[escaped])))
    active[escaped] = False

# Inside the set: 0 maps to black at low end of inferno colormap
escape_time[active] = 0
escape_time = np.clip(escape_time, 0, max_iter)

# Long-form DataFrame for plotnine
df = pd.DataFrame({"real": real_grid.ravel(), "imaginary": imag_grid.ravel(), "escape_time": escape_time.ravel()})

# Plot
plot = (
    ggplot(df, aes(x="real", y="imaginary", fill="escape_time"))
    + geom_raster(interpolate=True)
    + scale_fill_cmap(cmap_name="inferno", name="Escape\nIterations")
    + coord_fixed(ratio=1.0)
    + scale_x_continuous(expand=(0, 0))
    + scale_y_continuous(expand=(0, 0))
    + labs(x="Real Axis", y="Imaginary Axis", title="heatmap-mandelbrot \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold", ha="center"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16, color="#333333"),
        legend_title=element_text(size=16, weight="bold"),
        legend_text=element_text(size=14),
        legend_position="right",
        legend_key_height=50,
        legend_key_width=18,
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="black"),
        plot_background=element_rect(fill="white", color="none"),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
