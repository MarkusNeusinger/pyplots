""" pyplots.ai
streamline-basic: Basic Streamline Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seed for reproducibility
np.random.seed(42)

# Vortex flow field: u = -y, v = x (creates circular streamlines)
# Velocity magnitude = distance from center

# Generate streamlines using Euler integration
streamlines_data = []
streamline_id = 0

# Starting points at different radii - fewer inner streamlines to reduce overlap
radii = [0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9]
# Use fewer streamlines at inner radii to prevent crowding
n_per_radius_map = {0.5: 3, 0.9: 4, 1.3: 5, 1.7: 5, 2.1: 6, 2.5: 6, 2.9: 6}
dt = 0.03
max_steps = 250

for r in radii:
    n_per_radius = n_per_radius_map[r]
    for i in range(n_per_radius):
        angle = 2 * np.pi * i / n_per_radius + (r * 0.15)
        x = r * np.cos(angle)
        y = r * np.sin(angle)

        # Trace streamline using Euler integration
        for step in range(max_steps):
            # Check bounds first
            if abs(x) > 3.2 or abs(y) > 3.2:
                break

            # Vector field: circular vortex (u = -y, v = x)
            u = -y
            v = x
            speed = np.sqrt(u**2 + v**2)

            if speed < 1e-6:
                break

            # Store point with velocity magnitude (= radius in vortex)
            vel_mag = np.sqrt(x**2 + y**2)
            streamlines_data.append(
                {
                    "x": float(x),
                    "y": float(y),
                    "streamline_id": streamline_id,
                    "order": step,
                    "velocity": float(vel_mag),
                }
            )

            # Normalize and step
            x = x + dt * u / speed
            y = y + dt * v / speed

        streamline_id += 1

# Create DataFrame
df = pd.DataFrame(streamlines_data)

# Compute average velocity per streamline for color encoding
avg_velocity = df.groupby("streamline_id")["velocity"].mean().reset_index()
avg_velocity.columns = ["streamline_id", "avg_velocity"]
df = df.merge(avg_velocity, on="streamline_id")

# Set seaborn style
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Create square figure to better utilize canvas for equal aspect ratio plot
fig, ax = plt.subplots(figsize=(10, 10))

# Plot streamlines using seaborn's lineplot with hue for velocity
# Each streamline is a separate unit, colored by average velocity
sns.lineplot(
    data=df,
    x="x",
    y="y",
    hue="avg_velocity",
    units="streamline_id",
    estimator=None,
    sort=False,
    linewidth=2.5,
    alpha=0.85,
    palette="viridis",
    legend=False,
    ax=ax,
)

# Add colorbar manually (seaborn lineplot doesn't auto-create one for continuous hue)
norm = plt.Normalize(df["avg_velocity"].min(), df["avg_velocity"].max())
sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.8, aspect=20)
cbar.set_label("Flow Speed (m/s)", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Styling with units on axis labels
ax.set_xlabel("X Position (m)", fontsize=20)
ax.set_ylabel("Y Position (m)", fontsize=20)
ax.set_title("streamline-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.set_aspect("equal")
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
