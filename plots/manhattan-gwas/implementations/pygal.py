""" pyplots.ai
manhattan-gwas: Manhattan Plot for GWAS
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Seed for reproducibility
np.random.seed(42)

# Generate simulated GWAS data
# Chromosome lengths (simplified, in Mb scale)
chrom_lengths = {
    "1": 249,
    "2": 243,
    "3": 198,
    "4": 191,
    "5": 182,
    "6": 171,
    "7": 159,
    "8": 146,
    "9": 141,
    "10": 136,
    "11": 135,
    "12": 134,
    "13": 115,
    "14": 107,
    "15": 102,
    "16": 90,
    "17": 83,
    "18": 80,
    "19": 59,
    "20": 64,
    "21": 47,
    "22": 51,
}

chromosomes = list(chrom_lengths.keys())
n_snps_per_chrom = 500

# Storage for data
all_chroms = []
all_cumulative_pos = []
all_pvalues = []

cumulative_offset = 0

for chrom in chromosomes:
    length = chrom_lengths[chrom]
    positions = np.sort(np.random.uniform(0, length, n_snps_per_chrom))

    # Generate p-values: mostly uniform with some significant hits
    pvalues = np.random.uniform(0, 1, n_snps_per_chrom)

    # Add significant peaks on selected chromosomes
    if chrom in ["6", "11", "16"]:
        n_sig = np.random.randint(3, 8)
        sig_indices = np.random.choice(n_snps_per_chrom, n_sig, replace=False)
        pvalues[sig_indices] = 10 ** (-np.random.uniform(8, 15, n_sig))

    # Add suggestive signals
    n_sugg = np.random.randint(5, 15)
    sugg_indices = np.random.choice(n_snps_per_chrom, n_sugg, replace=False)
    pvalues[sugg_indices] = 10 ** (-np.random.uniform(5, 8, n_sugg))

    cumulative_positions = positions + cumulative_offset
    all_chroms.extend([chrom] * n_snps_per_chrom)
    all_cumulative_pos.extend(cumulative_positions)
    all_pvalues.extend(pvalues)

    cumulative_offset += length

# Convert to -log10 p-values
neg_log_pvalues = -np.log10(np.array(all_pvalues))

# Thresholds for reference
genome_wide_sig = -np.log10(5e-8)  # ~7.3
suggestive_sig = 5  # -log10(1e-5)

# Custom style with alternating blue/gray for chromosomes
chrom_colors = ["#306998" if i % 2 == 0 else "#808080" for i in range(22)]

custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(chrom_colors),
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=28,
    value_font_size=24,
    font_family="sans-serif",
)

# Create XY scatter chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="manhattan-gwas · pygal · pyplots.ai",
    x_title="Genomic Position (Mb)",
    y_title="-log₁₀(p-value)  |  Significance: 7.3  |  Suggestive: 5.0",
    show_legend=False,
    stroke=False,
    dots_size=8,
    show_x_guides=False,
    show_y_guides=True,
    truncate_label=-1,
    print_values=False,
    x_label_rotation=0,
    range=(0, 16),
    xrange=(0, cumulative_offset),
)

# Add data by chromosome with alternating colors
for chrom in chromosomes:
    chrom_mask = [c == chrom for c in all_chroms]
    chrom_x = [all_cumulative_pos[j] for j in range(len(all_chroms)) if chrom_mask[j]]
    chrom_y = [neg_log_pvalues[j] for j in range(len(all_chroms)) if chrom_mask[j]]
    points = list(zip(chrom_x, chrom_y, strict=True))
    chart.add(f"Chr {chrom}", points, stroke=False, show_dots=True)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
