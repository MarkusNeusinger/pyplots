"""pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import pygal
from pygal.style import Style


# Custom style for both charts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=(
        "#306998",
        "#FFD43B",
        "#4B8BBE",
        "#FFE873",
        "#646464",
        "#8EC07C",
        "#D65D0E",
        "#83A598",
        "#B16286",
        "#689D6A",
        "#458588",
        "#CC241D",
    ),
    title_font_size=48,
    label_font_size=24,
    major_label_font_size=22,
    legend_font_size=22,
    value_font_size=18,
    tooltip_font_size=20,
    stroke_width=2,
)

# Sample hierarchical data: Company budget allocation
# Structure: (label, value, parent_category)
budget_data = {
    "Engineering": {"Frontend": 450000, "Backend": 520000, "DevOps": 280000, "QA": 180000},
    "Marketing": {"Digital": 320000, "Brand": 180000, "Events": 150000},
    "Operations": {"HR": 220000, "Finance": 190000, "Legal": 160000, "Facilities": 130000},
    "Product": {"Research": 280000, "Design": 210000, "Analytics": 170000},
}

# Calculate totals for each department
department_totals = {dept: sum(items.values()) for dept, items in budget_data.items()}

# Create Treemap chart
treemap = pygal.Treemap(
    width=4800,
    height=2700,
    style=custom_style,
    title="Company Budget Allocation · hierarchy-toggle-view · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    margin=50,
    spacing=5,
    tooltip_border_radius=10,
)

# Add data to treemap - each department as a series with sub-items
for dept, items in budget_data.items():
    treemap.add(dept, [{"value": v, "label": k} for k, v in items.items()])

# Create Pie chart (sunburst approximation - showing department breakdown)
pie = pygal.Pie(
    width=4800,
    height=2700,
    style=custom_style,
    title="Company Budget Allocation · hierarchy-toggle-view · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    margin=50,
    inner_radius=0.3,
    tooltip_border_radius=10,
)

# Add department totals to pie chart with sub-item details in labels
for dept, items in budget_data.items():
    total = department_totals[dept]
    details = ", ".join([f"{k}: ${v / 1000:.0f}K" for k, v in items.items()])
    pie.add(
        f"{dept} (${total / 1000:.0f}K)", [{"value": v, "label": f"{k}: ${v / 1000:.0f}K"} for k, v in items.items()]
    )

# Render both charts as SVG strings
treemap_svg = treemap.render(is_unicode=True)
pie_svg = pie.render(is_unicode=True)

# Create HTML with toggle functionality
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hierarchy Toggle View - pygal</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .toggle-container {{
            margin: 20px 0;
            display: flex;
            gap: 10px;
            background: white;
            padding: 10px 20px;
            border-radius: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .toggle-btn {{
            padding: 12px 30px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #e0e0e0;
            color: #333;
        }}
        .toggle-btn.active {{
            background: #306998;
            color: white;
        }}
        .toggle-btn:hover:not(.active) {{
            background: #d0d0d0;
        }}
        .chart-container {{
            width: 100%;
            max-width: 1600px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        .chart {{
            display: none;
            width: 100%;
        }}
        .chart.active {{
            display: block;
        }}
        .chart svg {{
            width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="toggle-container">
        <button class="toggle-btn active" onclick="showChart('treemap', this)">Treemap View</button>
        <button class="toggle-btn" onclick="showChart('pie', this)">Sunburst View</button>
    </div>
    <div class="chart-container">
        <div id="treemap" class="chart active">
            {treemap_svg}
        </div>
        <div id="pie" class="chart">
            {pie_svg}
        </div>
    </div>
    <script>
        function showChart(chartId, btn) {{
            // Hide all charts
            document.querySelectorAll('.chart').forEach(c => c.classList.remove('active'));
            // Show selected chart
            document.getElementById(chartId).classList.add('active');
            // Update button states
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}
    </script>
</body>
</html>
"""

# Save HTML file
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Save PNG (treemap as the default static view)
treemap.render_to_png("plot.png")
