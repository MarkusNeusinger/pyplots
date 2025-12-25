"""pyplots.ai
residual-basic: Residual Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Simulate regression residuals with realistic patterns
np.random.seed(42)

# Generate realistic fitted values (predictions from a hypothetical regression)
n_points = 150
fitted = np.linspace(10, 90, n_points) + np.random.randn(n_points) * 5

# Generate residuals with mostly random scatter but slight heteroscedasticity
# (variance increases slightly with fitted values - common pattern)
base_residuals = np.random.randn(n_points) * 5
heteroscedasticity = np.random.randn(n_points) * (0.03 * fitted)
residuals = base_residuals + heteroscedasticity

# Add a few outliers for realism
outlier_indices = [20, 75, 120]
residuals[outlier_indices] = np.array([18, -22, 25])

# Sort by fitted values for LOWESS-like smoothing
sort_idx = np.argsort(fitted)
fitted_sorted = fitted[sort_idx]
residuals_sorted = residuals[sort_idx]

# Calculate smoothed trend line using moving average
window = 15
cumsum = np.cumsum(np.insert(residuals_sorted, 0, 0))
trend = (cumsum[window:] - cumsum[:-window]) / window
# Pad trend to match original length
pad_left = (len(residuals_sorted) - len(trend)) // 2
pad_right = len(residuals_sorted) - len(trend) - pad_left
trend = np.concatenate([np.full(pad_left, trend[0]), trend, np.full(pad_right, trend[-1])])

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Reference line at y=0
ax.axhline(y=0, color="#333333", linewidth=2, linestyle="-", zorder=1, label="Zero Reference")

# Scatter plot with transparency
ax.scatter(
    fitted,
    residuals,
    s=150,
    alpha=0.6,
    color="#306998",
    edgecolors="white",
    linewidths=0.5,
    zorder=3,
    label="Residuals",
)

# Smoothed trend line
ax.plot(fitted_sorted, trend, color="#FFD43B", linewidth=3, linestyle="-", zorder=2, label="Trend (Smoothed)")

# Styling
ax.set_xlabel("Fitted Values", fontsize=20)
ax.set_ylabel("Residuals", fontsize=20)
ax.set_title("residual-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Symmetric y-axis around zero
y_max = max(abs(residuals.min()), abs(residuals.max())) * 1.1
ax.set_ylim(-y_max, y_max)

# Grid and legend
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=16, loc="upper right")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
