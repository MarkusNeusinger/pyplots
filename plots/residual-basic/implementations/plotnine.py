""" pyplots.ai
residual-basic: Residual Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-26
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_text,
    geom_hline,
    geom_point,
    geom_smooth,
    ggplot,
    labs,
    scale_y_continuous,
    theme,
    theme_minimal,
)


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

# Create DataFrame for plotnine
df = pd.DataFrame({"fitted": fitted, "residuals": residuals})

# Calculate symmetric y-axis limits
y_max = max(abs(df["residuals"].min()), abs(df["residuals"].max())) * 1.1

# Create the residual plot
plot = (
    ggplot(df, aes(x="fitted", y="residuals"))
    # Reference line at y=0
    + geom_hline(yintercept=0, color="#333333", size=1.5, linetype="solid")
    # Smoothed trend line (LOWESS)
    + geom_smooth(method="lowess", color="#FFD43B", size=2, se=False, span=0.5)
    # Scatter points with transparency
    + geom_point(color="#306998", size=4, alpha=0.6, stroke=0.3)
    # Labels and title
    + labs(x="Fitted Values", y="Residuals", title="residual-basic \u00b7 plotnine \u00b7 pyplots.ai")
    # Symmetric y-axis around zero
    + scale_y_continuous(limits=(-y_max, y_max))
    # Theme and styling
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#CCCCCC", alpha=0.3, linetype="dashed"),
        panel_grid_minor=element_line(alpha=0),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
