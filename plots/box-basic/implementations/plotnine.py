"""
box-basic: Basic Box Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_boxplot, ggplot, labs, theme, theme_minimal


# Data
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = {"category": [], "value": []}

# Generate salary data for each department
for cat in categories:
    n = np.random.randint(50, 150)
    if cat == "Engineering":
        values = np.random.normal(95000, 15000, n)
    elif cat == "Marketing":
        values = np.random.normal(75000, 12000, n)
    elif cat == "Sales":
        values = np.random.normal(70000, 20000, n)
    else:  # Support
        values = np.random.normal(55000, 10000, n)
    data["category"].extend([cat] * n)
    data["value"].extend(values)

df = pd.DataFrame(data)

# Plot
plot = (
    ggplot(df, aes(x="category", y="value", fill="category"))
    + geom_boxplot(outlier_size=3, outlier_alpha=0.6, size=0.8)
    + labs(x="Department", y="Salary ($)", title="box-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
