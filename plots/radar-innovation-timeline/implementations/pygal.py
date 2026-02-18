""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: pygal 3.1.0 | Python 3.14.3
Quality: 73/100 | Created: 2026-02-18
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Technology innovations mapped to time-horizon rings and thematic sectors
np.random.seed(42)

sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech & Health"]
rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_values = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

innovations = [
    ("LLM Agents", "AI & ML", "Adopt"),
    ("RAG Pipelines", "AI & ML", "Adopt"),
    ("Edge AI Inference", "AI & ML", "Trial"),
    ("Federated Learning", "AI & ML", "Assess"),
    ("Neuromorphic Chips", "AI & ML", "Hold"),
    ("Causal AI", "AI & ML", "Assess"),
    ("Kubernetes", "Cloud & Infra", "Adopt"),
    ("GitOps Workflows", "Cloud & Infra", "Adopt"),
    ("WebAssembly Runtimes", "Cloud & Infra", "Trial"),
    ("Confidential Computing", "Cloud & Infra", "Trial"),
    ("Serverless GPUs", "Cloud & Infra", "Assess"),
    ("Quantum Networking", "Cloud & Infra", "Hold"),
    ("Carbon Accounting APIs", "Sustainability", "Trial"),
    ("Green Software Patterns", "Sustainability", "Adopt"),
    ("Digital Product Passports", "Sustainability", "Assess"),
    ("Energy-Harvesting IoT", "Sustainability", "Hold"),
    ("Circular Supply Chains", "Sustainability", "Assess"),
    ("AI-Optimized Grids", "Sustainability", "Trial"),
    ("mRNA Therapeutics", "Biotech & Health", "Adopt"),
    ("Digital Twins for Organs", "Biotech & Health", "Assess"),
    ("CRISPR Diagnostics", "Biotech & Health", "Trial"),
    ("Synthetic Biology", "Biotech & Health", "Hold"),
    ("Wearable Biomarkers", "Biotech & Health", "Trial"),
    ("Longevity Genomics", "Biotech & Health", "Hold"),
]

# Build angular slots: each sector gets sub-slots for angular spread of items.
# Place sector labels at first slot of each sector so they land at 0/90/180/270 degrees.
slots_per_sector = 9
total_slots = len(sectors) * slots_per_sector

x_labels = []
for sector in sectors:
    x_labels.append(sector)
    for _ in range(slots_per_sector - 1):
        x_labels.append("")

# Group innovations by sector
sector_items = {s: [] for s in sectors}
for name, sector, ring in innovations:
    sector_items[sector].append((name, ring))

# Place each item into slots within its sector (offset from label slot)
item_placements = []
for sector_idx, sector in enumerate(sectors):
    items = sector_items[sector]
    n_items = len(items)
    start_slot = sector_idx * slots_per_sector
    usable_start = 1
    usable_end = slots_per_sector - 1
    usable_range = usable_end - usable_start
    for i, (name, ring) in enumerate(items):
        slot_offset = usable_start + int((i + 0.5) * usable_range / n_items)
        slot_offset = max(usable_start, min(usable_end, slot_offset))
        slot = start_slot + slot_offset
        item_placements.append((name, ring, slot))

# Color palette per ring (colorblind-safe, distinct hues)
ring_colors = {"Adopt": "#27ae60", "Trial": "#2980b9", "Assess": "#e67e22", "Hold": "#c0392b"}

# Sort so first occurrence of each ring appears in order for clean legend
ring_order = {r: i for i, r in enumerate(rings)}
item_placements.sort(key=lambda x: (ring_order[x[1]], x[2]))

# Build one series per item; first per ring gets legend title, rest get None
ring_legend_used = set()
ring_legend_labels = {
    "Adopt": "Adopt (Now)",
    "Trial": "Trial (6-12 mo)",
    "Assess": "Assess (1-2 yr)",
    "Hold": "Hold (2-5 yr)",
}

series_list = []
for name, ring, slot in item_placements:
    values = [None] * total_slots
    values[slot] = {"value": ring_values[ring], "label": name}
    if ring not in ring_legend_used:
        title = ring_legend_labels[ring]
        ring_legend_used.add(ring)
    else:
        title = None
    series_list.append((title, values, ring_colors[ring]))

# Custom style
color_sequence = tuple(color for _, _, color in series_list)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#dddddd",
    colors=color_sequence,
    title_font_size=56,
    label_font_size=34,
    major_label_font_size=38,
    legend_font_size=32,
    value_font_size=20,
    opacity=0.9,
    opacity_hover=1.0,
)

# Chart
chart = pygal.Radar(
    width=4800,
    height=2700,
    style=custom_style,
    title="radar-innovation-timeline · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=28,
    fill=False,
    dots_size=14,
    stroke=False,
    show_dots=True,
    show_y_guides=True,
    show_x_guides=False,
    range=(0, 5),
    inner_radius=0.05,
    y_labels=[
        {"value": 1, "label": "Adopt"},
        {"value": 2, "label": "Trial"},
        {"value": 3, "label": "Assess"},
        {"value": 4, "label": "Hold"},
    ],
    show_minor_x_labels=False,
    x_labels_major=sectors,
    x_label_rotation=0,
    margin_bottom=80,
    margin_left=140,
    margin_right=140,
    margin_top=60,
)

chart.x_labels = x_labels

for title, values, _ in series_list:
    chart.add(title, values)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
