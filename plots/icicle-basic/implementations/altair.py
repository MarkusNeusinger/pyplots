""" pyplots.ai
icicle-basic: Basic Icicle Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-30
"""

import altair as alt
import pandas as pd


# Data: File system hierarchy with sizes
data = [
    # Root
    {"name": "root", "parent": None, "value": 0},
    # Level 1: Main folders
    {"name": "Documents", "parent": "root", "value": 0},
    {"name": "Media", "parent": "root", "value": 0},
    {"name": "Projects", "parent": "root", "value": 0},
    # Level 2: Documents subfolders
    {"name": "Reports", "parent": "Documents", "value": 0},
    {"name": "Presentations", "parent": "Documents", "value": 0},
    # Level 2: Media subfolders
    {"name": "Images", "parent": "Media", "value": 0},
    {"name": "Videos", "parent": "Media", "value": 0},
    {"name": "Audio", "parent": "Media", "value": 0},
    # Level 2: Projects subfolders
    {"name": "WebApp", "parent": "Projects", "value": 0},
    {"name": "DataPipeline", "parent": "Projects", "value": 0},
    # Level 3: Leaf nodes with actual sizes (in MB)
    {"name": "Q1_Report.pdf", "parent": "Reports", "value": 45},
    {"name": "Q2_Report.pdf", "parent": "Reports", "value": 52},
    {"name": "Annual.pdf", "parent": "Reports", "value": 78},
    {"name": "Sales.pptx", "parent": "Presentations", "value": 35},
    {"name": "Strategy.pptx", "parent": "Presentations", "value": 42},
    {"name": "photo1.jpg", "parent": "Images", "value": 28},
    {"name": "photo2.jpg", "parent": "Images", "value": 32},
    {"name": "banner.png", "parent": "Images", "value": 15},
    {"name": "tutorial.mp4", "parent": "Videos", "value": 450},
    {"name": "demo.mp4", "parent": "Videos", "value": 380},
    {"name": "podcast.mp3", "parent": "Audio", "value": 95},
    {"name": "music.mp3", "parent": "Audio", "value": 85},
    {"name": "app.js", "parent": "WebApp", "value": 25},
    {"name": "style.css", "parent": "WebApp", "value": 12},
    {"name": "index.html", "parent": "WebApp", "value": 8},
    {"name": "pipeline.py", "parent": "DataPipeline", "value": 55},
    {"name": "config.yaml", "parent": "DataPipeline", "value": 5},
]

df = pd.DataFrame(data)

# Build tree structure: calculate cumulative values and positions
name_to_idx = {row["name"]: i for i, row in enumerate(data)}
children = {row["name"]: [] for row in data}
for row in data:
    if row["parent"]:
        children[row["parent"]].append(row["name"])


# Calculate cumulative values (sum of children for non-leaf nodes)
def calc_value(name):
    if children[name]:
        return sum(calc_value(child) for child in children[name])
    return data[name_to_idx[name]]["value"]


for row in data:
    row["total_value"] = calc_value(row["name"])


# Calculate level (depth) for each node
def calc_level(name, level=0):
    data[name_to_idx[name]]["level"] = level
    for child in children[name]:
        calc_level(child, level + 1)


calc_level("root")

# Calculate x positions (horizontal placement based on value)
# Each node gets a portion of the parent's width


def calc_positions(name, x_start=0, x_end=1):
    idx = name_to_idx[name]
    data[idx]["x_start"] = x_start
    data[idx]["x_end"] = x_end

    if children[name]:
        total = sum(data[name_to_idx[c]]["total_value"] for c in children[name])
        if total > 0:
            current_x = x_start
            for child in children[name]:
                child_val = data[name_to_idx[child]]["total_value"]
                child_width = (x_end - x_start) * child_val / total
                calc_positions(child, current_x, current_x + child_width)
                current_x += child_width


calc_positions("root")

# Prepare data for Altair rectangles
rect_data = []
max_level = max(row["level"] for row in data)

for row in data:
    if row["total_value"] > 0:  # Only include nodes with values
        rect_data.append(
            {
                "name": row["name"],
                "x_start": row["x_start"],
                "x_end": row["x_end"],
                "y_start": row["level"],
                "y_end": row["level"] + 1,
                "level": row["level"],
                "value": row["total_value"],
                "parent": row["parent"] if row["parent"] else "None",
            }
        )

rect_df = pd.DataFrame(rect_data)

# Color scale by level
level_colors = ["#306998", "#4A89B8", "#6BA3C8", "#8CBDD8", "#FFD43B"]

# Create icicle chart with mark_rect
chart = (
    alt.Chart(rect_df)
    .mark_rect(stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x_start:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        x2=alt.X2("x_end:Q"),
        y=alt.Y(
            "y_start:Q",
            axis=alt.Axis(
                title="Hierarchy Level",
                labelFontSize=18,
                titleFontSize=22,
                values=list(range(max_level + 2)),
                format="d",
            ),
            scale=alt.Scale(domain=[0, max_level + 1]),
        ),
        y2=alt.Y2("y_end:Q"),
        color=alt.Color(
            "level:O",
            scale=alt.Scale(domain=list(range(max_level + 1)), range=level_colors),
            legend=alt.Legend(title="Level", labelFontSize=16, titleFontSize=18, orient="right"),
        ),
        tooltip=["name:N", "value:Q", "parent:N", "level:O"],
    )
)

# Add text labels for larger rectangles
text = (
    alt.Chart(rect_df)
    .mark_text(fontSize=14, color="white", fontWeight="bold", align="center")
    .encode(
        x=alt.X("x_mid:Q", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("y_mid:Q", scale=alt.Scale(domain=[0, max_level + 1])),
        text=alt.Text("label:N"),
    )
    .transform_calculate(
        x_mid="(datum.x_start + datum.x_end) / 2",
        y_mid="(datum.y_start + datum.y_end) / 2",
        width="datum.x_end - datum.x_start",
        label="datum.width > 0.06 ? datum.name : ''",
    )
)

# Combine chart and text
icicle = (
    (chart + text)
    .properties(width=1600, height=900, title="icicle-basic · altair · pyplots.ai")
    .configure_title(fontSize=28, anchor="middle")
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
icicle.save("plot.png", scale_factor=3.0)
icicle.save("plot.html")
