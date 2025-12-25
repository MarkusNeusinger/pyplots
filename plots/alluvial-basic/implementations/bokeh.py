""" pyplots.ai
alluvial-basic: Basic Alluvial Diagram
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import Label
from bokeh.plotting import figure


# Data: Voter migration between political parties across 4 election years
np.random.seed(42)

time_points = ["2012", "2016", "2020", "2024"]
categories = ["Democratic", "Republican", "Independent", "Other"]
colors = {"Democratic": "#306998", "Republican": "#D62728", "Independent": "#FFD43B", "Other": "#7F7F7F"}

# Define flows between consecutive time points (from_cat, to_cat, value)
# Flow data: (from_category, to_category, flow_value)
flows_data = [
    # 2012 -> 2016
    [
        ("Democratic", "Democratic", 35),
        ("Democratic", "Independent", 5),
        ("Democratic", "Republican", 2),
        ("Republican", "Republican", 30),
        ("Republican", "Independent", 4),
        ("Republican", "Democratic", 3),
        ("Independent", "Democratic", 4),
        ("Independent", "Republican", 3),
        ("Independent", "Independent", 8),
        ("Other", "Other", 3),
        ("Other", "Independent", 2),
        ("Other", "Democratic", 1),
    ],
    # 2016 -> 2020
    [
        ("Democratic", "Democratic", 38),
        ("Democratic", "Independent", 3),
        ("Democratic", "Republican", 2),
        ("Republican", "Republican", 32),
        ("Republican", "Independent", 3),
        ("Republican", "Democratic", 2),
        ("Independent", "Democratic", 5),
        ("Independent", "Republican", 4),
        ("Independent", "Independent", 8),
        ("Other", "Other", 2),
        ("Other", "Independent", 2),
        ("Other", "Republican", 1),
    ],
    # 2020 -> 2024
    [
        ("Democratic", "Democratic", 40),
        ("Democratic", "Independent", 4),
        ("Democratic", "Republican", 1),
        ("Republican", "Republican", 34),
        ("Republican", "Independent", 2),
        ("Republican", "Democratic", 3),
        ("Independent", "Democratic", 4),
        ("Independent", "Republican", 5),
        ("Independent", "Independent", 6),
        ("Other", "Other", 2),
        ("Other", "Democratic", 1),
        ("Other", "Independent", 1),
    ],
]

# Calculate node heights at each time point
node_heights = []
for t_idx, _t in enumerate(time_points):
    heights = {}
    if t_idx == 0:
        # First column: sum outgoing flows
        for cat in categories:
            heights[cat] = sum(f[2] for f in flows_data[0] if f[0] == cat)
    elif t_idx == len(time_points) - 1:
        # Last column: sum incoming flows
        for cat in categories:
            heights[cat] = sum(f[2] for f in flows_data[-1] if f[1] == cat)
    else:
        # Middle columns: use incoming flows (which should equal outgoing)
        for cat in categories:
            heights[cat] = sum(f[2] for f in flows_data[t_idx - 1] if f[1] == cat)
    node_heights.append(heights)

# Plot dimensions
x_positions = [0, 1, 2, 3]
node_width = 0.12
gap = 2  # Vertical gap between nodes

# Calculate node positions (y_start, y_end for each category at each time point)
node_positions = []
for t_idx in range(len(time_points)):
    positions = {}
    y_cursor = 0
    for cat in categories:
        height = node_heights[t_idx][cat]
        positions[cat] = {"y_start": y_cursor, "y_end": y_cursor + height}
        y_cursor += height + gap
    node_positions.append(positions)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="alluvial-basic · bokeh · pyplots.ai",
    x_range=(-0.8, 4.0),
    y_range=(-5, max(sum(node_heights[0].values()) + gap * len(categories), 120)),
    tools="",
    toolbar_location=None,
)

# Style the figure
p.title.text_font_size = "32pt"
p.title.align = "center"
p.xgrid.visible = False
p.ygrid.visible = False
p.xaxis.visible = False
p.yaxis.visible = False
p.outline_line_color = None
p.background_fill_color = "#FAFAFA"


# Helper function to create bezier curve points for flows
def bezier_curve(x0, y0, x1, y1, n_points=50):
    """Create bezier curve control points for smooth flow."""
    t = np.linspace(0, 1, n_points)
    cx0, cx1 = x0 + (x1 - x0) / 3, x0 + 2 * (x1 - x0) / 3
    x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * cx0 + 3 * (1 - t) * t**2 * cx1 + t**3 * x1
    y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y0 + 3 * (1 - t) * t**2 * y1 + t**3 * y1
    return x, y


# Draw flows (bands connecting nodes)
for t_idx, flows in enumerate(flows_data):
    x_start = x_positions[t_idx] + node_width / 2
    x_end = x_positions[t_idx + 1] - node_width / 2

    # Track current position for each category on source and target sides
    source_cursors = {cat: node_positions[t_idx][cat]["y_start"] for cat in categories}
    target_cursors = {cat: node_positions[t_idx + 1][cat]["y_start"] for cat in categories}

    for from_cat, to_cat, value in flows:
        if value == 0:
            continue

        # Source coordinates
        y_src_bottom = source_cursors[from_cat]
        y_src_top = y_src_bottom + value
        source_cursors[from_cat] = y_src_top

        # Target coordinates
        y_tgt_bottom = target_cursors[to_cat]
        y_tgt_top = y_tgt_bottom + value
        target_cursors[to_cat] = y_tgt_top

        # Create bezier paths for top and bottom edges
        x_top, y_top = bezier_curve(x_start, y_src_top, x_end, y_tgt_top)
        x_bottom, y_bottom = bezier_curve(x_start, y_src_bottom, x_end, y_tgt_bottom)

        # Create patch coordinates (top path + reversed bottom path)
        xs = list(x_top) + list(x_bottom[::-1])
        ys = list(y_top) + list(y_bottom[::-1])

        # Use source category color with transparency
        color = colors[from_cat]
        p.patch(xs, ys, fill_color=color, fill_alpha=0.5, line_color=color, line_alpha=0.7, line_width=1)

# Draw nodes (rectangles for each category at each time point)
for t_idx, _t in enumerate(time_points):
    x = x_positions[t_idx]
    for cat in categories:
        y_start = node_positions[t_idx][cat]["y_start"]
        y_end = node_positions[t_idx][cat]["y_end"]
        height = y_end - y_start

        if height > 0:
            # Draw node rectangle
            p.quad(
                left=x - node_width / 2,
                right=x + node_width / 2,
                top=y_end,
                bottom=y_start,
                fill_color=colors[cat],
                line_color="white",
                line_width=2,
            )

            # Add category label only for first and last columns to avoid clutter
            if t_idx == 0:
                # First column - label on left
                label = Label(
                    x=x - node_width / 2 - 0.03,
                    y=(y_start + y_end) / 2,
                    text=f"{cat} ({int(height)}M)",
                    text_font_size="16pt",
                    text_baseline="middle",
                    text_align="right",
                    text_color="#333333",
                )
                p.add_layout(label)
            elif t_idx == len(time_points) - 1:
                # Last column - label on right
                label = Label(
                    x=x + node_width / 2 + 0.03,
                    y=(y_start + y_end) / 2,
                    text=f"{cat} ({int(height)}M)",
                    text_font_size="16pt",
                    text_baseline="middle",
                    text_color="#333333",
                )
                p.add_layout(label)

# Add time point labels at the bottom
for t_idx, t in enumerate(time_points):
    label = Label(
        x=x_positions[t_idx],
        y=-3,
        text=t,
        text_font_size="22pt",
        text_align="center",
        text_baseline="top",
        text_color="#333333",
        text_font_style="bold",
    )
    p.add_layout(label)


# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactive version
output_file("plot.html")
save(p)
