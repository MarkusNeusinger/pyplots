""" pyplots.ai
volcano-basic: Volcano Plot for Statistical Significance
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated differential gene expression results
np.random.seed(42)
n_genes = 500

# Generate fold changes (mostly near zero, some with larger effects)
log2_fc = np.concatenate(
    [
        np.random.normal(0, 0.5, 400),  # Non-significant genes
        np.random.normal(2.5, 0.5, 50),  # Up-regulated
        np.random.normal(-2.5, 0.5, 50),  # Down-regulated
    ]
)

# Generate p-values (correlated with effect size)
base_pval = np.random.uniform(0.001, 0.9, n_genes)
# Significant genes have lower p-values
base_pval[400:] = np.random.uniform(0.0001, 0.01, 100)
neg_log10_pval = -np.log10(base_pval)

# Classification thresholds
fc_threshold = 1.0  # log2 fold change threshold (2-fold)
pval_threshold = 1.3  # -log10(0.05) ≈ 1.3

# Classify genes
up_regulated = (log2_fc > fc_threshold) & (neg_log10_pval > pval_threshold)
down_regulated = (log2_fc < -fc_threshold) & (neg_log10_pval > pval_threshold)
not_significant = ~(up_regulated | down_regulated)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#888888",
        "#c0392b",
        "#2980b9",
        "#555555",
        "#555555",
        "#555555",
    ),  # Gray, Red, Blue, then neutral for lines
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=36,
    value_font_size=20,
    stroke_width=2,
    opacity=0.7,
    opacity_hover=1.0,
    font_family="DejaVu Sans",
)

# Calculate y-axis range (ensure minimum at 0)
y_max = max(neg_log10_pval) + 0.5

# Create XY chart (scatter plot)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="volcano-basic · pygal · pyplots.ai",
    x_title="Log₂ Fold Change",
    y_title="-Log₁₀(p-value)",
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=28,
    dots_size=8,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    range=(-5, 5),
    yrange=(0, y_max),
    y_labels_major_count=6,
    x_labels_major_count=11,
    truncate_legend=-1,
)

# Prepare data points for each category
not_sig_points = [
    {"value": (float(log2_fc[i]), float(neg_log10_pval[i]))} for i in range(n_genes) if not_significant[i]
]
up_points = [{"value": (float(log2_fc[i]), float(neg_log10_pval[i]))} for i in range(n_genes) if up_regulated[i]]
down_points = [{"value": (float(log2_fc[i]), float(neg_log10_pval[i]))} for i in range(n_genes) if down_regulated[i]]

# Add data series
chart.add("Not Significant", not_sig_points)
chart.add("Up-regulated", up_points)
chart.add("Down-regulated", down_points)

# Add threshold lines as separate series (hidden from legend)
# Horizontal line at p-value threshold (y = 1.3)
h_line = [{"value": (-5, pval_threshold)}, {"value": (5, pval_threshold)}]
chart.add(None, h_line, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "10, 5"})

# Vertical lines at fold change thresholds (x = ±1)
v_line_pos = [{"value": (fc_threshold, 0)}, {"value": (fc_threshold, y_max)}]
v_line_neg = [{"value": (-fc_threshold, 0)}, {"value": (-fc_threshold, y_max)}]
chart.add(None, v_line_pos, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "10, 5"})
chart.add(None, v_line_neg, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "10, 5"})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
