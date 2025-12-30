""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 58/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Company budget allocation by department and team
# Hierarchical structure: Root > Department > Team
np.random.seed(42)
hierarchy = [
    # Engineering Department
    {"id": "eng", "parent": "root", "label": "Engineering", "value": None},
    {"id": "eng-backend", "parent": "eng", "label": "Backend", "value": 180},
    {"id": "eng-frontend", "parent": "eng", "label": "Frontend", "value": 150},
    {"id": "eng-devops", "parent": "eng", "label": "DevOps", "value": 90},
    {"id": "eng-mobile", "parent": "eng", "label": "Mobile", "value": 120},
    # Marketing Department
    {"id": "mkt", "parent": "root", "label": "Marketing", "value": None},
    {"id": "mkt-digital", "parent": "mkt", "label": "Digital", "value": 100},
    {"id": "mkt-content", "parent": "mkt", "label": "Content", "value": 80},
    {"id": "mkt-brand", "parent": "mkt", "label": "Brand", "value": 60},
    # Operations Department
    {"id": "ops", "parent": "root", "label": "Operations", "value": None},
    {"id": "ops-support", "parent": "ops", "label": "Support", "value": 70},
    {"id": "ops-hr", "parent": "ops", "label": "HR", "value": 50},
    {"id": "ops-admin", "parent": "ops", "label": "Admin", "value": 40},
    # Sales Department
    {"id": "sales", "parent": "root", "label": "Sales", "value": None},
    {"id": "sales-enterprise", "parent": "sales", "label": "Enterprise", "value": 130},
    {"id": "sales-smb", "parent": "sales", "label": "SMB", "value": 85},
    {"id": "sales-partners", "parent": "sales", "label": "Partners", "value": 55},
    # Root node
    {"id": "root", "parent": None, "label": "Company", "value": None},
]

# Build tree structure
nodes = {h["id"]: h.copy() for h in hierarchy}
for node in nodes.values():
    node["children"] = []

for node in nodes.values():
    if node["parent"] is not None:
        nodes[node["parent"]]["children"].append(node["id"])


# Calculate value for parent nodes (sum of children)
def calc_value(node_id):
    node = nodes[node_id]
    if node["value"] is not None:
        return node["value"]
    total = sum(calc_value(child) for child in node["children"])
    node["value"] = total
    return total


calc_value("root")


# Compute depth for each node
def calc_depth(node_id, depth=0):
    nodes[node_id]["depth"] = depth
    for child in nodes[node_id]["children"]:
        calc_depth(child, depth + 1)


calc_depth("root")


# Circle packing algorithm - pack circles tightly
def pack_circles_tight(radii):
    """Pack circles with given radii, returns (x, y) positions centered around origin."""
    n = len(radii)
    if n == 0:
        return [], []
    if n == 1:
        return [0.0], [0.0]

    # Sort by size (largest first) for better packing
    order = np.argsort(-np.array(radii))
    sorted_radii = [radii[i] for i in order]
    x_pos = [0.0] * n
    y_pos = [0.0] * n

    # Place first circle at origin
    x_pos[0], y_pos[0] = 0, 0

    # Place second circle touching first
    if n > 1:
        x_pos[1] = sorted_radii[0] + sorted_radii[1] + 3
        y_pos[1] = 0

    # Place remaining circles
    for i in range(2, n):
        best_x, best_y = 0.0, 0.0
        best_dist = float("inf")

        # Try positions tangent to pairs of already-placed circles
        for j in range(i):
            for k in range(j + 1, i):
                # Find positions tangent to both circles j and k
                d = np.sqrt((x_pos[j] - x_pos[k]) ** 2 + (y_pos[j] - y_pos[k]) ** 2)
                rj, rk, ri = sorted_radii[j], sorted_radii[k], sorted_radii[i]

                # Skip if circles too far apart
                if d > rj + rk + 2 * ri + 6:
                    continue

                # Try multiple angles around each circle
                for angle in np.linspace(0, 2 * np.pi, 36, endpoint=False):
                    test_x = x_pos[j] + (rj + ri + 3) * np.cos(angle)
                    test_y = y_pos[j] + (rj + ri + 3) * np.sin(angle)

                    # Check no overlap with any placed circle
                    valid = True
                    for m in range(i):
                        dx = test_x - x_pos[m]
                        dy = test_y - y_pos[m]
                        dist = np.sqrt(dx**2 + dy**2)
                        if dist < ri + sorted_radii[m] + 2:
                            valid = False
                            break

                    if valid:
                        center_dist = np.sqrt(test_x**2 + test_y**2)
                        if center_dist < best_dist:
                            best_dist = center_dist
                            best_x, best_y = test_x, test_y

        x_pos[i] = best_x
        y_pos[i] = best_y

    # Center the pack
    cx = sum(x_pos) / n
    cy = sum(y_pos) / n
    x_pos = [x - cx for x in x_pos]
    y_pos = [y - cy for y in y_pos]

    # Unsort to original order
    final_x = [0.0] * n
    final_y = [0.0] * n
    for sorted_idx, original_idx in enumerate(order):
        final_x[original_idx] = x_pos[sorted_idx]
        final_y[original_idx] = y_pos[sorted_idx]

    return final_x, final_y


def compute_enclosing_radius(x_pos, y_pos, radii, padding=8):
    """Compute radius of smallest circle that encloses all circles."""
    if len(x_pos) == 0:
        return padding
    max_extent = max(np.sqrt(x**2 + y**2) + r for x, y, r in zip(x_pos, y_pos, radii, strict=False))
    return max_extent + padding


# Scale factor for converting value to radius (sqrt for area-proportional)
max_leaf_value = max(n["value"] for n in nodes.values() if len(n["children"]) == 0)
min_radius = 35
max_radius = 75


def value_to_radius(value):
    return min_radius + (max_radius - min_radius) * np.sqrt(value / max_leaf_value)


# Store all circle data
all_circles = []


def layout_hierarchy(node_id):
    """Recursively layout a node and its children, return enclosing radius."""
    node = nodes[node_id]

    if len(node["children"]) == 0:
        # Leaf node - radius based on value
        radius = value_to_radius(node["value"])
        return {"id": node_id, "radius": radius, "x": 0, "y": 0, "children": []}

    # Layout all children first
    child_layouts = []
    for child_id in node["children"]:
        child_layout = layout_hierarchy(child_id)
        child_layouts.append(child_layout)

    # Pack children based on their enclosing radii
    child_radii = [c["radius"] for c in child_layouts]
    x_positions, y_positions = pack_circles_tight(child_radii)

    # Update child positions
    for i, child in enumerate(child_layouts):
        child["x"] = x_positions[i]
        child["y"] = y_positions[i]

    # Compute enclosing circle for this node
    enclosing_radius = compute_enclosing_radius(x_positions, y_positions, child_radii)

    return {"id": node_id, "radius": enclosing_radius, "x": 0, "y": 0, "children": child_layouts}


def flatten_layout(layout, offset_x=0, offset_y=0, depth=0):
    """Flatten hierarchical layout to list of circles with absolute positions."""
    node = nodes[layout["id"]]
    abs_x = offset_x + layout["x"]
    abs_y = offset_y + layout["y"]

    all_circles.append(
        {
            "id": layout["id"],
            "label": node["label"],
            "value": node["value"],
            "x": abs_x,
            "y": abs_y,
            "radius": layout["radius"],
            "depth": depth,
        }
    )

    for child in layout["children"]:
        flatten_layout(child, abs_x, abs_y, depth + 1)


# Build layout starting from root
root_layout = layout_hierarchy("root")
flatten_layout(root_layout)

# Create DataFrame
df = pd.DataFrame(all_circles)

# Color palette by depth - lighter at deeper levels
depth_colors = {
    0: "#1a3d5c",  # Root - darkest
    1: "#306998",  # Departments - Python Blue
    2: "#5b9bd5",  # Teams - lighter blue
}

df["color"] = df["depth"].map(depth_colors)
df["display_value"] = df.apply(lambda r: f"${r['value']}K" if r["depth"] > 0 else "Total", axis=1)

# Sort by depth (parents first, then children on top)
df = df.sort_values("depth").reset_index(drop=True)

# Separate DataFrames for each depth level
df_root = df[df["depth"] == 0].copy()
df_depts = df[df["depth"] == 1].copy()
df_teams = df[df["depth"] == 2].copy()

# Scale range for proper circle sizing
max_radius_sq = df["radius"].max() ** 2

# Create circle layers for each depth (to control drawing order)
root_circles = (
    alt.Chart(df_root)
    .mark_circle(opacity=0.25, stroke="white", strokeWidth=3)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        size=alt.Size("radius:Q", scale=alt.Scale(range=[min_radius**2 * 4, max_radius_sq * 4]), legend=None),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("label:N", title="Name"), alt.Tooltip("display_value:N", title="Budget")],
    )
)

dept_circles = (
    alt.Chart(df_depts)
    .mark_circle(opacity=0.45, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        size=alt.Size("radius:Q", scale=alt.Scale(range=[min_radius**2 * 4, max_radius_sq * 4]), legend=None),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("label:N", title="Name"), alt.Tooltip("display_value:N", title="Budget")],
    )
)

team_circles = (
    alt.Chart(df_teams)
    .mark_circle(opacity=0.9, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        size=alt.Size("radius:Q", scale=alt.Scale(range=[min_radius**2 * 4, max_radius_sq * 4]), legend=None),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("label:N", title="Name"), alt.Tooltip("display_value:N", title="Budget")],
    )
)

# Labels for leaf circles only (to avoid clutter)
df_labels = df_teams.copy()
df_labels["display_text"] = df_labels["label"] + "\n" + df_labels["display_value"]

labels_layer = (
    alt.Chart(df_labels)
    .mark_text(color="white", fontWeight="bold", fontSize=13, lineBreak="\n")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="display_text:N")
)

# Department labels (just name, positioned at department center)
dept_labels = (
    alt.Chart(df_depts)
    .mark_text(color="white", fontWeight="bold", fontSize=16, dy=-5)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="label:N")
)

# Combine layers
chart = (
    alt.layer(root_circles, dept_circles, team_circles, labels_layer)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title("circlepacking-basic · altair · pyplots.ai", fontSize=28, fontWeight="bold", anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs (3600x3600 px with scale_factor=3.0)
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
