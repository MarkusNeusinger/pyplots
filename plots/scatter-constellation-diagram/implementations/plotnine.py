""" pyplots.ai
scatter-constellation-diagram: Digital Modulation Constellation Diagram
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    coord_fixed,
    element_blank,
    element_line,
    element_text,
    geom_hline,
    geom_point,
    geom_vline,
    ggplot,
    labs,
    scale_alpha_identity,
    scale_color_identity,
    scale_size_identity,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)

ideal_coords = [-3, -1, 1, 3]
ideal_i = np.array([i for i in ideal_coords for _ in ideal_coords])
ideal_q = np.array([q for _ in ideal_coords for q in ideal_coords])

n_symbols = 1000
snr_db = 20
snr_linear = 10 ** (snr_db / 10)
avg_power = np.mean(ideal_i**2 + ideal_q**2)
noise_std = np.sqrt(avg_power / (2 * snr_linear))

symbol_indices = np.random.randint(0, 16, size=n_symbols)
received_i = ideal_i[symbol_indices] + np.random.normal(0, noise_std, n_symbols)
received_q = ideal_q[symbol_indices] + np.random.normal(0, noise_std, n_symbols)

error_i = received_i - ideal_i[symbol_indices]
error_q = received_q - ideal_q[symbol_indices]
evm = np.sqrt(np.mean(error_i**2 + error_q**2)) / np.sqrt(avg_power) * 100

df_received = pd.DataFrame({"i": received_i, "q": received_q, "color": "#306998", "alpha": 0.35, "size": 2.5})

df_ideal = pd.DataFrame({"i": ideal_i, "q": ideal_q, "color": "#D04848", "alpha": 1.0, "size": 6})

df_all = pd.concat([df_received, df_ideal], ignore_index=True)

# Decision boundaries
boundary_vals = [-2, 0, 2]

# Plot
plot = (
    ggplot(df_all, aes(x="i", y="q"))
    + geom_vline(xintercept=boundary_vals, linetype="dashed", color="#999999", size=0.4)
    + geom_hline(yintercept=boundary_vals, linetype="dashed", color="#999999", size=0.4)
    + geom_point(data=df_received, mapping=aes(x="i", y="q", color="color", alpha="alpha", size="size"))
    + geom_point(
        data=df_ideal, mapping=aes(x="i", y="q", color="color", alpha="alpha", size="size"), shape="X", stroke=1.2
    )
    + scale_color_identity()
    + scale_alpha_identity()
    + scale_size_identity()
    + annotate(
        "text", x=3.6, y=-3.8, label=f"EVM = {evm:.1f}%", size=14, ha="right", color="#333333", fontweight="bold"
    )
    + annotate(
        "text", x=3.6, y=-4.2, label=f"SNR = {snr_db} dB  ·  {n_symbols} symbols", size=10, ha="right", color="#666666"
    )
    + coord_fixed(ratio=1, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5))
    + labs(x="In-Phase (I)", y="Quadrature (Q)", title="scatter-constellation-diagram · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(10, 10),
        plot_title=element_text(size=18, weight="bold", ha="center"),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        axis_line=element_line(color="#333333", size=0.6),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
