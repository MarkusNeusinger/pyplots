"""
violin-basic: Basic Violin Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_violin, ggplot, labs, scale_fill_brewer, theme, theme_minimal


# Data - Employee performance scores by department
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
data = []

# Generate realistic performance scores with different distributions per department
distributions = {
    "Engineering": (75, 10),  # High mean, moderate spread
    "Marketing": (70, 15),  # Medium mean, wider spread
    "Sales": (65, 20),  # Lower mean, high variability
    "HR": (72, 8),  # Medium-high mean, tight distribution
    "Finance": (78, 12),  # High mean, moderate spread
}

for dept in departments:
    mean, std = distributions[dept]
    n = np.random.randint(80, 150)  # 80-150 observations per department
    scores = np.random.normal(mean, std, n)
    scores = np.clip(scores, 0, 100)  # Keep scores in valid range
    for score in scores:
        data.append({"Department": dept, "Performance Score": score})

df = pd.DataFrame(data)

# Create violin plot
plot = (
    ggplot(df, aes(x="Department", y="Performance Score", fill="Department"))
    + geom_violin(draw_quantiles=[0.25, 0.5, 0.75], trim=False)
    + labs(title="Employee Performance Score Distribution by Department", x="Department", y="Performance Score")
    + scale_fill_brewer(type="qual", palette="Set2")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20, weight="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="none",  # Hide legend since x-axis already shows categories
    )
)

# Save
plot.save("plot.png", dpi=300)
