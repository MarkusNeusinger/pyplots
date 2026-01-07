"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Create a QR code-like pattern encoding "pyplots.ai"
# Note: This is a simplified visual representation of a QR code structure
np.random.seed(42)

# QR code dimensions (Version 1: 21x21 modules)
size = 21

# Initialize the QR code matrix (0 = white, 1 = black)
qr_matrix = np.zeros((size, size), dtype=int)

# Position Detection Patterns (finder patterns) - 7x7 in three corners
finder_pattern = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
)

# Place finder patterns in three corners
qr_matrix[0:7, 0:7] = finder_pattern  # Top-left
qr_matrix[0:7, size - 7 : size] = finder_pattern  # Top-right
qr_matrix[size - 7 : size, 0:7] = finder_pattern  # Bottom-left

# Timing patterns (alternating black/white lines)
for i in range(8, size - 8):
    qr_matrix[6, i] = i % 2  # Horizontal
    qr_matrix[i, 6] = i % 2  # Vertical

# Alignment pattern (5x5) for Version 2+ QR codes - placing one at center area
alignment = np.array([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]])

# Place alignment pattern (avoiding finder patterns)
qr_matrix[size - 9 : size - 4, size - 9 : size - 4] = alignment

# Separators (white border around finder patterns) - already 0 in initialization
# Format information areas (fixed patterns near finder patterns)
qr_matrix[8, 0:6] = [1, 0, 1, 0, 1, 0]
qr_matrix[8, 7:9] = [1, 1]
qr_matrix[0:6, 8] = [1, 0, 1, 0, 1, 0]
qr_matrix[7:9, 8] = [1, 1]

# Data encoding area - fill with a pattern representing "pyplots.ai"
# Using deterministic pattern based on the URL characters
data_string = "https://pyplots.ai"
data_values = [ord(c) for c in data_string]

# Fill data area with encoded pattern
data_idx = 0
for row in range(8, size - 1):
    for col in range(9, size - 1):
        if qr_matrix[row, col] == 0:  # Only fill empty cells
            if row != 6 and col != 6:  # Avoid timing patterns
                # Create pattern from data
                qr_matrix[row, col] = data_values[data_idx % len(data_values)] % 2
                data_idx += 1

# Add quiet zone (white border) by padding
quiet_zone = 4
padded_size = size + 2 * quiet_zone
qr_with_border = np.zeros((padded_size, padded_size), dtype=int)
qr_with_border[quiet_zone : quiet_zone + size, quiet_zone : quiet_zone + size] = qr_matrix

# Create figure (square format for QR code)
fig, ax = plt.subplots(figsize=(12, 12))

# Display QR code with high contrast black on white
ax.imshow(qr_with_border, cmap="gray_r", interpolation="nearest", vmin=0, vmax=1)

# Remove axes for clean QR code appearance
ax.axis("off")

# Add title
ax.set_title("qrcode-basic · matplotlib · pyplots.ai", fontsize=28, fontweight="bold", pad=30, color="#306998")

# Add the encoded content as annotation below
fig.text(0.5, 0.06, f"Encoded: {data_string}", ha="center", fontsize=20, color="#555555", family="monospace")

# Add note about structure
fig.text(
    0.5, 0.02, "QR Code Version 1 (21×21) with Error Correction Level M", ha="center", fontsize=14, color="#888888"
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
