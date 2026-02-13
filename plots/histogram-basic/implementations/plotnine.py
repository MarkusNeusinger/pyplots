""" pyplots.ai
histogram-basic: Basic Histogram
Library: plotnine 0.15.3 | Python 3.14.0
Quality: 79/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_histogram, ggplot, labs, scale_x_continuous, theme, theme_minimal


# Data
np.random.seed(42)
n_points = 500
raw_scores = np.random.beta(a=5, b=3, size=n_points) * 100
scores = np.clip(raw_scores, 0, 100)

df = pd.DataFrame({"score": scores})

# Plot
plot = (
    ggplot(df, aes(x="score"))
    + geom_histogram(bins=25, fill="#306998", color="white", alpha=0.85)
    + scale_x_continuous(breaks=range(0, 101, 10))
    + labs(x="Test Score (points)", y="Frequency (count)", title="histogram-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
