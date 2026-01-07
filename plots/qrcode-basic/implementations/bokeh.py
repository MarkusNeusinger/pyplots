"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import numpy as np
import qrcode
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - URL to encode
content = "https://pyplots.ai"
error_correction = qrcode.constants.ERROR_CORRECT_M  # 15% error correction

# Generate QR code matrix
qr = qrcode.QRCode(
    version=1,
    error_correction=error_correction,
    box_size=1,
    border=4,  # Quiet zone for reliable scanning
)
qr.add_data(content)
qr.make(fit=True)

# Get QR code as numpy array (True = black, False = white)
qr_matrix = np.array(qr.get_matrix())
size = qr_matrix.shape[0]

# Create coordinates for black squares
black_x = []
black_y = []
for i in range(size):
    for j in range(size):
        if qr_matrix[i, j]:
            # Flip y-axis so QR code is oriented correctly (top-left origin)
            black_x.append(j + 0.5)
            black_y.append(size - i - 0.5)

source = ColumnDataSource(data={"x": black_x, "y": black_y})

# Create plot - square format for QR code (3600x3600)
p = figure(
    width=3600,
    height=3600,
    title="qrcode-basic · bokeh · pyplots.ai",
    x_range=(0, size),
    y_range=(0, size),
    tools="",
    toolbar_location=None,
    match_aspect=True,
)

# Style the figure - clean white background
p.background_fill_color = "white"
p.border_fill_color = "white"
p.outline_line_color = None

# Hide axes for clean QR code appearance
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False

# Title styling
p.title.text_font_size = "36pt"
p.title.align = "center"
p.title.text_color = "#306998"  # Python Blue

# Draw QR code using squares (rect glyph)
# Each module is a unit square
p.rect(
    x="x",
    y="y",
    width=1,
    height=1,
    source=source,
    fill_color="#000000",  # Black modules
    line_color=None,
)

# Add subtle border around the QR code area
p.rect(
    x=size / 2, y=size / 2, width=size, height=size, fill_color=None, line_color="#306998", line_width=3, line_alpha=0.5
)

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactive viewing
output_file("plot.html", title="QR Code - pyplots.ai")
save(p)
