""" pyplots.ai
box-basic: Basic Box Plot
Library: plotnine 0.15.3 | Python 3.14
Quality: 85/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_cartesian,
    element_blank,
    element_line,
    element_text,
    geom_boxplot,
    ggplot,
    labs,
    scale_fill_brewer,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support", "Research"]
records = []

for cat in categories:
    n = np.random.randint(60, 120)
    if cat == "Engineering":
        values = np.random.normal(95000, 15000, n)
    elif cat == "Marketing":
        values = np.random.normal(75000, 12000, n)
    elif cat == "Sales":
        base = np.random.normal(68000, 18000, n)
        outliers = np.random.uniform(120000, 145000, 5)
        values = np.concatenate([base, outliers])
    elif cat == "Support":
        values = np.random.normal(55000, 8000, n)
    else:  # Research
        values = np.random.normal(85000, 20000, n)
    records.extend({"department": cat, "salary": v} for v in values)

df = pd.DataFrame(records)
dept_order = ["Support", "Marketing", "Sales", "Research", "Engineering"]
df["department"] = pd.Categorical(df["department"], categories=dept_order, ordered=True)

# Plot
plot = (
    ggplot(df, aes(x="department", y="salary", fill="department"))
    + geom_boxplot(outlier_size=2.5, outlier_alpha=0.5, outlier_colour="#555555", size=0.6, alpha=0.85)
    + scale_fill_brewer(type="qual", palette="Set2")
    + coord_cartesian(ylim=(25000, 155000))
    + labs(x="Department", y="Salary ($)", title="box-basic \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_position="none",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#DDDDDD", size=0.5, alpha=0.4),
        axis_line_x=element_line(color="#333333", size=0.5),
        axis_line_y=element_line(color="#333333", size=0.5),
        axis_ticks_major_x=element_blank(),
        axis_ticks_major_y=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300)
