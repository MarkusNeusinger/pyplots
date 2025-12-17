"""
swarm-basic: Basic Swarm Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_text,
    geom_point,
    ggplot,
    labs,
    position_jitter,
    scale_color_manual,
    stat_summary,
    theme,
    theme_minimal,
)


# Data - Performance scores across departments
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "Support"]
data = []

# Generate varied distributions for each department
distributions = {
    "Engineering": {"mean": 82, "std": 8, "n": 45},
    "Marketing": {"mean": 75, "std": 12, "n": 50},
    "Sales": {"mean": 78, "std": 15, "n": 55},
    "Support": {"mean": 85, "std": 6, "n": 40},
}

for dept, params in distributions.items():
    scores = np.random.normal(params["mean"], params["std"], params["n"])
    # Clip scores to realistic range [0, 100]
    scores = np.clip(scores, 40, 100)
    data.extend([(dept, score) for score in scores])

df = pd.DataFrame(data, columns=["department", "score"])

# Create swarm plot using jittered points
plot = (
    ggplot(df, aes(x="department", y="score", color="department"))
    + geom_point(position=position_jitter(width=0.25, height=0, random_state=42), size=4, alpha=0.7)
    # Add median markers for each category
    + stat_summary(fun_y=np.median, geom="point", size=8, shape="D", color="#2C3E50")
    + scale_color_manual(values=["#306998", "#FFD43B", "#4B8BBE", "#FFE873"])
    + labs(x="Department", y="Performance Score", title="swarm-basic · plotnine · pyplots.ai")
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
