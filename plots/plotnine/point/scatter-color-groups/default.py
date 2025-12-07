"""
scatter-color-groups: Scatter Plot with Color Groups
Library: plotnine
"""

import seaborn as sns
from plotnine import aes, geom_point, ggplot, labs, scale_color_brewer, theme, theme_minimal


# Data
data = sns.load_dataset("iris")

# Create plot
plot = (
    ggplot(data, aes(x="sepal_length", y="sepal_width", color="species"))
    + geom_point(size=3, alpha=0.7)
    + labs(x="Sepal Length (cm)", y="Sepal Width (cm)", title="Scatter Plot with Color Groups", color="Species")
    + scale_color_brewer(type="qual", palette="Set2")
    + theme_minimal()
    + theme(figure_size=(16, 9))
)

# Save
plot.save("plot.png", dpi=300)
