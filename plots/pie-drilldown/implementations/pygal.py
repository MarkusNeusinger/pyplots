""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import pygal
from pygal.style import Style


# Define hierarchical data structure for company budget
# Root level: main departments
# Level 2: sub-categories within each department
data = {
    "root": {"name": "Company Budget", "children": ["engineering", "marketing", "operations", "hr"]},
    "engineering": {
        "name": "Engineering",
        "parent": "root",
        "value": 450000,
        "children": ["eng_salaries", "eng_tools", "eng_cloud", "eng_training"],
    },
    "eng_salaries": {"name": "Salaries", "parent": "engineering", "value": 280000},
    "eng_tools": {"name": "Tools & Software", "parent": "engineering", "value": 75000},
    "eng_cloud": {"name": "Cloud Services", "parent": "engineering", "value": 65000},
    "eng_training": {"name": "Training", "parent": "engineering", "value": 30000},
    "marketing": {
        "name": "Marketing",
        "parent": "root",
        "value": 280000,
        "children": ["mkt_digital", "mkt_content", "mkt_events", "mkt_brand"],
    },
    "mkt_digital": {"name": "Digital Ads", "parent": "marketing", "value": 120000},
    "mkt_content": {"name": "Content Creation", "parent": "marketing", "value": 65000},
    "mkt_events": {"name": "Events", "parent": "marketing", "value": 55000},
    "mkt_brand": {"name": "Brand Design", "parent": "marketing", "value": 40000},
    "operations": {
        "name": "Operations",
        "parent": "root",
        "value": 180000,
        "children": ["ops_facilities", "ops_equipment", "ops_supplies"],
    },
    "ops_facilities": {"name": "Facilities", "parent": "operations", "value": 95000},
    "ops_equipment": {"name": "Equipment", "parent": "operations", "value": 55000},
    "ops_supplies": {"name": "Supplies", "parent": "operations", "value": 30000},
    "hr": {
        "name": "Human Resources",
        "parent": "root",
        "value": 90000,
        "children": ["hr_recruiting", "hr_benefits", "hr_development"],
    },
    "hr_recruiting": {"name": "Recruiting", "parent": "hr", "value": 35000},
    "hr_benefits": {"name": "Benefits Admin", "parent": "hr", "value": 30000},
    "hr_development": {"name": "Development", "parent": "hr", "value": 25000},
}

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    # Extended color palette for categories and subcategories
    colors=(
        "#306998",
        "#FFD43B",
        "#4B8BBE",
        "#7FB069",
        "#E07A5F",
        "#3D5A80",
        "#EE6C4D",
        "#98C1D9",
        "#81B29A",
        "#F4A261",
    ),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=22,
    tooltip_font_size=22,
)

# Create main pie chart showing top-level departments
pie_chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    inner_radius=0.35,  # Creates a donut effect for better visual
    title="Company Budget · pie-drilldown · pygal · pyplots.ai",
    legend_at_bottom=True,
    legend_box_size=28,
    print_values=True,
    print_labels=True,
    value_formatter=lambda x: f"${x:,.0f}",
    margin=60,
)

# Add main category slices with drill-down links via xlink
root_children = data["root"]["children"]
for child_id in root_children:
    child_data = data[child_id]
    # In pygal, we can add interactivity via xlink attribute for SVG
    # Each slice links to its detail view
    pie_chart.add(child_data["name"], [{"value": child_data["value"], "label": child_data["name"]}])

# Add a subtitle showing breadcrumb
pie_chart.x_title = "All Departments  |  Click slice to drill down"

# Render to PNG for static preview
pie_chart.render_to_png("plot.png")

# Create interactive HTML with JavaScript for drilldown functionality
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>pie-drilldown · pygal · pyplots.ai</title>
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
            max-width: 900px;
            width: 100%;
        }
        h1 {
            color: #333;
            text-align: center;
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        .breadcrumb {
            background: #306998;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .breadcrumb span {
            cursor: pointer;
        }
        .breadcrumb span:hover {
            text-decoration: underline;
        }
        .breadcrumb .separator {
            opacity: 0.7;
        }
        .breadcrumb .current {
            font-weight: bold;
            cursor: default;
        }
        .breadcrumb .current:hover {
            text-decoration: none;
        }
        #chart-container {
            width: 100%;
            height: 600px;
        }
        #chart-container svg {
            width: 100%;
            height: 100%;
        }
        .back-btn {
            background: #FFD43B;
            color: #333;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 15px;
            font-weight: bold;
            transition: background 0.2s;
        }
        .back-btn:hover {
            background: #E6BE35;
        }
        .back-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .hint {
            text-align: center;
            color: #666;
            margin-top: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Company Budget · pie-drilldown · pygal · pyplots.ai</h1>
        <div class="breadcrumb">
            <button class="back-btn" id="backBtn" disabled>← Back</button>
            <div id="breadcrumb-path">
                <span class="current">All Departments</span>
            </div>
        </div>
        <div id="chart-container"></div>
        <p class="hint">💡 Click on a slice to drill down into its subcategories</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    <script>
        // Hierarchical data
        const data = {
            root: {
                name: "All Departments",
                children: ["engineering", "marketing", "operations", "hr"]
            },
            engineering: {
                name: "Engineering",
                parent: "root",
                value: 450000,
                children: ["eng_salaries", "eng_tools", "eng_cloud", "eng_training"]
            },
            eng_salaries: { name: "Salaries", parent: "engineering", value: 280000 },
            eng_tools: { name: "Tools & Software", parent: "engineering", value: 75000 },
            eng_cloud: { name: "Cloud Services", parent: "engineering", value: 65000 },
            eng_training: { name: "Training", parent: "engineering", value: 30000 },
            marketing: {
                name: "Marketing",
                parent: "root",
                value: 280000,
                children: ["mkt_digital", "mkt_content", "mkt_events", "mkt_brand"]
            },
            mkt_digital: { name: "Digital Ads", parent: "marketing", value: 120000 },
            mkt_content: { name: "Content Creation", parent: "marketing", value: 65000 },
            mkt_events: { name: "Events", parent: "marketing", value: 55000 },
            mkt_brand: { name: "Brand Design", parent: "marketing", value: 40000 },
            operations: {
                name: "Operations",
                parent: "root",
                value: 180000,
                children: ["ops_facilities", "ops_equipment", "ops_supplies"]
            },
            ops_facilities: { name: "Facilities", parent: "operations", value: 95000 },
            ops_equipment: { name: "Equipment", parent: "operations", value: 55000 },
            ops_supplies: { name: "Supplies", parent: "operations", value: 30000 },
            hr: {
                name: "Human Resources",
                parent: "root",
                value: 90000,
                children: ["hr_recruiting", "hr_benefits", "hr_development"]
            },
            hr_recruiting: { name: "Recruiting", parent: "hr", value: 35000 },
            hr_benefits: { name: "Benefits Admin", parent: "hr", value: 30000 },
            hr_development: { name: "Development", parent: "hr", value: 25000 }
        };

        const colors = ['#306998', '#FFD43B', '#4B8BBE', '#7FB069', '#E07A5F', '#3D5A80', '#EE6C4D', '#98C1D9'];

        let currentLevel = 'root';
        let chart = null;
        let history = [];

        Chart.register(ChartDataLabels);

        function formatCurrency(value) {
            return '$' + value.toLocaleString();
        }

        function getChildData(parentId) {
            const parent = data[parentId];
            if (!parent.children) return [];
            return parent.children.map((childId, index) => ({
                id: childId,
                name: data[childId].name,
                value: data[childId].value,
                hasChildren: !!data[childId].children,
                color: colors[index % colors.length]
            }));
        }

        function updateBreadcrumb() {
            const pathDiv = document.getElementById('breadcrumb-path');
            const backBtn = document.getElementById('backBtn');

            let html = '';
            const fullPath = ['root', ...history, currentLevel].filter((v, i, a) => a.indexOf(v) === i);

            fullPath.forEach((id, index) => {
                if (index > 0) {
                    html += '<span class="separator"> > </span>';
                }
                if (id === currentLevel) {
                    html += `<span class="current">${data[id].name}</span>`;
                } else {
                    html += `<span onclick="navigateTo('${id}')">${data[id].name}</span>`;
                }
            });

            pathDiv.innerHTML = html;
            backBtn.disabled = currentLevel === 'root';
        }

        function renderChart(levelId) {
            const children = getChildData(levelId);
            if (children.length === 0) return;

            const ctx = document.getElementById('chart-container');

            if (chart) {
                chart.destroy();
            }

            const canvas = document.createElement('canvas');
            ctx.innerHTML = '';
            ctx.appendChild(canvas);

            const total = children.reduce((sum, c) => sum + c.value, 0);

            chart = new Chart(canvas.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: children.map(c => c.name),
                    datasets: [{
                        data: children.map(c => c.value),
                        backgroundColor: children.map(c => c.color),
                        borderColor: 'white',
                        borderWidth: 3,
                        hoverOffset: 15
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '40%',
                    animation: {
                        animateRotate: true,
                        duration: 500
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: { size: 14, weight: 'bold' },
                                generateLabels: function(chart) {
                                    const data = chart.data;
                                    return data.labels.map((label, i) => ({
                                        text: `${label}: ${formatCurrency(data.datasets[0].data[i])}`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        strokeStyle: 'white',
                                        lineWidth: 2,
                                        index: i
                                    }));
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.parsed;
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${formatCurrency(value)} (${percentage}%)`;
                                }
                            },
                            titleFont: { size: 16 },
                            bodyFont: { size: 14 }
                        },
                        datalabels: {
                            color: '#fff',
                            font: { size: 14, weight: 'bold' },
                            formatter: function(value, context) {
                                const percentage = ((value / total) * 100).toFixed(0);
                                return percentage + '%';
                            },
                            textStrokeColor: 'rgba(0,0,0,0.3)',
                            textStrokeWidth: 2
                        }
                    },
                    onClick: function(event, elements) {
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            const childData = children[index];
                            if (childData.hasChildren) {
                                drillDown(childData.id);
                            }
                        }
                    },
                    onHover: function(event, elements) {
                        const canvas = event.native.target;
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            if (children[index].hasChildren) {
                                canvas.style.cursor = 'pointer';
                            } else {
                                canvas.style.cursor = 'default';
                            }
                        } else {
                            canvas.style.cursor = 'default';
                        }
                    }
                }
            });

            // Update hint based on whether children have sub-children
            const hint = document.querySelector('.hint');
            const hasClickableSlices = children.some(c => c.hasChildren);
            hint.style.display = hasClickableSlices ? 'block' : 'none';
        }

        function drillDown(id) {
            history.push(currentLevel);
            currentLevel = id;
            updateBreadcrumb();
            renderChart(currentLevel);
        }

        function goBack() {
            if (history.length > 0) {
                currentLevel = history.pop();
                updateBreadcrumb();
                renderChart(currentLevel);
            }
        }

        function navigateTo(id) {
            const idx = history.indexOf(id);
            if (idx >= 0) {
                history = history.slice(0, idx);
            } else {
                history = [];
            }
            currentLevel = id;
            updateBreadcrumb();
            renderChart(currentLevel);
        }

        document.getElementById('backBtn').addEventListener('click', goBack);

        // Initial render
        updateBreadcrumb();
        renderChart('root');
    </script>
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
