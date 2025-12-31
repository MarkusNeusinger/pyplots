""" pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Label, Legend, LegendItem, Slider
from bokeh.plotting import figure


# Data - Sales data across multiple years
np.random.seed(42)

years = list(range(2018, 2025))
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate sales data for each year with realistic growth trend
all_data = {}
for year in years:
    base = 50 + (year - 2018) * 8  # Growth trend
    seasonal = np.array([0.8, 0.75, 0.9, 1.0, 1.1, 1.15, 1.2, 1.15, 1.05, 1.1, 1.25, 1.4])
    noise = np.random.normal(0, 5, 12)
    sales = base * seasonal + noise
    all_data[year] = sales.tolist()

# Initial data for 2024 (most recent year)
initial_year = 2024
source = ColumnDataSource(data={"months": months, "sales": all_data[initial_year]})

# Create figure with categorical x-axis
p = figure(
    width=4800,
    height=2700,
    x_range=months,
    y_range=(0, 180),
    title=f"Monthly Sales ({initial_year}) · slider-control-basic · bokeh · pyplots.ai",
    x_axis_label="Month",
    y_axis_label="Sales (thousands USD)",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    toolbar_location="right",
)

# Style the plot for large canvas (4800x2700)
p.title.text_font_size = "42pt"
p.xaxis.axis_label_text_font_size = "32pt"
p.yaxis.axis_label_text_font_size = "32pt"
p.xaxis.major_label_text_font_size = "24pt"
p.yaxis.major_label_text_font_size = "24pt"

# Add bar chart
bars = p.vbar(
    x="months",
    top="sales",
    source=source,
    width=0.7,
    fill_color="#306998",
    line_color="#306998",
    fill_alpha=0.85,
    line_width=2,
)

# Add line connecting the bars
trend_line = p.line(x="months", y="sales", source=source, line_width=4, line_color="#FFD43B", line_alpha=0.9)

# Add scatter points on top of bars
trend_points = p.scatter(
    x="months",
    y="sales",
    source=source,
    size=20,
    fill_color="#FFD43B",
    line_color="#306998",
    line_width=3,
    fill_alpha=1.0,
)

# Add legend
legend = Legend(
    items=[
        LegendItem(label="Monthly Sales", renderers=[bars]),
        LegendItem(label="Trend Line", renderers=[trend_line, trend_points]),
    ],
    location="top_left",
    label_text_font_size="24pt",
    spacing=20,
    padding=20,
    background_fill_alpha=0.8,
)
p.add_layout(legend, "right")

# Style grid
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = [6, 4]

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "#ffffff"

# Create slider with width proportional to plot (4800 * 0.8 = 3840)
slider = Slider(
    start=2018, end=2024, value=2024, step=1, title="Select Year (2018-2024)", width=3840, bar_color="#306998"
)

# Add annotation to indicate interactive functionality (visible in static PNG context)
interactive_note = Label(
    x=3800,
    y=170,
    x_units="screen",
    y_units="data",
    text="[Interactive] Use slider to change year (2018-2024)",
    text_font_size="22pt",
    text_color="#666666",
    text_align="right",
)
p.add_layout(interactive_note)

# Prepare data for JavaScript callback
all_data_js = {str(k): v for k, v in all_data.items()}

# JavaScript callback for slider interaction
callback = CustomJS(
    args={"source": source, "all_data": all_data_js, "title": p.title},
    code="""
    const year = cb_obj.value;
    const data = source.data;
    data['sales'] = all_data[year.toString()];
    source.change.emit();
    title.text = 'Monthly Sales (' + year + ') · slider-control-basic · bokeh · pyplots.ai';
""",
)

slider.js_on_change("value", callback)

# Layout with slider below the plot
layout = column(p, slider, sizing_mode="fixed")

# Save as HTML (interactive version)
save(layout, filename="plot.html", title="slider-control-basic · bokeh · pyplots.ai")

# Export static PNG (shows 2024 data)
export_png(p, filename="plot.png")
