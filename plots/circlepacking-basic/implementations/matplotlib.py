"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


# Hierarchical data: Company departments with team sizes
# Structure: parent -> children with values (leaf nodes have sizes)
hierarchy = {
    "Company": {
        "Engineering": {"Frontend": 25, "Backend": 35, "DevOps": 15, "QA": 20},
        "Product": {"Design": 18, "Research": 12, "Management": 8},
        "Operations": {"HR": 10, "Finance": 12, "Legal": 6, "Admin": 8},
        "Sales": {"North": 22, "South": 18, "International": 28},
    }
}


def compute_hierarchy_values(node, name="root"):
    """Recursively compute values for non-leaf nodes."""
    if isinstance(node, dict):
        total = 0
        children = []
        for child_name, child_value in node.items():
            child_data = compute_hierarchy_values(child_value, child_name)
            children.append(child_data)
            total += child_data["value"]
        return {"name": name, "value": total, "children": children}
    else:
        return {"name": name, "value": node, "children": []}


def pack_circles(circles, container_radius):
    """Simple circle packing using force-directed placement."""
    if not circles:
        return []

    n = len(circles)
    radii = np.array([c["radius"] for c in circles])

    # Initialize positions in a spiral pattern
    np.random.seed(42)
    angles = np.linspace(0, 2 * np.pi * (1 - 1 / n), n) if n > 1 else [0]
    positions = np.zeros((n, 2))
    for i, angle in enumerate(angles):
        r = container_radius * 0.3 * (i / max(n - 1, 1))
        positions[i] = [r * np.cos(angle), r * np.sin(angle)]

    # Force-directed packing iterations
    for _ in range(200):
        forces = np.zeros((n, 2))

        # Repulsion between circles
        for i in range(n):
            for j in range(i + 1, n):
                diff = positions[i] - positions[j]
                dist = np.linalg.norm(diff)
                min_dist = radii[i] + radii[j] + 2
                if dist < min_dist and dist > 0:
                    force = (min_dist - dist) * 0.5 * diff / dist
                    forces[i] += force
                    forces[j] -= force

        # Attraction to center
        for i in range(n):
            dist_to_center = np.linalg.norm(positions[i])
            if dist_to_center > 0:
                forces[i] -= 0.02 * positions[i]

        # Containment force
        for i in range(n):
            dist_to_center = np.linalg.norm(positions[i])
            max_dist = container_radius - radii[i] - 5
            if dist_to_center > max_dist and dist_to_center > 0:
                forces[i] -= 0.5 * (dist_to_center - max_dist) * positions[i] / dist_to_center

        positions += forces * 0.3

    for i, c in enumerate(circles):
        c["x"] = positions[i, 0]
        c["y"] = positions[i, 1]

    return circles


def layout_circle_packing(node, x=0, y=0, radius=None, depth=0, result=None, scale_factor=1.0):
    """Recursively layout circles for packing visualization."""
    if result is None:
        result = []

    if radius is None:
        radius = np.sqrt(node["value"]) * scale_factor

    result.append({"name": node["name"], "x": x, "y": y, "radius": radius, "depth": depth, "value": node["value"]})

    if node["children"]:
        # Calculate child radii based on their values
        child_circles = []
        total_child_value = sum(c["value"] for c in node["children"])

        for child in node["children"]:
            # Scale radius so children fit within parent
            child_radius = np.sqrt(child["value"] / total_child_value) * radius * 0.75
            child_circles.append({"name": child["name"], "radius": child_radius, "node": child})

        # Pack children within this circle
        pack_circles(child_circles, radius * 0.85)

        # Recursively layout grandchildren
        for cc in child_circles:
            layout_circle_packing(
                cc["node"],
                x=x + cc["x"],
                y=y + cc["y"],
                radius=cc["radius"],
                depth=depth + 1,
                result=result,
                scale_factor=scale_factor,
            )

    return result


# Build hierarchy data structure
root = compute_hierarchy_values(hierarchy, "Company")

# Layout circles with appropriate scale for canvas
scale = 40
circles = layout_circle_packing(root, x=0, y=0, radius=scale * np.sqrt(root["value"]) * 0.35, scale_factor=scale)

# Color scheme by depth level (Python colors + complementary)
depth_colors = {
    0: "#306998",  # Python Blue - root
    1: "#FFD43B",  # Python Yellow - departments
    2: "#5BA0D0",  # Lighter blue - teams
    3: "#7EC8B8",  # Teal - sub-teams
}

# Create figure (square format for symmetric visualization)
fig, ax = plt.subplots(figsize=(12, 12))

# Draw circles from largest to smallest (painters algorithm)
circles_sorted = sorted(circles, key=lambda c: -c["radius"])

for circle in circles_sorted:
    color = depth_colors.get(circle["depth"], "#AAAAAA")
    alpha = 0.7 if circle["depth"] > 0 else 0.3

    # Draw circle
    circ = patches.Circle(
        (circle["x"], circle["y"]), circle["radius"], facecolor=color, edgecolor="#2C3E50", linewidth=2, alpha=alpha
    )
    ax.add_patch(circ)

    # Add labels for circles that are large enough
    if circle["radius"] > 25:
        fontsize = min(20, max(12, circle["radius"] * 0.3))
        # Use dark text on yellow (depth 1), white on other colors
        text_color = "#1A1A1A" if circle["depth"] == 1 else "#FFFFFF"
        ax.text(
            circle["x"],
            circle["y"],
            circle["name"],
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color=text_color,
        )

# Set equal aspect ratio and limits
ax.set_aspect("equal")
max_extent = max(abs(c["x"]) + c["radius"] for c in circles) * 1.1
ax.set_xlim(-max_extent, max_extent)
ax.set_ylim(-max_extent, max_extent)

# Remove axes for cleaner visualization
ax.axis("off")

# Title
ax.set_title(
    "Company Organization · circlepacking-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)

# Add legend for depth levels
legend_elements = [
    patches.Patch(facecolor="#306998", edgecolor="#2C3E50", alpha=0.3, label="Company (Root)"),
    patches.Patch(facecolor="#FFD43B", edgecolor="#2C3E50", alpha=0.7, label="Departments"),
    patches.Patch(facecolor="#5BA0D0", edgecolor="#2C3E50", alpha=0.7, label="Teams"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=16, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
