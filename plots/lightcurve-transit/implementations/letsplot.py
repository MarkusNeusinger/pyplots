""" pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-18
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_errorbar,
    geom_line,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - simulated exoplanet transit (phase-folded)
np.random.seed(42)
n_points = 400
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Transit parameters
transit_center = 0.5
transit_duration = 0.08
transit_depth = 0.01
ingress_duration = 0.015

# Generate model flux with quadratic limb darkening
model_flux = np.ones(n_points)
for i, p in enumerate(phase):
    dist = abs(p - transit_center)
    half_dur = transit_duration / 2
    half_ingress = ingress_duration / 2
    if dist < half_dur - half_ingress:
        # Full transit - apply limb darkening shape
        r = dist / (half_dur - half_ingress)
        limb = 1 - 0.3 * (1 - np.sqrt(1 - r**2))
        model_flux[i] = 1.0 - transit_depth * limb
    elif dist < half_dur + half_ingress:
        # Ingress/egress
        frac = (half_dur + half_ingress - dist) / (2 * half_ingress)
        model_flux[i] = 1.0 - transit_depth * frac

# Add noise to create observed flux
flux_err = np.random.uniform(0.001, 0.003, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

# Create smooth model curve
phase_model = np.linspace(0.0, 1.0, 1000)
model_smooth = np.ones(1000)
for i, p in enumerate(phase_model):
    dist = abs(p - transit_center)
    half_dur = transit_duration / 2
    half_ingress = ingress_duration / 2
    if dist < half_dur - half_ingress:
        r = dist / (half_dur - half_ingress)
        limb = 1 - 0.3 * (1 - np.sqrt(1 - r**2))
        model_smooth[i] = 1.0 - transit_depth * limb
    elif dist < half_dur + half_ingress:
        frac = (half_dur + half_ingress - dist) / (2 * half_ingress)
        model_smooth[i] = 1.0 - transit_depth * frac

# DataFrames
df_obs = pd.DataFrame(
    {
        "phase": phase,
        "flux": flux,
        "flux_err": flux_err,
        "ymin": flux - flux_err,
        "ymax": flux + flux_err,
        "series": "Observations",
    }
)

df_model = pd.DataFrame({"phase": phase_model, "flux": model_smooth, "series": "Transit Model"})

# Plot
plot = (
    ggplot()
    + geom_errorbar(
        aes(x="phase", ymin="ymin", ymax="ymax"), data=df_obs, color="#8FAFC8", alpha=0.4, size=0.5, width=0.0
    )
    + geom_point(aes(x="phase", y="flux"), data=df_obs, color="#306998", size=3, alpha=0.7)
    + geom_line(aes(x="phase", y="flux"), data=df_model, color="#E8442A", size=2)
    + scale_x_continuous(name="Orbital Phase", breaks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    + scale_y_continuous(name="Relative Flux")
    + labs(title="Exoplanet Transit · lightcurve-transit · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.5),
        axis_ticks=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", scale=3, path=".")
ggsave(plot, "plot.html", path=".")
