""" pyplots.ai
acf-pacf: Autocorrelation and Partial Autocorrelation (ACF/PACF) Plot
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 87/100 | Created: 2026-03-14
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from statsmodels.tsa.stattools import acf, pacf


# Data — synthetic monthly airline-style passenger counts with trend + seasonality
np.random.seed(42)
n_obs = 200
t = np.arange(n_obs)
trend = 0.5 * t
seasonal = 30 * np.sin(2 * np.pi * t / 12)
noise = np.random.normal(0, 8, n_obs)
passengers = 100 + trend + seasonal + noise

# Compute ACF and PACF
n_lags = 36
acf_values, acf_confint = acf(passengers, nlags=n_lags, alpha=0.05)
pacf_values, pacf_confint = pacf(passengers, nlags=n_lags, alpha=0.05)

acf_lags = np.arange(len(acf_values))
pacf_lags = np.arange(1, len(pacf_values))

# Confidence bounds
confidence_bound = 1.96 / np.sqrt(n_obs)

# Color palette
SIGNIFICANT_COLOR = "#306998"
INSIGNIFICANT_COLOR = "#a8c4d8"
CONF_COLOR = "#b04040"
BG_COLOR = "#fafbfd"

# Classify significance
acf_significant = np.abs(acf_values) > confidence_bound
pacf_significant = np.abs(pacf_values[1:]) > confidence_bound

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
fig.set_facecolor(BG_COLOR)
ax1.set_facecolor(BG_COLOR)
ax2.set_facecolor(BG_COLOR)


def plot_correlogram(ax, lags, values, significant_mask, ylabel):
    """Draw stem plot with significant/insignificant distinction using LineCollection."""
    # Build colored stem segments using LineCollection
    segments = []
    colors = []
    for lag, val, sig in zip(lags, values, significant_mask, strict=False):
        segments.append([(lag, 0), (lag, val)])
        colors.append(SIGNIFICANT_COLOR if sig else INSIGNIFICANT_COLOR)

    lc = LineCollection(segments, colors=colors, linewidths=2.8, zorder=3)
    ax.add_collection(lc)

    # Markers — significant vs insignificant
    sig_mask = np.array(significant_mask)
    if sig_mask.any():
        ax.scatter(
            lags[sig_mask],
            values[sig_mask],
            color=SIGNIFICANT_COLOR,
            s=64,
            zorder=5,
            edgecolors="white",
            linewidths=0.8,
            marker="o",
        )
    if (~sig_mask).any():
        ax.scatter(
            lags[~sig_mask],
            values[~sig_mask],
            color=INSIGNIFICANT_COLOR,
            s=44,
            zorder=5,
            edgecolors="white",
            linewidths=0.6,
            marker="o",
        )

    # Zero baseline
    ax.axhline(y=0, color="#333333", linewidth=0.6)

    # Confidence bands
    ax.axhline(y=confidence_bound, color=CONF_COLOR, linestyle="--", linewidth=1.5, alpha=0.55)
    ax.axhline(y=-confidence_bound, color=CONF_COLOR, linestyle="--", linewidth=1.5, alpha=0.55)
    ax.fill_between(lags, -confidence_bound, confidence_bound, color=CONF_COLOR, alpha=0.05, zorder=1)

    # Axis styling
    ax.set_ylabel(ylabel, fontsize=20, fontweight="medium", labelpad=12)
    ax.tick_params(axis="both", labelsize=16, length=4, width=0.8)
    ax.tick_params(axis="x", which="both", bottom=True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_linewidth(0.6)
        ax.spines[spine].set_color("#888888")
    ax.yaxis.grid(True, alpha=0.15, linewidth=0.6, color="#999999")
    ax.set_xlim(-0.8, max(lags) + 0.8)
    ax.margins(y=0.08)


# ACF (top subplot)
plot_correlogram(ax1, acf_lags, acf_values, acf_significant, "ACF")

# PACF (bottom subplot) — starts from lag 1
plot_correlogram(ax2, pacf_lags, pacf_values[1:], pacf_significant, "PACF")

# X-axis label on bottom subplot only
ax2.set_xlabel("Lag", fontsize=20, fontweight="medium", labelpad=10)

# Title
fig.suptitle(
    "acf-pacf · matplotlib · pyplots.ai",
    fontsize=24,
    fontweight="medium",
    y=0.97,
    color="#333333",
    fontfamily="sans-serif",
)

fig.subplots_adjust(top=0.93, hspace=0.12)
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
