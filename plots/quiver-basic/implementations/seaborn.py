"""
quiver-basic: Basic Quiver Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Data: Create a 15x15 grid for the vector field
np.random.seed(42)
n = 15
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

# Vector field: circular rotation pattern (u = -y, v = x)
U = -Y
V = X

# Calculate magnitude for color mapping
magnitude = np.sqrt(U**2 + V**2)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Create quiver plot with color mapped to magnitude
quiver = ax.quiver(
    X, Y, U, V, magnitude, cmap="viridis", scale=25, width=0.008, headwidth=4, headlength=5, headaxislength=4.5
)

# Add colorbar to show magnitude scale
cbar = plt.colorbar(quiver, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("Vector Magnitude", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and styling
ax.set_xlabel("X", fontsize=20)
ax.set_ylabel("Y", fontsize=20)
ax.set_title("quiver-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
