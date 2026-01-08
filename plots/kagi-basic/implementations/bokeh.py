"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-08
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool, Legend, LegendItem
from bokeh.plotting import figure


# Generate sample stock price data
np.random.seed(42)
n_days = 250  # ~1 year of trading days

# Simulate realistic stock price movements with trend
returns = np.random.normal(0.0005, 0.02, n_days)  # Daily returns
price = 100 * np.cumprod(1 + returns)

# Build Kagi chart data
reversal_pct = 0.04  # 4% reversal threshold

kagi_segments = []  # List of (x1, y1, x2, y2, is_yang)
direction = None  # 'up' or 'down'
last_price = price[0]
high = price[0]
low = price[0]
x_pos = 0

for i in range(1, len(price)):
    p = price[i]

    if direction is None:
        # Initialize direction
        change = (p - last_price) / last_price
        if change >= reversal_pct:
            direction = "up"
            is_yang = True
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            high = p
            last_price = p
        elif change <= -reversal_pct:
            direction = "down"
            is_yang = False
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            low = p
            last_price = p
    elif direction == "up":
        if p > high:
            # Continue uptrend
            if kagi_segments:
                seg = kagi_segments[-1]
                kagi_segments[-1] = (seg[0], seg[1], seg[2], p, seg[4])
            high = p
            last_price = p
        elif (high - p) / high >= reversal_pct:
            # Reversal to down
            x_pos += 1
            # Add horizontal connector
            kagi_segments.append(
                (x_pos - 1, last_price, x_pos, last_price, kagi_segments[-1][4] if kagi_segments else True)
            )
            # Check if breaking below previous low (transition to yin)
            is_yang = p >= low
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            direction = "down"
            low = p
            last_price = p
    else:  # direction == 'down'
        if p < low:
            # Continue downtrend
            if kagi_segments:
                seg = kagi_segments[-1]
                kagi_segments[-1] = (seg[0], seg[1], seg[2], p, seg[4])
            low = p
            last_price = p
        elif (p - low) / low >= reversal_pct:
            # Reversal to up
            x_pos += 1
            # Add horizontal connector
            kagi_segments.append(
                (x_pos - 1, last_price, x_pos, last_price, kagi_segments[-1][4] if kagi_segments else False)
            )
            # Check if breaking above previous high (transition to yang)
            is_yang = p > high
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            direction = "up"
            high = p
            last_price = p

# Prepare data for ColumnDataSource
yang_xs, yang_ys, yang_start, yang_end = [], [], [], []
yin_xs, yin_ys, yin_start, yin_end = [], [], [], []

for seg in kagi_segments:
    x1, y1, x2, y2, is_yang = seg
    if is_yang:
        yang_xs.append([x1, x2])
        yang_ys.append([y1, y2])
        yang_start.append(y1)
        yang_end.append(y2)
    else:
        yin_xs.append([x1, x2])
        yin_ys.append([y1, y2])
        yin_start.append(y1)
        yin_end.append(y2)

# Create ColumnDataSources for idiomatic Bokeh
yang_source = ColumnDataSource(
    data={
        "xs": yang_xs,
        "ys": yang_ys,
        "start_price": yang_start,
        "end_price": yang_end,
        "trend": ["Yang (Bullish)"] * len(yang_xs),
    }
)

yin_source = ColumnDataSource(
    data={
        "xs": yin_xs,
        "ys": yin_ys,
        "start_price": yin_start,
        "end_price": yin_end,
        "trend": ["Yin (Bearish)"] * len(yin_xs),
    }
)

# Create figure
fig = figure(
    width=4800,
    height=2700,
    title="kagi-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Kagi Line Index",
    y_axis_label="Price ($)",
    tools="",
    toolbar_location=None,
)

# Colorblind-safe colors: blue for yang (bullish), orange for yin (bearish)
YANG_COLOR = "#1f77b4"  # Blue
YIN_COLOR = "#ff7f0e"  # Orange

# Plot yang (bullish) segments - thick blue using multi_line with ColumnDataSource
yang_renderer = fig.multi_line(
    xs="xs", ys="ys", source=yang_source, line_width=14, line_color=YANG_COLOR, line_cap="round"
)

# Plot yin (bearish) segments - thin orange using multi_line with ColumnDataSource
yin_renderer = fig.multi_line(xs="xs", ys="ys", source=yin_source, line_width=6, line_color=YIN_COLOR, line_cap="round")

# Add HoverTool for interactivity
hover = HoverTool(
    tooltips=[("Trend", "@trend"), ("Start Price", "$@start_price{0.00}"), ("End Price", "$@end_price{0.00}")],
    renderers=[yang_renderer, yin_renderer],
)
fig.add_tools(hover)

# Add legend with larger text inside the plot area (top right, closer to data)
legend = Legend(
    items=[
        LegendItem(label="Yang (Bullish)", renderers=[yang_renderer]),
        LegendItem(label="Yin (Bearish)", renderers=[yin_renderer]),
    ],
    location="top_right",
    label_text_font_size="28pt",
    glyph_height=30,
    glyph_width=60,
    background_fill_alpha=0.9,
    background_fill_color="white",
    border_line_color="gray",
    border_line_width=2,
    padding=15,
    margin=20,
)
fig.add_layout(legend)

# Style configuration
fig.title.text_font_size = "32pt"
fig.title.align = "center"
fig.xaxis.axis_label_text_font_size = "24pt"
fig.yaxis.axis_label_text_font_size = "24pt"
fig.xaxis.major_label_text_font_size = "20pt"
fig.yaxis.major_label_text_font_size = "20pt"

# Grid styling
fig.grid.grid_line_alpha = 0.3
fig.grid.grid_line_dash = "dashed"

# Background
fig.background_fill_color = "#fafafa"

# Save PNG
export_png(fig, filename="plot.png")
