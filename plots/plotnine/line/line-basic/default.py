"""
line-basic: Basic Line Plot
Library: plotnine
"""

import pandas as pd
from plotnine import aes, geom_line, geom_point, ggplot, labs, theme, theme_minimal


# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

# Plot
plot = (
    ggplot(data, aes(x="time", y="value"))
    + geom_line(color="#306998", size=2)
    + geom_point(color="#306998", size=4)
    + labs(x="Time", y="Value", title="Basic Line Plot")
    + theme_minimal()
    + theme(figure_size=(16, 9))
)

# Save
plot.save("plot.png", dpi=300)
