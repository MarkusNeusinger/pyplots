""" pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-20
"""

import pygal
from pygal.style import Style
from pygal_maps_world.maps import World


# Hierarchical sales data: World -> Country -> State -> City
# Structure enables drill-down navigation at each level
hierarchy = {
    # Root level - World view
    "world": {"name": "World", "parent": None, "children": ["us", "de", "jp", "br", "au"], "value": None},
    # Level 1 - Countries
    "us": {"name": "United States", "parent": "world", "value": 2100, "children": ["us_ca", "us_tx", "us_ny", "us_fl"]},
    "de": {"name": "Germany", "parent": "world", "value": 580, "children": ["de_by", "de_nw", "de_he"]},
    "jp": {"name": "Japan", "parent": "world", "value": 850, "children": ["jp_13", "jp_27", "jp_23"]},
    "br": {"name": "Brazil", "parent": "world", "value": 520, "children": ["br_sp", "br_rj", "br_mg"]},
    "au": {"name": "Australia", "parent": "world", "value": 380, "children": ["au_nsw", "au_vic", "au_qld"]},
    # Level 2 - US States
    "us_ca": {"name": "California", "parent": "us", "value": 680, "children": ["us_ca_la", "us_ca_sf", "us_ca_sd"]},
    "us_tx": {"name": "Texas", "parent": "us", "value": 520, "children": ["us_tx_hou", "us_tx_dal", "us_tx_aus"]},
    "us_ny": {"name": "New York", "parent": "us", "value": 580, "children": ["us_ny_nyc", "us_ny_buf", "us_ny_alb"]},
    "us_fl": {"name": "Florida", "parent": "us", "value": 320, "children": ["us_fl_mia", "us_fl_orl", "us_fl_tam"]},
    # Level 2 - German States
    "de_by": {"name": "Bavaria", "parent": "de", "value": 210, "children": ["de_by_muc", "de_by_nur"]},
    "de_nw": {"name": "North Rhine-Westphalia", "parent": "de", "value": 240, "children": ["de_nw_col", "de_nw_dus"]},
    "de_he": {"name": "Hesse", "parent": "de", "value": 130, "children": ["de_he_fra", "de_he_wie"]},
    # Level 2 - Japanese Prefectures
    "jp_13": {"name": "Tokyo", "parent": "jp", "value": 420, "children": ["jp_13_shi", "jp_13_min"]},
    "jp_27": {"name": "Osaka", "parent": "jp", "value": 280, "children": ["jp_27_osa", "jp_27_sak"]},
    "jp_23": {"name": "Aichi", "parent": "jp", "value": 150, "children": ["jp_23_nag", "jp_23_toy"]},
    # Level 2 - Brazilian States
    "br_sp": {"name": "Sao Paulo", "parent": "br", "value": 280, "children": ["br_sp_sao", "br_sp_cam"]},
    "br_rj": {"name": "Rio de Janeiro", "parent": "br", "value": 160, "children": ["br_rj_rio", "br_rj_nit"]},
    "br_mg": {"name": "Minas Gerais", "parent": "br", "value": 80, "children": ["br_mg_bho", "br_mg_ube"]},
    # Level 2 - Australian States
    "au_nsw": {"name": "New South Wales", "parent": "au", "value": 180, "children": ["au_nsw_syd", "au_nsw_new"]},
    "au_vic": {"name": "Victoria", "parent": "au", "value": 140, "children": ["au_vic_mel", "au_vic_gee"]},
    "au_qld": {"name": "Queensland", "parent": "au", "value": 60, "children": ["au_qld_bri", "au_qld_gol"]},
    # Level 3 - US Cities (California)
    "us_ca_la": {"name": "Los Angeles", "parent": "us_ca", "value": 320, "children": []},
    "us_ca_sf": {"name": "San Francisco", "parent": "us_ca", "value": 240, "children": []},
    "us_ca_sd": {"name": "San Diego", "parent": "us_ca", "value": 120, "children": []},
    # Level 3 - US Cities (Texas)
    "us_tx_hou": {"name": "Houston", "parent": "us_tx", "value": 220, "children": []},
    "us_tx_dal": {"name": "Dallas", "parent": "us_tx", "value": 180, "children": []},
    "us_tx_aus": {"name": "Austin", "parent": "us_tx", "value": 120, "children": []},
    # Level 3 - US Cities (New York)
    "us_ny_nyc": {"name": "New York City", "parent": "us_ny", "value": 420, "children": []},
    "us_ny_buf": {"name": "Buffalo", "parent": "us_ny", "value": 90, "children": []},
    "us_ny_alb": {"name": "Albany", "parent": "us_ny", "value": 70, "children": []},
    # Level 3 - US Cities (Florida)
    "us_fl_mia": {"name": "Miami", "parent": "us_fl", "value": 140, "children": []},
    "us_fl_orl": {"name": "Orlando", "parent": "us_fl", "value": 100, "children": []},
    "us_fl_tam": {"name": "Tampa", "parent": "us_fl", "value": 80, "children": []},
    # Level 3 - German Cities
    "de_by_muc": {"name": "Munich", "parent": "de_by", "value": 150, "children": []},
    "de_by_nur": {"name": "Nuremberg", "parent": "de_by", "value": 60, "children": []},
    "de_nw_col": {"name": "Cologne", "parent": "de_nw", "value": 130, "children": []},
    "de_nw_dus": {"name": "Dusseldorf", "parent": "de_nw", "value": 110, "children": []},
    "de_he_fra": {"name": "Frankfurt", "parent": "de_he", "value": 90, "children": []},
    "de_he_wie": {"name": "Wiesbaden", "parent": "de_he", "value": 40, "children": []},
    # Level 3 - Japanese Cities
    "jp_13_shi": {"name": "Shibuya", "parent": "jp_13", "value": 280, "children": []},
    "jp_13_min": {"name": "Minato", "parent": "jp_13", "value": 140, "children": []},
    "jp_27_osa": {"name": "Osaka City", "parent": "jp_27", "value": 200, "children": []},
    "jp_27_sak": {"name": "Sakai", "parent": "jp_27", "value": 80, "children": []},
    "jp_23_nag": {"name": "Nagoya", "parent": "jp_23", "value": 100, "children": []},
    "jp_23_toy": {"name": "Toyota", "parent": "jp_23", "value": 50, "children": []},
    # Level 3 - Brazilian Cities
    "br_sp_sao": {"name": "Sao Paulo City", "parent": "br_sp", "value": 220, "children": []},
    "br_sp_cam": {"name": "Campinas", "parent": "br_sp", "value": 60, "children": []},
    "br_rj_rio": {"name": "Rio City", "parent": "br_rj", "value": 120, "children": []},
    "br_rj_nit": {"name": "Niteroi", "parent": "br_rj", "value": 40, "children": []},
    "br_mg_bho": {"name": "Belo Horizonte", "parent": "br_mg", "value": 60, "children": []},
    "br_mg_ube": {"name": "Uberlandia", "parent": "br_mg", "value": 20, "children": []},
    # Level 3 - Australian Cities
    "au_nsw_syd": {"name": "Sydney", "parent": "au_nsw", "value": 140, "children": []},
    "au_nsw_new": {"name": "Newcastle", "parent": "au_nsw", "value": 40, "children": []},
    "au_vic_mel": {"name": "Melbourne", "parent": "au_vic", "value": 110, "children": []},
    "au_vic_gee": {"name": "Geelong", "parent": "au_vic", "value": 30, "children": []},
    "au_qld_bri": {"name": "Brisbane", "parent": "au_qld", "value": 45, "children": []},
    "au_qld_gol": {"name": "Gold Coast", "parent": "au_qld", "value": 15, "children": []},
}

# Colorblind-friendly palette with high contrast (avoiding similar values)
# Using: dark blue, orange, teal, purple (distinct from each other)
COLORS = ("#1B4F72", "#E67E22", "#148F77", "#6C3483", "#922B21", "#1E8449")

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=COLORS,
    title_font_size=64,
    label_font_size=42,
    legend_font_size=38,
    major_label_font_size=38,
    value_font_size=32,
    tooltip_font_size=32,
    no_data_font_size=28,
)


def get_breadcrumb(node_id):
    """Build breadcrumb trail from root to current node."""
    trail = []
    current = node_id
    while current and current in hierarchy:
        trail.insert(0, hierarchy[current]["name"])
        current = hierarchy[current]["parent"]
    return " > ".join(trail)


def create_world_map_svg():
    """Create the world-level map using pygal_maps_world."""
    worldmap = World(
        style=custom_style,
        width=800,
        height=500,
        show_legend=True,
        legend_at_bottom=True,
        legend_at_bottom_columns=5,
        legend_box_size=20,
        print_values=False,
        print_labels=False,
        explicit_size=True,
    )

    # Group countries by sales tier for visual hierarchy
    # Only include countries that have drill-down data
    countries_with_data = {c: hierarchy[c]["value"] for c in hierarchy["world"]["children"]}

    # Add as single series for cleaner legend
    worldmap.add("Sales ($M) - Click to drill down", countries_with_data)

    return worldmap.render(is_unicode=True)


def create_bar_chart_svg(level_id):
    """Create a bar chart for state/city level showing children."""
    level_data = hierarchy[level_id]
    children_ids = level_data.get("children", [])
    if not children_ids:
        return None

    chart = pygal.Bar(
        style=Style(
            background="transparent",
            plot_background="transparent",
            foreground="#333333",
            foreground_strong="#333333",
            foreground_subtle="#666666",
            colors=COLORS,
            title_font_size=20,
            label_font_size=14,
            legend_font_size=14,
            value_font_size=12,
            tooltip_font_size=14,
        ),
        width=800,
        height=450,
        legend_at_bottom=False,
        show_legend=False,
        show_y_guides=True,
        y_title="Sales ($M)",
        print_values=True,
        print_values_position="top",
        value_formatter=lambda x: f"${x}M",
        human_readable=True,
        explicit_size=True,
    )

    names = []
    values = []
    for cid in children_ids:
        child = hierarchy[cid]
        names.append(child["name"])
        values.append(child["value"])

    chart.add("Sales", values)
    chart.x_labels = names

    return chart.render(is_unicode=True)


# Generate world map for PNG output (static preview at root level)
png_map = World(
    style=custom_style,
    width=4800,
    height=2700,
    title="map-drilldown-geographic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=40,
    print_values=False,
    print_labels=False,
    margin=50,
    margin_bottom=180,
)

# Add country data with tier grouping for visual hierarchy
tier1 = {k: hierarchy[k]["value"] for k in ["us"] if k in hierarchy}
tier2 = {k: hierarchy[k]["value"] for k in ["jp"] if k in hierarchy}
tier3 = {k: hierarchy[k]["value"] for k in ["de", "br"] if k in hierarchy}
tier4 = {k: hierarchy[k]["value"] for k in ["au"] if k in hierarchy}

png_map.add("$1B+ (click to drill)", tier1)
png_map.add("$500M-$1B", tier2)
png_map.add("$300M-$500M", tier3)
png_map.add("<$300M", tier4)

# Add subtitle showing breadcrumb
png_map.x_title = "World > Click any country to drill down to states/provinces"

png_map.render_to_png("plot.png")

# Generate SVG charts for all levels
svg_data = {"world": create_world_map_svg()}

# Generate bar charts for all drillable nodes
for node_id, node_data in hierarchy.items():
    if node_id != "world" and node_data.get("children"):
        svg = create_bar_chart_svg(node_id)
        if svg:
            svg_data[node_id] = svg

# Convert hierarchy to JSON for JavaScript
hierarchy_json = (
    str(hierarchy).replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
)

# Build interactive HTML with drill-down functionality
html_content = (
    """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>map-drilldown-geographic · pygal · pyplots.ai</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 950px;
            width: 100%;
        }
        h1 {
            color: #333;
            text-align: center;
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        .breadcrumb {
            background: #1B4F72;
            color: white;
            padding: 14px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .breadcrumb span {
            cursor: pointer;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .breadcrumb span:hover:not(.current):not(.separator) {
            background: rgba(255,255,255,0.2);
            text-decoration: underline;
        }
        .breadcrumb .separator {
            opacity: 0.7;
            cursor: default;
        }
        .breadcrumb .current {
            font-weight: bold;
            cursor: default;
            background: rgba(255,255,255,0.15);
        }
        .back-btn {
            background: #E67E22;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        .back-btn:hover:not(:disabled) {
            background: #D35400;
        }
        .back-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        #chart-container {
            width: 100%;
            min-height: 450px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #chart-container svg {
            max-width: 100%;
            height: auto;
        }
        .hint {
            text-align: center;
            color: #666;
            margin-top: 15px;
            font-size: 14px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        .level-info {
            text-align: center;
            color: #1B4F72;
            font-size: 16px;
            margin-bottom: 15px;
            font-weight: 500;
        }
        /* Make pygal elements interactive */
        .country, .bar, rect.rect {
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .country:hover, .bar:hover, rect.rect:hover {
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>map-drilldown-geographic · pygal · pyplots.ai</h1>
        <div class="breadcrumb">
            <button class="back-btn" id="backBtn" disabled>← Back</button>
            <div id="breadcrumb-path">
                <span class="current">World</span>
            </div>
        </div>
        <div class="level-info" id="level-info">World View - Sales by Country</div>
        <div id="chart-container"></div>
        <p class="hint" id="hint">Click on a country to drill down to states/provinces</p>
    </div>

    <script>
        // Hierarchical data structure
        const hierarchy = """
    + hierarchy_json
    + """;

        // Pre-rendered pygal SVG charts
        const svgCharts = {
"""
)

# Insert SVG data as JavaScript strings
for level_id, svg_content in svg_data.items():
    # Escape backticks and backslashes for JavaScript template literal
    escaped_svg = svg_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    html_content += f'            "{level_id}": `{escaped_svg}`,\n'

html_content += """        };

        let currentLevel = 'world';
        let historyStack = [];

        function getBreadcrumbPath() {
            const path = [];
            let current = currentLevel;
            while (current && hierarchy[current]) {
                path.unshift({ id: current, name: hierarchy[current].name });
                current = hierarchy[current].parent;
            }
            return path;
        }

        function getLevelType(id) {
            const depth = getBreadcrumbPath().length;
            if (id === 'world') return 'World View - Sales by Country';
            if (depth === 2) return 'Country Level - Sales by State/Province';
            if (depth === 3) return 'State Level - Sales by City';
            return 'City Level - Detailed Sales';
        }

        function updateBreadcrumb() {
            const pathDiv = document.getElementById('breadcrumb-path');
            const backBtn = document.getElementById('backBtn');
            const levelInfo = document.getElementById('level-info');

            const path = getBreadcrumbPath();
            let html = '';

            path.forEach((item, index) => {
                if (index > 0) {
                    html += '<span class="separator"> > </span>';
                }
                if (item.id === currentLevel) {
                    html += `<span class="current">${item.name}</span>`;
                } else {
                    html += `<span onclick="navigateTo('${item.id}')">${item.name}</span>`;
                }
            });

            pathDiv.innerHTML = html;
            backBtn.disabled = currentLevel === 'world';
            levelInfo.textContent = getLevelType(currentLevel);
        }

        function renderChart(levelId) {
            const container = document.getElementById('chart-container');
            const hint = document.getElementById('hint');
            const levelData = hierarchy[levelId];

            if (svgCharts[levelId]) {
                container.innerHTML = svgCharts[levelId];

                // Add click handlers based on level type
                if (levelId === 'world') {
                    // For world map, add click handlers to country paths
                    const countries = container.querySelectorAll('.country');
                    countries.forEach(country => {
                        const countryClass = Array.from(country.classList).find(c => c !== 'country' && c !== 'reactive');
                        if (countryClass && hierarchy[countryClass] && hierarchy[countryClass].children.length > 0) {
                            country.style.cursor = 'pointer';
                            country.onclick = () => drillDown(countryClass);
                        }
                    });
                    hint.textContent = 'Click on a highlighted country to drill down to states/provinces';
                } else {
                    // For bar charts, add click handlers to bars
                    const children = levelData.children || [];
                    const bars = container.querySelectorAll('.bar, rect.rect');

                    // Map bars to children
                    let barIndex = 0;
                    bars.forEach((bar) => {
                        if (barIndex < children.length) {
                            const childId = children[barIndex];
                            const childData = hierarchy[childId];

                            if (childData && childData.children && childData.children.length > 0) {
                                bar.style.cursor = 'pointer';
                                bar.onclick = () => drillDown(childId);
                            }
                            barIndex++;
                        }
                    });

                    // Update hint based on whether there are drillable children
                    const hasDrillable = children.some(cid =>
                        hierarchy[cid] && hierarchy[cid].children && hierarchy[cid].children.length > 0
                    );
                    hint.textContent = hasDrillable
                        ? 'Click on a bar to drill down further'
                        : 'Leaf level reached - no further drill-down available';
                }
            } else {
                container.innerHTML = '<p style="text-align:center;color:#666;padding:50px;">No detailed view available</p>';
                hint.textContent = '';
            }
        }

        function drillDown(id) {
            if (!hierarchy[id] || !svgCharts[id]) return;

            historyStack.push(currentLevel);
            currentLevel = id;
            updateBreadcrumb();
            renderChart(currentLevel);
        }

        function goBack() {
            if (historyStack.length > 0) {
                currentLevel = historyStack.pop();
                updateBreadcrumb();
                renderChart(currentLevel);
            }
        }

        function navigateTo(id) {
            // Rebuild history stack up to the target
            const newStack = [];
            let current = id;
            while (current && hierarchy[current] && hierarchy[current].parent) {
                newStack.unshift(hierarchy[current].parent);
                current = hierarchy[current].parent;
            }
            historyStack = newStack.slice(0, -1); // Remove 'world' from stack
            currentLevel = id;
            updateBreadcrumb();
            renderChart(currentLevel);
        }

        document.getElementById('backBtn').addEventListener('click', goBack);

        // Initial render
        updateBreadcrumb();
        renderChart('world');
    </script>
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
