"""pyplots.ai
histogram-basic: Basic Histogram
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_histogram, ggplot, labs, theme, theme_minimal


# Data
np.random.seed(42)
n_points = 500
values = np.random.normal(loc=70, scale=12, size=n_points)

df = pd.DataFrame({"values": values})

# Plot
plot = (
    ggplot(df, aes(x="values"))
    + geom_histogram(bins=25, fill="#306998", color="white", alpha=0.85)
    + labs(x="Test Score", y="Frequency", title="histogram-basic · plotnine · pyplots.ai")
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
