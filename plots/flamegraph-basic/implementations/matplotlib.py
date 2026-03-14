""" pyplots.ai
flamegraph-basic: Flame Graph for Performance Profiling
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-14
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


# Data - simulated CPU profiling stacks with sample counts
np.random.seed(42)

stacks = {
    "main": 950,
    "main;process_request": 800,
    "main;process_request;parse_input": 180,
    "main;process_request;parse_input;tokenize": 120,
    "main;process_request;parse_input;validate": 50,
    "main;process_request;compute": 450,
    "main;process_request;compute;matrix_multiply": 280,
    "main;process_request;compute;matrix_multiply;dot_product": 200,
    "main;process_request;compute;matrix_multiply;allocate_buffer": 60,
    "main;process_request;compute;transform": 130,
    "main;process_request;compute;transform;normalize": 80,
    "main;process_request;compute;transform;scale": 40,
    "main;process_request;send_response": 120,
    "main;process_request;send_response;serialize": 70,
    "main;process_request;send_response;write_socket": 40,
    "main;initialize": 100,
    "main;initialize;load_config": 55,
    "main;initialize;setup_logging": 35,
    "main;gc_collect": 40,
}

# Build flame graph rectangles from stack data
total_samples = stacks["main"]

# Parse stacks into (depth, function_name, start_x, width) rectangles
# Group by depth and parent to compute positions
rects = []

# For each depth level, track the x-offset for children of each parent
# First, organize stacks by depth
depth_map = {}
for stack_path, samples in stacks.items():
    parts = stack_path.split(";")
    depth = len(parts) - 1
    func_name = parts[-1]
    parent = ";".join(parts[:-1]) if depth > 0 else None
    if depth not in depth_map:
        depth_map[depth] = []
    depth_map[depth].append((stack_path, func_name, samples, parent))

# Assign x positions: root starts at 0 with full width
positions = {}
positions["main"] = (0.0, total_samples)

for depth in sorted(depth_map.keys()):
    if depth == 0:
        for _, func_name, samples, _ in depth_map[depth]:
            rects.append((depth, func_name, 0.0, samples))
        continue

    # Group children by parent
    parent_children = {}
    for stack_path, func_name, samples, parent in depth_map[depth]:
        if parent not in parent_children:
            parent_children[parent] = []
        parent_children[parent].append((stack_path, func_name, samples))

    for parent, children in parent_children.items():
        if parent not in positions:
            continue
        parent_x, parent_width = positions[parent]
        current_x = parent_x
        for stack_path, func_name, samples in children:
            positions[stack_path] = (current_x, samples)
            rects.append((depth, func_name, current_x, samples))
            current_x += samples

# Warm color palette for flame graph aesthetic
warm_colors = ["#FFDD57", "#FFB627", "#FF9505", "#FF6700", "#E8430A", "#D62828"]
cmap = mcolors.LinearSegmentedColormap.from_list("flame", warm_colors, N=256)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

bar_height = 0.85
max_depth = max(r[0] for r in rects)

for depth, func_name, x_start, width in rects:
    # Color based on depth with some randomness for visual variety
    color_val = (depth / (max_depth + 1)) * 0.7 + np.random.uniform(0, 0.3)
    color_val = min(color_val, 1.0)
    color = cmap(color_val)

    ax.barh(depth, width, left=x_start, height=bar_height, color=color, edgecolor="#FFFFFF", linewidth=0.5)

    # Add function name label if bar is wide enough
    bar_fraction = width / total_samples
    if bar_fraction > 0.05:
        label_fontsize = 14 if bar_fraction > 0.15 else 11
        ax.text(
            x_start + width / 2,
            depth,
            func_name,
            ha="center",
            va="center",
            fontsize=label_fontsize,
            fontweight="medium",
            color="#1a1a1a",
        )

# Style
ax.set_xlim(0, total_samples)
ax.set_ylim(-0.5, max_depth + 0.8)
ax.set_xlabel("CPU Samples", fontsize=20)
ax.set_ylabel("Stack Depth", fontsize=20)
ax.set_title("flamegraph-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_yticks(range(max_depth + 1))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
