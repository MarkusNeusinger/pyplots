"""pyplots.ai
band-basic: Basic Band Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_line,
    geom_ribbon,
    ggplot,
    labs,
    theme,
    theme_minimal,
)


# Data - time series with 95% confidence interval (model predictions)
np.random.seed(42)
n_points = 50
x = np.linspace(0, 10, n_points)

# Generate central trend with curvature
y_center = 3 * np.sin(0.5 * x) + 0.3 * x + 5

# Uncertainty grows with x (heteroscedastic - realistic for forecasts)
uncertainty = 0.5 + 0.15 * x
noise = np.random.normal(0, 0.3, n_points)
y_center = y_center + noise

# Confidence band boundaries (95% CI uses 1.96 standard errors)
y_lower = y_center - 1.96 * uncertainty
y_upper = y_center + 1.96 * uncertainty

df = pd.DataFrame({"x": x, "y_center": y_center, "y_lower": y_lower, "y_upper": y_upper})

# Plot
plot = (
    ggplot(df, aes(x="x"))
    + geom_ribbon(aes(ymin="y_lower", ymax="y_upper"), fill="#306998", alpha=0.3)
    + geom_line(aes(y="y_center"), color="#306998", size=2)
    + labs(
        x="Time",
        y="Predicted Value",
        title="Model Forecast with 95% Confidence Interval · band-basic · plotnine · pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", size=0.5, alpha=0.3),
        panel_grid_minor=element_blank(),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
