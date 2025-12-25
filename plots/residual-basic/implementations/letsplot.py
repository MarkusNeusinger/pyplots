"""pyplots.ai
residual-basic: Residual Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Generate regression data with realistic residual patterns
np.random.seed(42)

n_points = 100
x = np.linspace(5, 50, n_points)
true_slope = 1.8
true_intercept = 10
y_true = true_intercept + true_slope * x

# Create residuals with slight heteroscedasticity pattern (common in real data)
# and a few potential outliers for diagnostic interest
residual_noise = np.random.normal(0, 3, n_points)
# Add mild heteroscedasticity - variance increases slightly with fitted values
heteroscedastic_factor = 1 + 0.02 * (x - x.min())
residuals_raw = residual_noise * heteroscedastic_factor

# Add a few outliers for diagnostic interest
outlier_indices = [15, 45, 78]
for idx in outlier_indices:
    residuals_raw[idx] = np.random.choice([-1, 1]) * np.random.uniform(10, 15)

y_observed = y_true + residuals_raw

# Fit regression model
fitted_values = np.polyval(np.polyfit(x, y_observed, 1), x)
residuals = y_observed - fitted_values

# Create DataFrame
df = pd.DataFrame({"fitted": fitted_values, "residuals": residuals})

# Plot
plot = (
    ggplot(df, aes(x="fitted", y="residuals"))  # noqa: F405
    + geom_hline(yintercept=0, color="#DC2626", size=1.2, linetype="dashed", alpha=0.8)  # noqa: F405
    + geom_point(color="#306998", size=4, alpha=0.6)  # noqa: F405
    + geom_smooth(method="loess", color="#FFD43B", size=1.5, se=False, span=0.75)  # noqa: F405
    + labs(  # noqa: F405
        x="Fitted Values", y="Residuals (Observed − Predicted)", title="residual-basic · letsplot · pyplots.ai"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        panel_grid_major=element_line(color="#CCCCCC", size=0.5),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save as PNG and HTML
ggsave(plot, "plot.png", scale=3, path=".")
ggsave(plot, "plot.html", path=".")
