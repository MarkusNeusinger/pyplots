"""pyplots.ai
line-3d-trajectory: 3D Line Plot for Trajectory Visualization
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection


# Data - Lorenz attractor trajectory
np.random.seed(42)

# Lorenz system parameters
sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

# Integrate Lorenz system using Euler method
dt = 0.01
num_steps = 5000
trajectory = np.zeros((num_steps, 3))
trajectory[0] = [1.0, 1.0, 1.0]

for i in range(1, num_steps):
    x_prev, y_prev, z_prev = trajectory[i - 1]
    dx = sigma * (y_prev - x_prev)
    dy = x_prev * (rho - z_prev) - y_prev
    dz = x_prev * y_prev - beta * z_prev
    trajectory[i] = trajectory[i - 1] + np.array([dx, dy, dz]) * dt

x = trajectory[:, 0]
y = trajectory[:, 1]
z = trajectory[:, 2]

# Color based on time progression
time = np.linspace(0, 1, num_steps)

# Plot - 3D trajectory
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection="3d")

# Create line segments with color gradient for time progression
points = np.array([x, y, z]).T.reshape(-1, 1, 3)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create color array based on time
cmap = plt.cm.viridis
colors = cmap(time[:-1])

lc = Line3DCollection(segments, colors=colors, linewidths=2)
ax.add_collection3d(lc)

# Set axis limits
ax.set_xlim(x.min() - 2, x.max() + 2)
ax.set_ylim(y.min() - 2, y.max() + 2)
ax.set_zlim(z.min() - 2, z.max() + 2)

# Labels and styling
ax.set_xlabel("X Position", fontsize=18, labelpad=12)
ax.set_ylabel("Y Position", fontsize=18, labelpad=12)
ax.set_zlabel("Z Position", fontsize=18, labelpad=12)
ax.set_title("Lorenz Attractor · line-3d-trajectory · matplotlib · pyplots.ai", fontsize=22, pad=20)
ax.tick_params(axis="both", labelsize=14)

# Add colorbar for time progression
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=20, pad=0.1)
cbar.set_label("Time Progression", fontsize=16)
cbar.ax.tick_params(labelsize=14)

# Adjust viewing angle for better perspective
ax.view_init(elev=25, azim=45)

# Style the 3D panes
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("gray")
ax.yaxis.pane.set_edgecolor("gray")
ax.zaxis.pane.set_edgecolor("gray")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
