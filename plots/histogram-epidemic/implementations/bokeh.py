""" pyplots.ai
histogram-epidemic: Epidemic Curve (Epi Curve)
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-05
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Label, Legend, LegendItem, NumeralTickFormatter, Span
from bokeh.plotting import figure


# Data - Simulated foodborne illness outbreak over ~90 days
np.random.seed(42)

start_date = pd.Timestamp("2024-01-15")
dates = pd.date_range(start_date, periods=90, freq="D")

# Point-source outbreak with propagated secondary wave
days = np.arange(90)

# Primary wave: sharp peak around day 12 (point source from contaminated event)
confirmed_wave1 = np.random.poisson(lam=np.clip(45 * np.exp(-0.5 * ((days - 12) / 3.5) ** 2), 0.5, None))
# Secondary propagated wave around day 35
confirmed_wave2 = np.random.poisson(lam=np.clip(20 * np.exp(-0.5 * ((days - 35) / 6) ** 2), 0.2, None))
# Low endemic tail
confirmed_tail = np.random.poisson(lam=np.clip(1.5 * np.exp(-0.03 * days), 0.1, None))
confirmed = confirmed_wave1 + confirmed_wave2 + confirmed_tail

# Probable cases: ~30% of confirmed magnitude, slightly delayed
probable = np.random.poisson(
    lam=np.clip(12 * np.exp(-0.5 * ((days - 14) / 4) ** 2) + 7 * np.exp(-0.5 * ((days - 37) / 7) ** 2), 0.1, None)
)

# Suspect cases: smaller, broader distribution
suspect = np.random.poisson(
    lam=np.clip(5 * np.exp(-0.5 * ((days - 13) / 5) ** 2) + 3 * np.exp(-0.5 * ((days - 36) / 8) ** 2), 0.05, None)
)

df = pd.DataFrame({"date": dates, "confirmed": confirmed, "probable": probable, "suspect": suspect})

# Cumulative case count
df["total"] = df["confirmed"] + df["probable"] + df["suspect"]
df["cumulative"] = df["total"].cumsum()

# Stacking positions
df["bottom_confirmed"] = 0
df["top_confirmed"] = df["confirmed"]
df["bottom_probable"] = df["top_confirmed"]
df["top_probable"] = df["bottom_probable"] + df["probable"]
df["bottom_suspect"] = df["top_probable"]
df["top_suspect"] = df["bottom_suspect"] + df["suspect"]

# Convert dates for bokeh
df["date_str"] = df["date"].dt.strftime("%b %d")
bar_width = 0.8 * 24 * 60 * 60 * 1000  # ~0.8 day in ms

source = ColumnDataSource(
    data={
        "date": df["date"],
        "date_str": df["date_str"],
        "confirmed": df["confirmed"],
        "probable": df["probable"],
        "suspect": df["suspect"],
        "total": df["total"],
        "cumulative": df["cumulative"],
        "bottom_confirmed": df["bottom_confirmed"],
        "top_confirmed": df["top_confirmed"],
        "bottom_probable": df["bottom_probable"],
        "top_probable": df["top_probable"],
        "bottom_suspect": df["bottom_suspect"],
        "top_suspect": df["top_suspect"],
    }
)

# Plot
colors = {"Confirmed": "#306998", "Probable": "#FFD43B", "Suspect": "#E76F51"}

p = figure(
    width=4800,
    height=2700,
    title="histogram-epidemic · bokeh · pyplots.ai",
    x_axis_label="Date of Symptom Onset",
    y_axis_label="New Cases",
    x_axis_type="datetime",
    toolbar_location=None,
)

# Stacked bars
legend_items = []

r_confirmed = p.vbar(
    x="date",
    top="top_confirmed",
    bottom="bottom_confirmed",
    width=bar_width,
    source=source,
    color=colors["Confirmed"],
    line_color="white",
    line_width=0.8,
    alpha=0.9,
)
legend_items.append(LegendItem(label="Confirmed", renderers=[r_confirmed]))

r_probable = p.vbar(
    x="date",
    top="top_probable",
    bottom="bottom_probable",
    width=bar_width,
    source=source,
    color=colors["Probable"],
    line_color="white",
    line_width=0.8,
    alpha=0.9,
)
legend_items.append(LegendItem(label="Probable", renderers=[r_probable]))

r_suspect = p.vbar(
    x="date",
    top="top_suspect",
    bottom="bottom_suspect",
    width=bar_width,
    source=source,
    color=colors["Suspect"],
    line_color="white",
    line_width=0.8,
    alpha=0.9,
)
legend_items.append(LegendItem(label="Suspect", renderers=[r_suspect]))

# Hover tool
hover = HoverTool(
    renderers=[r_confirmed, r_probable, r_suspect],
    tooltips=[
        ("Date", "@date_str"),
        ("Confirmed", "@confirmed"),
        ("Probable", "@probable"),
        ("Suspect", "@suspect"),
        ("Total", "@total"),
        ("Cumulative", "@cumulative"),
    ],
    mode="vline",
)
p.add_tools(hover)

# Intervention vertical lines with annotations
contamination_date = pd.Timestamp("2024-01-27")
intervention_date = pd.Timestamp("2024-02-05")

span_contamination = Span(
    location=contamination_date,
    dimension="height",
    line_color="#C0392B",
    line_width=3,
    line_dash="dashed",
    line_alpha=0.8,
)
p.add_layout(span_contamination)

span_intervention = Span(
    location=intervention_date,
    dimension="height",
    line_color="#1A9E76",
    line_width=3,
    line_dash="dashed",
    line_alpha=0.8,
)
p.add_layout(span_intervention)

max_cases = df["total"].max()

label_contamination = Label(
    x=contamination_date,
    y=max_cases * 0.95,
    text="Source Identified",
    text_font_size="20pt",
    text_color="#C0392B",
    text_font_style="bold",
    x_offset=10,
)
p.add_layout(label_contamination)

label_intervention = Label(
    x=intervention_date,
    y=max_cases * 0.85,
    text="Intervention Began",
    text_font_size="20pt",
    text_color="#1A9E76",
    text_font_style="bold",
    x_offset=10,
)
p.add_layout(label_intervention)

# Cumulative line on secondary appearance (same y-axis scaled)
cumulative_max = df["cumulative"].max()
scale_factor = max_cases * 0.8 / cumulative_max
df["cumulative_scaled"] = df["cumulative"] * scale_factor

source_cumulative = ColumnDataSource(
    data={"date": df["date"], "cumulative_scaled": df["cumulative_scaled"], "cumulative": df["cumulative"]}
)

r_cumulative = p.line(
    x="date", y="cumulative_scaled", source=source_cumulative, line_color="#333333", line_width=4, line_alpha=0.7
)
legend_items.append(LegendItem(label=f"Cumulative (total: {int(cumulative_max):,})", renderers=[r_cumulative]))

# Legend
legend = Legend(
    items=legend_items,
    location="top_right",
    label_text_font_size="22pt",
    label_text_color="#333333",
    glyph_width=50,
    glyph_height=30,
    spacing=14,
    padding=20,
    background_fill_alpha=0.8,
    background_fill_color="white",
    border_line_color="#CCCCCC",
    border_line_alpha=0.5,
)
p.add_layout(legend, "center")

# Typography
p.title.text_font_size = "36pt"
p.title.text_color = "#222222"
p.title.text_font_style = "bold"
p.xaxis.axis_label_text_font_size = "26pt"
p.yaxis.axis_label_text_font_size = "26pt"
p.xaxis.axis_label_text_color = "#444444"
p.yaxis.axis_label_text_color = "#444444"
p.xaxis.major_label_text_font_size = "20pt"
p.yaxis.major_label_text_font_size = "20pt"
p.xaxis.major_label_text_color = "#555555"
p.yaxis.major_label_text_color = "#555555"

# Format y-axis
p.yaxis.formatter = NumeralTickFormatter(format="0,0")

# Grid
p.xgrid.visible = False
p.ygrid.grid_line_alpha = 0.15
p.ygrid.grid_line_color = "#CCCCCC"
p.ygrid.grid_line_width = 1

# Clean frame
p.outline_line_color = None
p.background_fill_color = "white"
p.border_fill_color = "white"
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.axis_line_color = "#AAAAAA"
p.yaxis.axis_line_color = "#AAAAAA"
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.major_tick_line_color = "#AAAAAA"
p.yaxis.major_tick_line_color = "#AAAAAA"

# Axis range
p.y_range.start = 0
p.y_range.end = max_cases * 1.15

# Margins
p.min_border_left = 140
p.min_border_right = 60
p.min_border_bottom = 110
p.min_border_top = 80

# Save
export_png(p, filename="plot.png")
output_file("plot.html", title="histogram-epidemic · bokeh · pyplots.ai")
save(p)
