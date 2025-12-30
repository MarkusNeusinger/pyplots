"""pyplots.ai
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
    "Root": "#2E4057",  # Dark blue-gray for root
    "Documents": "#306998",  # Python Blue
    "Media": "#FFD43B",  # Python Yellow
    "Projects": "#4B8BBE",  # Light Blue
    "System": "#646464",  # Gray
}

lighter_colors = {"Documents": "#5A93B8", "Media": "#FFE580", "Projects": "#7AB8E0", "System": "#909090"}

# Calculate total size for root
total_size = sum(sum(sum(items.values()) for items in subcats.values()) for subcats in hierarchy.values())

# Build circle hierarchy with proper packing
all_circles = []

# Calculate root radius to encompass all content
root_radius = 450

# Add root circle
all_circles.append(
    {"x": 0, "y": 0, "r": root_radius, "label": "Storage", "value": total_size, "color": colors["Root"], "level": -1}
)

# Calculate category totals
cat_data = []
for cat, subcats in hierarchy.items():
    total = sum(sum(items.values()) for items in subcats.values())
    cat_data.append((cat, total, subcats))

# Sort by size descending for better packing
cat_data.sort(key=lambda x: x[1], reverse=True)

# Pack main categories within root using circle packing algorithm
# Calculate radii based on values with scaling factor
cat_radii = [(cat, np.sqrt(total) * 5.5, total, subcats) for cat, total, subcats in cat_data]


# Simple greedy circle packing for categories within root
def pack_top_level(circles_data, container_radius):
    """Pack top-level category circles within container."""
    packed = []

    for i, (name, radius, value, subcats) in enumerate(circles_data):
        if i == 0:
            # First (largest) circle at center-top
            packed.append({"name": name, "r": radius, "value": value, "subcats": subcats, "x": 0, "y": radius * 0.4})
        else:
            # Find best position for subsequent circles
            best_pos = None
            min_dist_from_center = float("inf")

            for existing in packed:
                for angle in np.linspace(0, 2 * np.pi, 36):
                    dist = existing["r"] + radius + 8
                    nx = existing["x"] + dist * np.cos(angle)
                    ny = existing["y"] + dist * np.sin(angle)

                    # Check if inside container
                    d_to_center = np.sqrt(nx**2 + ny**2)
                    if d_to_center + radius > container_radius * 0.95:
                        continue

                    # Check overlap with other circles
                    overlaps = False
                    for other in packed:
                        d = np.sqrt((nx - other["x"]) ** 2 + (ny - other["y"]) ** 2)
                        if d < other["r"] + radius + 5:
                            overlaps = True
                            break

                    if not overlaps and d_to_center < min_dist_from_center:
                        min_dist_from_center = d_to_center
                        best_pos = (nx, ny)

            if best_pos:
                packed.append(
                    {"name": name, "r": radius, "value": value, "subcats": subcats, "x": best_pos[0], "y": best_pos[1]}
                )

    return packed


def pack_circles_in_parent(children, parent_radius, parent_x, parent_y, scale=2.0):
    """Pack child circles within parent circle."""
    packed = []
    if not children:
        return packed

    sorted_children = sorted(children, key=lambda x: x[1], reverse=True)

    # Place first circle at center
    name, value = sorted_children[0]
    r = np.sqrt(value) * scale
    packed.append({"name": name, "value": value, "r": r, "x": parent_x, "y": parent_y})

    for name, value in sorted_children[1:]:
        r = np.sqrt(value) * scale
        best_pos = None
        min_dist = float("inf")

        for existing in packed:
            for angle in np.linspace(0, 2 * np.pi, 24):
                dist = existing["r"] + r + 3
                nx = existing["x"] + dist * np.cos(angle)
                ny = existing["y"] + dist * np.sin(angle)

                d_to_parent = np.sqrt((nx - parent_x) ** 2 + (ny - parent_y) ** 2)
                if d_to_parent + r > parent_radius * 0.9:
                    continue

                overlaps = False
                for other in packed:
                    d = np.sqrt((nx - other["x"]) ** 2 + (ny - other["y"]) ** 2)
                    if d < other["r"] + r + 2:
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


# Pack categories within root
packed_cats = pack_top_level(cat_radii, root_radius)

# Build full hierarchy
for cat_info in packed_cats:
    cat = cat_info["name"]
    cx, cy = cat_info["x"], cat_info["y"]
    cat_radius = cat_info["r"]
    subcats = cat_info["subcats"]

    all_circles.append(
        {"x": cx, "y": cy, "r": cat_radius, "label": cat, "value": cat_info["value"], "color": colors[cat], "level": 0}
    )

    # Pack subcategories within category
    subcat_list = [(name, sum(items.values())) for name, items in subcats.items()]
    packed_subcats = pack_circles_in_parent(subcat_list, cat_radius, cx, cy, scale=2.5)

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
        packed_leaves = pack_circles_in_parent(leaf_items, sub_radius, sub["x"], sub["y"], scale=1.2)

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

# Draw circles by level (background to foreground: root, categories, subcategories, leaves)
for level in [-1, 0, 1, 2]:
    for circle in all_circles:
        if circle["level"] == level:
            if level == -1:
                opacity = 0.15
                line_width = 3
            elif level == 0:
                opacity = 0.85
                line_width = 4
            elif level == 1:
                opacity = 0.7
                line_width = 3
            else:
                opacity = 0.9
                line_width = 2

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

# Add labels for all levels
for circle in all_circles:
    level = circle["level"]

    if level == -1:
        # Root label at bottom
        fig.add_annotation(
            x=circle["x"],
            y=circle["y"] - circle["r"] * 0.85,
            text=f"<b>{circle['label']}</b><br>{circle['value']:,} MB Total",
            showarrow=False,
            font={"size": 22, "color": "#333333", "family": "Arial"},
            align="center",
        )
    elif level == 0:
        # Category labels
        text_color = "white" if circle["color"] in ["#306998", "#4B8BBE", "#646464"] else "#333333"
        fig.add_annotation(
            x=circle["x"],
            y=circle["y"],
            text=f"<b>{circle['label']}</b><br>{circle['value']} MB",
            showarrow=False,
            font={"size": 18, "color": text_color, "family": "Arial"},
            align="center",
        )
    elif level == 1:
        # Subcategory labels - show name
        text_color = "#333333" if circle["color"] in ["#FFE580"] else "white"
        if circle["r"] > 30:
            fig.add_annotation(
                x=circle["x"],
                y=circle["y"],
                text=f"<b>{circle['label']}</b>",
                showarrow=False,
                font={"size": 14, "color": text_color, "family": "Arial"},
                align="center",
            )
    elif level == 2:
        # Leaf node labels - show for larger circles
        if circle["r"] > 12:
            text_color = "white" if circle["color"] in ["#306998", "#4B8BBE", "#646464"] else "#333333"
            # Truncate long names
            label = circle["label"][:8] + ".." if len(circle["label"]) > 10 else circle["label"]
            fig.add_annotation(
                x=circle["x"],
                y=circle["y"],
                text=label,
                showarrow=False,
                font={"size": 10, "color": text_color, "family": "Arial"},
                align="center",
            )

# Add invisible scatter traces for hover on all circles
for circle in all_circles:
    level_names = {-1: "Root", 0: "Category", 1: "Subcategory", 2: "File"}
    level_name = level_names[circle["level"]]
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

# Add legend using actual traces for proper Plotly legend
legend_items = [
    ("Documents", colors["Documents"]),
    ("Media", colors["Media"]),
    ("Projects", colors["Projects"]),
    ("System", colors["System"]),
]

for name, color in legend_items:
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={"size": 16, "color": color, "line": {"color": "white", "width": 1}},
            name=name,
            showlegend=True,
        )
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
        "range": [-520, 520],
        "scaleanchor": "y",
        "scaleratio": 1,
    },
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-520, 520]},
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin={"t": 100, "l": 50, "r": 50, "b": 50},
    showlegend=True,
    legend={
        "x": 0.98,
        "y": 0.98,
        "xanchor": "right",
        "yanchor": "top",
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "#cccccc",
        "borderwidth": 1,
        "font": {"size": 14},
        "title": {"text": "Categories", "font": {"size": 16}},
    },
)

# Save outputs
fig.write_image("plot.png", width=1200, height=1200, scale=3)
fig.write_html("plot.html")
