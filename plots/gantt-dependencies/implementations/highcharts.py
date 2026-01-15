""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2026-01-15
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Download Highcharts Gantt JS (includes core + gantt module)
highcharts_gantt_url = "https://code.highcharts.com/gantt/highcharts-gantt.js"
with urllib.request.urlopen(highcharts_gantt_url, timeout=30) as response:
    highcharts_gantt_js = response.read().decode("utf-8")

# Project data: Software Development Project with phases and dependencies
# Each task has: id, name, start (ms), end (ms), parent (group), dependency
project_data = [
    # Phase 1: Requirements
    {"id": "requirements", "name": "Requirements Phase", "collapsed": False},
    {
        "id": "req_gather",
        "name": "Gather Requirements",
        "start": 1704067200000,  # Jan 1, 2024
        "end": 1704672000000,  # Jan 8, 2024
        "parent": "requirements",
    },
    {
        "id": "req_analysis",
        "name": "Requirements Analysis",
        "start": 1704672000000,  # Jan 8, 2024
        "end": 1705276800000,  # Jan 15, 2024
        "parent": "requirements",
        "dependency": "req_gather",
    },
    {
        "id": "req_approval",
        "name": "Stakeholder Approval",
        "start": 1705276800000,  # Jan 15, 2024
        "end": 1705536000000,  # Jan 18, 2024
        "parent": "requirements",
        "dependency": "req_analysis",
    },
    # Phase 2: Design
    {"id": "design", "name": "Design Phase", "collapsed": False},
    {
        "id": "design_arch",
        "name": "Architecture Design",
        "start": 1705536000000,  # Jan 18, 2024
        "end": 1706400000000,  # Jan 28, 2024
        "parent": "design",
        "dependency": "req_approval",
    },
    {
        "id": "design_ui",
        "name": "UI/UX Design",
        "start": 1705536000000,  # Jan 18, 2024 (parallel)
        "end": 1706832000000,  # Feb 2, 2024
        "parent": "design",
        "dependency": "req_approval",
    },
    {
        "id": "design_db",
        "name": "Database Design",
        "start": 1706400000000,  # Jan 28, 2024
        "end": 1707004800000,  # Feb 4, 2024
        "parent": "design",
        "dependency": "design_arch",
    },
    # Phase 3: Development
    {"id": "development", "name": "Development Phase", "collapsed": False},
    {
        "id": "dev_backend",
        "name": "Backend Development",
        "start": 1707004800000,  # Feb 4, 2024
        "end": 1709251200000,  # Mar 1, 2024
        "parent": "development",
        "dependency": ["design_arch", "design_db"],
    },
    {
        "id": "dev_frontend",
        "name": "Frontend Development",
        "start": 1706832000000,  # Feb 2, 2024
        "end": 1709078400000,  # Feb 28, 2024
        "parent": "development",
        "dependency": "design_ui",
    },
    {
        "id": "dev_integration",
        "name": "System Integration",
        "start": 1709251200000,  # Mar 1, 2024
        "end": 1710115200000,  # Mar 11, 2024
        "parent": "development",
        "dependency": ["dev_backend", "dev_frontend"],
    },
    # Phase 4: Testing
    {"id": "testing", "name": "Testing Phase", "collapsed": False},
    {
        "id": "test_unit",
        "name": "Unit Testing",
        "start": 1708041600000,  # Feb 16, 2024 (starts during dev)
        "end": 1709683200000,  # Mar 6, 2024
        "parent": "testing",
        "dependency": "dev_backend",
    },
    {
        "id": "test_integration",
        "name": "Integration Testing",
        "start": 1710115200000,  # Mar 11, 2024
        "end": 1710720000000,  # Mar 18, 2024
        "parent": "testing",
        "dependency": "dev_integration",
    },
    {
        "id": "test_uat",
        "name": "User Acceptance Testing",
        "start": 1710720000000,  # Mar 18, 2024
        "end": 1711324800000,  # Mar 25, 2024
        "parent": "testing",
        "dependency": "test_integration",
    },
]

# Colors for different phases
phase_colors = {
    "requirements": "#306998",  # Python Blue
    "design": "#FFD43B",  # Python Yellow
    "development": "#9467BD",  # Purple
    "testing": "#17BECF",  # Cyan
}

# Build the chart configuration as JavaScript
chart_config = """
Highcharts.ganttChart('container', {
    chart: {
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        spacingTop: 60,
        spacingBottom: 180,
        spacingLeft: 60,
        spacingRight: 150
    },
    title: {
        text: 'gantt-dependencies \\u00b7 highcharts \\u00b7 pyplots.ai',
        style: {
            fontSize: '56px',
            fontWeight: 'bold'
        },
        margin: 40
    },
    subtitle: {
        text: 'Software Development Project Schedule with Task Dependencies',
        style: {
            fontSize: '36px'
        }
    },
    xAxis: [{
        min: Date.UTC(2024, 0, 1),
        max: Date.UTC(2024, 3, 1),
        tickInterval: 7 * 24 * 3600 * 1000,
        labels: {
            style: {
                fontSize: '26px'
            },
            format: '{value:%b %e}'
        },
        gridLineWidth: 1,
        gridLineColor: '#e6e6e6'
    }],
    yAxis: {
        labels: {
            style: {
                fontSize: '30px'
            }
        },
        staticScale: 100,
        gridLineWidth: 1,
        gridLineColor: '#e6e6e6'
    },
    tooltip: {
        style: {
            fontSize: '22px'
        },
        dateTimeLabelFormats: {
            day: '%A, %b %e, %Y'
        }
    },
    legend: {
        enabled: true,
        align: 'center',
        verticalAlign: 'bottom',
        layout: 'horizontal',
        itemStyle: {
            fontSize: '28px'
        },
        symbolHeight: 24,
        symbolWidth: 50,
        itemMarginTop: 20,
        itemMarginBottom: 10
    },
    navigator: {
        enabled: false
    },
    scrollbar: {
        enabled: false
    },
    rangeSelector: {
        enabled: false
    },
    plotOptions: {
        series: {
            animation: false,
            borderRadius: 6,
            pointPadding: 0.1,
            groupPadding: 0.1,
            dataLabels: {
                enabled: true,
                align: 'center',
                style: {
                    fontSize: '22px',
                    fontWeight: 'bold',
                    textOutline: '3px white'
                },
                format: '{point.name}'
            },
            connectors: {
                lineWidth: 5,
                dashStyle: 'Solid',
                lineColor: '#666666',
                radius: 15,
                marker: {
                    enabled: true,
                    width: 16,
                    height: 16
                }
            }
        }
    },
    series: [{
        name: 'Requirements Phase',
        color: '#306998',
        data: [
            {
                id: 'req_gather',
                name: 'Gather Requirements',
                start: Date.UTC(2024, 0, 1),
                end: Date.UTC(2024, 0, 8),
                y: 0
            },
            {
                id: 'req_analysis',
                name: 'Requirements Analysis',
                start: Date.UTC(2024, 0, 8),
                end: Date.UTC(2024, 0, 15),
                dependency: 'req_gather',
                y: 1
            },
            {
                id: 'req_approval',
                name: 'Stakeholder Approval',
                start: Date.UTC(2024, 0, 15),
                end: Date.UTC(2024, 0, 18),
                dependency: 'req_analysis',
                y: 2
            }
        ]
    }, {
        name: 'Design Phase',
        color: '#FFD43B',
        data: [
            {
                id: 'design_arch',
                name: 'Architecture Design',
                start: Date.UTC(2024, 0, 18),
                end: Date.UTC(2024, 0, 28),
                dependency: 'req_approval',
                y: 3
            },
            {
                id: 'design_ui',
                name: 'UI/UX Design',
                start: Date.UTC(2024, 0, 18),
                end: Date.UTC(2024, 1, 2),
                dependency: 'req_approval',
                y: 4
            },
            {
                id: 'design_db',
                name: 'Database Design',
                start: Date.UTC(2024, 0, 28),
                end: Date.UTC(2024, 1, 4),
                dependency: 'design_arch',
                y: 5
            }
        ]
    }, {
        name: 'Development Phase',
        color: '#9467BD',
        data: [
            {
                id: 'dev_backend',
                name: 'Backend Development',
                start: Date.UTC(2024, 1, 4),
                end: Date.UTC(2024, 2, 1),
                dependency: ['design_arch', 'design_db'],
                y: 6
            },
            {
                id: 'dev_frontend',
                name: 'Frontend Development',
                start: Date.UTC(2024, 1, 2),
                end: Date.UTC(2024, 1, 28),
                dependency: 'design_ui',
                y: 7
            },
            {
                id: 'dev_integration',
                name: 'System Integration',
                start: Date.UTC(2024, 2, 1),
                end: Date.UTC(2024, 2, 11),
                dependency: ['dev_backend', 'dev_frontend'],
                y: 8
            }
        ]
    }, {
        name: 'Testing Phase',
        color: '#17BECF',
        data: [
            {
                id: 'test_unit',
                name: 'Unit Testing',
                start: Date.UTC(2024, 1, 16),
                end: Date.UTC(2024, 2, 6),
                dependency: 'dev_backend',
                y: 9
            },
            {
                id: 'test_integration',
                name: 'Integration Testing',
                start: Date.UTC(2024, 2, 11),
                end: Date.UTC(2024, 2, 18),
                dependency: 'dev_integration',
                y: 10
            },
            {
                id: 'test_uat',
                name: 'User Acceptance Testing',
                start: Date.UTC(2024, 2, 18),
                end: Date.UTC(2024, 2, 25),
                dependency: 'test_integration',
                y: 11
            }
        ]
    }]
});
"""

# Generate HTML with inline Highcharts Gantt
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_gantt_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width:4800px; height:2700px;"></div>
    <script>
    {chart_config}
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file

# Also save HTML for interactive version
html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>gantt-dependencies - Highcharts - pyplots.ai</title>
    <script src="https://code.highcharts.com/gantt/highcharts-gantt.js"></script>
</head>
<body style="margin:0; padding:20px; background:#ffffff;">
    <div id="container" style="width:100%; height:800px;"></div>
    <script>
    {chart_config}
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_output)
