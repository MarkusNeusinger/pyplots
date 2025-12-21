""" pyplots.ai
qq-basic: Basic Q-Q Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-17
"""

import altair as alt
import numpy as np
import pandas as pd


# Approximate inverse normal CDF using rational approximation (Abramowitz & Stegun)
def norm_ppf(p):
    """Approximate inverse normal CDF for 0 < p < 1."""
    # Constants for rational approximation
    a = [
        -3.969683028665376e1,
        2.209460984245205e2,
        -2.759285104469687e2,
        1.383577518672690e2,
        -3.066479806614716e1,
        2.506628277459239e0,
    ]
    b = [-5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2, 6.680131188771972e1, -1.328068155288572e1]
    c = [
        -7.784894002430293e-3,
        -3.223964580411365e-1,
        -2.400758277161838e0,
        -2.549732539343734e0,
        4.374664141464968e0,
        2.938163982698783e0,
    ]
    d = [7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996e0, 3.754408661907416e0]
    p_low = 0.02425
    p_high = 1 - p_low

    result = np.zeros_like(p, dtype=float)
    # Lower region
    mask_low = p < p_low
    if np.any(mask_low):
        q = np.sqrt(-2 * np.log(p[mask_low]))
        result[mask_low] = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    # Central region
    mask_mid = (p >= p_low) & (p <= p_high)
    if np.any(mask_mid):
        q = p[mask_mid] - 0.5
        r = q * q
        result[mask_mid] = ((((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q) / (
            ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1
        )
    # Upper region
    mask_high = p > p_high
    if np.any(mask_high):
        q = np.sqrt(-2 * np.log(1 - p[mask_high]))
        result[mask_high] = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    return result


# Data - sample with slight right skew to demonstrate Q-Q interpretation
np.random.seed(42)
sample = np.concatenate(
    [
        np.random.normal(50, 10, 80),  # Main distribution
        np.random.normal(75, 5, 20),  # Right tail (creates slight skew)
    ]
)

# Calculate theoretical quantiles (normal distribution)
n = len(sample)
sorted_sample = np.sort(sample)
probabilities = (np.arange(1, n + 1) - 0.5) / n
theoretical_quantiles = norm_ppf(probabilities)

# Scale theoretical quantiles to match sample mean and std
sample_mean = np.mean(sample)
sample_std = np.std(sample)
theoretical_scaled = theoretical_quantiles * sample_std + sample_mean

# Create DataFrame for Altair
df = pd.DataFrame({"Theoretical Quantiles": theoretical_scaled, "Sample Quantiles": sorted_sample})

# Reference line data (y = x)
line_min = min(theoretical_scaled.min(), sorted_sample.min())
line_max = max(theoretical_scaled.max(), sorted_sample.max())
line_df = pd.DataFrame({"x": [line_min, line_max], "y": [line_min, line_max]})

# Create Q-Q scatter plot
points = (
    alt.Chart(df)
    .mark_point(size=200, color="#306998", filled=True, opacity=0.7)
    .encode(
        x=alt.X("Theoretical Quantiles:Q", title="Theoretical Quantiles"),
        y=alt.Y("Sample Quantiles:Q", title="Sample Quantiles"),
        tooltip=["Theoretical Quantiles:Q", "Sample Quantiles:Q"],
    )
)

# Reference line (45-degree)
reference_line = (
    alt.Chart(line_df)
    .mark_line(color="#FFD43B", strokeWidth=3, strokeDash=[8, 4])
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"))
)

# Combine layers
chart = (
    (reference_line + points)
    .properties(width=1600, height=900, title=alt.Title("qq-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
