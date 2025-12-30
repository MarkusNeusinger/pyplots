"""pyplots.ai
icicle-basic: Basic Icicle Chart
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import pandas as pd
from plotnine import aes, element_text, geom_rect, geom_text, ggplot, labs, scale_fill_manual, theme, theme_void


# Data: File system hierarchy with sizes
data = [
    {"name": "root", "parent": "", "value": 0},
    {"name": "Documents", "parent": "root", "value": 0},
    {"name": "Photos", "parent": "root", "value": 0},
    {"name": "Projects", "parent": "root", "value": 0},
    {"name": "Reports", "parent": "Documents", "value": 450},
    {"name": "Invoices", "parent": "Documents", "value": 280},
    {"name": "Notes", "parent": "Documents", "value": 120},
    {"name": "Vacation", "parent": "Photos", "value": 680},
    {"name": "Family", "parent": "Photos", "value": 520},
    {"name": "Events", "parent": "Photos", "value": 340},
    {"name": "WebApp", "parent": "Projects", "value": 0},
    {"name": "DataSci", "parent": "Projects", "value": 0},
    {"name": "Mobile", "parent": "Projects", "value": 380},
    {"name": "Frontend", "parent": "WebApp", "value": 290},
    {"name": "Backend", "parent": "WebApp", "value": 410},
    {"name": "Config", "parent": "WebApp", "value": 85},
    {"name": "Models", "parent": "DataSci", "value": 520},
    {"name": "Scripts", "parent": "DataSci", "value": 180},
]

df = pd.DataFrame(data)


# Build hierarchy and calculate sizes (leaf-up aggregation)
def calculate_values(df):
    """Calculate values for non-leaf nodes by summing children."""
    result = df.copy()
    name_to_idx = {row["name"]: idx for idx, row in result.iterrows()}

    # Recursive function to get total value
    def get_total(name):
        idx = name_to_idx[name]
        children = result[result["parent"] == name]
        if len(children) == 0:
            return result.loc[idx, "value"]
        total = sum(get_total(child) for child in children["name"])
        result.loc[idx, "value"] = total
        return total

    get_total("root")
    return result


df = calculate_values(df)


# Calculate icicle layout (horizontal: root at top, children below)
def compute_icicle_layout(df):
    """Compute rectangle positions for icicle chart."""
    name_to_row = {row["name"]: row for _, row in df.iterrows()}

    # Assign depth levels
    depths = {}

    def get_depth(name):
        if name in depths:
            return depths[name]
        row = name_to_row.get(name)
        if row is None or row["parent"] == "":
            depths[name] = 0
            return 0
        depths[name] = get_depth(row["parent"]) + 1
        return depths[name]

    for name in df["name"]:
        get_depth(name)

    max_depth = max(depths.values())

    # Layout: rectangles based on value proportion
    rects = []

    def layout_node(name, x_start, x_end):
        row = name_to_row[name]
        depth = depths[name]
        y_top = max_depth - depth + 1
        y_bottom = max_depth - depth

        rects.append(
            {
                "name": name,
                "xmin": x_start,
                "xmax": x_end,
                "ymin": y_bottom,
                "ymax": y_top,
                "depth": depth,
                "value": row["value"],
            }
        )

        # Layout children
        children = df[df["parent"] == name].sort_values("value", ascending=False)
        if len(children) > 0:
            total_value = children["value"].sum()
            if total_value > 0:
                curr_x = x_start
                for _, child in children.iterrows():
                    width = (child["value"] / total_value) * (x_end - x_start)
                    layout_node(child["name"], curr_x, curr_x + width)
                    curr_x += width

    layout_node("root", 0, 1)
    return pd.DataFrame(rects)


rect_df = compute_icicle_layout(df)

# Color palette by depth level
colors = {
    0: "#306998",  # Python Blue - root
    1: "#4B8BBE",  # Lighter blue - level 1
    2: "#FFD43B",  # Python Yellow - level 2
    3: "#FFE873",  # Light yellow - level 3
    4: "#646464",  # Gray - level 4
}
rect_df["color"] = rect_df["depth"].map(colors)

# Add labels only for rectangles wide enough
rect_df["width"] = rect_df["xmax"] - rect_df["xmin"]
rect_df["label"] = rect_df.apply(lambda r: r["name"] if r["width"] > 0.05 else "", axis=1)
rect_df["x_center"] = (rect_df["xmin"] + rect_df["xmax"]) / 2
rect_df["y_center"] = (rect_df["ymin"] + rect_df["ymax"]) / 2

# Create plot
plot = (
    ggplot(rect_df)
    + geom_rect(aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="factor(depth)"), color="white", size=1.5)
    + geom_text(aes(x="x_center", y="y_center", label="label"), size=12, color="black", fontweight="bold")
    + scale_fill_manual(values=["#306998", "#4B8BBE", "#FFD43B", "#FFE873", "#90B4CE"], name="Hierarchy Level")
    + labs(title="icicle-basic · plotnine · pyplots.ai")
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=28, ha="center", weight="bold"),
        legend_position="right",
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
