"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: /100 | Updated: 2026-04-07
"""

import matplotlib.pyplot as plt
import numpy as np
import qrcode
from matplotlib.colors import ListedColormap


# Data - Generate a real, scannable QR code encoding "https://pyplots.ai"
content = "https://pyplots.ai"

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=4)
qr.add_data(content)
qr.make(fit=True)

# Convert QR code to numpy matrix
qr_matrix = np.array(qr.get_matrix(), dtype=int)

# Plot
fig, ax = plt.subplots(figsize=(12, 12), facecolor="white")

# Custom two-color colormap for crisp black-on-white rendering
qr_cmap = ListedColormap(["#FFFFFF", "#1A1A2E"])
ax.imshow(qr_matrix, cmap=qr_cmap, interpolation="nearest", vmin=0, vmax=1, aspect="equal")

# Style
ax.axis("off")
fig.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.12)

ax.set_title(
    "qrcode-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=28, fontweight="bold", pad=30, color="#306998"
)

fig.text(0.5, 0.06, f"Encoded: {content}", ha="center", fontsize=20, color="#555555", family="monospace")

version_info = (
    f"QR Code Version {qr.version} ({qr_matrix.shape[0]}\u00d7{qr_matrix.shape[1]}) \u00b7 Error Correction Level M"
)
fig.text(0.5, 0.02, version_info, ha="center", fontsize=14, color="#888888")

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
