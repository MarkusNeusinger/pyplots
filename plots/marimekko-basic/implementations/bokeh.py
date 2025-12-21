""" pyplots.ai
marimekko-basic: Basic Marimekko Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-16
"""

from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure


# Data: Market share across regions with varying market sizes
regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
products = ["Electronics", "Apparel", "Home & Garden", "Food & Beverage"]

# Market values (billions) - regions have different total market sizes
data = {
    "North America": {"Electronics": 120, "Apparel": 80, "Home & Garden": 60, "Food & Beverage": 140},
    "Europe": {"Electronics": 90, "Apparel": 110, "Home & Garden": 50, "Food & Beverage": 100},
    "Asia Pacific": {"Electronics": 200, "Apparel": 150, "Home & Garden": 80, "Food & Beverage": 170},
    "Latin America": {"Electronics": 40, "Apparel": 35, "Home & Garden": 25, "Food & Beverage": 50},
}

# Colors (Python Blue first, then complementary colors)
colors = ["#306998", "#FFD43B", "#4ECDC4", "#E8685D"]

# Calculate totals for each region (determines bar width)
region_totals = {region: sum(data[region].values()) for region in regions}
total_all = sum(region_totals.values())

# Calculate normalized widths (proportional to region total)
bar_gap = 0.02  # Gap between bars
total_width = 1.0 - (len(regions) - 1) * bar_gap
widths = {region: (region_totals[region] / total_all) * total_width for region in regions}

# Build rectangle data for each segment
rect_x = []
rect_y = []
rect_widths = []
rect_heights = []
rect_colors = []
rect_products = []
rect_regions = []
rect_values = []
rect_percentages = []

current_x = 0
for region in regions:
    bar_width = widths[region]
    bar_center_x = current_x + bar_width / 2

    # Calculate stack within this bar
    current_y = 0
    region_total = region_totals[region]

    for i, product in enumerate(products):
        value = data[region][product]
        height = value / region_total  # Proportion within column

        rect_x.append(bar_center_x)
        rect_y.append(current_y + height / 2)
        rect_widths.append(bar_width * 0.98)  # Slight gap
        rect_heights.append(height)
        rect_colors.append(colors[i])
        rect_products.append(product)
        rect_regions.append(region)
        rect_values.append(value)
        rect_percentages.append(f"{height * 100:.1f}%")

        current_y += height

    current_x += bar_width + bar_gap

# Create ColumnDataSource
source = ColumnDataSource(
    data={
        "x": rect_x,
        "y": rect_y,
        "width": rect_widths,
        "height": rect_heights,
        "color": rect_colors,
        "product": rect_products,
        "region": rect_regions,
        "value": rect_values,
        "percentage": rect_percentages,
    }
)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="marimekko-basic · bokeh · pyplots.ai",
    x_range=(0, 1.0),
    y_range=(0, 1.0),
    tools="",
    toolbar_location=None,
)

# Draw rectangles
p.rect(x="x", y="y", width="width", height="height", color="color", source=source, line_color="white", line_width=2)

# Add hover tool
hover = HoverTool(
    tooltips=[("Region", "@region"), ("Product", "@product"), ("Value", "$@value B"), ("Share", "@percentage")]
)
p.add_tools(hover)

# Add value labels on segments (only on larger segments)
label_x = []
label_y = []
label_text = []
for i in range(len(rect_x)):
    # Only add label if segment is large enough
    if rect_heights[i] > 0.10 and rect_widths[i] > 0.08:
        label_x.append(rect_x[i])
        label_y.append(rect_y[i])
        label_text.append(f"${rect_values[i]}B")

label_source = ColumnDataSource(data={"x": label_x, "y": label_y, "text": label_text})

labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_align="center",
    text_baseline="middle",
    text_color="white",
    text_font_size="18pt",
    text_font_style="bold",
)
p.add_layout(labels)

# Add region labels at bottom
region_label_x = []
region_label_text = []
current_x = 0
for region in regions:
    bar_width = widths[region]
    region_label_x.append(current_x + bar_width / 2)
    region_label_text.append(f"{region}\n(${region_totals[region]}B)")
    current_x += bar_width + bar_gap

region_source = ColumnDataSource(data={"x": region_label_x, "y": [-0.06] * len(regions), "text": region_label_text})

region_labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=region_source,
    text_align="center",
    text_baseline="top",
    text_color="#333333",
    text_font_size="20pt",
)
p.add_layout(region_labels)

# Style
p.title.text_font_size = "28pt"
p.title.align = "center"

# Hide axes (we use custom labels)
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None

# Extend y_range to accommodate region labels
p.y_range.start = -0.15

# Add legend manually using rectangles and text
legend_y = 0.92
legend_x_start = 0.75
legend_spacing = 0.05

for i, product in enumerate(products):
    legend_y_pos = legend_y - i * legend_spacing
    # Legend color box
    p.rect(x=legend_x_start, y=legend_y_pos, width=0.025, height=0.035, color=colors[i], line_color="white")
    # Legend text - use text glyph
    p.text(
        x=[legend_x_start + 0.025],
        y=[legend_y_pos],
        text=[product],
        text_font_size="18pt",
        text_baseline="middle",
        text_color="#333333",
    )

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML
output_file("plot.html")
save(p)
