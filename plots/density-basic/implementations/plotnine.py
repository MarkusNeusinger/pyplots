"""pyplots.ai
density-basic: Basic Density Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_cartesian,
    element_line,
    element_text,
    geom_density,
    geom_rug,
    ggplot,
    labs,
    scale_x_continuous,
    theme,
    theme_minimal,
)


# Data - simulating test scores with bimodal distribution
np.random.seed(42)
test_scores = np.concatenate(
    [
        np.random.normal(72, 10, 150),  # Main distribution
        np.random.normal(88, 5, 50),  # High achievers
    ]
)
test_scores = np.clip(test_scores, 0, 100)  # Scores between 0-100

df = pd.DataFrame({"score": test_scores})

# Plot with bandwidth adjustment for smoother curve
plot = (
    ggplot(df, aes(x="score"))
    + geom_density(fill="#306998", color="#306998", alpha=0.6, size=1.5, bw="scott")
    + geom_rug(color="#FFD43B", alpha=0.7, size=1)
    + labs(x="Test Score (points)", y="Probability Density", title="density-basic · plotnine · pyplots.ai")
    + scale_x_continuous(limits=(30, 100), breaks=range(30, 101, 10))
    + coord_cartesian(xlim=(30, 100))
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", alpha=0.3),
        panel_grid_minor=element_line(color="#eeeeee", alpha=0.2),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
