""" pyplots.ai
maze-circular: Circular Maze Puzzle
Library: altair 6.0.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-16
"""

import altair as alt
import numpy as np
import pandas as pd


# Maze parameters
np.random.seed(42)
num_rings = 7
sectors_per_ring = [1] + [12 + i * 4 for i in range(num_rings)]  # More sectors in outer rings
center_x, center_y = 0, 0
ring_width = 1.0

# Data structures for maze
# Each cell is (ring, sector) - track which walls exist
# walls[ring][sector] = {'outer': bool, 'cw': bool} (outer radial wall, clockwise wall)
walls = []
for ring in range(num_rings):
    ring_walls = []
    for _sector in range(sectors_per_ring[ring + 1]):
        ring_walls.append({"outer": True, "cw": True})
    walls.append(ring_walls)

# Union-Find for maze generation (ensures single path)
parent = {}


def find(cell):
    if parent[cell] != cell:
        parent[cell] = find(parent[cell])
    return parent[cell]


def union(cell1, cell2):
    root1, root2 = find(cell1), find(cell2)
    if root1 != root2:
        parent[root1] = root2
        return True
    return False


# Initialize each cell as its own set
for ring in range(num_rings):
    for sector in range(sectors_per_ring[ring + 1]):
        parent[(ring, sector)] = (ring, sector)

# Generate maze using randomized Kruskal's algorithm
# Create list of all possible wall removals
possible_walls = []

for ring in range(num_rings):
    num_sectors = sectors_per_ring[ring + 1]
    for sector in range(num_sectors):
        # Clockwise wall (connects to next sector in same ring)
        next_sector = (sector + 1) % num_sectors
        possible_walls.append(("cw", ring, sector, ring, next_sector))

        # Outer wall (connects to outer ring if exists)
        if ring < num_rings - 1:
            outer_sectors = sectors_per_ring[ring + 2]
            # Map current sector to corresponding outer sector(s)
            ratio = outer_sectors / num_sectors
            outer_sector = int(sector * ratio)
            possible_walls.append(("outer", ring, sector, ring + 1, outer_sector))

# Shuffle and process walls
np.random.shuffle(possible_walls)

for wall_type, r1, s1, r2, s2 in possible_walls:
    if union((r1, s1), (r2, s2)):
        if wall_type == "cw":
            walls[r1][s1]["cw"] = False
        else:
            walls[r1][s1]["outer"] = False

# Create entry and exit
entry_sector = np.random.randint(0, sectors_per_ring[num_rings])
# Mark entry on outer ring (remove outer boundary at entry point)

# Generate wall segments for plotting
wall_data = []


def add_arc(r_inner, theta_start, theta_end, wall_id):
    """Add arc wall segment data"""
    # Create arc points
    theta = np.linspace(theta_start, theta_end, 30)
    x = r_inner * np.cos(theta)
    y = r_inner * np.sin(theta)
    for i in range(len(x)):
        wall_data.append({"x": x[i], "y": y[i], "wall_id": wall_id, "order": i})


def add_radial(r_inner, r_outer, theta, wall_id):
    """Add radial wall segment data"""
    x1, y1 = r_inner * np.cos(theta), r_inner * np.sin(theta)
    x2, y2 = r_outer * np.cos(theta), r_outer * np.sin(theta)
    wall_data.append({"x": x1, "y": y1, "wall_id": wall_id, "order": 0})
    wall_data.append({"x": x2, "y": y2, "wall_id": wall_id, "order": 1})


wall_count = 0

# Draw outer boundary (except entry)
theta_vals = np.linspace(0, 2 * np.pi, sectors_per_ring[num_rings] + 1)
entry_theta_start = theta_vals[entry_sector]
entry_theta_end = theta_vals[entry_sector + 1]

# Outer boundary in two parts (leaving entry gap)
outer_r = num_rings * ring_width
if entry_sector > 0:
    add_arc(outer_r, 0, entry_theta_start, f"outer_bound_{wall_count}")
    wall_count += 1
if entry_sector < sectors_per_ring[num_rings] - 1:
    add_arc(outer_r, entry_theta_end, 2 * np.pi, f"outer_bound_{wall_count}")
    wall_count += 1

# Draw ring walls (concentric circles with gaps)
for ring in range(num_rings - 1):
    r = (ring + 1) * ring_width
    num_sectors = sectors_per_ring[ring + 1]
    theta_vals = np.linspace(0, 2 * np.pi, num_sectors + 1)

    # Track wall segments (gaps where walls[ring][sector]['outer'] is False)
    arc_start = None
    for sector in range(num_sectors):
        if walls[ring][sector]["outer"]:
            if arc_start is None:
                arc_start = theta_vals[sector]
        else:
            if arc_start is not None:
                add_arc(r, arc_start, theta_vals[sector], f"ring_{ring}_{wall_count}")
                wall_count += 1
                arc_start = None

    # Close final arc if needed
    if arc_start is not None:
        add_arc(r, arc_start, 2 * np.pi, f"ring_{ring}_{wall_count}")
        wall_count += 1

# Draw radial walls (sector dividers with gaps)
for ring in range(num_rings):
    num_sectors = sectors_per_ring[ring + 1]
    r_inner = ring * ring_width
    r_outer = (ring + 1) * ring_width
    theta_vals = np.linspace(0, 2 * np.pi, num_sectors + 1)

    for sector in range(num_sectors):
        if walls[ring][sector]["cw"]:
            theta = theta_vals[(sector + 1) % num_sectors] if sector < num_sectors - 1 else 2 * np.pi
            if ring == 0:
                r_inner = 0.3  # Leave center gap
            else:
                r_inner = ring * ring_width
            add_radial(r_inner, r_outer, theta, f"radial_{ring}_{sector}_{wall_count}")
            wall_count += 1

# Create center goal marker - use a star symbol
center_data = pd.DataFrame({"x": [0], "y": [0], "label": ["\u2605"]})  # Unicode star

# Entry marker - place it outside the opening with upward arrow pointing into maze
entry_angle = (entry_theta_start + entry_theta_end) / 2
entry_r = num_rings * ring_width + 1.0
# Create entry label with up arrow (pointing into the maze)
entry_data = pd.DataFrame(
    {"x": [entry_r * np.cos(entry_angle)], "y": [entry_r * np.sin(entry_angle)], "label": ["\u2191 ENTER"]}
)

# Convert wall data to DataFrame
df_walls = pd.DataFrame(wall_data)

# Create chart
base = (
    alt.Chart(df_walls)
    .mark_line(color="black", strokeWidth=3)
    .encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None), detail="wall_id:N", order="order:O")
)

# Center goal - star symbol
goal = (
    alt.Chart(center_data)
    .mark_text(fontSize=50, fontWeight="bold", color="#FFD43B")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Entry marker - horizontal text with arrow
entry = (
    alt.Chart(entry_data)
    .mark_text(fontSize=24, fontWeight="bold", color="#306998", angle=0)
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Combine layers
chart = (
    alt.layer(base, goal, entry)
    .properties(width=900, height=900, title=alt.Title("maze-circular · altair · pyplots.ai", fontSize=28))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False)
)

# Save outputs
chart.save("plot.png", scale_factor=4.0)
chart.save("plot.html")
