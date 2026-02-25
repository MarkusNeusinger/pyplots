""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: highcharts 1.10.3 | Python 3.14
Quality: 89/100 | Updated: 2026-02-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Download Highcharts Gantt JS (includes core + gantt module)
highcharts_gantt_url = "https://cdn.jsdelivr.net/npm/highcharts@11.4.8/highcharts-gantt.js"
with urllib.request.urlopen(highcharts_gantt_url, timeout=30) as response:
    highcharts_gantt_js = response.read().decode("utf-8")

# Chart configuration using Highcharts Gantt with parent/child grouping
# Software Development Project: 4 phases, 12 tasks + 2 milestones, finish-to-start dependencies
# Refined muted palette: slate blue, amber, muted purple, teal
chart_config = """
Highcharts.ganttChart('container', {
    chart: {
        width: 4800,
        height: 2700,
        backgroundColor: '#FAFBFC',
        spacingTop: 50,
        spacingBottom: 50,
        spacingLeft: 50,
        spacingRight: 50,
        style: {
            fontFamily: '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
        }
    },
    title: {
        text: 'gantt-dependencies \\u00b7 highcharts \\u00b7 pyplots.ai',
        style: {
            fontSize: '44px',
            fontWeight: '600',
            color: '#2C3E50'
        },
        margin: 30
    },
    subtitle: {
        text: 'Software Development Project Schedule \\u2014 Critical Path & Phase Dependencies',
        style: {
            fontSize: '32px',
            color: '#7F8C8D',
            fontWeight: '400'
        }
    },
    xAxis: [{
        min: Date.UTC(2024, 0, 1),
        max: Date.UTC(2024, 2, 31),
        tickInterval: 7 * 24 * 3600 * 1000,
        labels: {
            style: {
                fontSize: '22px',
                color: '#5D6D7E'
            },
            format: '{value:%b %e}'
        },
        gridLineWidth: 1,
        gridLineColor: '#E8ECF0',
        currentDateIndicator: false
    }],
    yAxis: {
        labels: {
            style: {
                fontSize: '26px',
                color: '#34495E'
            },
            indentation: 30
        },
        gridLineWidth: 1,
        gridLineColor: '#F0F2F5',
        alternateGridColor: '#F7F8FA'
    },
    tooltip: {
        style: {
            fontSize: '22px'
        },
        dateTimeLabelFormats: {
            day: '%A, %b %e, %Y'
        }
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
            borderRadius: 5,
            groupPadding: 0.05,
            dataLabels: {
                enabled: true,
                align: 'left',
                padding: 12,
                style: {
                    fontSize: '18px',
                    fontWeight: '600',
                    textOutline: '2.5px #FAFBFC'
                },
                format: '{point.name}',
                overflow: 'allow',
                crop: false
            },
            connectors: {
                lineWidth: 3,
                dashStyle: 'Solid',
                lineColor: '#5D6D7E',
                radius: 10,
                startMarker: {
                    enabled: false
                },
                endMarker: {
                    enabled: true,
                    width: 12,
                    height: 12,
                    color: '#5D6D7E'
                }
            }
        }
    },
    series: [{
        name: 'Project Schedule',
        data: [
            // Phase 1: Requirements (Jan 1 - Jan 20) — Slate Blue
            {
                id: 'requirements',
                name: 'Requirements Phase',
                color: '#306998'
            },
            {
                id: 'req_gather',
                name: 'Gather Requirements',
                parent: 'requirements',
                start: Date.UTC(2024, 0, 1),
                end: Date.UTC(2024, 0, 10),
                color: '#306998'
            },
            {
                id: 'req_analysis',
                name: 'Requirements Analysis',
                parent: 'requirements',
                start: Date.UTC(2024, 0, 11),
                end: Date.UTC(2024, 0, 17),
                dependency: 'req_gather',
                color: '#306998'
            },
            {
                id: 'req_approval',
                name: 'Stakeholder Approval',
                parent: 'requirements',
                start: Date.UTC(2024, 0, 18),
                end: Date.UTC(2024, 0, 22),
                dependency: 'req_analysis',
                color: '#306998'
            },
            // Milestone: Requirements Baseline
            {
                id: 'milestone_req',
                name: 'Requirements Baseline \\u2713',
                parent: 'requirements',
                start: Date.UTC(2024, 0, 22),
                milestone: true,
                dependency: 'req_approval',
                color: '#1A3A5C'
            },
            // Phase 2: Design (Jan 23 - Feb 9) — Amber
            {
                id: 'design',
                name: 'Design Phase',
                color: '#D4920B'
            },
            {
                id: 'design_arch',
                name: 'Architecture Design',
                parent: 'design',
                start: Date.UTC(2024, 0, 23),
                end: Date.UTC(2024, 1, 2),
                dependency: 'milestone_req',
                color: '#D4920B'
            },
            {
                id: 'design_ui',
                name: 'UI/UX Design',
                parent: 'design',
                start: Date.UTC(2024, 0, 23),
                end: Date.UTC(2024, 1, 5),
                dependency: 'milestone_req',
                color: '#E8A817'
            },
            {
                id: 'design_db',
                name: 'Database Design',
                parent: 'design',
                start: Date.UTC(2024, 1, 3),
                end: Date.UTC(2024, 1, 9),
                dependency: 'design_arch',
                color: '#D4920B'
            },
            // Phase 3: Development (Feb 10 - Mar 15) — Muted Purple
            {
                id: 'development',
                name: 'Development Phase',
                color: '#7B5EA7'
            },
            {
                id: 'dev_backend',
                name: 'Backend Development',
                parent: 'development',
                start: Date.UTC(2024, 1, 12),
                end: Date.UTC(2024, 2, 4),
                dependency: 'design_db',
                color: '#7B5EA7'
            },
            {
                id: 'dev_frontend',
                name: 'Frontend Development',
                parent: 'development',
                start: Date.UTC(2024, 1, 7),
                end: Date.UTC(2024, 2, 1),
                dependency: 'design_ui',
                color: '#9B7EC8'
            },
            {
                id: 'dev_integration',
                name: 'System Integration',
                parent: 'development',
                start: Date.UTC(2024, 2, 5),
                end: Date.UTC(2024, 2, 15),
                dependency: ['dev_backend', 'dev_frontend'],
                color: '#7B5EA7'
            },
            // Phase 4: Testing (Mar 5 - Mar 29) — Teal
            {
                id: 'testing',
                name: 'Testing Phase',
                color: '#0F8B8D'
            },
            {
                id: 'test_unit',
                name: 'Unit Testing',
                parent: 'testing',
                start: Date.UTC(2024, 2, 5),
                end: Date.UTC(2024, 2, 15),
                dependency: 'dev_backend',
                color: '#0F8B8D'
            },
            {
                id: 'test_integration',
                name: 'Integration Testing',
                parent: 'testing',
                start: Date.UTC(2024, 2, 16),
                end: Date.UTC(2024, 2, 22),
                dependency: ['dev_integration', 'test_unit'],
                color: '#0F8B8D'
            },
            {
                id: 'test_uat',
                name: 'User Acceptance Testing',
                parent: 'testing',
                start: Date.UTC(2024, 2, 23),
                end: Date.UTC(2024, 2, 29),
                dependency: 'test_integration',
                color: '#0F8B8D'
            },
            // Milestone: Release Ready
            {
                id: 'milestone_release',
                name: 'Release Ready \\u2605',
                parent: 'testing',
                start: Date.UTC(2024, 2, 29),
                milestone: true,
                dependency: 'test_uat',
                color: '#1A3A5C'
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
<body style="margin:0; padding:0; background:#FAFBFC;">
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
chrome_options.add_argument("--window-size=4800,5000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Capture the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Save HTML for interactive version
html_output = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>gantt-dependencies - Highcharts - pyplots.ai</title>
    <script src="https://code.highcharts.com/gantt/highcharts-gantt.js"></script>
</head>
<body style="margin:0; padding:20px; background:#FAFBFC;">
    <div id="container" style="width:100%; height:800px;"></div>
    <script>
    Highcharts.ganttChart('container', {
        chart: {
            backgroundColor: '#FAFBFC',
            style: {
                fontFamily: '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
            }
        },
        title: {
            text: 'gantt-dependencies \\u00b7 highcharts \\u00b7 pyplots.ai',
            style: { color: '#2C3E50' }
        },
        subtitle: {
            text: 'Software Development Project Schedule \\u2014 Critical Path & Phase Dependencies',
            style: { color: '#7F8C8D' }
        },
        xAxis: [{
            min: Date.UTC(2024, 0, 1),
            max: Date.UTC(2024, 2, 31)
        }],
        yAxis: {
            labels: { indentation: 30 },
            alternateGridColor: '#F7F8FA'
        },
        plotOptions: {
            series: {
                borderRadius: 5,
                connectors: {
                    lineWidth: 2,
                    lineColor: '#5D6D7E',
                    radius: 8,
                    endMarker: { enabled: true, color: '#5D6D7E' }
                }
            }
        },
        series: [{
            name: 'Project Schedule',
            data: [
                { id: 'requirements', name: 'Requirements Phase', color: '#306998' },
                { id: 'req_gather', name: 'Gather Requirements', parent: 'requirements', start: Date.UTC(2024, 0, 1), end: Date.UTC(2024, 0, 10), color: '#306998' },
                { id: 'req_analysis', name: 'Requirements Analysis', parent: 'requirements', start: Date.UTC(2024, 0, 11), end: Date.UTC(2024, 0, 17), dependency: 'req_gather', color: '#306998' },
                { id: 'req_approval', name: 'Stakeholder Approval', parent: 'requirements', start: Date.UTC(2024, 0, 18), end: Date.UTC(2024, 0, 22), dependency: 'req_analysis', color: '#306998' },
                { id: 'milestone_req', name: 'Requirements Baseline \\u2713', parent: 'requirements', start: Date.UTC(2024, 0, 22), milestone: true, dependency: 'req_approval', color: '#1A3A5C' },
                { id: 'design', name: 'Design Phase', color: '#D4920B' },
                { id: 'design_arch', name: 'Architecture Design', parent: 'design', start: Date.UTC(2024, 0, 23), end: Date.UTC(2024, 1, 2), dependency: 'milestone_req', color: '#D4920B' },
                { id: 'design_ui', name: 'UI/UX Design', parent: 'design', start: Date.UTC(2024, 0, 23), end: Date.UTC(2024, 1, 5), dependency: 'milestone_req', color: '#E8A817' },
                { id: 'design_db', name: 'Database Design', parent: 'design', start: Date.UTC(2024, 1, 3), end: Date.UTC(2024, 1, 9), dependency: 'design_arch', color: '#D4920B' },
                { id: 'development', name: 'Development Phase', color: '#7B5EA7' },
                { id: 'dev_backend', name: 'Backend Development', parent: 'development', start: Date.UTC(2024, 1, 12), end: Date.UTC(2024, 2, 4), dependency: 'design_db', color: '#7B5EA7' },
                { id: 'dev_frontend', name: 'Frontend Development', parent: 'development', start: Date.UTC(2024, 1, 7), end: Date.UTC(2024, 2, 1), dependency: 'design_ui', color: '#9B7EC8' },
                { id: 'dev_integration', name: 'System Integration', parent: 'development', start: Date.UTC(2024, 2, 5), end: Date.UTC(2024, 2, 15), dependency: ['dev_backend', 'dev_frontend'], color: '#7B5EA7' },
                { id: 'testing', name: 'Testing Phase', color: '#0F8B8D' },
                { id: 'test_unit', name: 'Unit Testing', parent: 'testing', start: Date.UTC(2024, 2, 5), end: Date.UTC(2024, 2, 15), dependency: 'dev_backend', color: '#0F8B8D' },
                { id: 'test_integration', name: 'Integration Testing', parent: 'testing', start: Date.UTC(2024, 2, 16), end: Date.UTC(2024, 2, 22), dependency: ['dev_integration', 'test_unit'], color: '#0F8B8D' },
                { id: 'test_uat', name: 'User Acceptance Testing', parent: 'testing', start: Date.UTC(2024, 2, 23), end: Date.UTC(2024, 2, 29), dependency: 'test_integration', color: '#0F8B8D' },
                { id: 'milestone_release', name: 'Release Ready \\u2605', parent: 'testing', start: Date.UTC(2024, 2, 29), milestone: true, dependency: 'test_uat', color: '#1A3A5C' }
            ]
        }]
    });
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_output)
