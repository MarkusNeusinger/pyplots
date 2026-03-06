""" pyplots.ai
genome-track-multi: Genome Track Viewer
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-06
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Label, NumeralTickFormatter, Range1d
from bokeh.plotting import figure


np.random.seed(42)

# Genomic region: chr7, EGFR gene locus (~126,000 bp window)
chrom = "chr7"
region_start = 55_086_000
region_end = 55_212_000

# --- Gene Track Data ---
genes = [{"name": "EGFR", "strand": "+", "tx_start": 55_086_714, "tx_end": 55_205_000}]
exons = [
    (55_086_714, 55_087_200),
    (55_088_900, 55_089_300),
    (55_092_100, 55_092_500),
    (55_096_200, 55_096_700),
    (55_100_300, 55_100_700),
    (55_105_500, 55_105_900),
    (55_110_800, 55_111_300),
    (55_117_500, 55_118_000),
    (55_122_400, 55_122_800),
    (55_127_300, 55_127_700),
    (55_131_500, 55_131_900),
    (55_136_800, 55_137_200),
    (55_140_100, 55_140_500),
    (55_143_700, 55_144_200),
    (55_148_000, 55_148_400),
    (55_151_800, 55_152_300),
    (55_155_500, 55_155_900),
    (55_160_200, 55_160_700),
    (55_165_300, 55_165_800),
    (55_170_800, 55_171_400),
    (55_174_200, 55_174_700),
    (55_181_300, 55_181_800),
    (55_189_200, 55_189_700),
    (55_196_400, 55_196_900),
    (55_200_500, 55_201_000),
    (55_203_800, 55_205_000),
]
utrs_5 = [(55_086_714, 55_087_000)]
utrs_3 = [(55_204_500, 55_205_000)]

# --- Coverage Track Data ---
positions = np.linspace(region_start, region_end, 2000)
base_coverage = np.random.exponential(15, 2000)
for ex_start, ex_end in exons:
    mask = (positions >= ex_start) & (positions <= ex_end)
    base_coverage[mask] += np.random.exponential(45, mask.sum())

# Smooth with numpy convolution (gaussian-like kernel)
kernel_size = 31
kernel = np.exp(-0.5 * np.linspace(-3, 3, kernel_size) ** 2)
kernel /= kernel.sum()
coverage = np.convolve(base_coverage, kernel, mode="same")
coverage = np.clip(coverage, 0, None)

# --- Variant Track Data ---
variant_positions = [
    55_088_100,
    55_092_300,
    55_100_500,
    55_111_000,
    55_118_200,
    55_127_500,
    55_137_000,
    55_144_000,
    55_155_700,
    55_165_500,
    55_174_400,
    55_189_500,
    55_196_700,
    55_201_200,
    55_105_700,
    55_140_300,
    55_152_100,
    55_160_400,
    55_181_500,
    55_170_900,
]
variant_types = ["SNP"] * 14 + ["Indel"] * 6
variant_quality = np.random.uniform(20, 100, len(variant_positions))

# --- Regulatory Track Data ---
reg_elements = [
    {"start": 55_086_000, "end": 55_086_600, "type": "Promoter"},
    {"start": 55_094_000, "end": 55_095_500, "type": "Enhancer"},
    {"start": 55_113_000, "end": 55_114_500, "type": "Enhancer"},
    {"start": 55_133_500, "end": 55_135_000, "type": "CTCF Binding"},
    {"start": 55_157_000, "end": 55_158_500, "type": "Enhancer"},
    {"start": 55_176_000, "end": 55_177_500, "type": "Promoter"},
    {"start": 55_193_000, "end": 55_194_500, "type": "CTCF Binding"},
    {"start": 55_207_000, "end": 55_209_000, "type": "Enhancer"},
]

# Colors
python_blue = "#306998"
exon_color = "#306998"
intron_color = "#7B9EC2"
utr_color = "#A8C4DB"
coverage_fill = "#306998"
snp_color = "#E8833A"
indel_color = "#8B5CF6"
promoter_color = "#22A06B"
enhancer_color = "#FFD43B"
ctcf_color = "#E06C75"

reg_color_map = {"Promoter": promoter_color, "Enhancer": enhancer_color, "CTCF Binding": ctcf_color}

shared_x_range = Range1d(start=region_start, end=region_end)
common_width = 4800
border_left = 200
border_right = 80

# ============================================================
# Track 1: Gene Annotations (top)
# ============================================================
p_gene = figure(
    width=common_width,
    height=550,
    x_range=shared_x_range,
    y_range=Range1d(-1.5, 1.5),
    title="genome-track-multi · bokeh · pyplots.ai",
    tools="",
    toolbar_location=None,
)

# Intron line (gene body)
p_gene.segment(
    x0=[genes[0]["tx_start"]], y0=[0], x1=[genes[0]["tx_end"]], y1=[0], line_color=intron_color, line_width=4
)

# Exons
exon_starts = [e[0] for e in exons]
exon_ends = [e[1] for e in exons]
exon_source = ColumnDataSource(
    data={"left": exon_starts, "right": exon_ends, "top": [0.45] * len(exons), "bottom": [-0.45] * len(exons)}
)
p_gene.quad(
    left="left",
    right="right",
    top="top",
    bottom="bottom",
    source=exon_source,
    fill_color=exon_color,
    line_color="white",
    line_width=1,
    alpha=0.9,
)

# UTRs (thinner)
for utr_start, utr_end in utrs_5 + utrs_3:
    p_gene.quad(
        left=[utr_start],
        right=[utr_end],
        top=[0.2],
        bottom=[-0.2],
        fill_color=utr_color,
        line_color="white",
        line_width=1,
        alpha=0.8,
    )

# Strand direction arrows
arrow_spacing = 6000
arrow_positions = np.arange(region_start + 3000, region_end - 3000, arrow_spacing)
for pos in arrow_positions:
    if region_start < pos < region_end:
        p_gene.scatter(
            x=[pos],
            y=[0],
            size=18,
            angle=-np.pi / 2,
            marker="triangle",
            fill_color=intron_color,
            line_color=None,
            alpha=0.5,
        )

# Gene label
p_gene.text(
    x=[(genes[0]["tx_start"] + genes[0]["tx_end"]) / 2],
    y=[1.0],
    text=["EGFR (+)"],
    text_font_size="26pt",
    text_align="center",
    text_color="#333333",
    text_font_style="italic",
)

# Track label
track_label_gene = Label(
    x=215,
    y=430,
    x_units="screen",
    y_units="screen",
    text="Genes",
    text_font_size="22pt",
    text_color="#555555",
    text_font_style="bold",
)
p_gene.add_layout(track_label_gene)

# Style
p_gene.title.text_font_size = "36pt"
p_gene.title.text_color = "#333333"
p_gene.xaxis.visible = False
p_gene.yaxis.visible = False
p_gene.xgrid.grid_line_color = None
p_gene.ygrid.grid_line_color = None
p_gene.background_fill_color = "#FAFBFC"
p_gene.border_fill_color = "white"
p_gene.outline_line_color = None
p_gene.min_border_left = border_left
p_gene.min_border_right = border_right

# ============================================================
# Track 2: Read Coverage
# ============================================================
p_cov = figure(width=common_width, height=700, x_range=shared_x_range, tools="", toolbar_location=None)

cov_source = ColumnDataSource(data={"x": positions, "y": coverage})
p_cov.varea(x="x", y1=0, y2="y", source=cov_source, fill_color=coverage_fill, fill_alpha=0.45)
p_cov.line(x="x", y="y", source=cov_source, line_color=coverage_fill, line_width=2, alpha=0.8)

# Track label
track_label_cov = Label(
    x=215,
    y=620,
    x_units="screen",
    y_units="screen",
    text="Coverage",
    text_font_size="22pt",
    text_color="#555555",
    text_font_style="bold",
)
p_cov.add_layout(track_label_cov)

# Style
p_cov.xaxis.visible = False
p_cov.yaxis.axis_label = "Read Depth"
p_cov.yaxis.axis_label_text_font_size = "20pt"
p_cov.yaxis.major_label_text_font_size = "16pt"
p_cov.xgrid.grid_line_color = None
p_cov.ygrid.grid_line_color = "#E0E0E0"
p_cov.ygrid.grid_line_alpha = 0.4
p_cov.background_fill_color = "#FAFBFC"
p_cov.border_fill_color = "white"
p_cov.outline_line_color = None
p_cov.min_border_left = border_left
p_cov.min_border_right = border_right

# ============================================================
# Track 3: Variants (lollipop markers)
# ============================================================
p_var = figure(width=common_width, height=600, x_range=shared_x_range, tools="", toolbar_location=None)

# Lollipop stems
for i, vp in enumerate(variant_positions):
    p_var.segment(x0=[vp], y0=[0], x1=[vp], y1=[variant_quality[i]], line_color="#999999", line_width=2)

# SNP markers
snp_mask = [vt == "SNP" for vt in variant_types]
snp_pos = [variant_positions[i] for i in range(len(variant_positions)) if snp_mask[i]]
snp_qual = [variant_quality[i] for i in range(len(variant_quality)) if snp_mask[i]]
p_var.scatter(
    x=snp_pos, y=snp_qual, size=22, color=snp_color, alpha=0.9, line_color="white", line_width=2, legend_label="SNP"
)

# Indel markers
indel_mask = [vt == "Indel" for vt in variant_types]
indel_pos = [variant_positions[i] for i in range(len(variant_positions)) if indel_mask[i]]
indel_qual = [variant_quality[i] for i in range(len(variant_quality)) if indel_mask[i]]
p_var.scatter(
    x=indel_pos,
    y=indel_qual,
    size=24,
    color=indel_color,
    marker="diamond",
    alpha=0.9,
    line_color="white",
    line_width=2,
    legend_label="Indel",
)

# Track label
track_label_var = Label(
    x=215,
    y=520,
    x_units="screen",
    y_units="screen",
    text="Variants",
    text_font_size="22pt",
    text_color="#555555",
    text_font_style="bold",
)
p_var.add_layout(track_label_var)

# Style
p_var.xaxis.visible = False
p_var.yaxis.axis_label = "Quality Score"
p_var.yaxis.axis_label_text_font_size = "20pt"
p_var.yaxis.major_label_text_font_size = "16pt"
p_var.xgrid.grid_line_color = None
p_var.ygrid.grid_line_color = "#E0E0E0"
p_var.ygrid.grid_line_alpha = 0.4
p_var.background_fill_color = "#FAFBFC"
p_var.border_fill_color = "white"
p_var.outline_line_color = None
p_var.min_border_left = border_left
p_var.min_border_right = border_right
p_var.legend.label_text_font_size = "20pt"
p_var.legend.glyph_height = 30
p_var.legend.glyph_width = 30
p_var.legend.spacing = 15
p_var.legend.padding = 20
p_var.legend.background_fill_alpha = 0.85
p_var.legend.border_line_color = "#CCCCCC"
p_var.legend.location = "top_right"

# ============================================================
# Track 4: Regulatory Elements (bottom, with x-axis)
# ============================================================
p_reg = figure(
    width=common_width, height=550, x_range=shared_x_range, y_range=Range1d(-1.0, 1.5), tools="", toolbar_location=None
)

for elem in reg_elements:
    color = reg_color_map[elem["type"]]
    p_reg.quad(
        left=[elem["start"]],
        right=[elem["end"]],
        top=[0.4],
        bottom=[-0.4],
        fill_color=color,
        line_color="white",
        line_width=1.5,
        alpha=0.85,
    )

# Legend entries via invisible glyphs
for reg_type, reg_col in reg_color_map.items():
    p_reg.quad(
        left=[0], right=[0], top=[0], bottom=[0], fill_color=reg_col, line_color=reg_col, alpha=0, legend_label=reg_type
    )

# Track label
track_label_reg = Label(
    x=215,
    y=470,
    x_units="screen",
    y_units="screen",
    text="Regulatory",
    text_font_size="22pt",
    text_color="#555555",
    text_font_style="bold",
)
p_reg.add_layout(track_label_reg)

# Style
p_reg.yaxis.visible = False
p_reg.xaxis.axis_label = f"Genomic Position ({chrom})"
p_reg.xaxis.axis_label_text_font_size = "22pt"
p_reg.xaxis.major_label_text_font_size = "18pt"
p_reg.xaxis.formatter = NumeralTickFormatter(format="0,0")
p_reg.xaxis.axis_line_width = 2
p_reg.xgrid.grid_line_color = None
p_reg.ygrid.grid_line_color = None
p_reg.background_fill_color = "#FAFBFC"
p_reg.border_fill_color = "white"
p_reg.outline_line_color = None
p_reg.min_border_left = border_left
p_reg.min_border_right = border_right
p_reg.legend.label_text_font_size = "18pt"
p_reg.legend.glyph_height = 25
p_reg.legend.glyph_width = 35
p_reg.legend.spacing = 12
p_reg.legend.padding = 15
p_reg.legend.background_fill_alpha = 0.85
p_reg.legend.border_line_color = "#CCCCCC"
p_reg.legend.location = "top_right"
p_reg.legend.orientation = "horizontal"

# Combine all tracks
layout = column(p_gene, p_cov, p_var, p_reg, spacing=5)

# Save
export_png(layout, filename="plot.png")
output_file("plot.html")
save(layout)
