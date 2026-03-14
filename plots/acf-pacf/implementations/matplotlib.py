"""pyplots.ai
acf-pacf: Autocorrelation and Partial Autocorrelation (ACF/PACF) Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-03-14
"""

import matplotlib.pyplot as plt
import numpy as np
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

# Confidence bounds (distance from value to bound)
confidence_bound = 1.96 / np.sqrt(n_obs)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)

# ACF (top)
markerline1, stemlines1, baseline1 = ax1.stem(acf_lags, acf_values, linefmt="-", markerfmt="o", basefmt="")
plt.setp(stemlines1, linewidth=2.5, color="#306998")
plt.setp(markerline1, markersize=7, color="#306998", zorder=5)
ax1.axhline(y=0, color="black", linewidth=0.8)
ax1.axhline(y=confidence_bound, color="#cc4444", linestyle="--", linewidth=1.8, alpha=0.7)
ax1.axhline(y=-confidence_bound, color="#cc4444", linestyle="--", linewidth=1.8, alpha=0.7)
ax1.fill_between(acf_lags, -confidence_bound, confidence_bound, color="#cc4444", alpha=0.06)

# PACF (bottom) — starts from lag 1
markerline2, stemlines2, baseline2 = ax2.stem(pacf_lags, pacf_values[1:], linefmt="-", markerfmt="o", basefmt="")
plt.setp(stemlines2, linewidth=2.5, color="#306998")
plt.setp(markerline2, markersize=7, color="#306998", zorder=5)
ax2.axhline(y=0, color="black", linewidth=0.8)
ax2.axhline(y=confidence_bound, color="#cc4444", linestyle="--", linewidth=1.8, alpha=0.7)
ax2.axhline(y=-confidence_bound, color="#cc4444", linestyle="--", linewidth=1.8, alpha=0.7)
ax2.fill_between(pacf_lags, -confidence_bound, confidence_bound, color="#cc4444", alpha=0.06)

# Style — ACF subplot
ax1.set_ylabel("ACF", fontsize=20)
ax1.tick_params(axis="both", labelsize=16)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Style — PACF subplot
ax2.set_xlabel("Lag", fontsize=20)
ax2.set_ylabel("PACF", fontsize=20)
ax2.tick_params(axis="both", labelsize=16)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Title
fig.suptitle("acf-pacf · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", y=0.97)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
