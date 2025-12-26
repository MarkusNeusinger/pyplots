"""pyplots.ai
precision-recall: Precision-Recall Curve
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-26
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Generate synthetic precision-recall data for two classifiers
np.random.seed(42)

# Simulate two classifiers with different performance characteristics
# Using realistic PR curve shapes (monotonically decreasing precision as recall increases)

# Logistic Regression - moderate performance
n_points = 50
recall_lr = np.linspace(0, 1, n_points)
# Simulate precision that decreases with recall (typical PR curve shape)
precision_lr = 0.95 * np.exp(-1.5 * recall_lr) + 0.30 + np.random.normal(0, 0.02, n_points)
precision_lr = np.clip(precision_lr, 0.30, 1.0)
# Ensure monotonically non-increasing (enforce PR curve property)
precision_lr = np.maximum.accumulate(precision_lr[::-1])[::-1]
# Add the final point (recall=1)
recall_lr = np.append(recall_lr, 1.0)
precision_lr = np.append(precision_lr, 0.30)
# Calculate Average Precision (area under PR curve)
ap_lr = np.trapezoid(precision_lr, recall_lr)

# Random Forest - better performance
recall_rf = np.linspace(0, 1, n_points)
precision_rf = 0.98 * np.exp(-0.8 * recall_rf) + 0.35 + np.random.normal(0, 0.015, n_points)
precision_rf = np.clip(precision_rf, 0.35, 1.0)
precision_rf = np.maximum.accumulate(precision_rf[::-1])[::-1]
recall_rf = np.append(recall_rf, 1.0)
precision_rf = np.append(precision_rf, 0.35)
ap_rf = np.trapezoid(precision_rf, recall_rf)

# Calculate baseline (positive class ratio for imbalanced dataset ~30%)
baseline = 0.30

# Create DataFrame for plotting
df_lr = pd.DataFrame({"Recall": recall_lr, "Precision": precision_lr, "Model": f"Logistic Regression (AP={ap_lr:.3f})"})

df_rf = pd.DataFrame({"Recall": recall_rf, "Precision": precision_rf, "Model": f"Random Forest (AP={ap_rf:.3f})"})

df = pd.concat([df_lr, df_rf], ignore_index=True)

# Create baseline annotation data
baseline_label_df = pd.DataFrame({"x": [0.95], "y": [baseline + 0.04], "label": [f"Random Baseline ({baseline:.2f})"]})

# Create precision-recall curve plot
plot = (
    ggplot(df, aes(x="Recall", y="Precision", color="Model"))
    + geom_step(size=1.5, direction="vh")  # Stepped line for PR curve
    + geom_hline(yintercept=baseline, linetype="dashed", color="#888888", size=1.0)
    + geom_text(data=baseline_label_df, mapping=aes(x="x", y="y", label="label"), color="#666666", size=14, hjust=1.0)
    + scale_color_manual(values=["#306998", "#FFD43B"])  # Python colors
    + scale_x_continuous(limits=[0, 1.0], breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    + scale_y_continuous(limits=[0, 1.05], breaks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    + labs(
        x="Recall (Sensitivity)",
        y="Precision (Positive Predictive Value)",
        title="precision-recall · letsplot · pyplots.ai",
        color="Classifier",
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position=[0.35, 0.25],
        legend_background=element_rect(fill="white", color="#cccccc"),
        panel_grid_major=element_line(color="#dddddd", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)  # Will be scaled 3x to 4800x2700
)

# Save as PNG (scale 3x for 4800x2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactive version
ggsave(plot, "plot.html", path=".")
