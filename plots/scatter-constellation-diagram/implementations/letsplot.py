""" pyplots.ai
scatter-constellation-diagram: Digital Modulation Constellation Diagram
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-17
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data
np.random.seed(42)

# 16-QAM ideal constellation points on a 4x4 grid at +/-1, +/-3
grid_vals = np.array([-3, -1, 1, 3])
ideal_i, ideal_q = np.meshgrid(grid_vals, grid_vals)
ideal_i = ideal_i.flatten()
ideal_q = ideal_q.flatten()

# Generate received symbols with additive Gaussian noise (~20 dB SNR)
n_symbols = 1000
symbol_indices = np.random.randint(0, 16, n_symbols)
snr_db = 20
signal_power = np.mean(ideal_i**2 + ideal_q**2)
noise_std = np.sqrt(signal_power / (2 * 10 ** (snr_db / 10)))

received_i = ideal_i[symbol_indices] + np.random.normal(0, noise_std, n_symbols)
received_q = ideal_q[symbol_indices] + np.random.normal(0, noise_std, n_symbols)

# Compute EVM
error_vectors = np.sqrt((received_i - ideal_i[symbol_indices]) ** 2 + (received_q - ideal_q[symbol_indices]) ** 2)
rms_reference = np.sqrt(np.mean(ideal_i**2 + ideal_q**2))
evm_percent = np.sqrt(np.mean(error_vectors**2)) / rms_reference * 100

# DataFrames
received_df = pd.DataFrame({"I": received_i, "Q": received_q})

ideal_df = pd.DataFrame({"I": ideal_i, "Q": ideal_q})

# Decision boundary lines
boundary_vals = np.array([-2, 0, 2])
boundary_v = pd.DataFrame({"x": boundary_vals})
boundary_h = pd.DataFrame({"y": boundary_vals})

# EVM annotation
evm_df = pd.DataFrame({"x": [3.6], "y": [3.6], "label": [f"EVM = {evm_percent:.1f}%"]})

# Plot
plot = (
    ggplot()  # noqa: F405
    # Decision boundary grid lines
    + geom_vline(data=boundary_v, mapping=aes(xintercept="x"), linetype="dashed", color="#999999", size=0.6, alpha=0.6)  # noqa: F405
    + geom_hline(data=boundary_h, mapping=aes(yintercept="y"), linetype="dashed", color="#999999", size=0.6, alpha=0.6)  # noqa: F405
    # Received symbols
    + geom_point(  # noqa: F405
        data=received_df,
        mapping=aes(x="I", y="Q"),  # noqa: F405
        color="#306998",
        size=2.5,
        alpha=0.35,
    )
    # Ideal constellation points
    + geom_point(  # noqa: F405
        data=ideal_df,
        mapping=aes(x="I", y="Q"),  # noqa: F405
        color="#CC3333",
        size=8,
        shape=4,
        stroke=3,
    )
    # EVM annotation
    + geom_text(  # noqa: F405
        data=evm_df,
        mapping=aes(x="x", y="y", label="label"),  # noqa: F405
        size=14,
        color="#333333",
        hjust=1,
    )
    # Axis lines through origin
    + geom_hline(yintercept=0, color="#AAAAAA", size=0.4)  # noqa: F405
    + geom_vline(xintercept=0, color="#AAAAAA", size=0.4)  # noqa: F405
    + labs(  # noqa: F405
        x="In-Phase (I)",
        y="Quadrature (Q)",
        title="16-QAM Constellation · scatter-constellation-diagram · letsplot · pyplots.ai",
    )
    + coord_fixed()  # noqa: F405
    + scale_x_continuous(limits=[-4.5, 4.5])  # noqa: F405
    + scale_y_continuous(limits=[-4.5, 4.5])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=22),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
