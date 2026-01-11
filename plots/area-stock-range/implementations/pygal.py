""" pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-11
"""

import datetime
import io

import numpy as np
import pygal
from PIL import Image, ImageDraw
from pygal.style import Style


# Data - Generate realistic stock price data over 2 years
np.random.seed(42)

# Generate business days without pandas
start_date = datetime.date(2024, 1, 1)
dates = []
current = start_date
while len(dates) < 500:
    if current.weekday() < 5:  # Monday to Friday
        dates.append(current)
    current += datetime.timedelta(days=1)

# Generate realistic stock price using random walk
initial_price = 150.0
returns = np.random.normal(0.0005, 0.02, len(dates))
prices = initial_price * np.cumprod(1 + returns)
prices_list = list(prices)

# Calculate range indices for buttons
total_days = len(dates)
today_idx = total_days - 1

# YTD - find first date of 2025
ytd_start = 0
for i, d in enumerate(dates):
    if d.year == 2025:
        ytd_start = i
        break

range_presets = {
    "1M": max(0, today_idx - 21),
    "3M": max(0, today_idx - 63),
    "6M": max(0, today_idx - 126),
    "1Y": max(0, today_idx - 252),
    "YTD": ytd_start,
    "All": 0,
}

# Currently selected range (1Y for a good visual demonstration)
selected_range = "1Y"
selected_start = range_presets[selected_range]

# Filter data to selected range for main chart
filtered_dates = dates[selected_start:]
filtered_prices = prices_list[selected_start:]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=32,
    opacity=0.4,
    opacity_hover=0.7,
    stroke_width=4,
)

# Create x-axis labels for filtered data - show fewer labels to avoid overlap
x_labels = []
label_interval = 45  # Show label every ~45 data points (roughly every 2 months)
for i, d in enumerate(filtered_dates):
    if i % label_interval == 0:
        x_labels.append(d.strftime("%b %Y"))
    else:
        x_labels.append("")

# Create main chart
main_chart = pygal.Line(
    width=4800,
    height=1900,
    title="area-stock-range · pygal · pyplots.ai",
    x_title="Date",
    y_title="Price (USD)",
    style=custom_style,
    fill=True,
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=35,
    truncate_label=-1,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=1,
    legend_box_size=28,
    show_minor_x_labels=False,
    stroke_style={"width": 4, "linecap": "round", "linejoin": "round"},
    margin=80,
    margin_top=150,
    margin_bottom=200,
    spacing=30,
)

main_chart.x_labels = x_labels
main_chart.add("Stock Price (1Y view)", filtered_prices)

# Mini chart style for range navigator
mini_style = Style(
    background="#fafafa",
    plot_background="#f0f0f0",
    foreground="#555555",
    foreground_strong="#555555",
    foreground_subtle="#888888",
    colors=("#306998",),
    title_font_size=44,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=0,
    value_font_size=0,
    opacity=0.6,
    stroke_width=3,
)

# Create mini chart showing full range
mini_chart = pygal.Line(
    width=4800,
    height=500,
    title="Range Navigator — Full History",
    style=mini_style,
    fill=True,
    show_dots=False,
    show_x_guides=False,
    show_y_guides=False,
    show_legend=False,
    show_x_labels=True,
    show_y_labels=False,
    x_label_rotation=0,
    margin=60,
    margin_top=90,
    margin_bottom=70,
    spacing=15,
)

# Sparse labels for mini chart - quarterly
mini_labels = []
for i, d in enumerate(dates):
    if i % 63 == 0:  # Every ~3 months
        mini_labels.append(d.strftime("%b '%y"))
    else:
        mini_labels.append("")

mini_chart.x_labels = mini_labels
mini_chart.add("", prices_list)

# Render both charts to PNG bytes
main_png = main_chart.render_to_png()
mini_png = mini_chart.render_to_png()

# Load as PIL images
main_img = Image.open(io.BytesIO(main_png))
mini_img = Image.open(io.BytesIO(mini_png))

# Create combined image (4800 x 2700)
combined = Image.new("RGB", (4800, 2700), "white")
combined.paste(main_img, (0, 0))

# Add range selector buttons area
draw = ImageDraw.Draw(combined)

# Draw range button bar between main chart and mini chart
button_bar_y = 1920
button_bar_height = 100

# Draw button background
draw.rectangle([100, button_bar_y, 4700, button_bar_y + button_bar_height], fill="#f5f5f5", outline="#dddddd", width=2)

# Draw range buttons
button_labels = ["1M", "3M", "6M", "1Y", "YTD", "All"]
button_width = 200
button_height = 70
button_spacing = 30
start_x = 200

for i, label in enumerate(button_labels):
    x = start_x + i * (button_width + button_spacing)
    y = button_bar_y + 15
    is_selected = label == selected_range

    if is_selected:
        draw.rectangle([x, y, x + button_width, y + button_height], fill="#306998", outline="#306998", width=2)
        text_color = "white"
    else:
        draw.rectangle([x, y, x + button_width, y + button_height], fill="white", outline="#306998", width=2)
        text_color = "#306998"

    # Center text in button (approximate)
    text_x = x + button_width // 2 - len(label) * 12
    text_y = y + 15
    draw.text((text_x, text_y), label, fill=text_color)

# Add "Range:" label
draw.text((110, button_bar_y + 30), "Range:", fill="#333333")

# Paste mini chart below button bar
mini_y = button_bar_y + button_bar_height + 30
combined.paste(mini_img, (0, mini_y))

# Draw range indicator on mini chart
chart_left_margin = 140
chart_right_margin = 140
chart_width = 4800 - chart_left_margin - chart_right_margin
indicator_start_pct = selected_start / total_days
indicator_width_pct = (total_days - selected_start) / total_days

indicator_left = int(chart_left_margin + indicator_start_pct * chart_width)
indicator_width = int(indicator_width_pct * chart_width)
indicator_top = mini_y + 100
indicator_bottom = mini_y + 420

# Create overlay with transparency
overlay = Image.new("RGBA", combined.size, (255, 255, 255, 0))
overlay_draw = ImageDraw.Draw(overlay)
overlay_draw.rectangle(
    [indicator_left, indicator_top, indicator_left + indicator_width, indicator_bottom],
    fill=(48, 105, 152, 50),
    outline=(48, 105, 152, 200),
    width=4,
)

# Composite the overlay onto combined image
combined = combined.convert("RGBA")
combined = Image.alpha_composite(combined, overlay)
combined = combined.convert("RGB")

# Save final PNG
combined.save("plot.png", "PNG")

# Create interactive HTML
main_svg = main_chart.render().decode("utf-8")
mini_svg = mini_chart.render().decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>area-stock-range · pygal · pyplots.ai</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: white;
            padding: 20px;
        }}
        .container {{ max-width: 4800px; margin: 0 auto; }}
        .range-selector {{
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 8px;
            align-items: center;
        }}
        .range-selector label {{
            font-size: 32px;
            font-weight: 600;
            color: #333;
            margin-right: 20px;
        }}
        .range-btn {{
            padding: 16px 32px;
            font-size: 28px;
            font-weight: 500;
            border: 2px solid #306998;
            background: white;
            color: #306998;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .range-btn:hover {{ background: #e8f0f7; }}
        .range-btn.active {{ background: #306998; color: white; }}
        .chart {{ border: 1px solid #eee; border-radius: 8px; overflow: hidden; margin-bottom: 20px; }}
        .chart svg {{ display: block; width: 100%; height: auto; }}
        .mini-container {{
            background: #fafafa;
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 15px;
        }}
        .mini-label {{ font-size: 24px; color: #666; margin-bottom: 10px; }}
        .mini-chart {{ position: relative; }}
        .mini-chart svg {{ display: block; width: 100%; height: auto; }}
        .range-indicator {{
            position: absolute;
            top: 0;
            height: 100%;
            background: rgba(48, 105, 152, 0.15);
            border-left: 3px solid #306998;
            border-right: 3px solid #306998;
            pointer-events: none;
            transition: left 0.3s ease, width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="range-selector">
            <label>Range:</label>
            <button class="range-btn" data-range="1M">1M</button>
            <button class="range-btn" data-range="3M">3M</button>
            <button class="range-btn" data-range="6M">6M</button>
            <button class="range-btn active" data-range="1Y">1Y</button>
            <button class="range-btn" data-range="YTD">YTD</button>
            <button class="range-btn" data-range="All">All</button>
        </div>
        <div class="chart" id="mainChart">{main_svg}</div>
        <div class="mini-container">
            <div class="mini-label">Full Date Range (Click buttons above to select range)</div>
            <div class="mini-chart" id="miniChart">
                {mini_svg}
                <div class="range-indicator" id="rangeIndicator"></div>
            </div>
        </div>
    </div>
    <script>
        const rangePresets = {str(range_presets).replace("'", '"')};
        const totalPoints = {total_days};
        function updateRangeIndicator(startIdx) {{
            const indicator = document.getElementById('rangeIndicator');
            const startPercent = (startIdx / totalPoints) * 100;
            const widthPercent = ((totalPoints - startIdx) / totalPoints) * 100;
            indicator.style.left = startPercent + '%';
            indicator.style.width = widthPercent + '%';
        }}
        document.querySelectorAll('.range-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const range = this.dataset.range;
                const startIdx = rangePresets[range];
                updateRangeIndicator(startIdx);
            }});
        }});
        updateRangeIndicator(rangePresets['1Y']);
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
