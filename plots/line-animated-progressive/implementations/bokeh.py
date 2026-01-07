"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, save
from bokeh.layouts import column, row
from bokeh.models import Button, ColorBar, ColumnDataSource, CustomJS, LinearColorMapper, Slider
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Monthly temperature readings over 5 years
np.random.seed(42)
months = pd.date_range(start="2019-01-01", periods=60, freq="ME")
base_temp = 15 + 10 * np.sin(np.linspace(0, 10 * np.pi, 60))  # Seasonal pattern
trend = np.linspace(0, 2, 60)  # Slight warming trend
noise = np.random.randn(60) * 1.5
temperatures = base_temp + trend + noise

# Create sequential index for color mapping (progression indicator)
progression = np.arange(len(months))

# Compute sizes for markers (larger = later in time, scaled for 4800x2700 canvas)
sizes = 12 + (progression / progression.max()) * 18

# ColumnDataSource for the main plot
source = ColumnDataSource(data={"x": months, "y": temperatures, "progression": progression, "sizes": sizes})

# Create figure for static PNG (shows complete line with progression gradient)
p_static = figure(
    width=4800,
    height=2700,
    title="line-animated-progressive · bokeh · pyplots.ai",
    x_axis_label="Date",
    y_axis_label="Temperature (°C)",
    x_axis_type="datetime",
)

# Style the figure for large canvas
p_static.title.text_font_size = "36pt"
p_static.xaxis.axis_label_text_font_size = "28pt"
p_static.yaxis.axis_label_text_font_size = "28pt"
p_static.xaxis.major_label_text_font_size = "22pt"
p_static.yaxis.major_label_text_font_size = "22pt"

# Color mapper for progression gradient
color_mapper = LinearColorMapper(palette=Viridis256, low=0, high=len(months) - 1)

# Draw the line segments with gradient color to show progression
for i in range(len(months) - 1):
    p_static.line(
        x=[months[i], months[i + 1]],
        y=[temperatures[i], temperatures[i + 1]],
        line_width=5,
        line_color=Viridis256[int(255 * i / (len(months) - 1))],
        line_alpha=0.85,
    )

# Add markers with size gradient (larger = later in time)
p_static.scatter(
    x="x",
    y="y",
    source=source,
    size="sizes",
    fill_color={"field": "progression", "transform": color_mapper},
    line_color="white",
    line_width=2,
    alpha=0.9,
)

# Highlight the final point (most recent)
p_static.scatter(
    x=[months[-1]],
    y=[temperatures[-1]],
    size=40,
    fill_color="#FFD43B",
    line_color="#306998",
    line_width=4,
    legend_label="Current",
)

# Add color bar to show progression
color_bar = ColorBar(
    color_mapper=color_mapper,
    width=40,
    location=(0, 0),
    title="Time Progression",
    title_text_font_size="22pt",
    major_label_text_font_size="18pt",
)
p_static.add_layout(color_bar, "right")

# Grid styling
p_static.grid.grid_line_alpha = 0.3
p_static.grid.grid_line_dash = [6, 4]

# Legend
p_static.legend.location = "top_left"
p_static.legend.label_text_font_size = "20pt"
p_static.legend.background_fill_alpha = 0.7
p_static.legend.glyph_height = 30
p_static.legend.glyph_width = 30

# Save static PNG
export_png(p_static, filename="plot.png")

# ============================================================
# Interactive HTML version with animation
# ============================================================

# Create animated version with interactive controls
p_anim = figure(
    width=1200,
    height=675,
    title="line-animated-progressive · bokeh · pyplots.ai",
    x_axis_label="Date",
    y_axis_label="Temperature (°C)",
    x_axis_type="datetime",
)

# Style
p_anim.title.text_font_size = "18pt"
p_anim.xaxis.axis_label_text_font_size = "14pt"
p_anim.yaxis.axis_label_text_font_size = "14pt"
p_anim.xaxis.major_label_text_font_size = "12pt"
p_anim.yaxis.major_label_text_font_size = "12pt"
p_anim.grid.grid_line_alpha = 0.3

# Source for animated line (starts empty, fills progressively)
anim_source = ColumnDataSource(data={"x": months.tolist(), "y": temperatures.tolist()})

# Source for visible portion
visible_source = ColumnDataSource(data={"x": [], "y": []})

# Source for current point marker
current_point = ColumnDataSource(data={"x": [], "y": []})

# Draw visible line
p_anim.line(x="x", y="y", source=visible_source, line_width=3, line_color="#306998", alpha=0.8)

# Draw markers
p_anim.scatter(x="x", y="y", source=visible_source, size=8, fill_color="#306998", line_color="white", alpha=0.7)

# Current point highlight
p_anim.scatter(x="x", y="y", source=current_point, size=15, fill_color="#FFD43B", line_color="#306998", line_width=2)

# Slider to control animation frame
slider = Slider(start=1, end=len(months), value=1, step=1, title="Data Points", width=400)

# Button controls
play_button = Button(label="▶ Play", button_type="success", width=100)
reset_button = Button(label="⟲ Reset", button_type="default", width=100)

# JavaScript callback for slider
slider_callback = CustomJS(
    args={"source": anim_source, "visible": visible_source, "current": current_point, "slider": slider},
    code="""
    const n = slider.value;
    const x_full = source.data['x'];
    const y_full = source.data['y'];

    visible.data['x'] = x_full.slice(0, n);
    visible.data['y'] = y_full.slice(0, n);

    if (n > 0) {
        current.data['x'] = [x_full[n-1]];
        current.data['y'] = [y_full[n-1]];
    } else {
        current.data['x'] = [];
        current.data['y'] = [];
    }

    visible.change.emit();
    current.change.emit();
""",
)

slider.js_on_change("value", slider_callback)

# Play animation callback
play_callback = CustomJS(
    args={"slider": slider, "button": play_button},
    code="""
    if (button.label === '▶ Play') {
        button.label = '⏸ Pause';
        button.button_type = 'warning';

        window.animInterval = setInterval(function() {
            if (slider.value < slider.end) {
                slider.value += 1;
            } else {
                clearInterval(window.animInterval);
                button.label = '▶ Play';
                button.button_type = 'success';
            }
        }, 100);
    } else {
        clearInterval(window.animInterval);
        button.label = '▶ Play';
        button.button_type = 'success';
    }
""",
)

play_button.js_on_click(play_callback)

# Reset callback
reset_callback = CustomJS(
    args={"slider": slider, "button": play_button},
    code="""
    if (window.animInterval) {
        clearInterval(window.animInterval);
    }
    slider.value = 1;
    button.label = '▶ Play';
    button.button_type = 'success';
""",
)

reset_button.js_on_click(reset_callback)

# Initial state - show first point
visible_source.data = {"x": [months[0]], "y": [temperatures[0]]}
current_point.data = {"x": [months[0]], "y": [temperatures[0]]}

# Layout with controls
controls = row(play_button, reset_button, slider)
layout = column(p_anim, controls)

# Save interactive HTML
save(layout, filename="plot.html", resources=CDN, title="line-animated-progressive · bokeh · pyplots.ai")
