"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
import qrcode
import seaborn as sns


# Generate QR code
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=4)
qr.add_data("https://pyplots.ai")
qr.make(fit=True)

# Get QR code as numpy array (0 = white, 1 = black in QR convention)
# We need to convert the QR image to a matrix
qr_matrix = np.array(qr.get_matrix(), dtype=int)

# Create figure - square format for QR code
fig, ax = plt.subplots(figsize=(12, 12))

# Use seaborn heatmap to display QR code matrix
# Invert colors: QR codes are black on white, so we use a reversed colormap
sns.heatmap(
    qr_matrix,
    ax=ax,
    cmap="Greys",
    square=True,
    cbar=False,
    xticklabels=False,
    yticklabels=False,
    linewidths=0,
    linecolor="white",
)

# Remove axes for clean QR code appearance
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_title("qrcode-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

# Remove axis spines for cleaner look
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
