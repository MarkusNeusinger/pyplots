""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: pygal 3.1.0 | Python 3.13.11
Quality: 45/100 | Created: 2026-01-11
"""

import io

import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Hierarchical data: Technology company budget allocation
hierarchy_data = [
    {"id": "root", "parent": "", "label": "Company", "value": 0},
    # Level 1: Main departments
    {"id": "eng", "parent": "root", "label": "Engineering", "value": 0},
    {"id": "sales", "parent": "root", "label": "Sales", "value": 0},
    {"id": "ops", "parent": "root", "label": "Operations", "value": 0},
    {"id": "hr", "parent": "root", "label": "HR", "value": 0},
    # Level 2: Engineering sub-departments
    {"id": "frontend", "parent": "eng", "label": "Frontend", "value": 45},
    {"id": "backend", "parent": "eng", "label": "Backend", "value": 55},
    {"id": "devops", "parent": "eng", "label": "DevOps", "value": 30},
    {"id": "qa", "parent": "eng", "label": "QA", "value": 25},
    # Level 2: Sales sub-departments
    {"id": "domestic", "parent": "sales", "label": "Domestic", "value": 40},
    {"id": "intl", "parent": "sales", "label": "International", "value": 50},
    {"id": "partners", "parent": "sales", "label": "Partners", "value": 25},
    # Level 2: Operations sub-departments
    {"id": "logistics", "parent": "ops", "label": "Logistics", "value": 35},
    {"id": "facilities", "parent": "ops", "label": "Facilities", "value": 20},
    {"id": "it", "parent": "ops", "label": "IT Support", "value": 25},
    # Level 2: HR sub-departments
    {"id": "recruiting", "parent": "hr", "label": "Recruiting", "value": 30},
    {"id": "training", "parent": "hr", "label": "Training", "value": 20},
    {"id": "benefits", "parent": "hr", "label": "Benefits", "value": 15},
]

# Build hierarchy lookup
nodes = {d["id"]: d for d in hierarchy_data}
children = {}
for d in hierarchy_data:
    p = d["parent"]
    if p:
        if p not in children:
            children[p] = []
        children[p].append(d["id"])

# Calculate parent values as sum of children
level1_ids = ["eng", "sales", "ops", "hr"]
for nid in level1_ids:
    total = sum(nodes[cid]["value"] for cid in children.get(nid, []))
    nodes[nid]["value"] = total

total_value = sum(nodes[nid]["value"] for nid in level1_ids)
nodes["root"]["value"] = total_value

# Color mapping (colorblind-safe, Python palette)
dept_colors = {
    "eng": "#306998",  # Python Blue
    "sales": "#FFD43B",  # Python Yellow
    "ops": "#2E8B57",  # Sea Green
    "hr": "#E07B39",  # Burnt Orange
}

# Assign colors to children (same as parent)
node_colors = {"root": "#CCCCCC"}
for dept_id, color in dept_colors.items():
    node_colors[dept_id] = color
    for cid in children.get(dept_id, []):
        node_colors[cid] = color

# Custom style for pygal charts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(dept_colors["eng"], dept_colors["sales"], dept_colors["ops"], dept_colors["hr"]),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=22,
    value_label_font_size=22,
    tooltip_font_size=22,
)

# ============ TREEMAP ============
# Prepare treemap data
treemap_data = {}
for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_children = {}
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        dept_children[child_label] = child_value
    treemap_data[dept_label] = dept_children

# Create treemap chart
treemap = pygal.Treemap(
    width=2200,
    height=2200,
    style=custom_style,
    title="Treemap View",
    print_values=True,
    print_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
)

# Add data to treemap
for dept_label, dept_children in treemap_data.items():
    treemap.add(dept_label, dept_children)

# Render treemap to PNG bytes
treemap_png = treemap.render_to_png()
treemap_img = Image.open(io.BytesIO(treemap_png))

# ============ SUNBURST (as nested pie/donut) ============
# Pygal doesn't have native sunburst, so we create a donut chart showing hierarchy
# Inner ring: departments, outer values shown in legend

# Create a pie chart for the sunburst approximation
# We'll show department proportions with sub-department details in tooltips

sunburst_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(dept_colors["eng"], dept_colors["sales"], dept_colors["ops"], dept_colors["hr"]),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=22,
    value_label_font_size=22,
    tooltip_font_size=22,
)

# Create a donut chart (pie with inner_radius) for sunburst-like appearance
sunburst = pygal.Pie(
    width=2200,
    height=2200,
    style=sunburst_style,
    title="Sunburst View",
    inner_radius=0.4,
    print_values=True,
    print_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
)

# Add department data with sub-department breakdown in label
for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_value = nodes[dept_id]["value"]
    # Build tooltip with children info
    child_info = []
    for cid in children.get(dept_id, []):
        child_info.append(f"{nodes[cid]['label']}: {nodes[cid]['value']}")
    tooltip = f"{dept_label} (${dept_value}M)\n" + ", ".join(child_info)
    sunburst.add(dept_label, [{"value": dept_value, "label": tooltip}])

# Render sunburst to PNG bytes
sunburst_png = sunburst.render_to_png()
sunburst_img = Image.open(io.BytesIO(sunburst_png))

# ============ COMBINE INTO FINAL IMAGE ============
# Target size: 4800 x 2700 (16:9)
final_width = 4800
final_height = 2700

# Create the final image
final_img = Image.new("RGB", (final_width, final_height), "white")

# Resize both charts to fit side by side
chart_width = 2200
chart_height = 2200

# Calculate positions (centered vertically, side by side horizontally)
left_x = 100
right_x = final_width - chart_width - 100
top_y = (final_height - chart_height - 200) // 2 + 150

# Resize images if needed
treemap_resized = treemap_img.resize((chart_width, chart_height), Image.Resampling.LANCZOS)
sunburst_resized = sunburst_img.resize((chart_width, chart_height), Image.Resampling.LANCZOS)

# Paste charts onto final image
final_img.paste(treemap_resized, (left_x, top_y))
final_img.paste(sunburst_resized, (right_x, top_y))

# Add main title and toggle UI using PIL
draw = ImageDraw.Draw(final_img)

# Try to use a good font, fall back to default
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    toggle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    toggle_font = ImageFont.load_default()

# Main title
title_text = "hierarchy-toggle-view \u00b7 pygal \u00b7 pyplots.ai"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (final_width - title_width) // 2
draw.text((title_x, 30), title_text, fill="#306998", font=title_font)

# Subtitle
subtitle_text = "Technology Company Budget Allocation"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (final_width - subtitle_width) // 2
draw.text((subtitle_x, 110), subtitle_text, fill="#666666", font=subtitle_font)

# Toggle switch visualization
toggle_y = 180
toggle_width = 400
toggle_height = 60
toggle_x = (final_width - toggle_width) // 2

# Toggle background
draw.rounded_rectangle(
    [toggle_x, toggle_y, toggle_x + toggle_width, toggle_y + toggle_height],
    radius=30,
    fill="#E8E8E8",
    outline="#CCCCCC",
    width=2,
)

# Toggle label
toggle_label = "Toggle View:"
label_bbox = draw.textbbox((0, 0), toggle_label, font=toggle_font)
label_width = label_bbox[2] - label_bbox[0]
draw.text((toggle_x - label_width - 20, toggle_y + 10), toggle_label, fill="#333333", font=toggle_font)

# Left button (Treemap - selected)
btn_width = toggle_width // 2 - 10
draw.rounded_rectangle(
    [toggle_x + 5, toggle_y + 5, toggle_x + btn_width, toggle_y + toggle_height - 5],
    radius=25,
    fill="#306998",
    outline="#1d4a6e",
    width=2,
)
treemap_btn_text = "Treemap"
btn_text_bbox = draw.textbbox((0, 0), treemap_btn_text, font=toggle_font)
btn_text_width = btn_text_bbox[2] - btn_text_bbox[0]
draw.text(
    (toggle_x + btn_width // 2 - btn_text_width // 2, toggle_y + 12), treemap_btn_text, fill="white", font=toggle_font
)

# Right button (Sunburst - unselected)
draw.rounded_rectangle(
    [toggle_x + btn_width + 15, toggle_y + 5, toggle_x + toggle_width - 5, toggle_y + toggle_height - 5],
    radius=25,
    fill="white",
    outline="#BBBBBB",
    width=2,
)
sunburst_btn_text = "Sunburst"
btn_text_bbox = draw.textbbox((0, 0), sunburst_btn_text, font=toggle_font)
btn_text_width = btn_text_bbox[2] - btn_text_bbox[0]
draw.text(
    (toggle_x + btn_width + 15 + btn_width // 2 - btn_text_width // 2, toggle_y + 12),
    sunburst_btn_text,
    fill="#666666",
    font=toggle_font,
)

# Save final composite image
final_img.save("plot.png", "PNG")

# Also save interactive HTML with both charts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>hierarchy-toggle-view - pygal - pyplots.ai</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: white;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #306998;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #666;
            font-weight: normal;
            margin-top: 0;
        }}
        .toggle-container {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 20px 0;
        }}
        .toggle-label {{
            font-weight: bold;
            color: #333;
        }}
        .toggle-switch {{
            display: flex;
            background: #E8E8E8;
            border-radius: 30px;
            padding: 5px;
            gap: 5px;
        }}
        .toggle-btn {{
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            border: 2px solid transparent;
            transition: all 0.3s;
        }}
        .toggle-btn.active {{
            background: #306998;
            color: white;
            border-color: #1d4a6e;
        }}
        .toggle-btn:not(.active) {{
            background: white;
            color: #666;
            border-color: #BBB;
        }}
        .toggle-btn:not(.active):hover {{
            background: #f0f0f0;
        }}
        .charts-container {{
            display: flex;
            gap: 40px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .chart {{
            transition: opacity 0.3s, transform 0.3s;
        }}
        .chart.hidden {{
            display: none;
        }}
        .chart-wrapper {{
            text-align: center;
        }}
        .chart-title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>hierarchy-toggle-view &middot; pygal &middot; pyplots.ai</h1>
    <h2>Technology Company Budget Allocation</h2>

    <div class="toggle-container">
        <span class="toggle-label">Toggle View:</span>
        <div class="toggle-switch">
            <div class="toggle-btn active" onclick="showView('treemap')">Treemap</div>
            <div class="toggle-btn" onclick="showView('sunburst')">Sunburst</div>
        </div>
    </div>

    <div class="charts-container">
        <div class="chart-wrapper" id="treemap-wrapper">
            <div class="chart-title">Treemap View</div>
            <div class="chart" id="treemap-chart">
                {treemap.render(is_unicode=True)}
            </div>
        </div>
        <div class="chart-wrapper hidden" id="sunburst-wrapper">
            <div class="chart-title">Sunburst View</div>
            <div class="chart" id="sunburst-chart">
                {sunburst.render(is_unicode=True)}
            </div>
        </div>
    </div>

    <script>
        function showView(view) {{
            const treemapWrapper = document.getElementById('treemap-wrapper');
            const sunburstWrapper = document.getElementById('sunburst-wrapper');
            const buttons = document.querySelectorAll('.toggle-btn');

            if (view === 'treemap') {{
                treemapWrapper.classList.remove('hidden');
                sunburstWrapper.classList.add('hidden');
                buttons[0].classList.add('active');
                buttons[1].classList.remove('active');
            }} else {{
                treemapWrapper.classList.add('hidden');
                sunburstWrapper.classList.remove('hidden');
                buttons[0].classList.remove('active');
                buttons[1].classList.add('active');
            }}
        }}
    </script>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
