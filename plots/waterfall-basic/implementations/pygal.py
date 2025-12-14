"""
waterfall-basic: Basic Waterfall Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Quarterly financial breakdown from revenue to net income
categories = ["Revenue", "Cost of Sales", "Operating Exp", "Taxes", "Net Income"]
changes = [150000, -45000, -35000, -22000, None]  # None = final total

# Calculate running total for the final value
running_total = sum(c for c in changes[:-1] if c is not None)
changes[-1] = running_total  # Set final total

# Define colors
TOTAL_COLOR = "#306998"  # Python Blue for totals
INCREASE_COLOR = "#4CAF50"  # Green for increases
DECREASE_COLOR = "#E53935"  # Red for decreases

# Custom style for waterfall chart - colors match series order: base, total, increase, decrease
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("rgba(255,255,255,0)", TOTAL_COLOR, INCREASE_COLOR, DECREASE_COLOR),
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=36,
    value_font_size=32,
    value_label_font_size=32,
    legend_font_size=36,
)

# Build the waterfall data structure
# Each bar needs: base (invisible portion), visible height, and color
bar_data = []
cumulative = 0

for i, (cat, val) in enumerate(zip(categories, changes, strict=True)):
    is_first = i == 0
    is_last = i == len(categories) - 1

    if is_first or is_last:
        # Total bars start from 0
        bar_data.append({"category": cat, "base": 0, "height": val, "color": TOTAL_COLOR, "value": val})
        if is_first:
            cumulative = val
    else:
        # Change bars
        if val >= 0:
            bar_data.append({"category": cat, "base": cumulative, "height": val, "color": INCREASE_COLOR, "value": val})
        else:
            bar_data.append(
                {"category": cat, "base": cumulative + val, "height": abs(val), "color": DECREASE_COLOR, "value": val}
            )
        cumulative += val

# Create a stacked bar chart - first stack is invisible base, second is visible bar
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    title="waterfall-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Amount ($)",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    print_values=True,
    value_formatter=lambda x: f"${x:,.0f}" if x and abs(x) > 0.01 else "",
    show_y_guides=True,
    show_x_guides=False,
    margin=50,
    spacing=40,
)

# Set x labels
chart.x_labels = categories

# Create the base (invisible) series and colored bar series
base_series = []
total_series = []
increase_series = []
decrease_series = []

for bar in bar_data:
    base_series.append({"value": bar["base"], "color": "rgba(255,255,255,0)"})

    if bar["color"] == TOTAL_COLOR:
        total_series.append({"value": bar["height"], "color": TOTAL_COLOR})
        increase_series.append({"value": None})
        decrease_series.append({"value": None})
    elif bar["color"] == INCREASE_COLOR:
        total_series.append({"value": None})
        increase_series.append({"value": bar["height"], "color": INCREASE_COLOR})
        decrease_series.append({"value": None})
    else:
        total_series.append({"value": None})
        increase_series.append({"value": None})
        decrease_series.append({"value": bar["height"], "color": DECREASE_COLOR})

# Add series - base is invisible spacer (no legend entry)
# Check if we have any increases to show in legend
has_increases = any(s.get("value") for s in increase_series)

chart.add("", base_series, show_dots=False, stroke=False)
chart.add("Total", total_series)
if has_increases:
    chart.add("Increase", increase_series)
chart.add("Decrease", decrease_series)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
