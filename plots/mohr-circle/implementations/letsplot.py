""" pyplots.ai
mohr-circle: Mohr's Circle for Stress Analysis
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-02-27
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - stress state for a beam under combined loading
sigma_x = 80.0  # MPa, normal stress in x-direction
sigma_y = -30.0  # MPa, normal stress in y-direction
tau_xy = 50.0  # MPa, shear stress on xy-plane

# Mohr's Circle parameters
center = (sigma_x + sigma_y) / 2.0
radius = np.sqrt(((sigma_x - sigma_y) / 2.0) ** 2 + tau_xy**2)
sigma_1 = center + radius  # major principal stress
sigma_2 = center - radius  # minor principal stress
tau_max = radius  # maximum shear stress
theta_p = 0.5 * np.degrees(np.arctan2(2 * tau_xy, sigma_x - sigma_y))

# Circle points
theta = np.linspace(0, 2 * np.pi, 360)
circle_sigma = center + radius * np.cos(theta)
circle_tau = radius * np.sin(theta)
df_circle = pd.DataFrame({"sigma": circle_sigma, "tau": circle_tau})

# Key points
points_data = pd.DataFrame(
    {
        "sigma": [sigma_x, sigma_y, sigma_1, sigma_2, center, center],
        "tau": [tau_xy, -tau_xy, 0.0, 0.0, tau_max, -tau_max],
        "label": [
            f"A (σx, τxy) = ({sigma_x:.0f}, {tau_xy:.0f})",
            f"B (σy, −τxy) = ({sigma_y:.0f}, {-tau_xy:.0f})",
            f"σ₁ = {sigma_1:.1f}",
            f"σ₂ = {sigma_2:.1f}",
            f"τ_max = {tau_max:.1f}",
            f"−τ_max = {-tau_max:.1f}",
        ],
        "type": ["Stress Point", "Stress Point", "Principal", "Principal", "Shear Max", "Shear Max"],
    }
)

# Line from A to B through center (diameter)
df_diameter = pd.DataFrame({"sigma": [sigma_x, sigma_y], "tau": [tau_xy, -tau_xy]})

# Reference lines through center
axis_padding = radius * 0.35
df_hline = pd.DataFrame({"sigma": [center - radius - axis_padding, center + radius + axis_padding], "tau": [0.0, 0.0]})
df_vline = pd.DataFrame({"sigma": [center, center], "tau": [-radius - axis_padding, radius + axis_padding]})

# Angle arc for 2θp
angle_2tp = np.radians(2 * theta_p)
arc_radius = radius * 0.35
arc_theta = np.linspace(0, angle_2tp, 50)
df_arc = pd.DataFrame({"sigma": center + arc_radius * np.cos(arc_theta), "tau": arc_radius * np.sin(arc_theta)})

# Plot
plot = (
    ggplot()  # noqa: F405
    # Reference lines through center
    + geom_line(  # noqa: F405
        data=df_hline,
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#CCCCCC",
        size=0.8,
        linetype="dashed",
    )
    + geom_line(  # noqa: F405
        data=df_vline,
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#CCCCCC",
        size=0.8,
        linetype="dashed",
    )
    # Mohr's Circle
    + geom_path(  # noqa: F405
        data=df_circle,
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#306998",
        size=1.8,
        alpha=0.9,
    )
    # Diameter line from A to B
    + geom_line(  # noqa: F405
        data=df_diameter,
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#666666",
        size=1.0,
        linetype="dashed",
    )
    # Angle arc for 2θp
    + geom_path(  # noqa: F405
        data=df_arc,
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#E07B39",
        size=1.2,
    )
    # Key points
    + geom_point(  # noqa: F405
        data=points_data[points_data["type"] == "Stress Point"],
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#DC2626",
        size=6,
        shape=16,
    )
    + geom_point(  # noqa: F405
        data=points_data[points_data["type"] == "Principal"],
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#16A34A",
        size=6,
        shape=18,
    )
    + geom_point(  # noqa: F405
        data=points_data[points_data["type"] == "Shear Max"],
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#E07B39",
        size=6,
        shape=17,
    )
    # Center point
    + geom_point(  # noqa: F405
        data=pd.DataFrame({"sigma": [center], "tau": [0.0]}),
        mapping=aes(x="sigma", y="tau"),  # noqa: F405
        color="#306998",
        size=5,
        shape=4,
    )
    # Labels for stress points A and B
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Stress Point"].iloc[[0]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#DC2626",
        size=11,
        nudge_y=radius * 0.12,
        nudge_x=-radius * 0.05,
        hjust=1,
    )
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Stress Point"].iloc[[1]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#DC2626",
        size=11,
        nudge_y=-radius * 0.12,
        nudge_x=radius * 0.05,
        hjust=0,
    )
    # Labels for principal stresses
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Principal"].iloc[[0]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#16A34A",
        size=11,
        nudge_y=-radius * 0.12,
        nudge_x=radius * 0.02,
        hjust=0,
    )
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Principal"].iloc[[1]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#16A34A",
        size=11,
        nudge_y=-radius * 0.12,
        nudge_x=-radius * 0.02,
        hjust=1,
    )
    # Labels for max shear
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Shear Max"].iloc[[0]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#E07B39",
        size=11,
        nudge_x=radius * 0.1,
        hjust=0,
    )
    + geom_text(  # noqa: F405
        data=points_data[points_data["type"] == "Shear Max"].iloc[[1]],
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#E07B39",
        size=11,
        nudge_x=radius * 0.1,
        hjust=0,
    )
    # Angle label
    + geom_text(  # noqa: F405
        data=pd.DataFrame(
            {
                "sigma": [center + arc_radius * 1.15 * np.cos(angle_2tp / 2)],
                "tau": [arc_radius * 1.15 * np.sin(angle_2tp / 2)],
                "label": [f"2θp = {2 * theta_p:.1f}°"],
            }
        ),
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#E07B39",
        size=11,
        hjust=0,
    )
    # Center label
    + geom_text(  # noqa: F405
        data=pd.DataFrame({"sigma": [center], "tau": [-radius * 0.12], "label": [f"C ({center:.0f}, 0)"]}),
        mapping=aes(x="sigma", y="tau", label="label"),  # noqa: F405
        color="#306998",
        size=10,
    )
    # Style
    + labs(  # noqa: F405
        x="Normal Stress σ (MPa)", y="Shear Stress τ (MPa)", title="mohr-circle · letsplot · pyplots.ai"
    )
    + coord_fixed()  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        panel_grid_major=element_line(size=0.5, color="#E5E5E5"),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
