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

# ============ TREEMAP-LIKE VIEW ============
# Since pygal Treemap has PNG rendering issues, create a horizontal bar
# chart that shows the hierarchical breakdown visually
treemap_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(dept_colors["eng"], dept_colors["sales"], dept_colors["ops"], dept_colors["hr"]),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=40,
    value_font_size=36,
    value_label_font_size=36,
    tooltip_font_size=36,
)

# Create a horizontal bar chart showing department totals
treemap_chart = pygal.HorizontalBar(
    width=2100,
    height=1600,
    style=treemap_style,
    title="Treemap View",
    print_values=True,
    print_labels=False,
    show_legend=True,
    legend_at_bottom=False,
    margin_left=50,
    margin_right=250,
    margin_bottom=100,
    margin_top=150,
    x_label_rotation=0,
    truncate_legend=-1,
)

# Add each department as a bar
for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_value = nodes[dept_id]["value"]
    treemap_chart.add(dept_label, [{"value": dept_value, "label": f"${dept_value}M"}])

# Render treemap to PNG bytes
treemap_png = treemap_chart.render_to_png()
treemap_img = Image.open(io.BytesIO(treemap_png))

# ============ SUNBURST VIEW (Multi-level Pie) ============
# Create TWO concentric pie charts to show hierarchy:
# Inner ring: departments (larger segments)
# Since pygal doesn't support true nested pies in one chart,
# we'll create an outer pie with sub-departments and larger inner_radius

sunburst_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        # Engineering sub-depts (blues)
        "#306998",
        "#4a8bc2",
        "#6ba8d9",
        "#8cc5f0",
        # Sales sub-depts (yellows)
        "#FFD43B",
        "#ffe066",
        "#ffeb99",
        # Operations sub-depts (greens)
        "#2E8B57",
        "#4aa876",
        "#6bc595",
        # HR sub-depts (oranges)
        "#E07B39",
        "#e8995c",
        "#f0b77f",
    ),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=34,
    legend_font_size=36,
    value_font_size=32,
    value_label_font_size=32,
    tooltip_font_size=32,
)

# Create pie chart showing ALL sub-departments (simulates outer ring of sunburst)
sunburst = pygal.Pie(
    width=2100,
    height=1600,
    style=sunburst_style,
    title="Sunburst View",
    inner_radius=0.35,
    print_values=True,
    print_labels=False,
    show_legend=False,
    margin_left=50,
    margin_right=50,
    margin_bottom=100,
    margin_top=150,
    truncate_legend=-1,
)

# Add all sub-departments grouped by parent color family
for dept_id in level1_ids:
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        sunburst.add(f"{child_label} (${child_value}M)", [child_value])

# Render sunburst to PNG bytes
sunburst_png = sunburst.render_to_png()
sunburst_img = Image.open(io.BytesIO(sunburst_png))

# ============ COMBINE INTO FINAL IMAGE ============
# Target size: 4800 x 2700 (16:9)
final_width = 4800
final_height = 2700

# Create the final image
final_img = Image.new("RGB", (final_width, final_height), "white")

# Chart dimensions - slightly smaller to fit legend
chart_width = 2100
chart_height = 1600

# Calculate positions - place charts side by side with minimal gap
left_x = 150
right_x = final_width - chart_width - 150
top_y = 320  # Below title and toggle, leaving room for legend at bottom

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
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 52)
    toggle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    legend_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    toggle_font = ImageFont.load_default()
    legend_font = ImageFont.load_default()

# Main title
title_text = "hierarchy-toggle-view · pygal · pyplots.ai"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (final_width - title_width) // 2
draw.text((title_x, 40), title_text, fill="#306998", font=title_font)

# Subtitle
subtitle_text = "Technology Company Budget Allocation ($M)"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (final_width - subtitle_width) // 2
draw.text((subtitle_x, 135), subtitle_text, fill="#666666", font=subtitle_font)

# Toggle switch visualization - show BOTH views indicator
toggle_y = 220
toggle_width = 700
toggle_height = 70
toggle_x = (final_width - toggle_width) // 2

# Toggle background
draw.rounded_rectangle(
    [toggle_x, toggle_y, toggle_x + toggle_width, toggle_y + toggle_height],
    radius=35,
    fill="#E8E8E8",
    outline="#CCCCCC",
    width=3,
)

# Toggle label
toggle_label = "Views:"
label_bbox = draw.textbbox((0, 0), toggle_label, font=toggle_font)
label_width = label_bbox[2] - label_bbox[0]
draw.text((toggle_x - label_width - 25, toggle_y + 14), toggle_label, fill="#333333", font=toggle_font)

# Both buttons shown as active to indicate side-by-side view
btn_width = toggle_width // 2 - 15

# Left button (Treemap - selected)
draw.rounded_rectangle(
    [toggle_x + 8, toggle_y + 8, toggle_x + btn_width, toggle_y + toggle_height - 8],
    radius=28,
    fill="#306998",
    outline="#1d4a6e",
    width=2,
)
treemap_btn_text = "Treemap"
btn_text_bbox = draw.textbbox((0, 0), treemap_btn_text, font=toggle_font)
btn_text_width = btn_text_bbox[2] - btn_text_bbox[0]
draw.text(
    (toggle_x + btn_width // 2 - btn_text_width // 2, toggle_y + 15), treemap_btn_text, fill="white", font=toggle_font
)

# Right button (Sunburst - also selected to show both)
draw.rounded_rectangle(
    [toggle_x + btn_width + 22, toggle_y + 8, toggle_x + toggle_width - 8, toggle_y + toggle_height - 8],
    radius=28,
    fill="#306998",
    outline="#1d4a6e",
    width=2,
)
sunburst_btn_text = "Sunburst"
btn_text_bbox = draw.textbbox((0, 0), sunburst_btn_text, font=toggle_font)
btn_text_width = btn_text_bbox[2] - btn_text_bbox[0]
draw.text(
    (toggle_x + btn_width + 22 + btn_width // 2 - btn_text_width // 2, toggle_y + 15),
    sunburst_btn_text,
    fill="white",
    font=toggle_font,
)

# Add comprehensive legend showing department hierarchy
legend_y = final_height - 200
legend_x_start = 200
box_size = 32
col_width = 580

# Draw legend for each department with its sub-departments
for col, dept_id in enumerate(level1_ids):
    x_base = legend_x_start + col * col_width
    color = dept_colors[dept_id]
    dept_label = nodes[dept_id]["label"]
    dept_value = nodes[dept_id]["value"]

    # Department header with color box
    draw.rectangle([x_base, legend_y, x_base + box_size, legend_y + box_size], fill=color, outline="#333333", width=2)
    draw.text(
        (x_base + box_size + 10, legend_y - 2), f"{dept_label} (${dept_value}M)", fill="#333333", font=legend_font
    )

    # Sub-departments
    for j, cid in enumerate(children.get(dept_id, [])):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        y_offset = legend_y + 45 + j * 38
        draw.text((x_base + 20, y_offset), f"• {child_label}: ${child_value}M", fill="#666666", font=legend_font)

# Save final composite image
final_img.save("plot.png", "PNG")

# Also save interactive HTML with toggle between views
# For HTML, we can use proper Treemap since SVG rendering works
treemap_html = pygal.Treemap(
    width=800,
    height=600,
    style=treemap_style,
    title="",
    print_values=True,
    print_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
)

for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_values = []
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        dept_values.append({"value": child_value, "label": f"{child_label}: ${child_value}M"})
    treemap_html.add(dept_label, dept_values)

sunburst_html = pygal.Pie(
    width=800,
    height=600,
    style=sunburst_style,
    title="",
    inner_radius=0.35,
    print_values=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
)

for dept_id in level1_ids:
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        sunburst_html.add(f"{child_label} (${child_value}M)", [child_value])

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
        .chart-wrapper {{
            text-align: center;
            max-width: 900px;
        }}
        .chart-title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .chart {{
            transition: opacity 0.3s;
        }}
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <h1>hierarchy-toggle-view &middot; pygal &middot; pyplots.ai</h1>
    <h2>Technology Company Budget Allocation ($M)</h2>

    <div class="toggle-container">
        <span class="toggle-label">Toggle View:</span>
        <div class="toggle-switch">
            <div class="toggle-btn active" onclick="showView('treemap')">Treemap</div>
            <div class="toggle-btn" onclick="showView('sunburst')">Sunburst</div>
        </div>
    </div>

    <div class="chart-wrapper" id="treemap-wrapper">
        <div class="chart-title">Treemap View</div>
        <div class="chart" id="treemap-chart">
            {treemap_html.render(is_unicode=True)}
        </div>
    </div>
    <div class="chart-wrapper hidden" id="sunburst-wrapper">
        <div class="chart-title">Sunburst View</div>
        <div class="chart" id="sunburst-chart">
            {sunburst_html.render(is_unicode=True)}
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
