""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure


np.random.seed(42)

# Build hierarchical data: Technology company budget allocation (in millions)
hierarchy = [
    {"id": "TechCorp", "parent": None, "value": 0, "label": "TechCorp"},
    # Level 1: Divisions
    {"id": "Engineering", "parent": "TechCorp", "value": 0, "label": "Engineering"},
    {"id": "Sales", "parent": "TechCorp", "value": 0, "label": "Sales"},
    {"id": "Operations", "parent": "TechCorp", "value": 0, "label": "Operations"},
    # Level 2: Engineering teams
    {"id": "Frontend", "parent": "Engineering", "value": 45, "label": "Frontend"},
    {"id": "Backend", "parent": "Engineering", "value": 60, "label": "Backend"},
    {"id": "DevOps", "parent": "Engineering", "value": 35, "label": "DevOps"},
    {"id": "Mobile", "parent": "Engineering", "value": 40, "label": "Mobile"},
    # Level 2: Sales teams
    {"id": "Enterprise", "parent": "Sales", "value": 75, "label": "Enterprise"},
    {"id": "SMB", "parent": "Sales", "value": 45, "label": "SMB"},
    {"id": "Partners", "parent": "Sales", "value": 30, "label": "Partners"},
    # Level 2: Operations teams
    {"id": "HR", "parent": "Operations", "value": 25, "label": "HR"},
    {"id": "Finance", "parent": "Operations", "value": 30, "label": "Finance"},
    {"id": "Legal", "parent": "Operations", "value": 20, "label": "Legal"},
]

# Build tree structure
nodes = {item["id"]: {**item, "children": [], "x": 0, "y": 0, "r": 0, "depth": 0} for item in hierarchy}

root = None
for _node_id, node in nodes.items():
    if node["parent"] is None:
        root = node
    else:
        parent = nodes[node["parent"]]
        parent["children"].append(node)
        node["depth"] = parent["depth"] + 1

scale_factor = 15


def enclose_circles(circles):
    """Find the minimum enclosing circle for a set of positioned circles."""
    if not circles:
        return 0, 0, 0
    if len(circles) == 1:
        return circles[0]["x"], circles[0]["y"], circles[0]["r"]

    # Welzl's algorithm is complex; use bounding approach
    min_x = min(c["x"] - c["r"] for c in circles)
    max_x = max(c["x"] + c["r"] for c in circles)
    min_y = min(c["y"] - c["r"] for c in circles)
    max_y = max(c["y"] + c["r"] for c in circles)

    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    r = max(np.sqrt((c["x"] - cx) ** 2 + (c["y"] - cy) ** 2) + c["r"] for c in circles)

    return cx, cy, r


def pack_siblings(circles):
    """Pack sibling circles using a front-chain algorithm."""
    if not circles:
        return

    # Sort by radius descending for better packing
    circles.sort(key=lambda c: -c["r"])

    n = len(circles)
    if n == 1:
        circles[0]["x"] = 0
        circles[0]["y"] = 0
        return

    # Place first two circles
    c0, c1 = circles[0], circles[1]
    c0["x"] = 0
    c0["y"] = 0
    c1["x"] = c0["r"] + c1["r"]
    c1["y"] = 0

    if n == 2:
        return

    # Place third circle tangent to first two
    c2 = circles[2]
    d01 = c0["r"] + c1["r"]
    d02 = c0["r"] + c2["r"]
    d12 = c1["r"] + c2["r"]
    # c2 is tangent to c0 at distance d02 and to c1 at distance d12
    # c0 is at origin, c1 is at (d01, 0)
    x2 = (d02**2 - d12**2 + d01**2) / (2 * d01)
    y2_sq = d02**2 - x2**2
    y2 = np.sqrt(max(0, y2_sq))
    c2["x"] = x2
    c2["y"] = y2

    if n == 3:
        return

    # Place remaining circles using front chain
    front = [0, 1, 2]  # indices forming the front chain

    for i in range(3, n):
        ci = circles[i]
        best_score = float("inf")
        best_pos = (0, 0)
        best_insert = 0

        # Try placing tangent to each adjacent pair in the front
        for f_idx in range(len(front)):
            j = front[f_idx]
            k = front[(f_idx + 1) % len(front)]
            cj, ck = circles[j], circles[k]

            # Find position tangent to cj and ck
            positions = find_tangent_pos(cj, ck, ci["r"])

            for px, py in positions:
                # Check no overlap with existing circles
                valid = True
                for m in range(i):
                    cm = circles[m]
                    dist = np.sqrt((px - cm["x"]) ** 2 + (py - cm["y"]) ** 2)
                    if dist < ci["r"] + cm["r"] - 1e-6:
                        valid = False
                        break

                if valid:
                    # Score: distance from centroid (prefer compact)
                    cx = sum(circles[m]["x"] for m in range(i)) / i
                    cy = sum(circles[m]["y"] for m in range(i)) / i
                    score = np.sqrt((px - cx) ** 2 + (py - cy) ** 2)

                    if score < best_score:
                        best_score = score
                        best_pos = (px, py)
                        best_insert = f_idx + 1

        ci["x"], ci["y"] = best_pos
        front.insert(best_insert, i)


def find_tangent_pos(c1, c2, r):
    """Find positions for circle of radius r tangent to c1 and c2."""
    dx = c2["x"] - c1["x"]
    dy = c2["y"] - c1["y"]
    d = np.sqrt(dx**2 + dy**2)

    if d < 1e-10:
        return []

    r1 = c1["r"] + r
    r2 = c2["r"] + r

    if d > r1 + r2 + 1e-6:
        return []
    if d < abs(r1 - r2) - 1e-6:
        return []

    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h_sq = r1**2 - a**2
    if h_sq < 0:
        return []

    h = np.sqrt(h_sq)
    mx = c1["x"] + a * dx / d
    my = c1["y"] + a * dy / d

    return [(mx - h * dy / d, my + h * dx / d), (mx + h * dy / d, my - h * dx / d)]


def compute_layout(node):
    """Recursively compute layout using bottom-up packing."""
    if not node["children"]:
        node["r"] = np.sqrt(node["value"]) * scale_factor
        return

    # First layout all children
    for child in node["children"]:
        compute_layout(child)

    # Pack children
    pack_siblings(node["children"])

    # Find enclosing circle
    cx, cy, r = enclose_circles(node["children"])

    # Center children around (0, 0)
    for child in node["children"]:
        child["x"] -= cx
        child["y"] -= cy

    node["r"] = r + 30  # padding


def position_children(node, px, py):
    """Recursively position children relative to parent."""
    node["x"] = px
    node["y"] = py
    for child in node["children"]:
        # Child positions are relative to parent center
        position_children(child, px + child["x"], py + child["y"])


# Compute layout
compute_layout(root)
position_children(root, 0, 0)

# Collect all nodes for plotting
all_circles = []


def collect_circles(node):
    all_circles.append(node)
    for child in node["children"]:
        collect_circles(child)


collect_circles(root)

# Prepare data for plotting
x_vals = [n["x"] for n in all_circles]
y_vals = [n["y"] for n in all_circles]
radii = [n["r"] for n in all_circles]
depths = [n["depth"] for n in all_circles]

# Color palette by depth
depth_colors = ["#306998", "#FFD43B", "#4ECDC4"]
colors = [depth_colors[min(d, 2)] for d in depths]

# Create figure (square aspect)
p = figure(width=3600, height=3600, title="circlepacking-basic · bokeh · pyplots.ai", match_aspect=True)

# Sort by depth and radius for proper layering (draw outer first)
sorted_indices = sorted(range(len(all_circles)), key=lambda i: (depths[i], -radii[i]))

# Draw circles
for idx in sorted_indices:
    alpha = 0.6 if depths[idx] == 0 else (0.65 if depths[idx] == 1 else 0.75)
    line_w = 3 if depths[idx] == 0 else 2
    p.circle(
        x=x_vals[idx],
        y=y_vals[idx],
        radius=radii[idx],
        fill_color=colors[idx],
        fill_alpha=alpha,
        line_color="#333333",
        line_width=line_w,
    )

# Prepare labels - only for leaf nodes
label_data = {"x": [], "y": [], "label": []}
for node in all_circles:
    if not node["children"] and node["r"] >= 50:
        label_data["x"].append(node["x"])
        label_data["y"].append(node["y"])
        label_data["label"].append(node["label"])

# Also add division labels (level 1)
for node in all_circles:
    if node["depth"] == 1:
        # Position label at top of the division circle
        label_data["x"].append(node["x"])
        label_data["y"].append(node["y"] + node["r"] * 0.7)
        label_data["label"].append(node["label"])

label_source = ColumnDataSource(data=label_data)

label_set = LabelSet(
    x="x",
    y="y",
    text="label",
    source=label_source,
    text_align="center",
    text_baseline="middle",
    text_font_size="28pt",
    text_color="#222222",
    text_font_style="bold",
)
p.add_layout(label_set)

# Style
p.title.text_font_size = "36pt"
p.title.align = "center"
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None
p.background_fill_color = "#FAFAFA"

# Set axis ranges
extent = root["r"] * 1.08
p.x_range.start = -extent
p.x_range.end = extent
p.y_range.start = -extent
p.y_range.end = extent

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
