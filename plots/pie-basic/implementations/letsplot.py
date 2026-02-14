"""pyplots.ai
pie-basic: Basic Pie Chart
Library: letsplot 4.8.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

from lets_plot import *  # noqa: F403
from lets_plot import ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Global smartphone market share (2024)
data = {
    "company": ["Apple", "Samsung", "Xiaomi", "OPPO", "Others"],
    "share": [23.1, 19.4, 13.7, 8.8, 35.0],
    "explode": [0.0, 0.0, 0.0, 0.08, 0.0],
}

# Percentage labels
total = sum(data["share"])
data["pct"] = [v / total * 100 for v in data["share"]]

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4CAF50", "#FF7043", "#90A4AE"]

# Plot
plot = (
    ggplot(data)  # noqa: F405
    + geom_pie(  # noqa: F405
        aes(slice="share", fill="company", explode="explode"),  # noqa: F405
        stat="identity",
        size=28,
        hole=0,
        stroke=1,
        stroke_side="outer",
        color="white",
        spacer_width=1.5,
        spacer_color="white",
        labels=layer_labels()  # noqa: F405
        .line("@pct")
        .format("pct", "{.1f}%")
        .size(16),
    )
    + scale_fill_manual(values=colors)  # noqa: F405
    + labs(  # noqa: F405
        title="Global Smartphone Market Share · pie-basic · letsplot · pyplots.ai", fill="Company"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_void()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=22, hjust=0.5),  # noqa: F405
        legend_title=element_text(size=18),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="bottom",
        legend_direction="horizontal",
        plot_margin=[60, 20, 30, 20],
    )
)

# Save
ggsave(plot, filename="plot.png", path=".", scale=3)
ggsave(plot, filename="plot.html", path=".")
