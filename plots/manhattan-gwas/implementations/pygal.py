"""pyplots.ai
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

# Track chromosome boundaries for x-axis labels
chrom_boundaries = {}
cumulative_offset = 0

for chrom in chromosomes:
    length = chrom_lengths[chrom]
    positions = np.sort(np.random.uniform(0, length, n_snps_per_chrom))

    # Store chromosome start and midpoint
    chrom_boundaries[chrom] = {
        "start": cumulative_offset,
        "mid": cumulative_offset + length / 2,
        "end": cumulative_offset + length,
    }

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

# Thresholds
genome_wide_sig = -np.log10(5e-8)  # ~7.3
suggestive_sig = 5.0  # -log10(1e-5)


# Function to map genomic position to chromosome label
def position_to_chromosome(pos):
    """Map genomic position to chromosome number for x-axis display."""
    for chrom in chromosomes:
        if chrom_boundaries[chrom]["start"] <= pos < chrom_boundaries[chrom]["end"]:
            return chrom
    return chromosomes[-1]


# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#306998",  # Blue - odd chromosomes
        "#888888",  # Gray - even chromosomes
        "#D62728",  # Red - genome-wide threshold
        "#FF7F0E",  # Orange - suggestive threshold
    ),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=24,
    value_font_size=20,
    font_family="sans-serif",
)

# Create XY scatter chart with interactivity
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="manhattan-gwas · pygal · pyplots.ai",
    x_title="Chromosome (1-22)",
    y_title="-log₁₀(p-value)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    stroke=False,
    dots_size=6,
    show_x_guides=False,
    show_y_guides=True,
    truncate_label=-1,
    print_values=False,
    x_label_rotation=0,
    range=(0, 16),
    xrange=(0, cumulative_offset),
    tooltip_border_radius=10,
    explicit_size=True,
    spacing=20,
    margin=40,
    margin_bottom=100,
    x_labels_major_every=1,
)

# Set x-labels at chromosome midpoints with chromosome numbers
x_label_values = [chrom_boundaries[c]["mid"] for c in chromosomes]
chart.x_labels = x_label_values
chart.x_value_formatter = lambda x: str(position_to_chromosome(x)) if x in x_label_values else ""

# Prepare data by chromosome with alternating colors
odd_chrom_points = []
even_chrom_points = []

for idx, chrom in enumerate(chromosomes):
    chrom_mask = [c == chrom for c in all_chroms]
    chrom_x = [all_cumulative_pos[j] for j in range(len(all_chroms)) if chrom_mask[j]]
    chrom_y = [neg_log_pvalues[j] for j in range(len(all_chroms)) if chrom_mask[j]]

    # Add tooltip with SNP details (pygal distinctive feature)
    points_with_tooltip = [
        {"value": (x, y), "label": f"Chr {chrom}: {x:.1f} Mb, -log₁₀(p)={y:.2f}"}
        for x, y in zip(chrom_x, chrom_y, strict=True)
    ]

    if idx % 2 == 0:
        odd_chrom_points.extend(points_with_tooltip)
    else:
        even_chrom_points.extend(points_with_tooltip)

# Add chromosome data series (blue for odd, gray for even)
chart.add("Odd chromosomes (1,3,5...)", odd_chrom_points, stroke=False, show_dots=True)
chart.add("Even chromosomes (2,4,6...)", even_chrom_points, stroke=False, show_dots=True)

# Add genome-wide significance threshold line (y ≈ 7.3)
n_line_points = 100
threshold_x = np.linspace(0, cumulative_offset, n_line_points)
threshold_line = [
    {"value": (x, genome_wide_sig), "label": f"Genome-wide significance (p=5×10⁻⁸): y={genome_wide_sig:.2f}"}
    for x in threshold_x
]
chart.add("Significance threshold (p=5×10⁻⁸)", threshold_line, stroke=True, show_dots=False, stroke_style={"width": 3})

# Add suggestive threshold line (y = 5.0)
suggestive_line = [
    {"value": (x, suggestive_sig), "label": f"Suggestive threshold (p=1×10⁻⁵): y={suggestive_sig:.1f}"}
    for x in threshold_x
]
chart.add("Suggestive threshold (p=1×10⁻⁵)", suggestive_line, stroke=True, show_dots=False, stroke_style={"width": 2})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
