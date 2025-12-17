"""
rug-basic: Basic Rug Plot
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Mixed distribution showing clustering and gaps
np.random.seed(42)
cluster1 = np.random.normal(2, 0.3, 40)
cluster2 = np.random.normal(5, 0.5, 60)
cluster3 = np.random.normal(8, 0.4, 30)
sparse = np.random.uniform(10, 12, 10)
values = np.concatenate([cluster1, cluster2, cluster3, sparse])

df = pd.DataFrame({"values": values})

# Rug data - create segments at bottom of plot
rug_height = 0.02  # Height of rug ticks as fraction of max density
df_rug = pd.DataFrame(
    {"x": values, "xend": values, "y": np.zeros(len(values)), "yend": np.full(len(values), rug_height)}
)

# Plot - Density with rug using segments at bottom
plot = (
    ggplot(df, aes(x="values"))
    + geom_density(fill="#306998", alpha=0.3, size=1.5, color="#306998")
    + geom_segment(aes(x="x", xend="xend", y="y", yend="yend"), data=df_rug, color="#306998", alpha=0.7, size=1.5)
    + labs(x="Values", y="Density", title="rug-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid=element_line(color="#cccccc", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save PNG and HTML
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
