"""pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-03-15
"""

from math import erf, sqrt

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data
np.random.seed(42)
n_samples = 200

# Generate slightly skewed data (right-skewed via mixture)
normal_component = np.random.normal(50, 12, 160)
skew_component = np.random.exponential(8, 40) + 40
observed = np.concatenate([normal_component, skew_component])
observed = observed[:n_samples]

# Sort observed data
observed_sorted = np.sort(observed)

# Compute empirical CDF using plotting position formula i/(n+1)
empirical_cdf = np.arange(1, n_samples + 1) / (n_samples + 1)

# Fit normal distribution (MLE: mean and std of data)
mu = np.mean(observed_sorted)
sigma = np.std(observed_sorted, ddof=0)

# Compute theoretical CDF values (normal CDF inline)
z_scores = (observed_sorted - mu) / (sigma * sqrt(2))
theoretical_cdf = 0.5 * (1 + np.vectorize(erf)(z_scores))

# Create dataframe for P-P plot points
df_pp = pd.DataFrame({"theoretical": theoretical_cdf, "empirical": empirical_cdf})

# Reference line (perfect fit diagonal)
df_ref = pd.DataFrame({"x": [0, 1], "y": [0, 1]})

# Plot
plot = (
    ggplot()
    + geom_line(aes(x="x", y="y"), data=df_ref, color="#888888", size=1.5, linetype="dashed")
    + geom_point(aes(x="theoretical", y="empirical"), data=df_pp, color="#306998", size=3, alpha=0.7)
    + labs(x="Theoretical CDF (Normal)", y="Empirical CDF", title="pp-basic · letsplot · pyplots.ai")
    + scale_x_continuous(limits=[0, 1], breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    + scale_y_continuous(limits=[0, 1], breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    + coord_fixed(ratio=1)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#E0E0E0", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1200, 1200)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
