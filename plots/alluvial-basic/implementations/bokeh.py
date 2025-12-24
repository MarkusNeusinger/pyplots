"""pyplots.ai
alluvial-basic: Basic Alluvial Diagram
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label, Title
from bokeh.plotting import figure


# Data: Voter migration between political parties across election years
# Time points (years)
years = ["2016", "2018", "2020", "2022"]
n_years = len(years)

# Categories (parties) with consistent colors
parties = ["Democratic", "Republican", "Independent", "Other"]
colors = {
    "Democratic": "#306998",  # Python Blue
    "Republican": "#D64545",  # Red
    "Independent": "#FFD43B",  # Python Yellow
    "Other": "#7B7B7B",  # Gray
}

# Vote counts (millions) at each time point
# Rows: parties, Columns: years
values = np.array(
    [
        [65, 60, 81, 52],  # Democratic
        [63, 55, 74, 50],  # Republican
        [12, 18, 15, 22],  # Independent
        [5, 7, 6, 8],  # Other
    ],
    dtype=float,
)

# Flow data: transitions between consecutive time points
# Simplified flow matrix for each transition (from -> to percentages)
# Format: for each year transition, what percentage of each party stays or moves
flows = [
    # 2016 -> 2018 transition matrix (row=from, col=to)
    np.array(
        [
            [0.85, 0.05, 0.08, 0.02],  # Dem: 85% stay, 5% to Rep, 8% to Ind, 2% Other
            [0.04, 0.88, 0.06, 0.02],  # Rep: 4% to Dem, 88% stay, 6% to Ind, 2% Other
            [0.15, 0.10, 0.70, 0.05],  # Ind: 15% to Dem, 10% to Rep, 70% stay, 5% Other
            [0.10, 0.10, 0.20, 0.60],  # Other: distributed
        ]
    ),
    # 2018 -> 2020 transition matrix
    np.array([[0.90, 0.03, 0.05, 0.02], [0.06, 0.85, 0.07, 0.02], [0.25, 0.15, 0.55, 0.05], [0.15, 0.15, 0.15, 0.55]]),
    # 2020 -> 2022 transition matrix
    np.array([[0.80, 0.08, 0.10, 0.02], [0.05, 0.82, 0.10, 0.03], [0.18, 0.12, 0.65, 0.05], [0.10, 0.10, 0.25, 0.55]]),
]

# Layout parameters
node_width = 0.15
gap = 3  # Gap between nodes

# Calculate total height for y-range
total_height = max(values.sum(axis=0)) + gap * (len(parties) - 1)

# Create figure
p = figure(
    width=4800,
    height=2700,
    x_range=(-0.6, n_years - 0.4),
    y_range=(-10, total_height + 5),
    tools="",
    toolbar_location=None,
)

# Remove axes and grid
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None

# Title
p.add_layout(Title(text="alluvial-basic · bokeh · pyplots.ai", text_font_size="32pt", align="center"), "above")

# For each time point, calculate y positions of nodes
node_positions = []  # List of dicts: {party: (y_bottom, y_top)}

for t in range(n_years):
    col_values = values[:, t]
    total = col_values.sum()

    # Add gaps between nodes
    total_with_gaps = total + gap * (len(parties) - 1)

    positions = {}
    y = 0
    for i, party in enumerate(parties):
        height = col_values[i]
        positions[party] = (y, y + height)
        y += height + gap

    node_positions.append(positions)

# Draw nodes (rectangles for each party at each time point)
for t in range(n_years):
    for i, party in enumerate(parties):
        y_bottom, y_top = node_positions[t][party]

        # Node rectangle
        xs = [t - node_width / 2, t + node_width / 2, t + node_width / 2, t - node_width / 2]
        ys = [y_bottom, y_bottom, y_top, y_top]

        source = ColumnDataSource(data={"xs": [xs], "ys": [ys]})
        p.patches("xs", "ys", source=source, fill_color=colors[party], line_color="white", line_width=2, alpha=0.9)

        # Node label (party name) - only on first and last columns
        if t == 0 or t == n_years - 1:
            label_x = t - node_width / 2 - 0.05 if t == 0 else t + node_width / 2 + 0.05
            label_anchor = "right" if t == 0 else "left"
            y_mid = (y_bottom + y_top) / 2

            label = Label(
                x=label_x,
                y=y_mid,
                text=f"{party} ({values[i, t]:.0f}M)",
                text_font_size="18pt",
                text_align=label_anchor,
                text_baseline="middle",
                text_color="#333333",
            )
            p.add_layout(label)

# Add year labels at bottom
for t, year in enumerate(years):
    label = Label(
        x=t,
        y=-3,
        text=year,
        text_font_size="24pt",
        text_align="center",
        text_baseline="top",
        text_color="#333333",
        text_font_style="bold",
    )
    p.add_layout(label)


# Draw flows between time points
def bezier_band(x0, x1, y0_bot, y0_top, y1_bot, y1_top, n_points=50):
    """Create bezier curves for flow band."""
    t_vals = np.linspace(0, 1, n_points)

    # Control points for bezier curve (middle x)
    cx = (x0 + x1) / 2

    # Top edge bezier
    top_x = (
        (1 - t_vals) ** 3 * x0
        + 3 * (1 - t_vals) ** 2 * t_vals * cx
        + 3 * (1 - t_vals) * t_vals**2 * cx
        + t_vals**3 * x1
    )
    top_y = (
        (1 - t_vals) ** 3 * y0_top
        + 3 * (1 - t_vals) ** 2 * t_vals * y0_top
        + 3 * (1 - t_vals) * t_vals**2 * y1_top
        + t_vals**3 * y1_top
    )

    # Bottom edge bezier
    bot_x = (
        (1 - t_vals) ** 3 * x0
        + 3 * (1 - t_vals) ** 2 * t_vals * cx
        + 3 * (1 - t_vals) * t_vals**2 * cx
        + t_vals**3 * x1
    )
    bot_y = (
        (1 - t_vals) ** 3 * y0_bot
        + 3 * (1 - t_vals) ** 2 * t_vals * y0_bot
        + 3 * (1 - t_vals) * t_vals**2 * y1_bot
        + t_vals**3 * y1_bot
    )

    # Combine to form closed polygon
    xs = list(top_x) + list(bot_x[::-1])
    ys = list(top_y) + list(bot_y[::-1])

    return xs, ys


# Draw flows for each transition
for t in range(n_years - 1):
    flow_matrix = flows[t]

    # Calculate actual flow values
    from_values = values[:, t]

    # Track cumulative positions for stacking flows
    from_offsets = {party: node_positions[t][party][0] for party in parties}
    to_offsets = {party: node_positions[t + 1][party][0] for party in parties}

    for i, from_party in enumerate(parties):
        for j, to_party in enumerate(parties):
            flow_amount = from_values[i] * flow_matrix[i, j]

            if flow_amount < 0.5:  # Skip very small flows
                continue

            # Source position
            y0_bot = from_offsets[from_party]
            y0_top = y0_bot + flow_amount
            from_offsets[from_party] = y0_top

            # Target position
            y1_bot = to_offsets[to_party]
            y1_top = y1_bot + flow_amount
            to_offsets[to_party] = y1_top

            # X positions (at edge of nodes)
            x0 = t + node_width / 2
            x1 = (t + 1) - node_width / 2

            # Create bezier band
            xs, ys = bezier_band(x0, x1, y0_bot, y0_top, y1_bot, y1_top)

            # Use source party color with transparency
            source = ColumnDataSource(data={"xs": [xs], "ys": [ys]})
            p.patches("xs", "ys", source=source, fill_color=colors[from_party], line_color=None, alpha=0.4)

# Add subtitle explaining the data (positioned at top of plot)
p.add_layout(
    Title(
        text="U.S. Voter Party Affiliation Over Election Cycles (millions)",
        text_font_size="22pt",
        text_color="#666666",
        align="center",
    ),
    "above",
)

# Save outputs
export_png(p, filename="plot.png")

# Save HTML for interactivity
output_file("plot.html", title="alluvial-basic · bokeh · pyplots.ai")
save(p)
