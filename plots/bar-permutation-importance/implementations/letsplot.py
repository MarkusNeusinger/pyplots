""" pyplots.ai
bar-permutation-importance: Permutation Feature Importance Plot
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_errorbar,
    geom_point,
    geom_vline,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_gradient,
    scale_y_discrete,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data: Simulated permutation importance from a Random Forest model
np.random.seed(42)

features = [
    "Income Level",
    "Credit Score",
    "Employment Years",
    "Debt Ratio",
    "Account Age",
    "Payment History",
    "Loan Amount",
    "Interest Rate",
    "Property Value",
    "Monthly Expenses",
    "Savings Balance",
    "Number of Accounts",
    "Recent Inquiries",
    "Education Level",
    "Region Code",
]

# Generate importance values - higher for more predictive features
base_importance = np.array(
    [0.15, 0.12, 0.09, 0.08, 0.06, 0.05, 0.04, 0.03, 0.025, 0.02, 0.015, 0.01, 0.008, 0.005, 0.002]
)
# Add some noise
importance_mean = base_importance + np.random.uniform(-0.005, 0.005, len(features))
importance_std = np.random.uniform(0.003, 0.02, len(features))

# Create DataFrame and sort by importance
df = pd.DataFrame({"feature": features, "importance_mean": importance_mean, "importance_std": importance_std})
df = df.sort_values("importance_mean", ascending=True).reset_index(drop=True)

# Create ordered categorical for proper y-axis ordering
df["feature"] = pd.Categorical(df["feature"], categories=df["feature"].tolist(), ordered=True)

# Calculate error bar positions
df["xmin"] = df["importance_mean"] - df["importance_std"]
df["xmax"] = df["importance_mean"] + df["importance_std"]

# Create the plot
plot = (
    ggplot(df, aes(x="importance_mean", y="feature", color="importance_mean"))
    + geom_vline(xintercept=0, color="#888888", size=0.8, linetype="dashed")
    + geom_errorbar(aes(xmin="xmin", xmax="xmax"), width=0.3, size=1.2, color="#666666")
    + geom_point(size=6, alpha=0.9)
    + scale_color_gradient(low="#FFD43B", high="#306998", name="Importance")
    + scale_y_discrete()
    + labs(x="Mean Decrease in Model Score", y="Feature", title="bar-permutation-importance · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_y=element_text(size=14),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800x2700) - path="." saves to current directory
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactive view
ggsave(plot, "plot.html", path=".")
