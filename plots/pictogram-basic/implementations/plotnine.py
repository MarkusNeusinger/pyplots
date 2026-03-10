""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-10
"""

import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    labs,
    scale_alpha_identity,
    scale_fill_identity,
    scale_x_continuous,
    scale_y_discrete,
    theme,
    theme_void,
)


# Data: Fruit production (thousands of tonnes) — sorted by value for visual hierarchy
categories = ["Apples", "Grapes", "Oranges", "Bananas", "Strawberries"]
values = [35, 28, 22, 18, 12]
unit_value = 5  # Each icon = 5 thousand tonnes

# Cohesive palette per fruit (starting with Python Blue)
fruit_colors = {
    "Apples": "#306998",
    "Grapes": "#7B4F8A",
    "Oranges": "#E8783A",
    "Bananas": "#D4A843",
    "Strawberries": "#C0392B",
}

# Expand data into one row per icon position
rows = []
for cat, val in zip(categories, values, strict=True):
    full_icons = val // unit_value
    remainder = val % unit_value
    for i in range(full_icons):
        rows.append({"category": cat, "col": i + 1, "alpha": 1.0, "fill": fruit_colors[cat]})
    if remainder > 0:
        rows.append(
            {"category": cat, "col": full_icons + 1, "alpha": remainder / unit_value, "fill": fruit_colors[cat]}
        )

df = pd.DataFrame(rows)

# Order categories by value (highest at top)
df["category"] = pd.Categorical(df["category"], categories=categories[::-1], ordered=True)

# Value labels at end of each row
max_col = df.groupby("category")["col"].max()
label_df = pd.DataFrame(
    {
        "category": pd.Categorical(categories, categories=categories[::-1], ordered=True),
        "col": [max_col.get(c, 0) + 0.7 for c in categories],
        "label": [f"{v}k" for v in values],
    }
)

# Dynamic x-axis limit based on actual data
x_max = df["col"].max() + 1.5

# Plot using geom_tile for filled square icons
plot = (
    ggplot(df, aes(x="col", y="category"))
    + geom_tile(aes(alpha="alpha", fill="fill"), width=0.78, height=0.7)
    + geom_text(
        aes(x="col", y="category", label="label"), data=label_df, size=14, color="#444444", ha="left", fontweight="bold"
    )
    + scale_fill_identity()
    + scale_alpha_identity()
    + scale_x_continuous(limits=(0.3, x_max), expand=(0, 0))
    + scale_y_discrete(expand=(0.15, 0.15))
    + labs(
        x="",
        y="",
        title="pictogram-basic · plotnine · pyplots.ai",
        caption="Each square = 5 thousand tonnes  ·  Faded = partial unit",
    )
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=26, weight="bold", margin={"b": 20}),
        plot_caption=element_text(size=15, color="#777777", ha="left", margin={"t": 18}),
        axis_text_y=element_text(size=20, color="#333333", ha="right", margin={"r": 14}),
        axis_text_x=element_blank(),
        plot_margin=0.06,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
