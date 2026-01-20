""" pyplots.ai
pie-portfolio-interactive: Interactive Portfolio Allocation Chart
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-20
"""

import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Portfolio allocation by asset class with individual holdings
portfolio_data = {
    "asset": [
        "Apple Inc.",
        "Microsoft Corp.",
        "Amazon.com",
        "NVIDIA Corp.",
        "US Treasury 10Y",
        "Corporate Bonds AAA",
        "Municipal Bonds",
        "Real Estate Fund",
        "Gold ETF",
        "Private Equity",
        "Cash Reserves",
    ],
    "weight": [12.0, 10.0, 8.0, 7.0, 18.0, 12.0, 8.0, 10.0, 6.0, 5.0, 4.0],
    "category": [
        "Equities",
        "Equities",
        "Equities",
        "Equities",
        "Fixed Income",
        "Fixed Income",
        "Fixed Income",
        "Alternatives",
        "Alternatives",
        "Alternatives",
        "Cash",
    ],
}

df = pd.DataFrame(portfolio_data)

# Aggregate by category for main pie chart
category_weights = df.groupby("category", as_index=False)["weight"].sum()
category_weights = category_weights.sort_values("weight", ascending=False)

# Reorder categories
category_order = category_weights["category"].tolist()
category_weights["category"] = pd.Categorical(category_weights["category"], categories=category_order, ordered=True)

# Color palette for asset categories (Python Blue first, colorblind-safe)
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create center label
center_df = pd.DataFrame({"x": [0.0], "y": [0.0], "label": ["Portfolio\n100%"]})

# Create interactive pie chart with tooltips for drill-down preview
plot = (
    ggplot(category_weights)  # noqa: F405
    + geom_pie(  # noqa: F405
        aes(slice="weight", fill="category"),  # noqa: F405
        stat="identity",
        size=40,
        hole=0.4,  # Donut style for better readability
        stroke=2,
        color="white",
        tooltips=layer_tooltips()  # noqa: F405
        .title("@category")
        .line("Allocation: @weight%")
        .format("weight", ".1f"),
        labels=layer_labels()  # noqa: F405
        .line("@weight%")
        .format("weight", ".1f")
        .size(16),
    )
    + geom_label(  # noqa: F405
        aes(x="x", y="y", label="label"),  # noqa: F405
        data=center_df,
        size=18,
        fill="white",
        alpha=0.9,
        label_padding=0.5,
    )
    + scale_fill_manual(values=colors)  # noqa: F405
    + labs(  # noqa: F405
        title="Portfolio Allocation · pie-portfolio-interactive · letsplot · pyplots.ai", fill="Asset Class"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_void()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=26, hjust=0.5, face="bold"),  # noqa: F405
        legend_title=element_text(size=20),  # noqa: F405
        legend_text=element_text(size=18),  # noqa: F405
        legend_position=[0.85, 0.5],
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
