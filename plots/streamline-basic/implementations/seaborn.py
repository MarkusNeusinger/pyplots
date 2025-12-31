""" pyplots.ai
streamline-basic: Basic Streamline Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 35/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")

# Data: Create a vortex flow field
# Grid coordinates
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)
X, Y = np.meshgrid(x, y)

# Vortex flow: u = -y, v = x creates circular streamlines
# Adding a slight radial component for visual interest
r = np.sqrt(X**2 + Y**2) + 0.1  # Avoid division by zero
u = -Y / r
v = X / r

# Velocity magnitude for coloring
magnitude = np.sqrt(u**2 + v**2)

# Create plot (landscape format for vector field)
fig, ax = plt.subplots(figsize=(16, 9))

# Create streamline plot using matplotlib (seaborn provides styling)
# Color by velocity magnitude using a colorblind-safe palette
stream = ax.streamplot(
    X, Y, u, v, color=magnitude, cmap="viridis", linewidth=2.5, density=1.8, arrowsize=2.0, arrowstyle="->"
)

# Add colorbar for velocity magnitude
cbar = plt.colorbar(stream.lines, ax=ax, shrink=0.85, aspect=30, pad=0.02)
cbar.set_label("Velocity Magnitude", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Styling
ax.set_xlabel("X Position", fontsize=20)
ax.set_ylabel("Y Position", fontsize=20)
ax.set_title("streamline-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3, linestyle="--")

# Set axis limits to show full field
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
