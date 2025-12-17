"""
strip-basic: Basic Strip Plot
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


# Data - Test scores across different teaching methods
np.random.seed(42)

methods = ["Traditional", "Flipped", "Hybrid", "Online"]
data = []

# Generate varied distributions for each method
distributions = {
    "Traditional": {"mean": 72, "std": 10, "n": 35},
    "Flipped": {"mean": 78, "std": 8, "n": 40},
    "Hybrid": {"mean": 75, "std": 12, "n": 38},
    "Online": {"mean": 70, "std": 15, "n": 42},
}

for method, params in distributions.items():
    scores = np.random.normal(params["mean"], params["std"], params["n"])
    # Clip scores to realistic range
    scores = np.clip(scores, 40, 100)
    data.extend([(method, score) for score in scores])

df = pd.DataFrame(data, columns=["method", "score"])

# Create strip plot with jittered points
plot = (
    ggplot(df, aes(x="method", y="score", color="method"))
    + geom_point(position=position_jitter(width=0.2, height=0, random_state=42), size=4, alpha=0.6)
    # Add mean markers as reference
    + stat_summary(fun_y=np.mean, geom="point", size=8, shape="D", color="#2C3E50")
    + scale_color_manual(values=["#306998", "#FFD43B", "#4B8BBE", "#FFE873"])
    + labs(x="Teaching Method", y="Test Score", title="strip-basic · plotnine · pyplots.ai")
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
