"""pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Download required JavaScript files
highmaps_url = "https://code.highcharts.com/maps/highmaps.js"
drilldown_url = "https://code.highcharts.com/modules/drilldown.js"
us_url = "https://code.highcharts.com/mapdata/countries/us/us-all.topo.json"

with urllib.request.urlopen(highmaps_url, timeout=60) as response:
    highmaps_js = response.read().decode("utf-8")

with urllib.request.urlopen(drilldown_url, timeout=60) as response:
    drilldown_js = response.read().decode("utf-8")

with urllib.request.urlopen(us_url, timeout=60) as response:
    us_topo = response.read().decode("utf-8")

# State topology URLs for drilldown (will be fetched dynamically in JS)
# Using a selection of states with available TopoJSON data

# Build the complete Highcharts Maps configuration with drilldown
chart_config = """
(function() {
    // Sales data by state (synthetic data representing regional sales in $M)
    var statesData = [
        { 'hc-key': 'us-ca', name: 'California', value: 245, drilldown: 'us-ca' },
        { 'hc-key': 'us-tx', name: 'Texas', value: 198, drilldown: 'us-tx' },
        { 'hc-key': 'us-fl', name: 'Florida', value: 156, drilldown: 'us-fl' },
        { 'hc-key': 'us-ny', name: 'New York', value: 215, drilldown: 'us-ny' },
        { 'hc-key': 'us-il', name: 'Illinois', value: 98, drilldown: 'us-il' },
        { 'hc-key': 'us-pa', name: 'Pennsylvania', value: 87, drilldown: 'us-pa' },
        { 'hc-key': 'us-oh', name: 'Ohio', value: 76, drilldown: 'us-oh' },
        { 'hc-key': 'us-ga', name: 'Georgia', value: 89, drilldown: 'us-ga' },
        { 'hc-key': 'us-nc', name: 'North Carolina', value: 72, drilldown: 'us-nc' },
        { 'hc-key': 'us-mi', name: 'Michigan', value: 68, drilldown: 'us-mi' },
        { 'hc-key': 'us-nj', name: 'New Jersey', value: 94, drilldown: 'us-nj' },
        { 'hc-key': 'us-va', name: 'Virginia', value: 65, drilldown: 'us-va' },
        { 'hc-key': 'us-wa', name: 'Washington', value: 112, drilldown: 'us-wa' },
        { 'hc-key': 'us-az', name: 'Arizona', value: 58, drilldown: 'us-az' },
        { 'hc-key': 'us-ma', name: 'Massachusetts', value: 78, drilldown: 'us-ma' },
        { 'hc-key': 'us-tn', name: 'Tennessee', value: 52, drilldown: 'us-tn' },
        { 'hc-key': 'us-in', name: 'Indiana', value: 45, drilldown: 'us-in' },
        { 'hc-key': 'us-mo', name: 'Missouri', value: 42, drilldown: 'us-mo' },
        { 'hc-key': 'us-md', name: 'Maryland', value: 56, drilldown: 'us-md' },
        { 'hc-key': 'us-wi', name: 'Wisconsin', value: 48, drilldown: 'us-wi' },
        { 'hc-key': 'us-co', name: 'Colorado', value: 67, drilldown: 'us-co' },
        { 'hc-key': 'us-mn', name: 'Minnesota', value: 55, drilldown: 'us-mn' },
        { 'hc-key': 'us-sc', name: 'South Carolina', value: 38, drilldown: 'us-sc' },
        { 'hc-key': 'us-al', name: 'Alabama', value: 35, drilldown: 'us-al' },
        { 'hc-key': 'us-la', name: 'Louisiana', value: 42, drilldown: 'us-la' },
        { 'hc-key': 'us-ky', name: 'Kentucky', value: 34, drilldown: 'us-ky' },
        { 'hc-key': 'us-or', name: 'Oregon', value: 52, drilldown: 'us-or' },
        { 'hc-key': 'us-ok', name: 'Oklahoma', value: 32, drilldown: 'us-ok' },
        { 'hc-key': 'us-ct', name: 'Connecticut', value: 45, drilldown: 'us-ct' },
        { 'hc-key': 'us-ut', name: 'Utah', value: 38, drilldown: 'us-ut' },
        { 'hc-key': 'us-ia', name: 'Iowa', value: 28, drilldown: 'us-ia' },
        { 'hc-key': 'us-nv', name: 'Nevada', value: 42, drilldown: 'us-nv' },
        { 'hc-key': 'us-ar', name: 'Arkansas', value: 24, drilldown: 'us-ar' },
        { 'hc-key': 'us-ms', name: 'Mississippi', value: 22, drilldown: 'us-ms' },
        { 'hc-key': 'us-ks', name: 'Kansas', value: 26, drilldown: 'us-ks' },
        { 'hc-key': 'us-nm', name: 'New Mexico', value: 18, drilldown: 'us-nm' },
        { 'hc-key': 'us-ne', name: 'Nebraska', value: 16, drilldown: 'us-ne' },
        { 'hc-key': 'us-id', name: 'Idaho', value: 14, drilldown: 'us-id' },
        { 'hc-key': 'us-wv', name: 'West Virginia', value: 12, drilldown: 'us-wv' },
        { 'hc-key': 'us-hi', name: 'Hawaii', value: 28, drilldown: 'us-hi' },
        { 'hc-key': 'us-nh', name: 'New Hampshire', value: 15, drilldown: 'us-nh' },
        { 'hc-key': 'us-me', name: 'Maine', value: 12, drilldown: 'us-me' },
        { 'hc-key': 'us-mt', name: 'Montana', value: 10, drilldown: 'us-mt' },
        { 'hc-key': 'us-ri', name: 'Rhode Island', value: 14, drilldown: 'us-ri' },
        { 'hc-key': 'us-de', name: 'Delaware', value: 12, drilldown: 'us-de' },
        { 'hc-key': 'us-sd', name: 'South Dakota', value: 8, drilldown: 'us-sd' },
        { 'hc-key': 'us-nd', name: 'North Dakota', value: 7, drilldown: 'us-nd' },
        { 'hc-key': 'us-ak', name: 'Alaska', value: 18, drilldown: 'us-ak' },
        { 'hc-key': 'us-vt', name: 'Vermont', value: 8, drilldown: 'us-vt' },
        { 'hc-key': 'us-wy', name: 'Wyoming', value: 6, drilldown: 'us-wy' }
    ];

    // City-level data for drilldown (top cities by sales in each state)
    var cityDrilldowns = {
        'us-ca': {
            name: 'California',
            data: [
                { name: 'Los Angeles', value: 85 },
                { name: 'San Francisco', value: 62 },
                { name: 'San Diego', value: 38 },
                { name: 'San Jose', value: 32 },
                { name: 'Sacramento', value: 18 },
                { name: 'Other', value: 10 }
            ]
        },
        'us-tx': {
            name: 'Texas',
            data: [
                { name: 'Houston', value: 68 },
                { name: 'Dallas', value: 52 },
                { name: 'Austin', value: 42 },
                { name: 'San Antonio', value: 24 },
                { name: 'Fort Worth', value: 12 }
            ]
        },
        'us-fl': {
            name: 'Florida',
            data: [
                { name: 'Miami', value: 58 },
                { name: 'Orlando', value: 35 },
                { name: 'Tampa', value: 28 },
                { name: 'Jacksonville', value: 22 },
                { name: 'Other', value: 13 }
            ]
        },
        'us-ny': {
            name: 'New York',
            data: [
                { name: 'New York City', value: 165 },
                { name: 'Buffalo', value: 18 },
                { name: 'Rochester', value: 15 },
                { name: 'Albany', value: 12 },
                { name: 'Other', value: 5 }
            ]
        },
        'us-il': {
            name: 'Illinois',
            data: [
                { name: 'Chicago', value: 72 },
                { name: 'Aurora', value: 8 },
                { name: 'Naperville', value: 7 },
                { name: 'Springfield', value: 6 },
                { name: 'Other', value: 5 }
            ]
        },
        'us-pa': {
            name: 'Pennsylvania',
            data: [
                { name: 'Philadelphia', value: 52 },
                { name: 'Pittsburgh', value: 22 },
                { name: 'Allentown', value: 8 },
                { name: 'Other', value: 5 }
            ]
        },
        'us-wa': {
            name: 'Washington',
            data: [
                { name: 'Seattle', value: 78 },
                { name: 'Spokane', value: 15 },
                { name: 'Tacoma', value: 12 },
                { name: 'Other', value: 7 }
            ]
        },
        'us-ma': {
            name: 'Massachusetts',
            data: [
                { name: 'Boston', value: 58 },
                { name: 'Worcester', value: 10 },
                { name: 'Cambridge', value: 7 },
                { name: 'Other', value: 3 }
            ]
        },
        'us-ga': {
            name: 'Georgia',
            data: [
                { name: 'Atlanta', value: 65 },
                { name: 'Augusta', value: 12 },
                { name: 'Savannah', value: 8 },
                { name: 'Other', value: 4 }
            ]
        },
        'us-co': {
            name: 'Colorado',
            data: [
                { name: 'Denver', value: 45 },
                { name: 'Colorado Springs', value: 12 },
                { name: 'Boulder', value: 7 },
                { name: 'Other', value: 3 }
            ]
        }
    };

    // Create the map chart
    var chart = Highcharts.mapChart('container', {
        chart: {
            width: 4800,
            height: 2700,
            backgroundColor: '#ffffff',
            spacing: [100, 80, 100, 80],
            events: {
                drilldown: function(e) {
                    if (!e.seriesOptions && e.point.drilldown) {
                        var drilldownId = e.point.drilldown;
                        var drilldownData = cityDrilldowns[drilldownId];

                        if (drilldownData) {
                            // Add column series for city-level drilldown
                            chart.addSeriesAsDrilldown(e.point, {
                                type: 'column',
                                name: drilldownData.name + ' Cities',
                                data: drilldownData.data.map(function(item) {
                                    return {
                                        name: item.name,
                                        y: item.value
                                    };
                                }),
                                colorByPoint: true,
                                colors: ['#306998', '#FFD43B', '#9467BD', '#17BECF', '#8C564B', '#E377C2'],
                                dataLabels: {
                                    enabled: true,
                                    format: '${point.y}M',
                                    style: {
                                        fontSize: '28px',
                                        fontWeight: 'bold',
                                        textOutline: '2px white'
                                    }
                                }
                            });
                        }
                    }
                }
            }
        },
        title: {
            text: 'map-drilldown-geographic \\u00b7 highcharts \\u00b7 pyplots.ai',
            style: {
                fontSize: '64px',
                fontWeight: 'bold'
            },
            y: 60
        },
        subtitle: {
            text: 'Regional Sales Performance ($M) \\u2014 Click a state to drill down to cities',
            style: {
                fontSize: '42px',
                color: '#666666'
            },
            y: 120
        },
        mapNavigation: {
            enabled: false
        },
        colorAxis: {
            min: 0,
            max: 250,
            stops: [
                [0, '#f7fbff'],
                [0.2, '#c6dbef'],
                [0.4, '#6baed6'],
                [0.6, '#306998'],
                [0.8, '#2171b5'],
                [1, '#08306b']
            ],
            labels: {
                style: {
                    fontSize: '32px'
                },
                formatter: function() {
                    return '$' + this.value + 'M';
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            floating: false,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            padding: 30,
            symbolHeight: 500,
            symbolWidth: 50,
            itemStyle: {
                fontSize: '32px'
            },
            title: {
                text: 'Sales<br/>($M)',
                style: {
                    fontSize: '36px',
                    fontWeight: 'bold'
                }
            }
        },
        tooltip: {
            style: {
                fontSize: '32px'
            },
            headerFormat: '',
            pointFormat: '<b>{point.name}</b><br/>Sales: ${point.value}M',
            valueSuffix: 'M'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            map: {
                cursor: 'pointer',
                states: {
                    hover: {
                        color: '#FFD43B'
                    }
                },
                dataLabels: {
                    enabled: true,
                    format: '{point.name}',
                    style: {
                        fontSize: '18px',
                        fontWeight: 'normal',
                        textOutline: '2px white'
                    }
                },
                borderColor: '#ffffff',
                borderWidth: 2
            },
            column: {
                borderRadius: 8,
                cursor: 'pointer'
            }
        },
        xAxis: {
            visible: false,
            labels: {
                style: {
                    fontSize: '28px'
                }
            }
        },
        yAxis: {
            visible: false,
            title: {
                text: 'Sales ($M)',
                style: {
                    fontSize: '32px'
                }
            },
            labels: {
                style: {
                    fontSize: '28px'
                },
                formatter: function() {
                    return '$' + this.value + 'M';
                }
            }
        },
        drilldown: {
            breadcrumbs: {
                position: {
                    align: 'left',
                    x: 100,
                    y: 30
                },
                style: {
                    fontSize: '32px'
                },
                buttonTheme: {
                    style: {
                        fontSize: '32px',
                        fontWeight: 'bold'
                    },
                    states: {
                        hover: {
                            fill: '#f0f0f0'
                        }
                    }
                },
                separator: {
                    style: {
                        fontSize: '32px'
                    }
                },
                showFullPath: true
            },
            activeAxisLabelStyle: {
                textDecoration: 'none',
                fontStyle: 'normal',
                fontSize: '28px'
            },
            activeDataLabelStyle: {
                textDecoration: 'none',
                fontStyle: 'normal',
                fontSize: '28px'
            }
        },
        series: [{
            type: 'map',
            mapData: topology,
            name: 'US States',
            data: statesData,
            joinBy: 'hc-key',
            nullColor: '#e0e0e0',
            allowPointSelect: true
        }]
    });
})();
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highmaps_js}</script>
    <script>{drilldown_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        var topology = {us_topo};
        {chart_config}
    </script>
</body>
</html>"""

# Save HTML for interactive version (with CDN links for portability)
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/maps/highmaps.js"></script>
    <script src="https://code.highcharts.com/modules/drilldown.js"></script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        fetch('https://code.highcharts.com/mapdata/countries/us/us-all.topo.json')
            .then(response => response.json())
            .then(function(topology) {{
                {chart_config}
            }});
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Set up Chrome for screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(8)  # Wait for map to render (maps need more time)
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
