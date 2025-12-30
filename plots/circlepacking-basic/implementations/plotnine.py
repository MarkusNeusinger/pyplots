""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_text,
    geom_polygon,
    geom_text,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_fill_manual,
    scale_size_identity,
    theme,
    theme_void,
)


np.random.seed(42)


# Create polygon points for a circle
def make_circle_points(cx, cy, r, n_points=64):
    angles = np.linspace(0, 2 * np.pi, n_points)
    return cx + r * np.cos(angles), cy + r * np.sin(angles)


# Find tangent positions for circle packing
def find_tangent_positions(x1, y1, r1, x2, y2, r2, r):
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if d == 0 or d > r1 + r2 + 2 * r:
        return []
    a, b = r1 + r, r2 + r
    cos_val = (a**2 + d**2 - b**2) / (2 * a * d)
    if abs(cos_val) > 1:
        return []
    angle = np.arccos(cos_val)
    base = np.arctan2(y2 - y1, x2 - x1)
    return [
        (x1 + a * np.cos(base + angle), y1 + a * np.sin(base + angle)),
        (x1 + a * np.cos(base - angle), y1 + a * np.sin(base - angle)),
    ]


# Pack child circles within parent
def pack_circles(children, parent_x, parent_y, parent_r, depth):
    if not children:
        return []

    # Sort by value (largest first)
    sorted_children = sorted(children, key=lambda x: x.get("value", 1), reverse=True)
    total_val = sum(c.get("value", 1) for c in sorted_children)

    # Calculate radii proportional to value (area encoding)
    usable_r = parent_r * 0.85
    radii = []
    for c in sorted_children:
        val = c.get("value", 1)
        r = np.sqrt(val / total_val) * usable_r * 0.58
        radii.append(max(r, usable_r * 0.08))

    placed = []
    result = []

    for i, child in enumerate(sorted_children):
        r = radii[i]

        if i == 0:
            # First circle: offset from center
            cx, cy = parent_x, parent_y
        elif i == 1:
            # Second: tangent to first
            px, py, pr = placed[0]
            angle = np.pi * 2 / 3
            cx = px + (pr + r) * np.cos(angle)
            cy = py + (pr + r) * np.sin(angle)
        else:
            # Find best tangent position
            best_pos, best_dist = None, float("inf")
            for j in range(len(placed)):
                for k in range(j + 1, len(placed)):
                    x1, y1, r1 = placed[j]
                    x2, y2, r2 = placed[k]
                    for px, py in find_tangent_positions(x1, y1, r1, x2, y2, r2, r):
                        dist = np.sqrt((px - parent_x) ** 2 + (py - parent_y) ** 2)
                        if dist + r > usable_r:
                            continue
                        overlap = any(
                            np.sqrt((px - ox) ** 2 + (py - oy) ** 2) < r + orr - 0.001 for ox, oy, orr in placed
                        )
                        if not overlap and dist < best_dist:
                            best_dist, best_pos = dist, (px, py)

            if best_pos:
                cx, cy = best_pos
            else:
                angle = i * 2.39996  # Golden angle
                dist = usable_r * 0.5
                cx = parent_x + dist * np.cos(angle)
                cy = parent_y + dist * np.sin(angle)

        placed.append((cx, cy, r))
        result.append(
            {
                "id": child["id"],
                "label": child.get("label", child["id"]),
                "x": cx,
                "y": cy,
                "r": r,
                "depth": depth,
                "value": child.get("value", 1),
            }
        )

    return result


# Hierarchical data - Company organizational structure
hierarchy = {
    "id": "root",
    "label": "Company",
    "children": [
        {
            "id": "eng",
            "label": "Engineering",
            "value": 50,
            "children": [
                {"id": "be", "label": "Backend", "value": 20},
                {"id": "fe", "label": "Frontend", "value": 18},
                {"id": "dops", "label": "DevOps", "value": 12},
            ],
        },
        {
            "id": "ops",
            "label": "Operations",
            "value": 35,
            "children": [
                {"id": "fin", "label": "Finance", "value": 15},
                {"id": "leg", "label": "Legal", "value": 10},
                {"id": "hr", "label": "HR", "value": 10},
            ],
        },
        {
            "id": "prod",
            "label": "Product",
            "value": 30,
            "children": [
                {"id": "des", "label": "Design", "value": 12},
                {"id": "pm", "label": "PM", "value": 10},
                {"id": "res", "label": "Research", "value": 8},
            ],
        },
    ],
}

# Build all circles
all_circles = []

# Root circle
root_x, root_y, root_r = 0, 0, 1.0
all_circles.append({"id": "root", "label": "Company", "x": root_x, "y": root_y, "r": root_r, "depth": 0})

# Level 1: departments
dept_circles = pack_circles(hierarchy["children"], root_x, root_y, root_r, depth=1)
all_circles.extend(dept_circles)

# Level 2: teams within each department
for dc in dept_circles:
    dept_data = next((d for d in hierarchy["children"] if d["id"] == dc["id"]), None)
    if dept_data and "children" in dept_data:
        team_circles = pack_circles(dept_data["children"], dc["x"], dc["y"], dc["r"], depth=2)
        all_circles.extend(team_circles)

# Sort by depth for proper layering (root first, teams last/on top)
all_circles_sorted = sorted(all_circles, key=lambda c: c["depth"])

# Build polygon dataframe
polygon_rows = []
for circle in all_circles_sorted:
    xs, ys = make_circle_points(circle["x"], circle["y"], circle["r"])
    for j, (x, y) in enumerate(zip(xs, ys, strict=True)):
        polygon_rows.append({"circle_id": circle["id"], "x": x, "y": y, "order": j, "depth": circle["depth"]})

df_circles = pd.DataFrame(polygon_rows)

# Labels - position department labels at top of their circles, team labels centered
label_rows = []
for circle in all_circles:
    if circle["depth"] == 0:
        continue
    text_size = max(9, min(14, circle["r"] * 28))
    if circle["depth"] == 1:
        # Department labels: position at top edge of circle
        label_y = circle["y"] + circle["r"] * 0.75
    else:
        # Team labels: centered
        label_y = circle["y"]
    label_rows.append({"x": circle["x"], "y": label_y, "label": circle["label"], "text_size": text_size})

df_labels = pd.DataFrame(label_rows)

# Create the plot
plot = (
    ggplot()
    + geom_polygon(
        df_circles, aes(x="x", y="y", group="circle_id", fill="factor(depth)"), color="#333333", size=0.5, alpha=0.92
    )
    + geom_text(
        df_labels,
        aes(x="x", y="y", label="label", size="text_size"),
        color="#222222",
        fontweight="bold",
        show_legend=False,
    )
    + scale_fill_manual(
        values=["#E0E0E0", "#306998", "#FFD43B"], labels=["Root", "Departments", "Teams"], name="Hierarchy Level"
    )
    + scale_size_identity()
    + coord_fixed(ratio=1)
    + labs(title="circlepacking-basic · plotnine · pyplots.ai")
    + theme_void()
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=28, ha="center", weight="bold", margin={"b": 20}),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16, weight="bold"),
        legend_position="bottom",
        legend_direction="horizontal",
    )
    + guides(fill=guide_legend(override_aes={"size": 0.5}))
)

plot.save("plot.png", dpi=300, width=12, height=12, verbose=False)
