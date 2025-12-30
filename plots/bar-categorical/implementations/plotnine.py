"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_blank, element_text, geom_bar, ggplot, labs, scale_fill_manual, theme, theme_minimal


# Data - Survey responses for product satisfaction
np.random.seed(42)
categories = ["Excellent", "Good", "Average", "Poor", "Very Poor"]
# Create uneven distribution to show varying counts
weights = [0.25, 0.35, 0.20, 0.12, 0.08]
n_responses = 200
responses = np.random.choice(categories, size=n_responses, p=weights)

df = pd.DataFrame({"Satisfaction": responses})

# Reorder categories for logical display
df["Satisfaction"] = pd.Categorical(df["Satisfaction"], categories=categories, ordered=True)

# Plot
plot = (
    ggplot(df, aes(x="Satisfaction", fill="Satisfaction"))
    + geom_bar(width=0.7, alpha=0.9)
    + labs(x="Satisfaction Level", y="Number of Responses", title="bar-categorical · plotnine · pyplots.ai")
    + scale_fill_manual(values=["#306998", "#4A90C2", "#FFD43B", "#E8A838", "#CC6633"])
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
        panel_grid_major_x=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
