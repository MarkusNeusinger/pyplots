"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: altair 6.0.0 | Python 3.14.3
Quality: /100 | Updated: 2026-04-07
"""

import altair as alt
import numpy as np
import pandas as pd
import qrcode


# Data - Generate a real, scannable QR code encoding "https://pyplots.ai"
content = "https://pyplots.ai"

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
qr.add_data(content)
qr.make(fit=True)

# Convert QR code to numpy matrix and add quiet zone
qr_matrix = np.array(qr.get_matrix(), dtype=int)
quiet_zone = 4
padded = np.zeros((qr_matrix.shape[0] + 2 * quiet_zone, qr_matrix.shape[1] + 2 * quiet_zone), dtype=int)
padded[quiet_zone : quiet_zone + qr_matrix.shape[0], quiet_zone : quiet_zone + qr_matrix.shape[1]] = qr_matrix
total_size = padded.shape[0]

# Build DataFrame for Altair (row, col, value)
rows, cols = np.where(np.ones_like(padded, dtype=bool))
module_type = []
for r, c in zip(rows, cols, strict=True):
    qr_r, qr_c = r - quiet_zone, c - quiet_zone
    if qr_r < 0 or qr_r >= qr_matrix.shape[0] or qr_c < 0 or qr_c >= qr_matrix.shape[1]:
        module_type.append("Quiet Zone")
    elif (
        (qr_r < 7 and qr_c < 7)
        or (qr_r < 7 and qr_c >= qr_matrix.shape[1] - 7)
        or (qr_r >= qr_matrix.shape[0] - 7 and qr_c < 7)
    ):
        module_type.append("Finder Pattern")
    elif qr_r == 6 or qr_c == 6:
        module_type.append("Timing Pattern")
    else:
        module_type.append("Data")
data = pd.DataFrame({"x": cols, "y": total_size - 1 - rows, "value": padded[rows, cols], "region": module_type})

# Plot - QR code visualization using mark_rect
chart = (
    alt.Chart(data)
    .mark_rect(stroke=None, strokeWidth=0)
    .encode(
        x=alt.X("x:O", axis=None),
        y=alt.Y("y:O", axis=None),
        color=alt.Color("value:N", scale=alt.Scale(domain=[0, 1], range=["#FFFFFF", "#000000"]), legend=None),
        tooltip=[
            alt.Tooltip("region:N", title="Region"),
            alt.Tooltip("x:O", title="Col"),
            alt.Tooltip("y:O", title="Row"),
        ],
    )
    .properties(
        width=800,
        height=800,
        title=alt.Title("qrcode-basic · altair · pyplots.ai", fontSize=28, anchor="middle", dy=-10),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False)
)

# Save
chart.save("plot.png", scale_factor=4.5)
chart.save("plot.html")
