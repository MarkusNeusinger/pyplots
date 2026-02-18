""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 74/100 | Created: 2026-02-18
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import Label, Legend, LegendItem
from bokeh.plotting import figure


# Data - Technology innovation radar
np.random.seed(42)

sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech"]
rings = ["Adopt", "Trial", "Assess", "Hold"]

# Ring radii (inner to outer): Adopt is closest (near-term), Hold is farthest (future)
ring_inner = [0, 80, 160, 240]
ring_outer = [80, 160, 240, 320]
ring_mid = [(i + o) / 2 for i, o in zip(ring_inner, ring_outer, strict=True)]

# Innovation items: (name, ring_index, sector_index)
items = [
    # AI & ML (sector 0)
    ("LLM Agents", 0, 0),
    ("RAG Pipelines", 0, 0),
    ("Vision Models", 1, 0),
    ("AI Code Review", 1, 0),
    ("Neuro-Symbolic AI", 2, 0),
    ("Quantum ML", 3, 0),
    ("Autonomous Research", 3, 0),
    # Cloud & Infra (sector 1)
    ("K8s GitOps", 0, 1),
    ("Edge Computing", 0, 1),
    ("WebAssembly", 1, 1),
    ("Serverless GPUs", 1, 1),
    ("eBPF Networking", 2, 1),
    ("Confidential Compute", 2, 1),
    ("Satellite Internet", 3, 1),
    # Sustainability (sector 2)
    ("Carbon Tracking", 0, 2),
    ("Green Cloud", 1, 2),
    ("Circular Supply Chain", 1, 2),
    ("Smart Grid AI", 2, 2),
    ("Ocean Carbon Capture", 3, 2),
    ("Fusion Energy", 3, 2),
    # Biotech (sector 3)
    ("mRNA Therapeutics", 0, 3),
    ("CRISPR Diagnostics", 1, 3),
    ("Digital Twins (Health)", 2, 3),
    ("Organ-on-Chip", 2, 3),
    ("Synthetic Biology", 3, 3),
    ("Brain-Computer Interface", 3, 3),
]

n_sectors = len(sectors)

# Use 270 degrees (three-quarter circle) to leave room for legend/title
total_angle = 3 * np.pi / 2
start_angle = np.pi / 4  # Start at 45 degrees (upper-right gap for legend)

# Sector angular boundaries
sector_width = total_angle / n_sectors
sector_starts = [start_angle + i * sector_width for i in range(n_sectors)]
sector_ends = [start_angle + (i + 1) * sector_width for i in range(n_sectors)]

# Sector colors
sector_colors = ["#306998", "#E57373", "#4CAF50", "#9C27B0"]
sector_fill_colors = ["#306998", "#E57373", "#4CAF50", "#9C27B0"]

# Create figure
p = figure(
    width=3600,
    height=3600,
    title="radar-innovation-timeline · bokeh · pyplots.ai",
    x_range=(-480, 480),
    y_range=(-480, 480),
    tools="",
    toolbar_location=None,
)

# Remove axes and grid
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = "white"

# Draw ring background fills with subtle shading
ring_fills = ["#F0F4F8", "#F5F5F5", "#FAF7F2", "#FFF5F5"]
for ring_idx in range(len(rings)):
    r_out = ring_outer[ring_idx]
    r_in = ring_inner[ring_idx]
    theta = np.linspace(start_angle, start_angle + total_angle, 200)

    # Outer arc
    x_out = r_out * np.cos(theta)
    y_out = r_out * np.sin(theta)

    # Inner arc (reversed)
    x_in = r_in * np.cos(theta[::-1])
    y_in = r_in * np.sin(theta[::-1])

    x_fill = np.concatenate([x_out, x_in])
    y_fill = np.concatenate([y_out, y_in])

    p.patch(x_fill.tolist(), y_fill.tolist(), fill_color=ring_fills[ring_idx], fill_alpha=0.6, line_color=None)

# Draw ring boundary circles (arcs for 270 degrees)
for r in ring_outer:
    theta = np.linspace(start_angle, start_angle + total_angle, 200)
    x_arc = r * np.cos(theta)
    y_arc = r * np.sin(theta)
    p.line(x_arc.tolist(), y_arc.tolist(), line_color="#BBBBBB", line_width=2.5, line_alpha=0.7)

# Inner boundary line (center)
theta = np.linspace(start_angle, start_angle + total_angle, 200)
x_arc = ring_inner[0] * np.cos(theta)
y_arc = ring_inner[0] * np.sin(theta)

# Draw sector divider lines
for i in range(n_sectors + 1):
    angle = start_angle + i * sector_width
    x_line = [0, ring_outer[-1] * np.cos(angle)]
    y_line = [0, ring_outer[-1] * np.sin(angle)]
    p.line(x_line, y_line, line_color="#BBBBBB", line_width=2.5, line_alpha=0.7)

# Add ring labels along one radial line (at the start angle boundary)
label_angle = start_angle - 0.06
for ring_idx, ring_name in enumerate(rings):
    r = ring_mid[ring_idx]
    x_pos = r * np.cos(label_angle)
    y_pos = r * np.sin(label_angle)
    p.add_layout(
        Label(
            x=x_pos,
            y=y_pos,
            text=ring_name,
            text_font_size="20pt",
            text_color="#777777",
            text_font_style="italic",
            text_align="center",
            text_baseline="middle",
        )
    )

# Add sector header labels along the outer edge
for i, sector_name in enumerate(sectors):
    mid_angle = (sector_starts[i] + sector_ends[i]) / 2
    label_r = ring_outer[-1] + 40
    x_pos = label_r * np.cos(mid_angle)
    y_pos = label_r * np.sin(mid_angle)

    # Determine text alignment based on position
    cos_val = np.cos(mid_angle)
    if abs(cos_val) < 0.3:
        text_align = "center"
    elif cos_val > 0:
        text_align = "left"
    else:
        text_align = "right"

    p.add_layout(
        Label(
            x=x_pos,
            y=y_pos,
            text=sector_name,
            text_font_size="26pt",
            text_color=sector_colors[i],
            text_font_style="bold",
            text_align=text_align,
            text_baseline="middle",
        )
    )

# Place innovation items
legend_renderers = {s: [] for s in sectors}

for idx, (name, ring_idx, sector_idx) in enumerate(items):
    # Count items in same ring+sector for spacing
    same_group = [(i, n, ri, si) for i, (n, ri, si) in enumerate(items) if ri == ring_idx and si == sector_idx]
    pos_in_group = [i for i, _ in enumerate(same_group) if same_group[i][0] == idx][0]
    n_in_group = len(same_group)

    # Distribute items within the sector angular range
    sector_start = sector_starts[sector_idx]
    sector_end = sector_ends[sector_idx]
    margin = sector_width * 0.1
    usable_start = sector_start + margin
    usable_end = sector_end - margin

    if n_in_group == 1:
        angle = (usable_start + usable_end) / 2
    else:
        angle = usable_start + (usable_end - usable_start) * pos_in_group / (n_in_group - 1)

    # Radial position: jitter within ring
    r_base = ring_mid[ring_idx]
    ring_half_width = (ring_outer[ring_idx] - ring_inner[ring_idx]) / 2
    r_jitter = np.random.uniform(-ring_half_width * 0.4, ring_half_width * 0.4)
    r = r_base + r_jitter

    x = r * np.cos(angle)
    y = r * np.sin(angle)

    color = sector_colors[sector_idx]

    # Draw marker
    renderer = p.scatter([x], [y], size=22, fill_color=color, line_color="white", line_width=3, alpha=0.9)
    legend_renderers[sectors[sector_idx]].append(renderer)

    # Add label with smart positioning
    label_offset_x = 12 * np.cos(angle)
    label_offset_y = 12 * np.sin(angle)

    cos_val = np.cos(angle)
    if abs(cos_val) < 0.3:
        text_align = "center"
    elif cos_val > 0:
        text_align = "left"
    else:
        text_align = "right"

    sin_val = np.sin(angle)
    if abs(sin_val) < 0.3:
        text_baseline = "middle"
    elif sin_val > 0:
        text_baseline = "bottom"
    else:
        text_baseline = "top"

    p.add_layout(
        Label(
            x=x + label_offset_x,
            y=y + label_offset_y,
            text=name,
            text_font_size="14pt",
            text_color="#333333",
            text_align=text_align,
            text_baseline=text_baseline,
        )
    )

# Add legend
legend_items = []
for sector_name in sectors:
    if legend_renderers[sector_name]:
        legend_items.append(LegendItem(label=sector_name, renderers=[legend_renderers[sector_name][0]]))

legend = Legend(
    items=legend_items,
    location="top_right",
    label_text_font_size="22pt",
    glyph_height=35,
    glyph_width=35,
    spacing=18,
    padding=25,
    background_fill_alpha=0.85,
    border_line_color="#CCCCCC",
)
p.add_layout(legend, "right")

# Style
p.title.text_font_size = "32pt"
p.title.align = "center"
p.title.text_color = "#333333"

# Save
export_png(p, filename="plot.png")
output_file("plot.html", title="radar-innovation-timeline · bokeh · pyplots.ai")
save(p)
