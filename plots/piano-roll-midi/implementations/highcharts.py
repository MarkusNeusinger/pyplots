""" pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: highcharts unknown | Python 3.14.3
Quality: 85/100 | Created: 2026-03-07
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


np.random.seed(42)

# MIDI helpers
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BLACK_KEY_INDICES = {1, 3, 6, 8, 10}

# Data - A chord progression with melody (C-Am-F-G, 8 measures of 4/4)
# Each note: (start_beat, duration_beats, midi_pitch, velocity)
notes = [
    # Measure 1-2: C major chord + melody
    (0.0, 4.0, 48, 90),  # C3 bass
    (0.0, 2.0, 52, 75),  # E3
    (0.0, 2.0, 55, 75),  # G3
    (2.0, 2.0, 52, 70),  # E3
    (2.0, 2.0, 55, 70),  # G3
    (0.0, 1.0, 64, 100),  # E4 melody
    (1.0, 1.0, 67, 105),  # G4
    (2.0, 1.5, 72, 110),  # C5
    (3.5, 0.5, 71, 80),  # B4
    (4.0, 4.0, 48, 85),  # C3 bass
    (4.0, 2.0, 52, 72),  # E3
    (4.0, 2.0, 55, 72),  # G3
    (6.0, 2.0, 52, 68),  # E3
    (6.0, 2.0, 55, 68),  # G3
    (4.0, 1.0, 72, 108),  # C5 melody
    (5.0, 0.5, 71, 85),  # B4
    (5.5, 0.5, 69, 82),  # A4
    (6.0, 2.0, 67, 95),  # G4
    # Measure 3-4: A minor chord + melody
    (8.0, 4.0, 57, 88),  # A3 bass
    (8.0, 2.0, 48, 72),  # C3
    (8.0, 2.0, 52, 72),  # E3
    (10.0, 2.0, 48, 68),  # C3
    (10.0, 2.0, 52, 68),  # E3
    (8.0, 1.0, 69, 102),  # A4 melody
    (9.0, 1.0, 67, 95),  # G4
    (10.0, 1.5, 64, 100),  # E4
    (11.5, 0.5, 62, 78),  # D4
    (12.0, 4.0, 57, 85),  # A3 bass
    (12.0, 2.0, 48, 70),  # C3
    (12.0, 2.0, 52, 70),  # E3
    (14.0, 2.0, 48, 65),  # C3
    (14.0, 2.0, 52, 65),  # E3
    (12.0, 1.0, 60, 98),  # C4 melody
    (13.0, 1.0, 62, 90),  # D4
    (14.0, 2.0, 64, 105),  # E4
    # Measure 5-6: F major chord + melody
    (16.0, 4.0, 53, 92),  # F3 bass
    (16.0, 2.0, 57, 74),  # A3
    (16.0, 2.0, 60, 74),  # C4
    (18.0, 2.0, 57, 70),  # A3
    (18.0, 2.0, 60, 70),  # C4
    (16.0, 1.0, 65, 100),  # F4 melody
    (17.0, 1.0, 67, 106),  # G4
    (18.0, 1.5, 69, 112),  # A4
    (19.5, 0.5, 67, 82),  # G4
    (20.0, 4.0, 53, 88),  # F3 bass
    (20.0, 2.0, 57, 72),  # A3
    (20.0, 2.0, 60, 72),  # C4
    (22.0, 2.0, 57, 66),  # A3
    (22.0, 2.0, 60, 66),  # C4
    (20.0, 1.0, 69, 108),  # A4 melody
    (21.0, 0.5, 67, 84),  # G4
    (21.5, 0.5, 65, 80),  # F4
    (22.0, 2.0, 64, 96),  # E4
    # Measure 7-8: G major chord + melody (building to end)
    (24.0, 4.0, 55, 95),  # G3 bass
    (24.0, 2.0, 59, 76),  # B3
    (24.0, 2.0, 62, 76),  # D4
    (26.0, 2.0, 59, 72),  # B3
    (26.0, 2.0, 62, 72),  # D4
    (24.0, 1.0, 67, 105),  # G4 melody
    (25.0, 1.0, 69, 110),  # A4
    (26.0, 1.5, 71, 118),  # B4
    (27.5, 0.5, 69, 85),  # A4
    (28.0, 4.0, 55, 90),  # G3 bass
    (28.0, 2.0, 59, 74),  # B3
    (28.0, 2.0, 62, 74),  # D4
    (30.0, 2.0, 59, 70),  # B3
    (30.0, 2.0, 62, 70),  # D4
    (28.0, 1.0, 71, 115),  # B4 melody
    (29.0, 1.0, 72, 120),  # C5 - climax
    (30.0, 2.0, 72, 125),  # C5 - final sustained
]

# Determine pitch range - only include pitches that have notes
used_pitches = sorted({n[2] for n in notes})
min_pitch = min(used_pitches) - 1
max_pitch = max(used_pitches) + 1

# Build category list for only the used range
all_midi_range = list(range(min_pitch, max_pitch + 1))
categories = []
for midi in all_midi_range:
    octave = midi // 12 - 1
    name = NOTE_NAMES[midi % 12]
    categories.append(f"{name}{octave}")

pitch_to_index = {midi: i for i, midi in enumerate(all_midi_range)}

# Velocity color mapping: teal (soft) → gold (medium) → crimson (loud)
# Better perceptual separation than blue→purple→red
vel_min, vel_max = 60, 127
color_stops_rgb = [
    (30, 120, 140),  # #1e788c teal (soft/piano)
    (240, 180, 40),  # #f0b428 golden yellow (medium/mezzo)
    (190, 30, 45),  # #be1e2d crimson (loud/forte)
]

# Build xrange data points with inline color interpolation
data_points = []
for start, dur, pitch, vel in notes:
    t = float(np.clip((vel - vel_min) / (vel_max - vel_min), 0.0, 1.0))
    if t < 0.5:
        s = t / 0.5
        r = int(color_stops_rgb[0][0] * (1 - s) + color_stops_rgb[1][0] * s)
        g = int(color_stops_rgb[0][1] * (1 - s) + color_stops_rgb[1][1] * s)
        b = int(color_stops_rgb[0][2] * (1 - s) + color_stops_rgb[1][2] * s)
    else:
        s = (t - 0.5) / 0.5
        r = int(color_stops_rgb[1][0] * (1 - s) + color_stops_rgb[2][0] * s)
        g = int(color_stops_rgb[1][1] * (1 - s) + color_stops_rgb[2][1] * s)
        b = int(color_stops_rgb[1][2] * (1 - s) + color_stops_rgb[2][2] * s)
    color = f"#{r:02x}{g:02x}{b:02x}"
    data_points.append(
        {
            "x": start,
            "x2": start + dur,
            "y": pitch_to_index[pitch],
            "color": color,
            "custom": {"pitch": pitch, "velocity": vel, "noteName": categories[pitch_to_index[pitch]]},
        }
    )

# Plot bands for black keys (subtle darker background rows)
plot_bands = []
for midi in all_midi_range:
    if (midi % 12) in BLACK_KEY_INDICES:
        idx = pitch_to_index[midi]
        plot_bands.append({"from": idx - 0.5, "to": idx + 0.5, "color": "rgba(0, 0, 0, 0.06)"})

# Beat grid lines for x-axis (stronger at measure boundaries)
total_beats = 32
beat_lines = []
for beat in range(total_beats + 1):
    is_measure = beat % 4 == 0
    beat_lines.append(
        {"value": beat, "color": "#999999" if is_measure else "#dddddd", "width": 2 if is_measure else 1, "zIndex": 3}
    )

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "xrange",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#fafafa",
    "marginLeft": 200,
    "marginTop": 180,
    "marginBottom": 200,
    "marginRight": 380,
    "style": {"fontFamily": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"},
}

chart.options.title = {
    "text": "piano-roll-midi \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "44px", "fontWeight": "600", "color": "#2c2c2c"},
    "y": 55,
}

chart.options.subtitle = {
    "text": "C \u2013 Am \u2013 F \u2013 G chord progression \u00b7 8 measures \u00b7 velocity-colored dynamics",
    "style": {"fontSize": "26px", "color": "#666666", "fontWeight": "400"},
    "y": 100,
}

chart.options.x_axis = {
    "title": {"text": "Beats", "style": {"fontSize": "28px", "color": "#444444"}},
    "labels": {"style": {"fontSize": "22px", "color": "#555555"}, "step": 1},
    "min": 0,
    "max": 32,
    "tickInterval": 4,
    "gridLineWidth": 0,
    "plotLines": beat_lines,
    "lineWidth": 0,
}

chart.options.y_axis = {
    "type": "category",
    "categories": categories,
    "title": {"text": "Pitch", "style": {"fontSize": "28px", "color": "#444444"}},
    "labels": {"style": {"fontSize": "20px", "color": "#555555"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.04)",
    "plotBands": plot_bands,
    "reversed": False,
    "lineWidth": 0,
}

chart.options.legend = {"enabled": False}

chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": '<span style="font-size:22px"><b>{point.custom.noteName}</b> (MIDI {point.custom.pitch})<br/>'
    "Beat {point.x} \u2013 {point.x2}<br/>"
    "Velocity: {point.custom.velocity}</span>",
    "backgroundColor": "rgba(255,255,255,0.95)",
    "borderColor": "#cccccc",
    "borderRadius": 8,
    "shadow": {"color": "rgba(0,0,0,0.15)", "offsetX": 2, "offsetY": 2, "width": 4},
}

chart.options.series = [
    {
        "type": "xrange",
        "name": "Notes",
        "data": data_points,
        "pointWidth": 60,
        "borderRadius": 5,
        "borderWidth": 1,
        "borderColor": "rgba(0, 0, 0, 0.15)",
        "dataLabels": {"enabled": False},
    }
]

chart.options.credits = {"enabled": False}

# Download Highcharts JS modules
cache_dir = Path("/tmp")
cdn_urls = {
    "highcharts": ("https://cdn.jsdelivr.net/npm/highcharts@11.4.8/highcharts.js", cache_dir / "highcharts.js"),
    "xrange": ("https://cdn.jsdelivr.net/npm/highcharts@11.4.8/modules/xrange.js", cache_dir / "hc_xrange.js"),
}
js_scripts = {}
for name, (url, cache_path) in cdn_urls.items():
    if cache_path.exists() and cache_path.stat().st_size > 1000:
        js_scripts[name] = cache_path.read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(url, timeout=30) as resp:
            content = resp.read().decode("utf-8")
        cache_path.write_text(content, encoding="utf-8")
        js_scripts[name] = content
highcharts_js = js_scripts["highcharts"]
xrange_js = js_scripts["xrange"]

# Generate HTML with inline scripts and velocity colorbar via Highcharts renderer callback
html_str = chart.to_js_literal()

# JavaScript to draw velocity colorbar using Highcharts SVG renderer (segmented gradient)
colorbar_js = """
<script>
(function() {
  var checkChart = setInterval(function() {
    var chart = Highcharts.charts[0];
    if (!chart) return;
    clearInterval(checkChart);
    var r = chart.renderer;
    var x = 4470, y = 220, w = 36, totalH = 2200;
    var stops = [[30,120,140],[240,180,40],[190,30,45]];
    var nSegs = 80;
    var segH = totalH / nSegs;
    for (var i = 0; i < nSegs; i++) {
      var t = 1 - i / (nSegs - 1);
      var c0, c1, s;
      if (t < 0.5) { s = t / 0.5; c0 = stops[0]; c1 = stops[1]; }
      else { s = (t - 0.5) / 0.5; c0 = stops[1]; c1 = stops[2]; }
      var cr = Math.round(c0[0]*(1-s)+c1[0]*s);
      var cg = Math.round(c0[1]*(1-s)+c1[1]*s);
      var cb = Math.round(c0[2]*(1-s)+c1[2]*s);
      var ry = (i === 0) ? 4 : 0;
      var ry2 = (i === nSegs-1) ? 4 : 0;
      r.rect(x, y + i*segH, w, segH+1, 0).attr({fill:'rgb('+cr+','+cg+','+cb+')', 'stroke-width':0}).add();
    }
    r.rect(x, y, w, totalH, 6).attr({fill:'none', stroke:'#bbb', 'stroke-width':1}).add();
    r.text('Velocity', x + w/2, y - 15).attr({'text-anchor':'middle'}).css({fontSize:'24px', color:'#444', fontWeight:'600'}).add();
    r.text('127 (forte)', x + w + 14, y + 18).css({fontSize:'20px', color:'#666'}).add();
    r.text('93 (mezzo)', x + w + 14, y + totalH/2 + 6).css({fontSize:'20px', color:'#666'}).add();
    r.text('60 (piano)', x + w + 14, y + totalH - 4).css({fontSize:'20px', color:'#666'}).add();
  }, 100);
})();
</script>
"""

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{xrange_js}</script>
</head>
<body style="margin:0; padding:0; background: #fafafa;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
    {colorbar_js}
</body>
</html>"""

# Save HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Screenshot with Selenium
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")

driver.quit()
Path(temp_path).unlink()
