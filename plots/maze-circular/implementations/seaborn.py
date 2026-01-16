""" pyplots.ai
maze-circular: Circular Maze Puzzle
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-16
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Configuration
np.random.seed(42)
rings = 7
sectors_per_ring = 12
difficulty = "medium"

# Set seaborn style for clean aesthetics
sns.set_style("white")
sns.set_context("talk", font_scale=1.2)

# Create figure with square aspect
fig, ax = plt.subplots(figsize=(12, 12))


# Maze generation using Union-Find for guaranteed single solution
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


# Cell indexing: cell (ring, sector) -> unique id
def cell_id(ring, sector):
    if ring == 0:
        return 0  # Center is a single cell
    return 1 + sum(sectors_per_ring for _ in range(ring - 1)) + (sector % sectors_per_ring)


# Total cells
total_cells = 1 + rings * sectors_per_ring

# Initialize Union-Find
uf = UnionFind(total_cells)

# Generate all possible walls (edges between adjacent cells)
walls = []

# Radial walls: between ring r and ring r+1
for r in range(rings):
    if r == 0:
        # From center to first ring
        for s in range(sectors_per_ring):
            walls.append(("radial", 0, s, cell_id(0, 0), cell_id(1, s)))
    else:
        for s in range(sectors_per_ring):
            walls.append(("radial", r, s, cell_id(r, s), cell_id(r + 1, s)))

# Circular walls: between adjacent sectors in same ring
for r in range(1, rings + 1):
    for s in range(sectors_per_ring):
        next_s = (s + 1) % sectors_per_ring
        walls.append(("circular", r, s, cell_id(r, s), cell_id(r, next_s)))

# Shuffle walls for random maze generation
np.random.shuffle(walls)

# Kruskal's algorithm: remove walls to create spanning tree (single path)
passages = set()
for wall in walls:
    wall_type, r, s, c1, c2 = wall
    if uf.union(c1, c2):
        passages.add((wall_type, r, s))

# Adjust passage density based on difficulty
if difficulty == "easy":
    extra_passages = int(len(walls) * 0.15)
elif difficulty == "medium":
    extra_passages = int(len(walls) * 0.08)
else:  # hard
    extra_passages = int(len(walls) * 0.02)

# Add some extra passages to make easier (multiple paths)
remaining_walls = [w for w in walls if (w[0], w[1], w[2]) not in passages]
np.random.shuffle(remaining_walls)
for i in range(min(extra_passages, len(remaining_walls))):
    w = remaining_walls[i]
    passages.add((w[0], w[1], w[2]))

# Drawing parameters
inner_radius = 0.15
ring_width = (1 - inner_radius) / (rings + 0.5)
wall_color = "#1a1a1a"
wall_linewidth = 3

# Draw outer boundary
theta = np.linspace(0, 2 * np.pi, 200)
outer_r = inner_radius + (rings + 0.3) * ring_width
ax.plot(outer_r * np.cos(theta), outer_r * np.sin(theta), color=wall_color, linewidth=wall_linewidth + 1)

# Draw concentric ring walls (circular walls between rings)
for r in range(1, rings + 1):
    radius = inner_radius + r * ring_width
    sector_angle = 2 * np.pi / sectors_per_ring

    for s in range(sectors_per_ring):
        # Check if there's a passage here (circular wall between sectors)
        if ("circular", r, s) not in passages:
            # Draw arc wall between sector s and s+1
            start_angle = s * sector_angle
            end_angle = start_angle + sector_angle
            arc_theta = np.linspace(start_angle, end_angle, 30)
            ax.plot(radius * np.cos(arc_theta), radius * np.sin(arc_theta), color=wall_color, linewidth=wall_linewidth)

# Draw radial walls
for r in range(rings):
    if r == 0:
        inner_r = inner_radius
    else:
        inner_r = inner_radius + r * ring_width
    outer_r_wall = inner_radius + (r + 1) * ring_width

    sector_angle = 2 * np.pi / sectors_per_ring

    for s in range(sectors_per_ring):
        # Check if there's a passage here (radial wall)
        if ("radial", r, s) not in passages:
            angle = s * sector_angle
            ax.plot(
                [inner_r * np.cos(angle), outer_r_wall * np.cos(angle)],
                [inner_r * np.sin(angle), outer_r_wall * np.sin(angle)],
                color=wall_color,
                linewidth=wall_linewidth,
            )

# Draw center circle
center_theta = np.linspace(0, 2 * np.pi, 100)
ax.fill(
    inner_radius * 0.8 * np.cos(center_theta), inner_radius * 0.8 * np.sin(center_theta), color="#306998", alpha=0.8
)
ax.text(0, 0, "★", fontsize=28, ha="center", va="center", color="#FFD43B", fontweight="bold")

# Mark entry point on outer edge
entry_sector = 0
entry_angle = entry_sector * (2 * np.pi / sectors_per_ring) + (np.pi / sectors_per_ring)
entry_r = inner_radius + (rings + 0.15) * ring_width
ax.plot(entry_r * np.cos(entry_angle), entry_r * np.sin(entry_angle), "o", color="#306998", markersize=20)
ax.annotate(
    "START",
    xy=(entry_r * np.cos(entry_angle), entry_r * np.sin(entry_angle)),
    xytext=(entry_r * 1.15 * np.cos(entry_angle), entry_r * 1.15 * np.sin(entry_angle)),
    fontsize=16,
    fontweight="bold",
    ha="center",
    color="#306998",
)

# Create opening at entry point
entry_inner_r = inner_radius + rings * ring_width
entry_outer_r = outer_r
ax.plot(
    [entry_inner_r * np.cos(entry_angle), entry_outer_r * np.cos(entry_angle)],
    [entry_inner_r * np.sin(entry_angle), entry_outer_r * np.sin(entry_angle)],
    color="white",
    linewidth=wall_linewidth + 3,
)

# Set equal aspect ratio and remove axes
ax.set_aspect("equal")
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.axis("off")

# Title
ax.set_title("maze-circular · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
