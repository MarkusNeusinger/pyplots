"""pyplots.ai
heatmap-risk-matrix: Risk Assessment Matrix (Probability vs Impact)
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 80/100 | Created: 2026-03-17
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data
np.random.seed(42)

likelihood_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
impact_labels = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]

# Build background grid with risk zones
grid_rows = []
for li in range(1, 6):
    for im in range(1, 6):
        score = li * im
        if score <= 4:
            zone = "Low"
        elif score <= 9:
            zone = "Medium"
        elif score <= 16:
            zone = "High"
        else:
            zone = "Critical"
        grid_rows.append({"likelihood": li, "impact": im, "score": score, "zone": zone, "score_label": str(score)})
grid_df = pd.DataFrame(grid_rows)
grid_df["zone"] = pd.Categorical(grid_df["zone"], categories=["Low", "Medium", "High", "Critical"], ordered=True)

# Risk items - distributed across all zones including Critical
risks = pd.DataFrame(
    {
        "risk_name": [
            "Server Outage",
            "Data Breach",
            "Budget Overrun",
            "Key Staff Loss",
            "Vendor Failure",
            "Scope Creep",
            "Regulatory Change",
            "Tech Debt",
            "Integration Bug",
            "Supply Delay",
            "Currency Risk",
            "PR Crisis",
            "Patent Dispute",
            "Power Failure",
            "Cyber Attack",
        ],
        "likelihood": [4, 3, 4, 2, 2, 5, 3, 4, 3, 1, 3, 1, 1, 2, 5],
        "impact": [5, 5, 3, 4, 3, 2, 3, 2, 4, 3, 2, 5, 4, 1, 5],
        "category": [
            "Technical",
            "Technical",
            "Financial",
            "Operational",
            "Operational",
            "Operational",
            "Financial",
            "Technical",
            "Technical",
            "Operational",
            "Financial",
            "Operational",
            "Financial",
            "Technical",
            "Technical",
        ],
    }
)

# Smart jitter: offset risks sharing same cell to avoid label overlap
cell_counts = {}
offsets_x = []
offsets_y = []
for _, row in risks.iterrows():
    cell = (row["likelihood"], row["impact"])
    idx = cell_counts.get(cell, 0)
    cell_counts[cell] = idx + 1
    # Spread items in same cell with distinct offsets
    offset_patterns = [(0, 0.15), (0, -0.15), (-0.2, 0), (0.2, 0)]
    ox, oy = offset_patterns[idx % len(offset_patterns)]
    offsets_x.append(ox)
    offsets_y.append(oy)

risks["lk_jitter"] = risks["likelihood"] + np.array(offsets_x)
risks["im_jitter"] = risks["impact"] + np.array(offsets_y)

# Tooltips for lets-plot distinctive interactivity
risk_tooltips = (
    layer_tooltips()
    .line("@risk_name")
    .line("Category: @category")
    .line("Likelihood: @likelihood")
    .line("Impact: @impact")
)

# Colorblind-safe zone palette (blue-yellow-orange-dark)
zone_colors = {"Low": "#4575B4", "Medium": "#FEE090", "High": "#F46D43", "Critical": "#A50026"}

# Plot
plot = (
    ggplot()
    + geom_tile(aes(x="likelihood", y="impact", fill="zone"), data=grid_df, color="white", size=1.5, tooltips="none")
    + geom_text(aes(x="likelihood", y="impact", label="score_label"), data=grid_df, size=11, color="rgba(0,0,0,0.2)")
    + geom_point(
        aes(x="lk_jitter", y="im_jitter", color="category"), data=risks, size=7, alpha=0.9, tooltips=risk_tooltips
    )
    + geom_text(
        aes(x="lk_jitter", y="im_jitter", label="risk_name"),
        data=risks,
        size=8,
        nudge_y=0.28,
        fontface="bold",
        label_padding=0.2,
    )
    + scale_fill_manual(values=zone_colors, name="Risk Level")
    + scale_color_manual(
        values={"Technical": "#306998", "Financial": "#7B2D8E", "Operational": "#D35400"}, name="Category"
    )
    + scale_x_continuous(breaks=[1, 2, 3, 4, 5], labels=likelihood_labels, limits=[0.5, 5.5])
    + scale_y_continuous(breaks=[1, 2, 3, 4, 5], labels=impact_labels, limits=[0.5, 5.5])
    + coord_fixed(ratio=1)
    + labs(x="Likelihood", y="Impact", title="heatmap-risk-matrix · lets-plot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        panel_grid=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
