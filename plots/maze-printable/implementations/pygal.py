""" pyplots.ai
maze-printable: Printable Maze Puzzle
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-07
"""

import numpy as np
import pygal
from pygal.style import Style


# Seed for reproducibility
np.random.seed(42)

# Maze dimensions (25x25 as specified in spec)
maze_width = 25
maze_height = 25

# Generate maze using DFS algorithm
# Each cell: 0 = wall, 1 = passage
grid_h = maze_height * 2 + 1
grid_w = maze_width * 2 + 1
maze = np.zeros((grid_h, grid_w), dtype=int)

# Initialize cells (passages between walls)
for y in range(maze_height):
    for x in range(maze_width):
        maze[y * 2 + 1, x * 2 + 1] = 1

# DFS maze generation
stack = [(0, 0)]
visited = set()
visited.add((0, 0))

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

while stack:
    cx, cy = stack[-1]
    neighbors = []
    for dx, dy in directions:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < maze_width and 0 <= ny < maze_height and (nx, ny) not in visited:
            neighbors.append((nx, ny, dx, dy))

    if neighbors:
        idx = np.random.randint(len(neighbors))
        nx, ny, dx, dy = neighbors[idx]
        # Remove wall between current and neighbor
        maze[cy * 2 + 1 + dy, cx * 2 + 1 + dx] = 1
        visited.add((nx, ny))
        stack.append((nx, ny))
    else:
        stack.pop()

# Create entrance (top-left) and exit (bottom-right)
maze[0, 1] = 1  # Entrance at top
maze[grid_h - 1, grid_w - 2] = 1  # Exit at bottom

# All walls are black - create enough black entries for each row
colors = tuple(["#000000"] * grid_h)

# Custom style - clean black and white for printability
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#000000",
    foreground_strong="#000000",
    foreground_subtle="#000000",
    colors=colors,
    title_font_size=72,
    label_font_size=1,
    major_label_font_size=1,
    legend_font_size=1,
    value_font_size=1,
    font_family="monospace",
)

# Use Dot chart to create grid representation
chart = pygal.Dot(
    width=3600,
    height=3600,
    style=custom_style,
    title="maze-printable · pygal · pyplots.ai",
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    dots_size=32,
    margin=100,
)

# Add wall rows - walls show as black dots, passages are empty
for y in range(grid_h):
    row_data = []
    for x in range(grid_w):
        if maze[y, x] == 0:  # Wall
            row_data.append(1)
        else:  # Passage
            row_data.append(None)
    chart.add("", row_data)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
