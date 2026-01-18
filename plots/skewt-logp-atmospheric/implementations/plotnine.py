""" pyplots.ai
skewt-logp-atmospheric: Skew-T Log-P Atmospheric Diagram
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_path,
    geom_segment,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_log10,
    theme,
)


# Skew-T transformation parameters
# The skew angle is 45 degrees, so for every 1 unit increase in log-p, temperature shifts
SKEW_SLOPE = 45  # degrees
SKEW_FACTOR = np.tan(np.radians(SKEW_SLOPE))  # ~1.0 for 45 degrees

# Pressure range (hPa) - log scale with surface at bottom
P_MIN = 100  # Top of diagram (stratosphere)
P_MAX = 1050  # Bottom of diagram (surface)
P_SURFACE = 1000  # Reference pressure

# Temperature range (°C)
T_MIN = -40
T_MAX = 40


# Skew-T transformation functions
def skew_transform(temp, pressure):
    """Transform temperature to skewed x-coordinate based on log pressure."""
    log_p = np.log10(pressure / P_SURFACE)  # Normalized log pressure
    return temp + SKEW_FACTOR * log_p * 40  # Scale factor for visual appearance


# Generate synthetic atmospheric sounding data
np.random.seed(42)

# Pressure levels (typical radiosonde)
pressure_levels = np.array(
    [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150]
)

# Temperature profile (realistic lapse rate with inversion)
# Surface ~25°C, standard lapse rate ~6.5°C/km, with tropopause around 200 hPa
base_temp = 25
temp_profile = []
for p in pressure_levels:
    altitude_km = 44.3308 * (1 - (p / 1013.25) ** 0.190284)  # Barometric formula approx
    if p > 200:  # Troposphere
        t = base_temp - 6.5 * altitude_km + np.random.normal(0, 1)
    else:  # Stratosphere (isothermal/warming)
        t = -55 + (200 - p) * 0.02 + np.random.normal(0, 0.5)
    temp_profile.append(t)
temp_profile = np.array(temp_profile)

# Dewpoint profile (always <= temperature, represents moisture)
# Higher moisture near surface, decreasing with altitude
dewpoint_profile = []
for p, t in zip(pressure_levels, temp_profile, strict=True):
    if p > 700:  # Lower atmosphere - more moist
        depression = 5 + np.random.uniform(0, 5)
    elif p > 400:  # Mid-levels - drier
        depression = 15 + np.random.uniform(0, 10)
    else:  # Upper levels - very dry
        depression = 30 + np.random.uniform(0, 15)
    dp = min(t - depression, t)
    dewpoint_profile.append(dp)
dewpoint_profile = np.array(dewpoint_profile)

# Create reference lines data

# 1. Temperature isotherms (skewed lines at 45 degrees)
isotherm_temps = np.arange(-80, 50, 10)  # Every 10°C
isotherm_data = []
for t_ref in isotherm_temps:
    p_range = np.array([P_MIN, P_MAX])
    x_skewed = skew_transform(np.array([t_ref, t_ref]), p_range)
    isotherm_data.append(
        {"x": x_skewed[0], "xend": x_skewed[1], "y": P_MIN, "yend": P_MAX, "temp": t_ref, "type": "isotherm"}
    )
isotherm_df = pd.DataFrame(isotherm_data)

# 2. Isobars (horizontal pressure lines)
isobar_pressures = [1000, 850, 700, 500, 300, 200, 100]
isobar_data = []
for p in isobar_pressures:
    x_left = skew_transform(T_MIN - 20, p)
    x_right = skew_transform(T_MAX + 20, p)
    isobar_data.append({"x": x_left, "xend": x_right, "y": p, "yend": p, "pressure": p, "type": "isobar"})
isobar_df = pd.DataFrame(isobar_data)

# 3. Dry adiabats (lines of constant potential temperature)
# These curve upward as air rises and cools adiabatically
dry_adiabat_data = []
theta_values = np.arange(-30, 80, 10)  # Potential temperatures
for theta in theta_values:
    points_x = []
    points_y = []
    for p in np.arange(P_MIN, P_MAX + 1, 25):
        # Poisson equation: T = theta * (p/1000)^(R/cp)
        # R/cp ≈ 0.286 for dry air
        t = (theta + 273.15) * (p / 1000) ** 0.286 - 273.15
        x = skew_transform(t, p)
        points_x.append(x)
        points_y.append(p)
    for i in range(len(points_x) - 1):
        dry_adiabat_data.append(
            {
                "x": points_x[i],
                "xend": points_x[i + 1],
                "y": points_y[i],
                "yend": points_y[i + 1],
                "theta": theta,
                "type": "dry_adiabat",
            }
        )
dry_adiabat_df = pd.DataFrame(dry_adiabat_data)

# 4. Moist adiabats (saturated adiabatic lapse rate)
moist_adiabat_data = []
moist_theta_values = np.arange(-20, 40, 10)
for theta_e in moist_theta_values:
    points_x = []
    points_y = []
    t_current = theta_e + 5  # Start warmer than dry
    for p in np.arange(P_MAX, P_MIN - 1, -25):
        x = skew_transform(t_current, p)
        points_x.append(x)
        points_y.append(p)
        # Approximate moist adiabatic lapse rate (varies with temperature)
        if t_current > 0:
            lapse = 5.5  # °C per pressure decrement (approx 500m)
        else:
            lapse = 6.0
        t_current -= lapse * 0.05  # Scale for pressure step
    for i in range(len(points_x) - 1):
        moist_adiabat_data.append(
            {
                "x": points_x[i],
                "xend": points_x[i + 1],
                "y": points_y[i],
                "yend": points_y[i + 1],
                "theta_e": theta_e,
                "type": "moist_adiabat",
            }
        )
moist_adiabat_df = pd.DataFrame(moist_adiabat_data)

# 5. Mixing ratio lines (lines of constant saturation mixing ratio)
mixing_ratio_data = []
mixing_ratios = [1, 2, 4, 7, 10, 15, 20]  # g/kg
for w in mixing_ratios:
    points_x = []
    points_y = []
    for p in np.arange(P_MIN + 50, P_MAX + 1, 25):
        # Approximate dewpoint from mixing ratio: Td ≈ (234.67 * ln(e)) / (17.67 - ln(e))
        # where e = w * p / (622 + w) in hPa
        e = w * p / (622 + w)
        if e > 0:
            td = (243.5 * np.log(e / 6.112)) / (17.67 - np.log(e / 6.112))
            if T_MIN - 20 < td < T_MAX + 20:
                x = skew_transform(td, p)
                points_x.append(x)
                points_y.append(p)
    if len(points_x) > 1:
        for i in range(len(points_x) - 1):
            mixing_ratio_data.append(
                {
                    "x": points_x[i],
                    "xend": points_x[i + 1],
                    "y": points_y[i],
                    "yend": points_y[i + 1],
                    "w": w,
                    "type": "mixing_ratio",
                }
            )
mixing_ratio_df = pd.DataFrame(mixing_ratio_data)

# Create profile data (temperature and dewpoint)
temp_skewed = skew_transform(temp_profile, pressure_levels)
dewpoint_skewed = skew_transform(dewpoint_profile, pressure_levels)

profile_df = pd.DataFrame(
    {
        "pressure": np.concatenate([pressure_levels, pressure_levels]),
        "x": np.concatenate([temp_skewed, dewpoint_skewed]),
        "variable": ["Temperature"] * len(pressure_levels) + ["Dewpoint"] * len(pressure_levels),
    }
)

# Calculate axis limits
x_min = skew_transform(T_MIN - 10, P_MAX)
x_max = skew_transform(T_MAX + 10, P_MIN)

# Build the plot - use profile_df as base to ensure y scale works
plot = (
    ggplot(profile_df, aes(x="x", y="pressure"))
    # Reference lines - drawn first (background)
    # Isobars (horizontal pressure lines) - light gray
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=isobar_df,
        color="#CCCCCC",
        size=0.5,
        linetype="solid",
        inherit_aes=False,
    )
    # Isotherms (skewed temperature lines) - light blue
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=isotherm_df,
        color="#89CFF0",
        size=0.5,
        linetype="solid",
        inherit_aes=False,
    )
    # Dry adiabats - dashed tan/orange
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=dry_adiabat_df,
        color="#D2691E",
        size=0.4,
        linetype="dashed",
        inherit_aes=False,
    )
    # Moist adiabats - dotted green
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=moist_adiabat_df,
        color="#228B22",
        size=0.4,
        linetype="dotted",
        inherit_aes=False,
    )
    # Mixing ratio lines - dashed teal
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=mixing_ratio_df,
        color="#20B2AA",
        size=0.3,
        linetype="dashed",
        inherit_aes=False,
    )
    # Temperature profile - solid red, thick
    + geom_path(aes(color="variable"), data=profile_df[profile_df["variable"] == "Temperature"], size=2.5)
    # Dewpoint profile - dashed blue, thick
    + geom_path(
        aes(color="variable"), data=profile_df[profile_df["variable"] == "Dewpoint"], size=2.5, linetype="dashed"
    )
    # Color scale for profiles
    + scale_color_manual(
        values={"Temperature": "#CC0000", "Dewpoint": "#306998"},  # Red for temp, Python blue for dewpoint
        name="Profile",
    )
    # Logarithmic pressure scale (inverted - high pressure at bottom)
    + scale_y_log10(
        limits=(1100, 90),  # Inverted: surface at bottom, top at 90 hPa
        breaks=[1000, 850, 700, 500, 400, 300, 200, 150, 100],
    )
    # X-axis (skewed temperature coordinates)
    + scale_x_continuous(breaks=[], labels=[], limits=(x_min - 10, x_max + 20))
    + labs(x="Temperature (°C, skewed 45°)", y="Pressure (hPa)", title="skewt-logp-atmospheric · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 16),  # Square for this specialized diagram
        plot_background=element_rect(fill="white"),
        panel_background=element_rect(fill="white"),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        axis_line=element_line(color="#333333", size=1),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_title_x=element_text(margin={"t": 15}),
        axis_title_y=element_text(margin={"r": 15}),
        axis_text_x=element_blank(),  # Hide x-axis labels (skewed coords)
        axis_text_y=element_text(size=18, color="black"),  # Show pressure labels
        plot_title=element_text(size=24, ha="center"),
        legend_position="right",
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_background=element_rect(fill="white", alpha=0.9),
        axis_ticks_major_y=element_line(color="black", size=1),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
