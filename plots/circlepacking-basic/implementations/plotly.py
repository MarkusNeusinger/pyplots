""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


np.random.seed(42)

# Data: File system hierarchy with sizes (in MB) - 40+ nodes across 3 levels
hierarchy = {
    "Documents": {
        "Reports": {"Q1 Report": 45, "Q2 Report": 52, "Annual": 78, "Summary": 35},
        "Spreadsheets": {"Budget": 28, "Expenses": 32, "Forecast": 41, "Analysis": 25},
        "Presentations": {"Sales Deck": 65, "Training": 48, "Overview": 55},
    },
    "Media": {
        "Photos": {"Vacation": 120, "Family": 95, "Work Events": 75, "Archive": 140},
        "Videos": {"Tutorials": 180, "Recordings": 210, "Backups": 160},
        "Music": {"Playlists": 85, "Podcasts": 95, "Audiobooks": 110},
    },
    "Projects": {
        "Python": {"ML Models": 68, "Scripts": 42, "Libraries": 55, "Tests": 38},
        "Web": {"Frontend": 52, "Backend": 48, "Assets": 65},
        "Data": {"Datasets": 120, "Exports": 85, "Logs": 45},
    },
    "System": {
        "Logs": {"App Logs": 35, "System Logs": 28, "Error Logs": 22},
        "Config": {"Settings": 15, "Profiles": 18, "Backup Cfg": 12},
        "Cache": {"Browser": 65, "App Cache": 48, "Temp": 38},
    },
}

# Color palette by category
colors = {
    "Documents": "#306998",  # Python Blue
    "Media": "#FFD43B",  # Python Yellow
    "Projects": "#4B8BBE",  # Light Blue
    "System": "#646464",  # Gray
}

lighter_colors = {"Documents": "#5A93B8", "Media": "#FFE580", "Projects": "#7AB8E0", "System": "#909090"}


def pack_circles_in_parent(children, parent_radius, parent_x, parent_y):
    """Simple circle packing using front-chain algorithm approximation."""
    packed = []
    if not children:
        return packed

    sorted_children = sorted(children, key=lambda x: x[1], reverse=True)

    # Place first circle at center-top
    name, value = sorted_children[0]
    r = np.sqrt(value) * 2.2
    packed.append({"name": name, "value": value, "r": r, "x": parent_x, "y": parent_y + parent_radius * 0.3})

    for name, value in sorted_children[1:]:
        r = np.sqrt(value) * 2.2
        best_pos = None
        min_dist = float("inf")

        # Try positions around existing circles
        for existing in packed:
            for angle in np.linspace(0, 2 * np.pi, 24):
                dist = existing["r"] + r + 2
                nx = existing["x"] + dist * np.cos(angle)
                ny = existing["y"] + dist * np.sin(angle)

                # Check if inside parent
                d_to_parent = np.sqrt((nx - parent_x) ** 2 + (ny - parent_y) ** 2)
                if d_to_parent + r > parent_radius * 0.92:
                    continue

                # Check overlap with other circles
                overlaps = False
                for other in packed:
                    d = np.sqrt((nx - other["x"]) ** 2 + (ny - other["y"]) ** 2)
                    if d < other["r"] + r + 1:
                        overlaps = True
                        break

                if not overlaps:
                    d_center = np.sqrt((nx - parent_x) ** 2 + (ny - parent_y) ** 2)
                    if d_center < min_dist:
                        min_dist = d_center
                        best_pos = (nx, ny)

        if best_pos:
            packed.append({"name": name, "value": value, "r": r, "x": best_pos[0], "y": best_pos[1]})

    return packed


# Build complete circle hierarchy
all_circles = []

# Calculate category totals and radii
cat_data = []
for cat, subcats in hierarchy.items():
    total = sum(sum(items.values()) for items in subcats.values())
    cat_data.append((cat, total, subcats))

# Position main categories using circle packing
positions = [(-180, 180), (180, 180), (-180, -180), (180, -180)]

for idx, (cat, total, subcats) in enumerate(cat_data):
    cat_radius = np.sqrt(total) * 4.5
    cx, cy = positions[idx]

    all_circles.append(
        {"x": cx, "y": cy, "r": cat_radius, "label": cat, "value": total, "color": colors[cat], "level": 0}
    )

    # Pack subcategories within each category
    subcat_list = [(name, sum(items.values())) for name, items in subcats.items()]
    packed_subcats = pack_circles_in_parent(subcat_list, cat_radius, cx, cy)

    for sub in packed_subcats:
        sub_radius = sub["r"]
        all_circles.append(
            {
                "x": sub["x"],
                "y": sub["y"],
                "r": sub_radius,
                "label": sub["name"],
                "value": sub["value"],
                "color": lighter_colors[cat],
                "level": 1,
                "parent": cat,
            }
        )

        # Pack leaf nodes within subcategory
        leaf_items = list(subcats[sub["name"]].items())
        packed_leaves = pack_circles_in_parent(leaf_items, sub_radius, sub["x"], sub["y"])

        for leaf in packed_leaves:
            all_circles.append(
                {
                    "x": leaf["x"],
                    "y": leaf["y"],
                    "r": leaf["r"],
                    "label": leaf["name"],
                    "value": leaf["value"],
                    "color": colors[cat],
                    "level": 2,
                    "parent": sub["name"],
                }
            )

# Create figure
fig = go.Figure()

# Draw circles by level (background to foreground)
for level in [0, 1, 2]:
    for circle in all_circles:
        if circle["level"] == level:
            opacity = 0.9 if level == 0 else (0.75 if level == 1 else 0.95)
            line_width = 4 if level == 0 else (3 if level == 1 else 2)

            fig.add_shape(
                type="circle",
                xref="x",
                yref="y",
                x0=circle["x"] - circle["r"],
                y0=circle["y"] - circle["r"],
                x1=circle["x"] + circle["r"],
                y1=circle["y"] + circle["r"],
                fillcolor=circle["color"],
                opacity=opacity,
                line={"color": "white", "width": line_width},
            )

# Add labels for category circles only (level 0)
for circle in all_circles:
    if circle["level"] == 0:
        text_color = "white" if circle["color"] in ["#306998", "#4B8BBE", "#646464"] else "#333333"
        fig.add_annotation(
            x=circle["x"],
            y=circle["y"] - circle["r"] * 0.75,
            text=f"<b>{circle['label']}</b><br>{circle['value']} MB",
            showarrow=False,
            font={"size": 20, "color": text_color, "family": "Arial"},
            align="center",
        )

# Add invisible scatter traces for hover on all circles
for circle in all_circles:
    level_name = ["Category", "Subcategory", "File"][circle["level"]]
    fig.add_trace(
        go.Scatter(
            x=[circle["x"]],
            y=[circle["y"]],
            mode="markers",
            marker={"size": max(circle["r"] * 1.2, 15), "opacity": 0},
            hovertemplate=f"<b>{circle['label']}</b><br>{level_name}: {circle['value']} MB<extra></extra>",
            showlegend=False,
        )
    )

# Add legend as annotations
legend_x = 420
legend_y = 350
legend_items = [
    ("Documents", colors["Documents"]),
    ("Media", colors["Media"]),
    ("Projects", colors["Projects"]),
    ("System", colors["System"]),
]

for i, (name, color) in enumerate(legend_items):
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=legend_x - 12,
        y0=legend_y - i * 45 - 12,
        x1=legend_x + 12,
        y1=legend_y - i * 45 + 12,
        fillcolor=color,
        line={"color": "white", "width": 2},
    )
    fig.add_annotation(
        x=legend_x + 30,
        y=legend_y - i * 45,
        text=name,
        showarrow=False,
        font={"size": 16, "color": "#333333", "family": "Arial"},
        xanchor="left",
    )

# Layout
fig.update_layout(
    title={
        "text": "circlepacking-basic · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.97,
    },
    xaxis={
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
        "range": [-480, 520],
        "scaleanchor": "y",
        "scaleratio": 1,
    },
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-480, 420]},
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin={"t": 100, "l": 30, "r": 100, "b": 30},
    showlegend=False,
)

# Save outputs
fig.write_image("plot.png", width=1200, height=1200, scale=3)
fig.write_html("plot.html")
