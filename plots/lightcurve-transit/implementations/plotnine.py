"""pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 83/100 | Created: 2026-03-18
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_text,
    geom_line,
    geom_linerange,
    geom_point,
    geom_ribbon,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)
n_points = 400
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

transit_center = 0.5
transit_half_dur = 0.04
ingress_half = 0.01
transit_depth = 0.012
u1, u2 = 0.4, 0.1


def compute_transit(phases, center, half_dur, ing_half, depth, u1, u2):
    """Vectorized transit model with quadratic limb darkening."""
    model = np.ones_like(phases)
    dist = np.abs(phases - center)
    full_transit = dist < half_dur - ing_half
    ingress = (dist >= half_dur - ing_half) & (dist < half_dur + ing_half)
    r = np.clip(dist / half_dur, 0, 1)
    mu = np.sqrt(np.maximum(1 - r**2, 0))
    limb = 1 - u1 * (1 - mu) - u2 * (1 - mu) ** 2
    model[full_transit] = 1.0 - depth * limb[full_transit]
    frac = (half_dur + ing_half - dist[ingress]) / (2 * ing_half)
    frac = 3 * frac**2 - 2 * frac**3
    model[ingress] = 1.0 - depth * limb[ingress] * frac
    return model


transit_model = compute_transit(phase, transit_center, transit_half_dur, ingress_half, transit_depth, u1, u2)
flux_err = np.random.uniform(0.0008, 0.0025, n_points)
flux = transit_model + np.random.normal(0, 1, n_points) * flux_err

phase_fine = np.linspace(0.0, 1.0, 2000)
model_fine = compute_transit(phase_fine, transit_center, transit_half_dur, ingress_half, transit_depth, u1, u2)

# Model uncertainty ribbon (simulate photon noise envelope)
model_upper = model_fine + 0.0012
model_lower = model_fine - 0.0012

df_obs = pd.DataFrame({"phase": phase, "flux": flux, "flux_err": flux_err, "series": "Observations"})

df_model = pd.DataFrame(
    {"phase": phase_fine, "flux": model_fine, "upper": model_upper, "lower": model_lower, "series": "Transit Model"}
)

# Transit depth annotation
min_model = model_fine.min()
depth_pct = (1.0 - min_model) * 100

# Plot
plot = (
    ggplot()
    + geom_ribbon(aes(x="phase", ymin="lower", ymax="upper"), data=df_model, fill="#d4a373", alpha=0.15)
    + geom_linerange(
        aes(x="phase", ymin="flux - flux_err", ymax="flux + flux_err"),
        data=df_obs,
        color="#8fb8de",
        alpha=0.35,
        size=0.3,
    )
    + geom_point(aes(x="phase", y="flux", color="series"), data=df_obs, alpha=0.65, size=2.5, stroke=0)
    + geom_line(aes(x="phase", y="flux", color="series"), data=df_model, size=1.8)
    + scale_color_manual(name="", values={"Observations": "#306998", "Transit Model": "#c46210"})
    + annotate(
        "text",
        x=0.62,
        y=min_model - 0.001,
        label=f"Depth: {depth_pct:.2f}%",
        size=14,
        color="#5a3e1b",
        fontstyle="italic",
    )
    + annotate(
        "segment", x=0.54, xend=0.54, y=1.0, yend=min_model, color="#5a3e1b", size=0.5, linetype="dashed", alpha=0.6
    )
)

# Style
plot = (
    plot
    + labs(x="Orbital Phase", y="Relative Flux", title="lightcurve-transit · plotnine · pyplots.ai")
    + scale_x_continuous(breaks=np.arange(0, 1.1, 0.1))
    + scale_y_continuous(labels=lambda lst: [f"{v:.3f}" for v in lst])
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold", margin={"b": 15}),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=16),
        legend_position=(0.85, 0.95),
        legend_background=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", alpha=0.25, size=0.4),
        plot_background=element_blank(),
        panel_background=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
