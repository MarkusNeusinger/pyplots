"""
qq-basic: Basic Q-Q Plot
Library: lets-plot
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - sample with slight right skew to demonstrate Q-Q plot characteristics
np.random.seed(42)
sample = np.concatenate(
    [
        np.random.normal(loc=50, scale=10, size=80),  # Main bulk of data
        np.random.normal(loc=75, scale=5, size=20),  # Slight right tail for asymmetry
    ]
)

# Sort sample and calculate positions for quantiles
sample_sorted = np.sort(sample)
n = len(sample_sorted)
probabilities = (np.arange(1, n + 1) - 0.5) / n

# Inverse normal CDF (Abramowitz & Stegun approximation) for theoretical quantiles
a = [
    -3.969683028665376e01,
    2.209460984245205e02,
    -2.759285104469687e02,
    1.383577518672690e02,
    -3.066479806614716e01,
    2.506628277459239e00,
]
b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02, 6.680131188771972e01, -1.328068155288572e01]
c = [
    -7.784894002430293e-03,
    -3.223964580411365e-01,
    -2.400758277161838e00,
    -2.549732539343734e00,
    4.374664141464968e00,
    2.938163982698783e00,
]
d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00, 3.754408661907416e00]

p_low, p_high = 0.02425, 1 - 0.02425
theoretical_quantiles = np.zeros(n)

# Low region
mask_low = probabilities < p_low
q = np.sqrt(-2 * np.log(probabilities[mask_low]))
theoretical_quantiles[mask_low] = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
    (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
)

# Central region
mask_mid = (probabilities >= p_low) & (probabilities <= p_high)
q = probabilities[mask_mid] - 0.5
r = q * q
theoretical_quantiles[mask_mid] = (
    (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
    * q
    / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
)

# High region
mask_high = probabilities > p_high
q = np.sqrt(-2 * np.log(1 - probabilities[mask_high]))
theoretical_quantiles[mask_high] = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
    (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
)

# Standardize sample quantiles for comparison
sample_mean = np.mean(sample_sorted)
sample_std = np.std(sample_sorted, ddof=1)
sample_quantiles = (sample_sorted - sample_mean) / sample_std

# Create dataframe for plotting
df = pd.DataFrame({"theoretical": theoretical_quantiles, "sample": sample_quantiles})

# Reference line data (y = x)
line_min = min(theoretical_quantiles.min(), sample_quantiles.min())
line_max = max(theoretical_quantiles.max(), sample_quantiles.max())
line_df = pd.DataFrame({"x": [line_min, line_max], "y": [line_min, line_max]})

# Plot
plot = (
    ggplot()  # noqa: F405
    + geom_line(data=line_df, mapping=aes(x="x", y="y"), color="#FFD43B", size=2, linetype="dashed")  # noqa: F405
    + geom_point(data=df, mapping=aes(x="theoretical", y="sample"), color="#306998", size=5, alpha=0.7)  # noqa: F405
    + labs(  # noqa: F405
        x="Theoretical Quantiles", y="Sample Quantiles", title="qq-basic · lets-plot · pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 × 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
