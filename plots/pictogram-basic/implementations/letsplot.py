"""pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-03-10
"""

from lets_plot import *


LetsPlot.setup_html()

# Data - Fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 12, 8]
icon_value = 5  # Each icon represents 5 thousand tonnes

# Build pictogram grid using numeric y positions
cat_list = []
col_list = []
alpha_list = []
y_list = []

for i, (cat, val) in enumerate(zip(categories, values)):
    y_pos = len(categories) - 1 - i  # Highest value at top
    full_icons = int(val // icon_value)
    remainder = val % icon_value
    for c in range(full_icons):
        cat_list.append(cat)
        col_list.append(float(c))
        y_list.append(float(y_pos))
        alpha_list.append(1.0)
    if remainder > 0:
        cat_list.append(cat)
        col_list.append(float(full_icons))
        y_list.append(float(y_pos))
        alpha_list.append(remainder / icon_value)

# Color palette per category
palette = ["#306998", "#E8843C", "#E8C53C", "#7B4F8B", "#3DAE6F"]
color_list = [palette[categories.index(c)] for c in cat_list]

data = {"category": cat_list, "col": col_list, "row": y_list, "alpha": alpha_list, "fill_color": color_list}

# Y-axis labels
y_breaks = [float(len(categories) - 1 - i) for i in range(len(categories))]

# Plot using geom_tile for larger, tightly packed squares
plot = (
    ggplot(data, aes(x="col", y="row"))
    + geom_tile(aes(alpha="alpha", fill="category"), width=0.85, height=0.85, color="white", size=2)
    + scale_alpha_identity()
    + scale_fill_manual(values=palette, limits=categories)
    + scale_y_continuous(breaks=y_breaks, labels=categories, expand=[0.08, 0])
    + scale_x_continuous(limits=[-0.6, 7.6], expand=[0, 0])
    + labs(
        x="",
        y="",
        title="Fruit Production · pictogram-basic · letsplot · pyplots.ai",
        caption=f"Each square = {icon_value} thousand tonnes",
    )
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        plot_caption=element_text(size=18, color="#666666"),
        axis_title=element_blank(),
        axis_text_y=element_text(size=20, face="bold"),
        axis_text_x=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        legend_position="none",
    )
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
