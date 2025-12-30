"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_jitter, ggplot, labs, scale_color_manual, theme, theme_minimal


# Data
np.random.seed(42)

# Create realistic crop yield data across different soil types
categories = ["Sandy Soil", "Clay Soil", "Loam Soil", "Peat Soil"]
n_per_category = 25

data = []
# Different distributions for each soil type to show variety
means = [32, 45, 52, 38]
stds = [6, 8, 5, 10]

for cat, mean, std in zip(categories, means, stds, strict=True):
    values = np.random.normal(mean, std, n_per_category)
    for val in values:
        data.append({"Soil Type": cat, "Yield": val})

df = pd.DataFrame(data)

# Define colors using Python Blue and colorblind-safe palette
colors = ["#306998", "#FFD43B", "#2E8B57", "#CD853F"]

# Plot
plot = (
    ggplot(df, aes(x="Soil Type", y="Yield", color="Soil Type"))
    + geom_jitter(size=4, alpha=0.7, width=0.25, height=0)
    + labs(x="Soil Type", y="Crop Yield (kg/m²)", title="cat-strip · plotnine · pyplots.ai")
    + scale_color_manual(values=colors)
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
