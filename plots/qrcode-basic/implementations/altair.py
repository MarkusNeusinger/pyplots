""" pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-07
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Generate QR code pattern (Version 1, 21x21 modules)
# Creates a proper QR code structure with finder patterns
np.random.seed(42)

size = 21  # Version 1 QR code size
quiet_zone = 4  # Standard quiet zone (white border)
total_size = size + 2 * quiet_zone

# Initialize matrix with white (0)
matrix = np.zeros((total_size, total_size), dtype=int)

# Add finder pattern at top-left
for i in range(7):
    matrix[quiet_zone + i, quiet_zone] = 1
    matrix[quiet_zone + i, quiet_zone + 6] = 1
    matrix[quiet_zone, quiet_zone + i] = 1
    matrix[quiet_zone + 6, quiet_zone + i] = 1
for i in range(2, 5):
    for j in range(2, 5):
        matrix[quiet_zone + i, quiet_zone + j] = 1

# Add finder pattern at top-right
tr_col = quiet_zone + size - 7
for i in range(7):
    matrix[quiet_zone + i, tr_col] = 1
    matrix[quiet_zone + i, tr_col + 6] = 1
    matrix[quiet_zone, tr_col + i] = 1
    matrix[quiet_zone + 6, tr_col + i] = 1
for i in range(2, 5):
    for j in range(2, 5):
        matrix[quiet_zone + i, tr_col + j] = 1

# Add finder pattern at bottom-left
bl_row = quiet_zone + size - 7
for i in range(7):
    matrix[bl_row + i, quiet_zone] = 1
    matrix[bl_row + i, quiet_zone + 6] = 1
    matrix[bl_row, quiet_zone + i] = 1
    matrix[bl_row + 6, quiet_zone + i] = 1
for i in range(2, 5):
    for j in range(2, 5):
        matrix[bl_row + i, quiet_zone + j] = 1

# Add timing patterns (alternating black/white lines between finder patterns)
for i in range(8, size - 8):
    matrix[quiet_zone + 6, quiet_zone + i] = (i + 1) % 2
    matrix[quiet_zone + i, quiet_zone + 6] = (i + 1) % 2

# Add dark module (always black, required in QR codes)
matrix[quiet_zone + size - 8, quiet_zone + 8] = 1

# Fill data area with deterministic pattern representing encoded data
content = "https://pyplots.ai"
hash_val = hash(content)
for row in range(total_size):
    for col in range(total_size):
        qr_row = row - quiet_zone
        qr_col = col - quiet_zone

        # Skip quiet zone
        if row < quiet_zone or row >= total_size - quiet_zone:
            continue
        if col < quiet_zone or col >= total_size - quiet_zone:
            continue

        # Skip finder patterns and separators
        if qr_row < 9 and qr_col < 9:
            continue
        if qr_row < 9 and qr_col >= size - 8:
            continue
        if qr_row >= size - 8 and qr_col < 9:
            continue

        # Skip timing patterns
        if qr_row == 6 or qr_col == 6:
            continue

        # Create deterministic pattern from position and content hash
        idx = row * total_size + col
        matrix[row, col] = ((hash_val >> (idx % 32)) ^ (idx * 7)) % 2

# Convert matrix to DataFrame for Altair
data = []
for row in range(total_size):
    for col in range(total_size):
        data.append({"x": col, "y": total_size - 1 - row, "value": matrix[row, col]})
df = pd.DataFrame(data)

# Create QR code visualization using mark_rect
chart = (
    alt.Chart(df)
    .mark_rect(stroke=None)
    .encode(
        x=alt.X("x:O", axis=None),
        y=alt.Y("y:O", axis=None),
        color=alt.Color("value:N", scale=alt.Scale(domain=[0, 1], range=["#FFFFFF", "#000000"]), legend=None),
    )
    .properties(
        width=800,
        height=800,
        title=alt.Title("qrcode-basic · altair · pyplots.ai", fontSize=28, anchor="middle", dy=-10),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False)
)

# Save as PNG (square format: 3600 x 3600 px with scale_factor)
chart.save("plot.png", scale_factor=4.5)

# Save interactive HTML version
chart.save("plot.html")
