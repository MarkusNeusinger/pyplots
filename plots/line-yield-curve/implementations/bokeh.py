""" pyplots.ai
line-yield-curve: Yield Curve (Interest Rate Term Structure)
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-14
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label, Legend, LegendItem
from bokeh.plotting import figure


# Data - U.S. Treasury yield curves on three dates
maturity_labels = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
maturity_years = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])

# Normal upward-sloping curve (Jan 2024)
yields_normal = np.array([5.53, 5.46, 5.36, 4.95, 4.42, 4.15, 3.98, 4.03, 4.10, 4.38, 4.27])

# Flat curve (Jun 2024)
yields_flat = np.array([5.47, 5.49, 5.40, 5.12, 4.75, 4.55, 4.32, 4.30, 4.28, 4.52, 4.40])

# Inverted curve (Jul 2023)
yields_inverted = np.array([5.47, 5.52, 5.56, 5.40, 4.87, 4.56, 4.18, 4.09, 3.96, 4.22, 4.03])

# Create ColumnDataSources
source_normal = ColumnDataSource(data={"maturity": maturity_years, "yield_pct": yields_normal})
source_flat = ColumnDataSource(data={"maturity": maturity_years, "yield_pct": yields_flat})
source_inverted = ColumnDataSource(data={"maturity": maturity_years, "yield_pct": yields_inverted})

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="U.S. Treasury Yield Curves · line-yield-curve · bokeh · pyplots.ai",
    x_axis_label="Maturity (Years)",
    y_axis_label="Yield (%)",
)

# Plot curves
line_normal = p.line(x="maturity", y="yield_pct", source=source_normal, line_width=5, line_color="#306998")
scatter_normal = p.scatter(
    x="maturity", y="yield_pct", source=source_normal, size=18, fill_color="#306998", line_color="white", line_width=3
)

line_flat = p.line(x="maturity", y="yield_pct", source=source_flat, line_width=5, line_color="#E8833A")
scatter_flat = p.scatter(
    x="maturity", y="yield_pct", source=source_flat, size=18, fill_color="#E8833A", line_color="white", line_width=3
)

line_inverted = p.line(
    x="maturity", y="yield_pct", source=source_inverted, line_width=5, line_color="#D64045", line_dash="dashed"
)
scatter_inverted = p.scatter(
    x="maturity", y="yield_pct", source=source_inverted, size=18, fill_color="#D64045", line_color="white", line_width=3
)

# Shading for inversion region (where short-term yields > 30Y yield)
inv_30y = yields_inverted[-1]
inv_mask = yields_inverted > inv_30y
inv_idx = np.where(inv_mask)[0]
inv_x = maturity_years[inv_idx]
inv_upper = yields_inverted[inv_idx]
p.varea(x=inv_x, y1=np.full_like(inv_x, inv_30y), y2=inv_upper, fill_color="#D64045", fill_alpha=0.08)

# Inversion annotation
inversion_label = Label(
    x=3.5,
    y=5.50,
    text="Inversion zone: short-term yields exceed long-term",
    text_font_size="24pt",
    text_color="#D64045",
    text_font_style="italic",
)
p.add_layout(inversion_label)

# Legend
legend = Legend(
    items=[
        LegendItem(label="Jan 2024 — Normal", renderers=[line_normal, scatter_normal]),
        LegendItem(label="Jun 2024 — Flat", renderers=[line_flat, scatter_flat]),
        LegendItem(label="Jul 2023 — Inverted", renderers=[line_inverted, scatter_inverted]),
    ],
    location="bottom_right",
)
legend.label_text_font_size = "22pt"
legend.glyph_width = 50
legend.glyph_height = 30
legend.spacing = 15
legend.padding = 20
legend.background_fill_alpha = 0.7
legend.border_line_alpha = 0.3
p.add_layout(legend)

# Custom x-axis tick labels using maturity names
# Skip 3M to avoid overlap with 1M and 6M at left edge
display_indices = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p.xaxis.ticker = [maturity_years[i] for i in display_indices]
p.xaxis.major_label_overrides = {maturity_years[i]: maturity_labels[i] for i in display_indices}

# Style text sizes for 4800x2700 px
p.title.text_font_size = "38pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "20pt"
p.yaxis.major_label_text_font_size = "20pt"

# Grid styling - subtle y-axis only
p.xgrid.grid_line_alpha = 0
p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_dash = "dashed"

# Background styling
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

# Axis styling
p.axis.axis_line_width = 2
p.axis.axis_line_color = "#333333"
p.axis.major_tick_line_width = 2
p.axis.minor_tick_line_color = None

# Remove toolbar for cleaner static image
p.toolbar_location = None

# Save
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
