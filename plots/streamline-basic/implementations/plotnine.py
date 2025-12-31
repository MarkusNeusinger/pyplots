"""pyplots.ai
streamline-basic: Basic Streamline Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_rect,
    element_text,
    geom_path,
    ggplot,
    labs,
    scale_color_gradient,
    theme,
    theme_minimal,
)
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator


# Set seed for reproducibility
np.random.seed(42)

# Create grid for vector field
nx, ny = 40, 40
x = np.linspace(-3, 3, nx)
y = np.linspace(-3, 3, ny)
X, Y = np.meshgrid(x, y)

# Define vector field: vortex flow with a dipole effect
# u = -y, v = x creates circular streamlines (vortex)
U = -Y
V = X

# Create interpolators for the velocity field
u_interp = RegularGridInterpolator((y, x), U, bounds_error=False, fill_value=0)
v_interp = RegularGridInterpolator((y, x), V, bounds_error=False, fill_value=0)


def velocity_field(t, pos):
    """Velocity function for ODE solver."""
    u = u_interp([pos[1], pos[0]])[0]
    v = v_interp([pos[1], pos[0]])[0]
    return [u, v]


# Compute streamlines from various starting points
streamlines_data = []
streamline_id = 0

# Create starting points in a circle around the origin at different radii
radii = [0.5, 1.0, 1.5, 2.0, 2.5]
n_starts_per_radius = 8

for r in radii:
    for i in range(n_starts_per_radius):
        angle = 2 * np.pi * i / n_starts_per_radius
        x0 = r * np.cos(angle)
        y0 = r * np.sin(angle)

        # Integrate forward
        try:
            result = solve_ivp(velocity_field, [0, 6], [x0, y0], max_step=0.05, dense_output=True, events=None)
            if result.success and len(result.t) > 2:
                t_eval = np.linspace(0, result.t[-1], 150)
                trajectory = result.sol(t_eval)

                # Calculate velocity magnitude at each point
                for j in range(len(t_eval)):
                    px, py = trajectory[0, j], trajectory[1, j]
                    # Keep points within bounds
                    if -3 <= px <= 3 and -3 <= py <= 3:
                        speed = np.sqrt(px**2 + py**2)  # For vortex: speed = r
                        streamlines_data.append(
                            {"x": px, "y": py, "streamline": streamline_id, "order": j, "speed": speed}
                        )
                streamline_id += 1
        except Exception:
            pass

# Convert to DataFrame
df = pd.DataFrame(streamlines_data)

# Create the plot using plotnine's native geom_path
plot = (
    ggplot(df, aes(x="x", y="y", group="streamline", color="speed"))
    + geom_path(size=1.2, alpha=0.8)
    + scale_color_gradient(low="#306998", high="#FFD43B", name="Flow Speed")
    + labs(x="X Position", y="Y Position", title="streamline-basic · plotnine · pyplots.ai")
    + coord_fixed(ratio=1)
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
