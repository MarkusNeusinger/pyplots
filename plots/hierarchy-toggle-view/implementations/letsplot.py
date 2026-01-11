"""pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-01-11
"""

import json
import math

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_blank,
    element_text,
    geom_polygon,
    geom_rect,
    geom_text,
    gggrid,
    ggplot,
    ggsize,
    labs,
    scale_fill_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_void,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

np.random.seed(42)

# Hierarchical data - Company budget allocation
# Structure follows spec: id, parent, label, value
hierarchy_data = {
    "root": {"id": "root", "parent": None, "label": "Company", "value": 0},
    # Level 1 - Departments
    "engineering": {"id": "engineering", "parent": "root", "label": "Engineering", "value": 450},
    "sales": {"id": "sales", "parent": "root", "label": "Sales", "value": 380},
    "marketing": {"id": "marketing", "parent": "root", "label": "Marketing", "value": 220},
    "operations": {"id": "operations", "parent": "root", "label": "Operations", "value": 150},
    # Level 2 - Engineering teams
    "eng_backend": {"id": "eng_backend", "parent": "engineering", "label": "Backend", "value": 180},
    "eng_frontend": {"id": "eng_frontend", "parent": "engineering", "label": "Frontend", "value": 150},
    "eng_devops": {"id": "eng_devops", "parent": "engineering", "label": "DevOps", "value": 120},
    # Level 2 - Sales teams
    "sales_north": {"id": "sales_north", "parent": "sales", "label": "North", "value": 160},
    "sales_south": {"id": "sales_south", "parent": "sales", "label": "South", "value": 120},
    "sales_east": {"id": "sales_east", "parent": "sales", "label": "East", "value": 100},
    # Level 2 - Marketing teams
    "mkt_digital": {"id": "mkt_digital", "parent": "marketing", "label": "Digital", "value": 130},
    "mkt_brand": {"id": "mkt_brand", "parent": "marketing", "label": "Brand", "value": 90},
    # Level 2 - Operations teams
    "ops_facilities": {"id": "ops_facilities", "parent": "operations", "label": "Facilities", "value": 85},
    "ops_logistics": {"id": "ops_logistics", "parent": "operations", "label": "Logistics", "value": 65},
    # Level 3 - Engineering Backend projects
    "api_core": {"id": "api_core", "parent": "eng_backend", "label": "API Core", "value": 100},
    "api_analytics": {"id": "api_analytics", "parent": "eng_backend", "label": "Analytics", "value": 80},
    # Level 3 - Engineering Frontend projects
    "webapp": {"id": "webapp", "parent": "eng_frontend", "label": "Web App", "value": 90},
    "mobile": {"id": "mobile", "parent": "eng_frontend", "label": "Mobile", "value": 60},
    # Level 3 - Engineering DevOps projects
    "infra": {"id": "infra", "parent": "eng_devops", "label": "Infra", "value": 70},
    "monitoring": {"id": "monitoring", "parent": "eng_devops", "label": "Monitoring", "value": 50},
}

# Color palette - consistent across both views
colors = {
    "Engineering": "#306998",
    "Sales": "#FFD43B",
    "Marketing": "#4CAF50",
    "Operations": "#E07A5F",
    # Sub-colors for Engineering (blue shades)
    "Backend": "#4A8BBE",
    "Frontend": "#6BA3D6",
    "DevOps": "#8CBBEE",
    "API Core": "#A3CCF4",
    "Analytics": "#B8D9F9",
    "Web App": "#8CBBEE",
    "Mobile": "#A3CCF4",
    "Infra": "#A3CCF4",
    "Monitoring": "#B8D9F9",
    # Sub-colors for Sales (yellow shades)
    "North": "#F5C800",
    "South": "#E6BE35",
    "East": "#D4A72C",
    # Sub-colors for Marketing (green shades)
    "Digital": "#66BB6A",
    "Brand": "#81C784",
    # Sub-colors for Operations (coral shades)
    "Facilities": "#EF9A9A",
    "Logistics": "#F48FB1",
}


# Get leaf nodes (nodes with no children)
def get_leaves(data):
    """Get all leaf nodes (nodes with no children)."""
    all_ids = set(data.keys())
    parents = {d["parent"] for d in data.values() if d["parent"]}
    leaves = all_ids - parents - {"root"}
    return [data[leaf_id] for leaf_id in leaves]


leaves = get_leaves(hierarchy_data)
leaves_df = pd.DataFrame(leaves)
leaves_df = leaves_df.sort_values("value", ascending=False).reset_index(drop=True)
total_value = leaves_df["value"].sum()


# Squarify algorithm for treemap layout
def squarify(values, x, y, width, height):
    """Compute treemap rectangles using squarify algorithm."""
    if len(values) == 0:
        return []

    total = sum(values)
    if total == 0:
        return []

    rects = []
    remaining_values = list(values)
    remaining_x, remaining_y = x, y
    remaining_w, remaining_h = width, height

    while remaining_values:
        if remaining_w >= remaining_h:
            row_values = []
            row_sum = 0
            best_ratio = float("inf")

            for v in remaining_values:
                test_values = row_values + [v]
                test_sum = row_sum + v
                row_width = (test_sum / total) * width if total > 0 else 0

                if row_width > 0:
                    worst_ratio = 0
                    for rv in test_values:
                        rect_height = (rv / test_sum) * remaining_h if test_sum > 0 else 0
                        ratio = (
                            max(row_width / rect_height, rect_height / row_width) if rect_height > 0 else float("inf")
                        )
                        worst_ratio = max(worst_ratio, ratio)

                    if worst_ratio <= best_ratio:
                        best_ratio = worst_ratio
                        row_values = test_values
                        row_sum = test_sum
                    else:
                        break
                else:
                    row_values = test_values
                    row_sum = test_sum

            row_width = (row_sum / total) * width if total > 0 else 0
            current_y = remaining_y
            for rv in row_values:
                rect_height = (rv / row_sum) * remaining_h if row_sum > 0 else 0
                rects.append((remaining_x, current_y, row_width, rect_height))
                current_y += rect_height

            remaining_x += row_width
            remaining_w -= row_width
            remaining_values = remaining_values[len(row_values) :]
        else:
            col_values = []
            col_sum = 0
            best_ratio = float("inf")

            for v in remaining_values:
                test_values = col_values + [v]
                test_sum = col_sum + v
                col_height = (test_sum / total) * height if total > 0 else 0

                if col_height > 0:
                    worst_ratio = 0
                    for cv in test_values:
                        rect_width = (cv / test_sum) * remaining_w if test_sum > 0 else 0
                        ratio = (
                            max(col_height / rect_width, rect_width / col_height) if rect_width > 0 else float("inf")
                        )
                        worst_ratio = max(worst_ratio, ratio)

                    if worst_ratio <= best_ratio:
                        best_ratio = worst_ratio
                        col_values = test_values
                        col_sum = test_sum
                    else:
                        break
                else:
                    col_values = test_values
                    col_sum = test_sum

            col_height = (col_sum / total) * height if total > 0 else 0
            current_x = remaining_x
            for cv in col_values:
                rect_width = (cv / col_sum) * remaining_w if col_sum > 0 else 0
                rects.append((current_x, remaining_y, rect_width, col_height))
                current_x += rect_width

            remaining_y += col_height
            remaining_h -= col_height
            remaining_values = remaining_values[len(col_values) :]

    return rects


# Build treemap rectangles
rects = squarify(leaves_df["value"].tolist(), 0, 0, 100, 100)
treemap_df = pd.DataFrame(
    {
        "xmin": [r[0] for r in rects],
        "ymin": [r[1] for r in rects],
        "xmax": [r[0] + r[2] for r in rects],
        "ymax": [r[1] + r[3] for r in rects],
        "label": leaves_df["label"].tolist(),
        "value": leaves_df["value"].tolist(),
    }
)
treemap_df["label_x"] = (treemap_df["xmin"] + treemap_df["xmax"]) / 2
treemap_df["label_y"] = (treemap_df["ymin"] + treemap_df["ymax"]) / 2
treemap_df["width"] = treemap_df["xmax"] - treemap_df["xmin"]
treemap_df["height"] = treemap_df["ymax"] - treemap_df["ymin"]


def make_label(row):
    w, h = row["width"], row["height"]
    pct = row["value"] / total_value * 100
    if w > 15 and h > 12:
        return f"{row['label']}\n{pct:.0f}%"
    elif w > 8 and h > 8:
        return f"{pct:.0f}%"
    return ""


treemap_df["display_label"] = treemap_df.apply(make_label, axis=1)

# Get colors for treemap
treemap_colors = [colors.get(label, "#888888") for label in treemap_df["label"]]


# Create treemap plot
treemap_plot = (
    ggplot(treemap_df)
    + geom_rect(
        aes(xmin="xmin", ymin="ymin", xmax="xmax", ymax="ymax", fill="label"), color="white", size=2.5, alpha=0.92
    )
    + geom_text(aes(x="label_x", y="label_y", label="display_label"), size=14, color="white", fontface="bold")
    + scale_fill_manual(values=treemap_colors)
    + labs(title="Treemap View")
    + theme_void()
    + theme(
        plot_title=element_text(size=22, hjust=0.5, face="bold"),
        legend_position="none",
        axis_title=element_blank(),
        axis_text=element_blank(),
    )
    + ggsize(750, 750)
)


# Create sunburst plot
def create_wedge(inner_r, outer_r, start_angle, end_angle, n_points=30):
    """Create polygon points for a wedge (arc segment)."""
    angles_outer = [start_angle + (end_angle - start_angle) * i / n_points for i in range(n_points + 1)]
    angles_inner = angles_outer[::-1]

    x_outer = [outer_r * math.cos(a) for a in angles_outer]
    y_outer = [outer_r * math.sin(a) for a in angles_outer]
    x_inner = [inner_r * math.cos(a) for a in angles_inner]
    y_inner = [inner_r * math.sin(a) for a in angles_inner]

    return x_outer + x_inner, y_outer + y_inner


# Build sunburst from leaves
sunburst_polygons = []
sunburst_labels = []
segment_id = 0

# Ring radii for single-level sunburst of leaf nodes
r_inner, r_outer = 20, 80

# Calculate angles
start_angle = math.pi / 2  # Start at top
for _, row in leaves_df.iterrows():
    pct = row["value"] / total_value
    end_angle = start_angle - pct * 2 * math.pi

    x_pts, y_pts = create_wedge(r_inner, r_outer, end_angle, start_angle)
    for x, y in zip(x_pts, y_pts, strict=True):
        sunburst_polygons.append(
            {"x": x, "y": y, "segment_id": segment_id, "label": row["label"], "color": row["label"]}
        )

    mid_angle = (start_angle + end_angle) / 2
    label_r = (r_inner + r_outer) / 2
    if pct > 0.03:  # Only label segments > 3%
        sunburst_labels.append(
            {"x": label_r * math.cos(mid_angle), "y": label_r * math.sin(mid_angle), "label": row["label"]}
        )

    segment_id += 1
    start_angle = end_angle

sunburst_df = pd.DataFrame(sunburst_polygons)
label_df = pd.DataFrame(sunburst_labels)

# Get colors for sunburst
unique_labels = sunburst_df["label"].unique()
sunburst_colors = [colors.get(lbl, "#888888") for lbl in unique_labels]

sunburst_plot = (
    ggplot(sunburst_df)
    + geom_polygon(aes(x="x", y="y", fill="color", group="segment_id"), color="white", size=1.5, alpha=0.9)
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, size=12, color="#333333", fontface="bold")
    + scale_fill_manual(values=sunburst_colors)
    + coord_fixed(ratio=1)
    + scale_x_continuous(limits=(-100, 100))
    + scale_y_continuous(limits=(-100, 100))
    + labs(title="Sunburst View")
    + ggsize(750, 750)
    + theme(
        plot_title=element_text(size=22, hjust=0.5, face="bold"),
        legend_position="none",
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
    )
)

# Combine both views side by side for static PNG
combined_plot = gggrid([treemap_plot, sunburst_plot], ncol=2)
final_plot = (
    combined_plot
    + ggsize(1600, 900)
    + labs(
        title="hierarchy-toggle-view · letsplot · pyplots.ai",
        subtitle="Company Budget Allocation · Toggle between views in HTML (interactive)",
    )
    + theme(
        plot_title=element_text(size=24, hjust=0.5, face="bold"),
        plot_subtitle=element_text(size=16, hjust=0.5, color="#666666"),
    )
)

# Save static PNG (scale 3 for 4800x2700)
ggsave(final_plot, "plot.png", path=".", scale=3)


# Interactive HTML with toggle functionality
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>hierarchy-toggle-view · letsplot · pyplots.ai</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 900px;
            width: 100%;
        }}
        h1 {{
            color: #333;
            text-align: center;
            font-size: 24px;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: #666;
            text-align: center;
            font-size: 14px;
            margin-bottom: 24px;
        }}
        .toggle-container {{
            display: flex;
            justify-content: center;
            gap: 0;
            margin-bottom: 24px;
        }}
        .toggle-btn {{
            padding: 14px 32px;
            font-size: 16px;
            font-weight: 600;
            border: 2px solid #306998;
            background: white;
            color: #306998;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .toggle-btn:first-child {{
            border-radius: 8px 0 0 8px;
        }}
        .toggle-btn:last-child {{
            border-radius: 0 8px 8px 0;
            border-left: none;
        }}
        .toggle-btn.active {{
            background: #306998;
            color: white;
        }}
        .toggle-btn:hover:not(.active) {{
            background: #f0f4f8;
        }}
        #chart-container {{
            position: relative;
            width: 100%;
            height: 550px;
        }}
        canvas {{
            width: 100%;
            height: 100%;
        }}
        .legend {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            margin-top: 20px;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #333;
        }}
        .legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
        }}
        .view-label {{
            text-align: center;
            color: #306998;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>hierarchy-toggle-view · letsplot · pyplots.ai</h1>
        <p class="subtitle">Company Budget Allocation - Toggle between Treemap and Sunburst views</p>

        <div class="toggle-container">
            <button class="toggle-btn active" id="treemapBtn" onclick="showTreemap()">Treemap</button>
            <button class="toggle-btn" id="sunburstBtn" onclick="showSunburst()">Sunburst</button>
        </div>

        <div class="view-label" id="viewLabel">Treemap View - Areas show relative size</div>

        <div id="chart-container">
            <canvas id="chart-canvas"></canvas>
        </div>

        <div class="legend" id="legend"></div>
    </div>

    <script>
        const hierarchyData = {json.dumps(dict(hierarchy_data.items()))};
        const colorMap = {json.dumps(colors)};

        // Get leaf nodes
        function getLeaves() {{
            const allIds = new Set(Object.keys(hierarchyData));
            const parents = new Set(Object.values(hierarchyData).map(d => d.parent).filter(p => p));
            const leaves = [...allIds].filter(id => !parents.has(id) && id !== 'root');
            return leaves.map(id => hierarchyData[id]).sort((a, b) => b.value - a.value);
        }}

        const leaves = getLeaves();
        const totalValue = leaves.reduce((sum, d) => sum + d.value, 0);

        let currentView = 'treemap';
        const canvas = document.getElementById('chart-canvas');
        const ctx = canvas.getContext('2d');

        function setupCanvas() {{
            const rect = canvas.parentElement.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            canvas.style.width = rect.width + 'px';
            canvas.style.height = rect.height + 'px';
            ctx.scale(dpr, dpr);
        }}

        // Squarify algorithm
        function squarify(values, x, y, width, height) {{
            if (values.length === 0) return [];
            const total = values.reduce((a, b) => a + b, 0);
            if (total === 0) return [];

            const rects = [];
            let remaining = [...values];
            let rx = x, ry = y, rw = width, rh = height;

            while (remaining.length > 0) {{
                if (rw >= rh) {{
                    let row = [], rowSum = 0, bestRatio = Infinity;

                    for (const v of remaining) {{
                        const testRow = [...row, v];
                        const testSum = rowSum + v;
                        const rowWidth = (testSum / total) * width;

                        if (rowWidth > 0) {{
                            let worstRatio = 0;
                            for (const rv of testRow) {{
                                const rectHeight = (rv / testSum) * rh;
                                const ratio = rectHeight > 0 ? Math.max(rowWidth / rectHeight, rectHeight / rowWidth) : Infinity;
                                worstRatio = Math.max(worstRatio, ratio);
                            }}
                            if (worstRatio <= bestRatio) {{
                                bestRatio = worstRatio;
                                row = testRow;
                                rowSum = testSum;
                            }} else break;
                        }} else {{
                            row = testRow;
                            rowSum = testSum;
                        }}
                    }}

                    const rowWidth = (rowSum / total) * width;
                    let cy = ry;
                    for (const rv of row) {{
                        const rectHeight = (rv / rowSum) * rh;
                        rects.push({{x: rx, y: cy, w: rowWidth, h: rectHeight}});
                        cy += rectHeight;
                    }}
                    rx += rowWidth;
                    rw -= rowWidth;
                    remaining = remaining.slice(row.length);
                }} else {{
                    let col = [], colSum = 0, bestRatio = Infinity;

                    for (const v of remaining) {{
                        const testCol = [...col, v];
                        const testSum = colSum + v;
                        const colHeight = (testSum / total) * height;

                        if (colHeight > 0) {{
                            let worstRatio = 0;
                            for (const cv of testCol) {{
                                const rectWidth = (cv / testSum) * rw;
                                const ratio = rectWidth > 0 ? Math.max(colHeight / rectWidth, rectWidth / colHeight) : Infinity;
                                worstRatio = Math.max(worstRatio, ratio);
                            }}
                            if (worstRatio <= bestRatio) {{
                                bestRatio = worstRatio;
                                col = testCol;
                                colSum = testSum;
                            }} else break;
                        }} else {{
                            col = testCol;
                            colSum = testSum;
                        }}
                    }}

                    const colHeight = (colSum / total) * height;
                    let cx = rx;
                    for (const cv of col) {{
                        const rectWidth = (cv / colSum) * rw;
                        rects.push({{x: cx, y: ry, w: rectWidth, h: colHeight}});
                        cx += rectWidth;
                    }}
                    ry += colHeight;
                    rh -= colHeight;
                    remaining = remaining.slice(col.length);
                }}
            }}
            return rects;
        }}

        function drawTreemap() {{
            setupCanvas();
            const rect = canvas.parentElement.getBoundingClientRect();
            const padding = 40;
            const width = rect.width - 2 * padding;
            const height = rect.height - 2 * padding;

            ctx.clearRect(0, 0, rect.width, rect.height);

            const values = leaves.map(d => d.value);
            const rects = squarify(values, padding, padding, width, height);

            rects.forEach((r, i) => {{
                const leaf = leaves[i];
                const color = colorMap[leaf.label] || '#888888';

                ctx.fillStyle = color;
                ctx.fillRect(r.x, r.y, r.w, r.h);
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 3;
                ctx.strokeRect(r.x, r.y, r.w, r.h);

                // Label
                const pct = (leaf.value / totalValue * 100).toFixed(0);
                if (r.w > 60 && r.h > 40) {{
                    ctx.fillStyle = 'white';
                    ctx.font = 'bold 14px -apple-system, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(leaf.label, r.x + r.w/2, r.y + r.h/2 - 10);
                    ctx.font = '12px -apple-system, sans-serif';
                    ctx.fillText(pct + '%', r.x + r.w/2, r.y + r.h/2 + 10);
                }} else if (r.w > 30 && r.h > 25) {{
                    ctx.fillStyle = 'white';
                    ctx.font = 'bold 11px -apple-system, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(pct + '%', r.x + r.w/2, r.y + r.h/2);
                }}
            }});
        }}

        function drawSunburst() {{
            setupCanvas();
            const rect = canvas.parentElement.getBoundingClientRect();
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const outerRadius = Math.min(centerX, centerY) - 50;
            const innerRadius = outerRadius * 0.25;

            ctx.clearRect(0, 0, rect.width, rect.height);

            let startAngle = -Math.PI / 2;

            leaves.forEach((leaf, i) => {{
                const pct = leaf.value / totalValue;
                const endAngle = startAngle + pct * 2 * Math.PI;
                const color = colorMap[leaf.label] || '#888888';

                // Draw arc
                ctx.beginPath();
                ctx.moveTo(centerX + innerRadius * Math.cos(startAngle), centerY + innerRadius * Math.sin(startAngle));
                ctx.arc(centerX, centerY, outerRadius, startAngle, endAngle);
                ctx.lineTo(centerX + innerRadius * Math.cos(endAngle), centerY + innerRadius * Math.sin(endAngle));
                ctx.arc(centerX, centerY, innerRadius, endAngle, startAngle, true);
                ctx.closePath();

                ctx.fillStyle = color;
                ctx.fill();
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Label
                if (pct > 0.03) {{
                    const midAngle = startAngle + (endAngle - startAngle) / 2;
                    const labelR = (innerRadius + outerRadius) / 2;
                    const labelX = centerX + labelR * Math.cos(midAngle);
                    const labelY = centerY + labelR * Math.sin(midAngle);

                    ctx.fillStyle = '#333';
                    ctx.font = 'bold 12px -apple-system, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(leaf.label, labelX, labelY - 8);
                    ctx.font = '11px -apple-system, sans-serif';
                    ctx.fillText((pct * 100).toFixed(0) + '%', labelX, labelY + 8);
                }}

                startAngle = endAngle;
            }});

            // Center text
            ctx.fillStyle = '#333';
            ctx.font = 'bold 16px -apple-system, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Total', centerX, centerY - 10);
            ctx.font = '14px -apple-system, sans-serif';
            ctx.fillText('$' + (totalValue/1000).toFixed(1) + 'M', centerX, centerY + 10);
        }}

        function showTreemap() {{
            currentView = 'treemap';
            document.getElementById('treemapBtn').classList.add('active');
            document.getElementById('sunburstBtn').classList.remove('active');
            document.getElementById('viewLabel').textContent = 'Treemap View - Areas show relative size';
            drawTreemap();
        }}

        function showSunburst() {{
            currentView = 'sunburst';
            document.getElementById('sunburstBtn').classList.add('active');
            document.getElementById('treemapBtn').classList.remove('active');
            document.getElementById('viewLabel').textContent = 'Sunburst View - Radial segments show hierarchy';
            drawSunburst();
        }}

        function updateLegend() {{
            const legend = document.getElementById('legend');
            legend.innerHTML = leaves.map(leaf => {{
                const color = colorMap[leaf.label] || '#888888';
                const pct = (leaf.value / totalValue * 100).toFixed(1);
                return `<div class="legend-item">
                    <div class="legend-color" style="background: ${{color}}"></div>
                    <span>${{leaf.label}} (${{pct}}%)</span>
                </div>`;
            }}).join('');
        }}

        window.addEventListener('resize', () => {{
            if (currentView === 'treemap') drawTreemap();
            else drawSunburst();
        }});

        // Initial render
        updateLegend();
        drawTreemap();
    </script>
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
