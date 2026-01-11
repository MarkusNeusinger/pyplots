"""pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: pygal 3.1.0 | Python 3.13.11
Quality: 45/100 | Created: 2026-01-11
"""

import pygal
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

# Color mapping (colorblind-safe)
dept_colors = {
    "eng": "#306998",  # Python Blue
    "sales": "#FFD43B",  # Python Yellow
    "ops": "#2E8B57",  # Sea Green
    "hr": "#E07B39",  # Burnt Orange
}

# Create style for large canvas
chart_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#555555",
    colors=(dept_colors["eng"], dept_colors["sales"], dept_colors["ops"], dept_colors["hr"]),
    title_font_size=100,
    label_font_size=52,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=48,
    value_label_font_size=48,
    tooltip_font_size=48,
)

# Create Treemap chart for PNG (the "active" toggle state)
# pygal Treemap shows hierarchical data as nested rectangles
treemap = pygal.Treemap(
    width=4800,
    height=2700,
    style=chart_style,
    title="hierarchy-toggle-view · pygal · pyplots.ai",
    print_values=True,
    print_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=30,
    margin_left=100,
    margin_right=100,
    margin_bottom=200,
    margin_top=200,
    truncate_legend=-1,
)

# Add hierarchical data - each department with its sub-departments
for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_values = []
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        dept_values.append({"value": child_value, "label": f"{child_label}: ${child_value}M"})
    treemap.add(f"{dept_label} (${nodes[dept_id]['value']}M)", dept_values)

# Save PNG using pygal's native render_to_png
treemap.render_to_png("plot.png")

# Create interactive HTML version with toggle between Treemap and Sunburst views
# Sunburst style with sub-department colors
sunburst_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#555555",
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
    title_font_size=36,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=18,
    value_font_size=18,
    tooltip_font_size=18,
)

# HTML Treemap (smaller for web)
treemap_html = pygal.Treemap(
    width=900,
    height=600,
    style=Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#555555",
        colors=(dept_colors["eng"], dept_colors["sales"], dept_colors["ops"], dept_colors["hr"]),
        title_font_size=28,
        label_font_size=16,
        major_label_font_size=14,
        legend_font_size=16,
        value_font_size=14,
        tooltip_font_size=14,
    ),
    title="",
    print_values=True,
    print_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    truncate_legend=-1,
)

for dept_id in level1_ids:
    dept_label = nodes[dept_id]["label"]
    dept_values = []
    for cid in children.get(dept_id, []):
        child_label = nodes[cid]["label"]
        child_value = nodes[cid]["value"]
        dept_values.append({"value": child_value, "label": f"{child_label}: ${child_value}M"})
    treemap_html.add(f"{dept_label} (${nodes[dept_id]['value']}M)", dept_values)

# HTML Sunburst (pie with inner radius)
sunburst_html = pygal.Pie(
    width=900,
    height=600,
    style=sunburst_style,
    title="",
    inner_radius=0.35,
    print_values=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    truncate_legend=-1,
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
    <title>hierarchy-toggle-view · pygal · pyplots.ai</title>
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
            padding: 12px 30px;
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
            max-width: 950px;
        }}
        .chart-title {{
            font-size: 22px;
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
        <div class="chart-title">Treemap View - Nested Rectangles by Value</div>
        <div class="chart" id="treemap-chart">
            {treemap_html.render(is_unicode=True)}
        </div>
    </div>
    <div class="chart-wrapper hidden" id="sunburst-wrapper">
        <div class="chart-title">Sunburst View - Radial Hierarchy</div>
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
