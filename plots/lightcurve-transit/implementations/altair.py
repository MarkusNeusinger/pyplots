""" pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: altair 6.0.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-18
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - simulated exoplanet transit light curve (phase-folded)
np.random.seed(42)

n_points = 500
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Transit parameters
transit_center = 0.5
transit_width = 0.025
transit_depth = 0.01
limb_u1, limb_u2 = 0.4, 0.2
sharpness = 120

# Smooth transit model: tanh ingress/egress with quadratic limb darkening
dist = np.abs(phase - transit_center)
box = 0.5 * (np.tanh(sharpness * (transit_width - dist)) + 1.0)
mu = np.clip(1.0 - (dist / transit_width) ** 2, 0, 1)
limb = 1.0 - limb_u1 * (1 - mu) - limb_u2 * (1 - mu) ** 2
model_flux = 1.0 - transit_depth * box * limb

# Observed flux with Gaussian noise
flux_err = np.random.uniform(0.0008, 0.0018, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

df = pd.DataFrame(
    {"phase": phase, "flux": flux, "flux_err": flux_err, "flux_upper": flux + flux_err, "flux_lower": flux - flux_err}
)

# Dense model curve for smooth overlay
phase_model = np.linspace(0.0, 1.0, 2000)
dist_m = np.abs(phase_model - transit_center)
box_m = 0.5 * (np.tanh(sharpness * (transit_width - dist_m)) + 1.0)
mu_m = np.clip(1.0 - (dist_m / transit_width) ** 2, 0, 1)
limb_m = 1.0 - limb_u1 * (1 - mu_m) - limb_u2 * (1 - mu_m) ** 2
model_dense = 1.0 - transit_depth * box_m * limb_m

df_model = pd.DataFrame({"phase": phase_model, "model_flux": model_dense})

# Plot
y_scale = alt.Scale(domain=[0.986, 1.006])
y_axis = alt.Axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.2, gridDash=[4, 4], format=".3f")
x_axis = alt.Axis(labelFontSize=18, titleFontSize=22)

# Error bars
error_bars = (
    alt.Chart(df)
    .mark_rule(strokeWidth=1.2, opacity=0.3, color="#306998")
    .encode(
        x=alt.X("phase:Q", title="Orbital Phase", axis=x_axis),
        y=alt.Y("flux_lower:Q", scale=y_scale),
        y2="flux_upper:Q",
    )
)

# Data points
points = (
    alt.Chart(df)
    .mark_circle(size=80, color="#306998", opacity=0.6, stroke="white", strokeWidth=0.5)
    .encode(
        x=alt.X("phase:Q", title="Orbital Phase", axis=x_axis),
        y=alt.Y("flux:Q", title="Relative Flux", scale=y_scale, axis=y_axis),
        tooltip=[
            alt.Tooltip("phase:Q", title="Phase", format=".4f"),
            alt.Tooltip("flux:Q", title="Flux", format=".5f"),
            alt.Tooltip("flux_err:Q", title="Error", format=".5f"),
        ],
    )
)

# Transit model curve
model_line = (
    alt.Chart(df_model)
    .mark_line(strokeWidth=3, color="#E8524A")
    .encode(x=alt.X("phase:Q"), y=alt.Y("model_flux:Q", scale=y_scale))
)

# Layer and configure
chart = (
    alt.layer(error_bars, points, model_line)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("Exoplanet Transit · lightcurve-transit · altair · pyplots.ai", fontSize=28),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
