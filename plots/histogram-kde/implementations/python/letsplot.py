""" anyplot.ai
histogram-kde: Histogram with KDE Overlay
Library: letsplot 4.9.0 | Python 3.13.13
Quality: 84/100 | Updated: 2026-05-06
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()  # noqa: F405

# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"
BRAND = "#009E73"  # Okabe-Ito position 1

# Data - Simulated stock daily returns (realistic financial scenario)
np.random.seed(42)
returns = np.concatenate(
    [np.random.normal(0.001, 0.015, 400), np.random.normal(-0.02, 0.03, 50), np.random.normal(0.02, 0.025, 50)]
)
returns = returns * 100

df = pd.DataFrame({"Daily Return (%)": returns})

# Plot
anyplot_theme = (
    theme(  # noqa: F405
        plot_background=element_rect(fill=PAGE_BG, color=PAGE_BG),  # noqa: F405
        panel_background=element_rect(fill=PAGE_BG),  # noqa: F405
        panel_grid_major=element_line(  # noqa: F405
            color=INK_SOFT, size=0.3
        ),
        panel_grid_minor=element_blank(),  # noqa: F405
        axis_title=element_text(size=20, color=INK),  # noqa: F405
        axis_text=element_text(size=16, color=INK_SOFT),  # noqa: F405
        axis_line=element_line(color=INK_SOFT, size=0.5),  # noqa: F405
        plot_title=element_text(size=24, color=INK),  # noqa: F405
        legend_background=element_rect(  # noqa: F405
            fill=ELEVATED_BG, color=INK_SOFT
        ),
        legend_text=element_text(size=16, color=INK_SOFT),  # noqa: F405
        legend_title=element_text(size=16, color=INK),  # noqa: F405
    )
    + theme_minimal()  # noqa: F405
)

plot = (
    ggplot(df, aes(x="Daily Return (%)"))  # noqa: F405
    + geom_histogram(  # noqa: F405
        aes(y="..density.."),  # noqa: F405
        bins=35,
        fill=BRAND,
        alpha=0.5,
        color=BRAND,
        size=0.5,
    )
    + geom_density(  # noqa: F405
        color=INK_SOFT, size=1.5, fill="rgba(0,0,0,0)"
    )
    + labs(  # noqa: F405
        x="Daily Return (%)", y="Density", title="histogram-kde · letsplot · anyplot.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + anyplot_theme
)

# Save
output_dir = Path(__file__).parent
ggsave(plot, str(output_dir / f"plot-{THEME}.png"), scale=3)  # noqa: F405
ggsave(plot, str(output_dir / f"plot-{THEME}.html"))  # noqa: F405
