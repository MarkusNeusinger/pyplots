"""
line-basic: Basic Line Plot
Library: bokeh
"""

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

source = ColumnDataSource(data={"x": data["time"], "y": data["value"]})

# Create figure
p = figure(width=4800, height=2700, title="Basic Line Plot", x_axis_label="Time", y_axis_label="Value")

# Plot line
p.line(x="x", y="y", source=source, line_width=2, line_color="#306998")

# Add markers at data points
p.scatter(x="x", y="y", source=source, size=8, color="#306998")

# Styling
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.grid.grid_line_alpha = 0.3

# Setup Chrome/Chromium webdriver for PNG export
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# Use system chromedriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Save
export_png(p, filename="plot.png", webdriver=driver)
driver.quit()
