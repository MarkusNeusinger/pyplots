""" pyplots.ai
cartogram-area-distortion: Cartogram with Area Distortion by Data Value
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 74/100 | Created: 2026-03-13
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, Label, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure, save
from bokeh.transform import transform


# Data - US states: approximate centroid positions, population (2023 estimates in millions)
np.random.seed(42)

states = {
    "WA": (-122.0, 47.5, 7.7),
    "OR": (-120.5, 44.0, 4.2),
    "CA": (-119.5, 37.0, 39.0),
    "NV": (-116.8, 39.0, 3.2),
    "ID": (-114.5, 44.0, 2.0),
    "MT": (-109.5, 47.0, 1.1),
    "WY": (-107.5, 43.0, 0.6),
    "UT": (-111.5, 39.5, 3.4),
    "CO": (-105.5, 39.0, 5.8),
    "AZ": (-111.5, 34.0, 7.4),
    "NM": (-106.0, 34.5, 2.1),
    "ND": (-100.5, 47.5, 0.8),
    "SD": (-100.0, 44.5, 0.9),
    "NE": (-99.5, 41.5, 2.0),
    "KS": (-98.5, 38.5, 2.9),
    "OK": (-97.5, 35.5, 4.0),
    "TX": (-99.0, 31.0, 30.5),
    "MN": (-94.5, 46.0, 5.7),
    "IA": (-93.5, 42.0, 3.2),
    "MO": (-92.5, 38.5, 6.2),
    "AR": (-92.5, 34.8, 3.0),
    "LA": (-92.0, 31.0, 4.6),
    "WI": (-89.5, 44.5, 5.9),
    "IL": (-89.0, 40.0, 12.6),
    "MI": (-84.5, 44.5, 10.0),
    "IN": (-86.0, 40.0, 6.8),
    "OH": (-82.5, 40.5, 11.8),
    "KY": (-85.5, 37.8, 4.5),
    "TN": (-86.0, 35.8, 7.1),
    "MS": (-89.5, 32.5, 2.9),
    "AL": (-86.8, 32.8, 5.1),
    "GA": (-83.5, 33.0, 11.0),
    "FL": (-81.5, 28.0, 22.6),
    "SC": (-80.5, 34.0, 5.3),
    "NC": (-79.0, 35.5, 10.7),
    "VA": (-78.5, 37.5, 8.6),
    "WV": (-80.5, 38.5, 1.8),
    "PA": (-77.5, 41.0, 13.0),
    "NY": (-75.5, 43.0, 19.7),
    "NJ": (-74.5, 40.0, 9.3),
    "DE": (-75.5, 39.0, 1.0),
    "MD": (-76.6, 39.0, 6.2),
    "CT": (-72.7, 41.6, 3.6),
    "RI": (-71.5, 41.7, 1.1),
    "MA": (-71.8, 42.3, 7.0),
    "VT": (-72.6, 44.0, 0.6),
    "NH": (-71.5, 43.5, 1.4),
    "ME": (-69.0, 45.0, 1.4),
}

names = list(states.keys())
lons = [states[s][0] for s in names]
lats = [states[s][1] for s in names]
populations = [states[s][2] for s in names]

# Scale circle sizes: area proportional to population
# sqrt because circle area ~ r^2
min_pop, max_pop = min(populations), max(populations)
min_size, max_size = 18, 90
sizes = [min_size + (max_size - min_size) * np.sqrt((p - min_pop) / (max_pop - min_pop)) for p in populations]

# Population density approximation (pop per rough state area estimate)
# Using population directly for color to reinforce the size variable
pop_array = np.array(populations)

source = ColumnDataSource(
    data={
        "lon": lons,
        "lat": lats,
        "population": populations,
        "size": sizes,
        "name": names,
        "pop_label": [f"{p:.1f}M" for p in populations],
    }
)

# Color mapper
color_mapper = LinearColorMapper(palette=Viridis256, low=min(populations), high=max(populations))

# Plot
p = figure(
    width=4800,
    height=2700,
    title="US States by Population · cartogram-area-distortion · bokeh · pyplots.ai",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tools="hover,pan,wheel_zoom,reset",
    tooltips=[("State", "@name"), ("Population", "@pop_label")],
)

p.scatter(
    x="lon",
    y="lat",
    size="size",
    source=source,
    fill_color=transform("population", color_mapper),
    fill_alpha=0.85,
    line_color="white",
    line_width=1.5,
)

# Add state labels for major states (pop > 8M)
for i, name in enumerate(names):
    if populations[i] > 8.0:
        label = Label(
            x=lons[i],
            y=lats[i],
            text=name,
            text_font_size="14pt",
            text_align="center",
            text_baseline="middle",
            text_color="#1a1a1a",
            text_font_style="bold",
        )
        p.add_layout(label)

# Color bar
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=BasicTicker(desired_num_ticks=6),
    label_standoff=14,
    major_label_text_font_size="16pt",
    title="Population (millions)",
    title_text_font_size="18pt",
    width=30,
    padding=30,
)
p.add_layout(color_bar, "right")

# Style
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.xgrid.grid_line_alpha = 0.15
p.ygrid.grid_line_alpha = 0.15
p.xgrid.grid_line_width = 1
p.ygrid.grid_line_width = 1

p.background_fill_color = "#fafafa"
p.border_fill_color = "white"
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="Cartogram Area Distortion - Bokeh")
