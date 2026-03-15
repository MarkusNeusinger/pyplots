""" pyplots.ai
column-stratigraphic: Stratigraphic Column with Lithology Patterns
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-15
"""

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool, Label, Legend, LegendItem, Range1d, Span
from bokeh.plotting import figure, output_file, save


# Data: Synthetic sedimentary section with 10 layers (varied thicknesses)
layers = [
    {"top": 0, "bottom": 12, "lithology": "Sandstone", "formation": "Dakota Fm", "age": "Late Cretaceous"},
    {"top": 12, "bottom": 38, "lithology": "Shale", "formation": "Mancos Fm", "age": "Late Cretaceous"},
    {"top": 38, "bottom": 52, "lithology": "Limestone", "formation": "Niobrara Fm", "age": "Late Cretaceous"},
    {"top": 52, "bottom": 60, "lithology": "Siltstone", "formation": "Pierre Fm", "age": "Late Cretaceous"},
    {"top": 60, "bottom": 88, "lithology": "Sandstone", "formation": "Fox Hills Fm", "age": "Late Cretaceous"},
    {"top": 88, "bottom": 112, "lithology": "Conglomerate", "formation": "Dawson Fm", "age": "Paleocene"},
    {"top": 112, "bottom": 140, "lithology": "Shale", "formation": "Green River Fm", "age": "Eocene"},
    {"top": 140, "bottom": 158, "lithology": "Limestone", "formation": "Leadville Fm", "age": "Eocene"},
    {"top": 158, "bottom": 180, "lithology": "Sandstone", "formation": "Wasatch Fm", "age": "Eocene"},
    {"top": 180, "bottom": 200, "lithology": "Siltstone", "formation": "Uinta Fm", "age": "Eocene"},
]

# Lithology style mapping: color, hatch_pattern (improved color differentiation)
lithology_styles = {
    "Sandstone": {"color": "#F5DEB3", "hatch_pattern": ".", "hatch_color": "#8B7355"},
    "Shale": {"color": "#A9A9A9", "hatch_pattern": "-", "hatch_color": "#4A4A4A"},
    "Limestone": {"color": "#87CEEB", "hatch_pattern": "+", "hatch_color": "#2E5A88"},
    "Siltstone": {"color": "#8B6F5E", "hatch_pattern": "/", "hatch_color": "#3E2F23"},
    "Conglomerate": {"color": "#E8923F", "hatch_pattern": "o", "hatch_color": "#6B3A00"},
}

# K-Pg boundary depth (between Fox Hills Fm / Late Cretaceous and Dawson Fm / Paleocene)
KPG_DEPTH = 88

# Column x-position and width (wider column for better canvas use)
col_center = 0.5
col_width = 1.0

# Plot (tighter x_range for better horizontal utilization)
p = figure(
    width=4800,
    height=2700,
    title="column-stratigraphic · bokeh · pyplots.ai",
    y_axis_label="Depth (m)",
    toolbar_location=None,
    x_range=Range1d(-0.7, 2.0),
    y_range=Range1d(210, -10),
)

# Draw each layer as a rectangle with hatch pattern
legend_items_dict = {}
for layer in layers:
    source = ColumnDataSource(
        data={
            "x": [col_center],
            "y": [(layer["top"] + layer["bottom"]) / 2],
            "width": [col_width],
            "height": [layer["bottom"] - layer["top"]],
            "lithology": [layer["lithology"]],
            "formation": [layer["formation"]],
            "age": [layer["age"]],
            "top_depth": [layer["top"]],
            "bottom_depth": [layer["bottom"]],
            "thickness": [layer["bottom"] - layer["top"]],
        }
    )

    style = lithology_styles[layer["lithology"]]
    renderer = p.rect(
        x="x",
        y="y",
        width="width",
        height="height",
        source=source,
        fill_color=style["color"],
        line_color="#2C2C2C",
        line_width=2,
        hatch_pattern=style["hatch_pattern"],
        hatch_color=style["hatch_color"],
        hatch_alpha=0.7,
        hatch_scale=16,
        hatch_weight=2,
    )

    lith = layer["lithology"]
    if lith not in legend_items_dict:
        legend_items_dict[lith] = renderer

    hover = HoverTool(
        renderers=[renderer],
        tooltips=[
            ("Lithology", "@lithology"),
            ("Formation", "@formation"),
            ("Age", "@age"),
            ("Top", "@top_depth{0.0} m"),
            ("Bottom", "@bottom_depth{0.0} m"),
            ("Thickness", "@thickness{0.0} m"),
        ],
    )
    p.add_tools(hover)

# K-Pg boundary emphasis — bold red dashed line with annotation
kpg_span = Span(location=KPG_DEPTH, dimension="width", line_color="#CC0000", line_width=4, line_dash="dashed")
p.add_layout(kpg_span)

kpg_label = Label(
    x=col_center,
    y=KPG_DEPTH,
    text="K-Pg Boundary (~66 Ma)",
    text_font_size="16pt",
    text_font_style="bold",
    text_color="#CC0000",
    text_align="center",
    text_baseline="bottom",
    y_offset=8,
)
p.add_layout(kpg_label)

# Formation labels on the right side
for layer in layers:
    mid_y = (layer["top"] + layer["bottom"]) / 2
    label = Label(
        x=1.08,
        y=mid_y,
        text=layer["formation"],
        text_font_size="18pt",
        text_align="left",
        text_baseline="middle",
        text_color="#2C2C2C",
    )
    p.add_layout(label)

# Age labels on the left side with brackets
age_groups = {}
for layer in layers:
    age = layer["age"]
    if age not in age_groups:
        age_groups[age] = {"top": layer["top"], "bottom": layer["bottom"]}
    else:
        age_groups[age]["bottom"] = max(age_groups[age]["bottom"], layer["bottom"])
        age_groups[age]["top"] = min(age_groups[age]["top"], layer["top"])

for age, bounds in age_groups.items():
    mid_y = (bounds["top"] + bounds["bottom"]) / 2
    label = Label(
        x=-0.08,
        y=mid_y,
        text=age,
        text_font_size="18pt",
        text_align="right",
        text_baseline="middle",
        text_color="#2C2C2C",
        text_font_style="italic",
    )
    p.add_layout(label)

    p.line(x=[-0.05, -0.05], y=[bounds["top"], bounds["bottom"]], line_color="#2C2C2C", line_width=2)
    p.line(x=[-0.07, -0.05], y=[bounds["top"], bounds["top"]], line_color="#2C2C2C", line_width=2)
    p.line(x=[-0.07, -0.05], y=[bounds["bottom"], bounds["bottom"]], line_color="#2C2C2C", line_width=2)

# Legend — positioned adjacent to column, not in far corner
legend_items = [LegendItem(label=lith, renderers=[rend]) for lith, rend in legend_items_dict.items()]
legend = Legend(
    items=legend_items,
    location="top_right",
    label_text_font_size="20pt",
    spacing=12,
    padding=20,
    background_fill_alpha=0.85,
    glyph_height=30,
    glyph_width=30,
    title="Lithology",
    title_text_font_size="22pt",
    title_text_font_style="bold",
)
p.add_layout(legend, "right")

# Style
p.title.text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "22pt"

p.xaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.15
p.ygrid.grid_line_dash = "dashed"

p.yaxis.minor_tick_line_color = None
p.outline_line_color = None
p.background_fill_color = "#FAFAFA"

# Save
export_png(p, filename="plot.png")
output_file("plot.html", title="column-stratigraphic · bokeh · pyplots.ai")
save(p)
