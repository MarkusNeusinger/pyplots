"""pyplots.ai
line-arrhenius: Arrhenius Plot for Reaction Kinetics
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-03-21
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    labs,
    scale_x_continuous,
    theme,
    theme_minimal,
)
from scipy import stats


# Data
temperature_K = np.array([300, 350, 400, 450, 500, 550, 600])
rate_constant_k = np.array([0.0012, 0.0095, 0.052, 0.21, 0.68, 1.8, 4.1])

inv_T = 1.0 / temperature_K
ln_k = np.log(rate_constant_k)

slope, intercept, r_value, p_value, std_err = stats.linregress(inv_T, ln_k)
r_squared = r_value**2

R = 8.314
Ea_kJ = -slope * R / 1000

inv_T_fit = np.linspace(inv_T.min() - 0.0001, inv_T.max() + 0.0001, 100)
ln_k_fit = slope * inv_T_fit + intercept

df_data = pd.DataFrame({"inv_T": inv_T, "ln_k": ln_k})
df_fit = pd.DataFrame({"inv_T": inv_T_fit, "ln_k": ln_k_fit})

# Tick labels showing 1/T with temperature reference
tick_positions = inv_T.tolist()
tick_labels = [f"{v:.2e}\n({1 / v:.0f} K)" for v in inv_T]

# Annotation position
anno_x = inv_T.mean()
anno_y_top = ln_k.max() - 0.3

# Plot
plot = (
    ggplot()
    + geom_line(df_fit, aes(x="inv_T", y="ln_k"), color="#306998", size=1.5, alpha=0.7)
    + geom_point(df_data, aes(x="inv_T", y="ln_k"), color="#306998", size=5, stroke=0.8)
    + scale_x_continuous(breaks=tick_positions, labels=tick_labels)
    + annotate("text", x=anno_x, y=anno_y_top, label=f"R² = {r_squared:.4f}", size=14, color="#333333", ha="center")
    + annotate(
        "text", x=anno_x, y=anno_y_top - 0.9, label=f"Eₐ = {Ea_kJ:.1f} kJ/mol", size=14, color="#333333", ha="center"
    )
    + annotate(
        "text",
        x=anno_x,
        y=anno_y_top - 1.8,
        label=f"slope = −Eₐ/R = {slope:.0f} K",
        size=11,
        color="#666666",
        ha="center",
    )
    + labs(x="1/T (K⁻¹)", y="ln(k)", title="line-arrhenius · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=14),
        axis_text_x=element_text(size=11),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#dddddd", size=0.5, alpha=0.5),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
