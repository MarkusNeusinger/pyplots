"""pyplots.ai
feynman-basic: Feynman Diagram for Particle Interactions
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-03-07
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import Arrow, ColumnDataSource, Label, NormalHead, Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Electron-positron annihilation: e- + e+ -> gamma -> e- + e+
v1 = (1.5, 3.0)
v2 = (4.5, 3.0)

propagators = [
    {"start": (0.0, 5.0), "end": v1, "type": "fermion", "label": "e\u207b", "arrow": "forward"},
    {"start": (0.0, 1.0), "end": v1, "type": "fermion", "label": "e\u207a", "arrow": "backward"},
    {"start": v1, "end": v2, "type": "photon", "label": "\u03b3"},
    {"start": v2, "end": (6.0, 5.0), "type": "fermion", "label": "e\u207b", "arrow": "forward"},
    {"start": v2, "end": (6.0, 1.0), "type": "fermion", "label": "e\u207a", "arrow": "backward"},
]

# Plot
p = figure(
    width=4800,
    height=2700,
    title="feynman-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_range=Range1d(-0.8, 6.8),
    y_range=Range1d(-0.3, 6.3),
    toolbar_location=None,
)

p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Style
p.title.text_font_size = "28pt"
p.title.align = "center"
p.background_fill_color = "#fafafa"

# Draw propagators
for prop in propagators:
    x0, y0 = prop["start"]
    x1, y1 = prop["end"]
    dx = x1 - x0
    dy = y1 - y0
    length = np.sqrt(dx**2 + dy**2)

    if prop["type"] == "fermion":
        p.line([x0, x1], [y0, y1], line_width=4, color="#306998")

        # Arrow at midpoint showing particle/antiparticle flow
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        offset = 0.15
        if prop.get("arrow") == "backward":
            arrow_sx = mid_x + offset * dx / length
            arrow_sy = mid_y + offset * dy / length
            arrow_ex = mid_x - offset * dx / length
            arrow_ey = mid_y - offset * dy / length
        else:
            arrow_sx = mid_x - offset * dx / length
            arrow_sy = mid_y - offset * dy / length
            arrow_ex = mid_x + offset * dx / length
            arrow_ey = mid_y + offset * dy / length

        p.add_layout(
            Arrow(
                end=NormalHead(size=25, fill_color="#306998", line_color="#306998"),
                x_start=arrow_sx,
                y_start=arrow_sy,
                x_end=arrow_ex,
                y_end=arrow_ey,
                line_width=0,
                line_alpha=0,
            )
        )

    elif prop["type"] == "photon":
        n_waves = 8
        t = np.linspace(0, 1, 300)
        perp_x = -dy / length
        perp_y = dx / length
        amplitude = 0.25
        wave_offset = amplitude * np.sin(2 * np.pi * n_waves * t)
        wave_x = (x0 + t * dx) + wave_offset * perp_x
        wave_y = (y0 + t * dy) + wave_offset * perp_y
        p.line(wave_x.tolist(), wave_y.tolist(), line_width=4, color="#D4A017")

    # Label offset perpendicular to the line
    mid_x = (x0 + x1) / 2
    mid_y = (y0 + y1) / 2
    perp_x = -dy / length
    perp_y = dx / length
    label_x = mid_x + 0.35 * perp_x
    label_y = mid_y + 0.35 * perp_y

    p.add_layout(
        Label(
            x=label_x,
            y=label_y,
            text=prop["label"],
            text_font_size="22pt",
            text_font_style="italic",
            text_color="#333333",
            text_align="center",
            text_baseline="middle",
        )
    )

# Draw vertices
vertex_source = ColumnDataSource(data={"x": [v1[0], v2[0]], "y": [v1[1], v2[1]]})
p.scatter("x", "y", source=vertex_source, size=20, color="#306998", line_color="white", line_width=2)

# Time axis
p.add_layout(
    Arrow(
        end=NormalHead(size=20, fill_color="#999999", line_color="#999999"),
        x_start=1.0,
        y_start=0.0,
        x_end=5.0,
        y_end=0.0,
        line_width=3,
        line_color="#999999",
    )
)
p.add_layout(
    Label(
        x=3.0,
        y=-0.1,
        text="time",
        text_font_size="20pt",
        text_color="#999999",
        text_align="center",
        text_baseline="top",
    )
)

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="Feynman Diagram")
