"""pyplots.ai
skewt-logp-atmospheric: Skew-T Log-P Atmospheric Diagram
Library: lets-plot | Python 3.13
Quality: pending | Created: 2026-01-17
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Atmospheric sounding data (synthetic radiosonde profile)
np.random.seed(42)

# Pressure levels from surface to upper troposphere (hPa)
pressure = np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100])

# Temperature profile (°C) - typical mid-latitude sounding
# Decreasing with height, with a tropopause around 200 hPa
temperature = np.array([25, 22, 18, 14, 10, 6, 2, -3, -8, -14, -21, -29, -38, -47, -55, -58, -56, -55, -56])

# Dewpoint profile (°C) - typically lower than temperature
# Shows moisture decreasing with height
dewpoint = np.array([18, 16, 12, 8, 4, 0, -5, -12, -20, -28, -35, -42, -50, -58, -65, -70, -72, -75, -78])

# For Skew-T: we need to skew the temperature by adding an offset based on pressure
# The skew factor converts the diagram coordinates
# In a Skew-T, x_plot = T + skew_factor * log(p0/p)
p0 = 1000  # Reference pressure
skew_factor = 40  # Degrees of skew per pressure decade

# Calculate skewed coordinates for plotting
log_pressure = np.log10(p0 / pressure)
temp_skewed = temperature + skew_factor * log_pressure
dewpoint_skewed = dewpoint + skew_factor * log_pressure

# Create DataFrame for main profiles
df_temp = pd.DataFrame({"pressure": pressure, "log_p": log_pressure, "value": temp_skewed, "type": "Temperature"})

df_dewpoint = pd.DataFrame({"pressure": pressure, "log_p": log_pressure, "value": dewpoint_skewed, "type": "Dewpoint"})

# Generate isotherms (temperature reference lines, skewed 45 degrees)
isotherm_temps = np.arange(-80, 50, 10)  # °C
isotherm_data = []
p_range = np.array([1000, 100])
for t in isotherm_temps:
    log_p_vals = np.log10(p0 / p_range)
    t_skewed = t + skew_factor * log_p_vals
    isotherm_data.append(
        {"x_start": t_skewed[0], "x_end": t_skewed[1], "y_start": p_range[0], "y_end": p_range[1], "temp": t}
    )
df_isotherms = pd.DataFrame(isotherm_data)

# Generate dry adiabats (lines of constant potential temperature)
# theta = T * (p0/p)^(R/cp) where R/cp ≈ 0.286
dry_adiabat_thetas = np.arange(250, 450, 20)  # K
dry_adiabat_data = []
p_levels = np.linspace(1000, 100, 50)
for theta in dry_adiabat_thetas:
    temps = (theta * (p_levels / p0) ** 0.286) - 273.15  # Convert to Celsius
    log_p_vals = np.log10(p0 / p_levels)
    temps_skewed = temps + skew_factor * log_p_vals
    for i in range(len(p_levels)):
        dry_adiabat_data.append({"pressure": p_levels[i], "temp_skewed": temps_skewed[i], "theta": theta})
df_dry_adiabats = pd.DataFrame(dry_adiabat_data)

# Generate mixing ratio lines (lines of constant water vapor mixing ratio)
# Simplified: ws = 622 * es(T) / (p - es(T)) where es is saturation vapor pressure
mixing_ratios = [1, 2, 4, 7, 10, 15, 20]  # g/kg
mixing_data = []
for ws in mixing_ratios:
    for p in [1000, 700, 500]:
        # Approximate temperature for given mixing ratio and pressure
        # Using simplified formula: T ≈ 35 * log(ws * p / 622) - 20
        t = 35 * np.log10(ws * p / 622) - 20
        log_p_val = np.log10(p0 / p)
        t_skewed = t + skew_factor * log_p_val
        mixing_data.append({"pressure": p, "temp_skewed": t_skewed, "ws": ws})
df_mixing = pd.DataFrame(mixing_data)

# Build the plot using lets-plot
plot = (
    ggplot()
    # Isotherms (skewed temperature lines) - light gray
    + geom_segment(
        aes(x="x_start", xend="x_end", y="y_start", yend="y_end"),
        data=df_isotherms,
        color="#CCCCCC",
        size=0.5,
        alpha=0.7,
    )
    # Dry adiabats - light red/orange dashed
    + geom_path(
        aes(x="temp_skewed", y="pressure", group="theta"),
        data=df_dry_adiabats,
        color="#E07020",
        size=0.5,
        alpha=0.5,
        linetype="dashed",
    )
    # Mixing ratio lines - green dotted
    + geom_path(
        aes(x="temp_skewed", y="pressure", group="ws"),
        data=df_mixing,
        color="#20A020",
        size=0.5,
        alpha=0.5,
        linetype="dotted",
    )
    # Temperature profile - solid red line
    + geom_path(aes(x="value", y="pressure"), data=df_temp, color="#DC2626", size=2)
    # Dewpoint profile - dashed blue line
    + geom_path(aes(x="value", y="pressure"), data=df_dewpoint, color="#306998", size=2, linetype="dashed")
    # Points on profiles for clarity
    + geom_point(aes(x="value", y="pressure"), data=df_temp, color="#DC2626", size=3)
    + geom_point(aes(x="value", y="pressure"), data=df_dewpoint, color="#306998", size=3)
    # Reverse y-axis (pressure decreases upward) and log scale
    + scale_y_reverse()
    + scale_y_log10()
    # Labels and title
    + labs(x="Temperature (°C) - Skewed", y="Pressure (hPa)", title="skewt-logp-atmospheric · letsplot · pyplots.ai")
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
    )
)

# Add annotation for legend-like labels
plot = (
    plot
    + geom_text(x=55, y=150, label="— Temperature", color="#DC2626", size=14, hjust=0)
    + geom_text(x=55, y=180, label="-- Dewpoint", color="#306998", size=14, hjust=0)
    + geom_text(x=55, y=220, label="Dry Adiabats", color="#E07020", size=12, hjust=0)
    + geom_text(x=55, y=270, label="Mixing Ratio", color="#20A020", size=12, hjust=0)
)

# Save the plot
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")
