"""pyplots.ai
flamegraph-basic: Flame Graph for Performance Profiling
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-03-14
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_rect,
    element_text,
    geom_rect,
    geom_text,
    ggplot,
    labs,
    scale_fill_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_void,
)


# Data - simulated CPU profiling stacks
np.random.seed(42)

stacks = {
    "main": 1000,
    "main;request_handler": 800,
    "main;request_handler;parse_headers": 150,
    "main;request_handler;parse_body": 120,
    "main;request_handler;parse_body;decode_json": 90,
    "main;request_handler;parse_body;validate_schema": 25,
    "main;request_handler;route_dispatch": 480,
    "main;request_handler;route_dispatch;auth_middleware": 100,
    "main;request_handler;route_dispatch;auth_middleware;verify_token": 70,
    "main;request_handler;route_dispatch;auth_middleware;check_permissions": 25,
    "main;request_handler;route_dispatch;query_database": 250,
    "main;request_handler;route_dispatch;query_database;build_query": 40,
    "main;request_handler;route_dispatch;query_database;execute_sql": 160,
    "main;request_handler;route_dispatch;query_database;execute_sql;fetch_rows": 100,
    "main;request_handler;route_dispatch;query_database;execute_sql;deserialize": 45,
    "main;request_handler;route_dispatch;query_database;cache_result": 35,
    "main;request_handler;route_dispatch;render_template": 110,
    "main;request_handler;route_dispatch;render_template;compile_template": 40,
    "main;request_handler;route_dispatch;render_template;apply_filters": 55,
    "main;request_handler;send_response": 40,
    "main;request_handler;send_response;compress_gzip": 30,
    "main;gc_collect": 80,
    "main;gc_collect;mark_sweep": 60,
    "main;gc_collect;compact_heap": 15,
    "main;logging": 100,
    "main;logging;format_message": 40,
    "main;logging;write_file": 50,
}

# Build flame graph rectangles from stack data
total_samples = stacks["main"]
records = []

warm_colors = ["#FFEB3B", "#FFC107", "#FF9800", "#FF7043", "#F44336", "#E53935", "#D32F2F"]


def get_color(depth, func_name):
    hash_val = sum(ord(c) for c in func_name)
    base_idx = min(depth, len(warm_colors) - 1)
    idx = (base_idx + hash_val) % len(warm_colors)
    return warm_colors[idx]


# Group stacks by depth and compute positions
depth_children = {}
for stack_path, samples in stacks.items():
    parts = stack_path.split(";")
    depth = len(parts) - 1
    parent = ";".join(parts[:-1]) if depth > 0 else None
    func_name = parts[-1]

    if (depth, parent) not in depth_children:
        depth_children[(depth, parent)] = []
    depth_children[(depth, parent)].append((func_name, stack_path, samples))

# Compute x positions recursively
positions = {}
positions["main"] = (0, total_samples)

for depth in range(1, 8):
    for (d, parent), children in sorted(depth_children.items()):
        if d != depth:
            continue
        if parent not in positions:
            continue
        parent_xmin = positions[parent][0]
        x_cursor = parent_xmin
        for _func_name, stack_path, samples in children:
            positions[stack_path] = (x_cursor, x_cursor + samples)
            x_cursor += samples

# Build dataframe for plotting
for stack_path, (xmin, xmax) in positions.items():
    parts = stack_path.split(";")
    depth = len(parts) - 1
    func_name = parts[-1]
    width_frac = (xmax - xmin) / total_samples

    records.append(
        {
            "xmin": xmin,
            "xmax": xmax,
            "ymin": depth - 0.45,
            "ymax": depth + 0.45,
            "depth": depth,
            "func": func_name,
            "fill_color": get_color(depth, func_name),
            "label": func_name if width_frac > 0.06 else "",
            "label_x": (xmin + xmax) / 2,
            "label_y": depth,
        }
    )

df = pd.DataFrame(records)

# Plot
plot = (
    ggplot(df)
    + geom_rect(aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="fill_color"), color="white", size=0.3)
    + geom_text(aes(x="label_x", y="label_y", label="label"), size=7, color="#1a1a1a", fontweight="bold")
    + scale_fill_identity()
    + scale_x_continuous(expand=(0, 0))
    + scale_y_continuous(expand=(0.02, 0.02))
    + labs(title="flamegraph-basic · plotnine · pyplots.ai")
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center", weight="bold", margin={"b": 15}),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="#1a1a1a", color="#1a1a1a"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
