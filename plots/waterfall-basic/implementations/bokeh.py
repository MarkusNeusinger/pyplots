""" pyplots.ai
waterfall-basic: Basic Waterfall Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure, save


# Data - quarterly financial breakdown
categories = ["Starting Revenue", "Product Sales", "Services", "Refunds", "Operating Costs", "Marketing", "Net Income"]
values = [0, 150000, 45000, -12000, -85000, -28000, 0]

# Calculate waterfall positions
running_total = 0
bar_bottoms = []
bar_heights = []
bar_colors = []
totals_at_step = []

for i, (_cat, val) in enumerate(zip(categories, values, strict=True)):
    if i == 0:
        # Starting total - show as a full bar from 0
        running_total = 150000  # Initial value
        bar_bottoms.append(0)
        bar_heights.append(running_total)
        bar_colors.append("#306998")  # Python Blue for totals
        totals_at_step.append(running_total)
    elif i == len(categories) - 1:
        # Final total - show as a full bar from 0
        bar_bottoms.append(0)
        bar_heights.append(running_total)
        bar_colors.append("#306998")  # Python Blue for totals
        totals_at_step.append(running_total)
    else:
        # Intermediate values - changes from running total
        if val >= 0:
            bar_bottoms.append(running_total)
            bar_heights.append(val)
            bar_colors.append("#2ECC71")  # Green for positive
        else:
            bar_bottoms.append(running_total + val)
            bar_heights.append(abs(val))
            bar_colors.append("#E74C3C")  # Red for negative
        running_total += val
        totals_at_step.append(running_total)

# Calculate tops for bars
bar_tops = [b + h for b, h in zip(bar_bottoms, bar_heights, strict=True)]

# Create data source
source = ColumnDataSource(
    data={
        "categories": categories,
        "bottom": bar_bottoms,
        "top": bar_tops,
        "height": bar_heights,
        "color": bar_colors,
        "totals": totals_at_step,
    }
)

# Create figure (4800 x 2700 px)
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="waterfall-basic · bokeh · pyplots.ai",
    x_axis_label="Category",
    y_axis_label="Amount ($)",
    toolbar_location=None,
)

# Draw bars
p.vbar(
    x="categories",
    top="top",
    bottom="bottom",
    width=0.6,
    source=source,
    color="color",
    line_color="white",
    line_width=2,
    alpha=0.9,
)

# Draw connector lines between bars
for i in range(len(categories) - 1):
    # Line from top of current bar to start of next bar
    current_top = bar_bottoms[i] + bar_heights[i]
    if i == 0:
        # From starting total to next bar
        next_bottom = bar_bottoms[i + 1] if values[i + 1] >= 0 else bar_bottoms[i + 1] + bar_heights[i + 1]
    else:
        next_bottom = bar_bottoms[i + 1] if values[i + 1] >= 0 else bar_bottoms[i + 1] + bar_heights[i + 1]

    if i < len(categories) - 2:  # Don't draw connector to final total bar
        p.line(
            x=[categories[i], categories[i + 1]],
            y=[current_top, current_top],
            line_color="#7F8C8D",
            line_width=2,
            line_dash="dashed",
            alpha=0.7,
        )

# Add value labels on bars
for i, (_cat, bottom, height, total) in enumerate(
    zip(categories, bar_bottoms, bar_heights, totals_at_step, strict=True)
):
    # Label position
    label_y = bottom + height + 5000
    if i == 0 or i == len(categories) - 1:
        label_text = f"${total:,.0f}"
    else:
        val = values[i]
        sign = "+" if val >= 0 else ""
        label_text = f"{sign}${val:,.0f}"

    label = Label(
        x=i,
        y=label_y,
        text=label_text,
        text_font_size="20pt",
        text_align="center",
        text_baseline="bottom",
        text_color="#2C3E50",
    )
    p.add_layout(label)

# Style
p.title.text_font_size = "32pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.major_label_orientation = 0.5  # Slight rotation for readability

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#FAFAFA"
p.border_fill_color = "#FFFFFF"

# Axis styling
p.yaxis.formatter.use_scientific = False
p.y_range.start = -10000
p.y_range.end = max(totals_at_step) + 25000

# Save as PNG and HTML
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="waterfall-basic · bokeh · pyplots.ai")
