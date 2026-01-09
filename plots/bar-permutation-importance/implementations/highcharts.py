"""pyplots.ai
bar-permutation-importance: Permutation Feature Importance Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


# Data - Calculate permutation importance on breast cancer dataset
np.random.seed(42)
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a simple model
model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Calculate permutation importance
perm_importance = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1)

# Get top 15 features sorted by importance
importance_mean = perm_importance.importances_mean
importance_std = perm_importance.importances_std
sorted_idx = np.argsort(importance_mean)[::-1][:15]

features = [str(feature_names[i]) for i in sorted_idx]
means = [float(importance_mean[i]) for i in sorted_idx]
stds = [float(importance_std[i]) for i in sorted_idx]

# Reverse for horizontal bar chart (highest at top)
features = features[::-1]
means = means[::-1]
stds = stds[::-1]

# Create color gradient based on importance (blue shades)
max_imp = max(means) if max(means) > 0 else 1
colors = []
for m in means:
    ratio = m / max_imp if max_imp > 0 else 0
    # Gradient from light (#c8d4e0) to Python Blue (#306998)
    r = int(48 + (200 - 48) * (1 - ratio))
    g = int(105 + (212 - 105) * (1 - ratio))
    b = int(152 + (224 - 152) * (1 - ratio))
    colors.append(f"rgb({r},{g},{b})")

# Prepare data for chart
bar_data = [{"y": round(m, 4), "color": c} for m, c in zip(means, colors, strict=True)]
error_data = [[round(m - s, 4), round(m + s, 4)] for m, s in zip(means, stds, strict=True)]

# Download Highcharts JS and highcharts-more for error bars
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Build chart configuration as JSON
chart_config = {
    "chart": {
        "type": "bar",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginLeft": 420,
        "marginRight": 120,
        "marginTop": 140,
        "marginBottom": 180,
    },
    "title": {
        "text": "bar-permutation-importance \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "52px", "fontWeight": "bold"},
        "margin": 40,
    },
    "xAxis": {
        "categories": features,
        "title": {"text": "Feature", "style": {"fontSize": "36px", "fontWeight": "bold"}, "margin": 20},
        "labels": {"style": {"fontSize": "28px"}},
        "lineWidth": 2,
        "lineColor": "#333333",
    },
    "yAxis": {
        "title": {"text": "Mean Accuracy Decrease", "style": {"fontSize": "36px", "fontWeight": "bold"}, "margin": 30},
        "labels": {"style": {"fontSize": "24px"}, "format": "{value:.3f}"},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dash",
        "gridLineColor": "#cccccc",
        "tickInterval": 0.002,
        "plotLines": [{"value": 0, "color": "#333333", "width": 3, "zIndex": 5, "dashStyle": "Solid"}],
    },
    "legend": {"enabled": False},
    "tooltip": {
        "style": {"fontSize": "24px"},
        "headerFormat": "<b>{point.key}</b><br/>",
        "pointFormat": "Importance: {point.y:.4f}",
    },
    "plotOptions": {
        "bar": {"pointPadding": 0.05, "groupPadding": 0.1, "borderWidth": 1, "borderColor": "#666666"},
        "errorbar": {"lineWidth": 4, "color": "#333333", "whiskerLength": "50%", "whiskerWidth": 4},
    },
    "series": [
        {"name": "Importance", "type": "bar", "data": bar_data, "colorByPoint": True},
        {"name": "Error", "type": "errorbar", "data": error_data},
    ],
    "credits": {"enabled": False},
}

chart_json = json.dumps(chart_config)

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {chart_json});
    </script>
</body>
</html>"""

# Save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Get the container element and take screenshot of just the chart area
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
