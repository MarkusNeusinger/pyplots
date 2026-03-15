"""pyplots.ai
psychrometric-basic: Psychrometric Chart for HVAC
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-15
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


# Constants
P_ATM = 101325  # Pa, standard atmosphere
np.random.seed(42)


# Psychrometric calculations (ASHRAE formulas)
def saturation_pressure(t):
    """Antoine-like saturation pressure (Pa) for water vapor."""
    if np.isscalar(t):
        t = np.array([t])
    result = np.where(t >= 0, np.exp(23.196 - 3816.44 / (t + 227.02)), np.exp(23.33 - 3841.0 / (t + 231.0)))
    return result


def humidity_ratio_from_rh(t, rh):
    """Humidity ratio (kg/kg) from dry-bulb temp (C) and RH (0-1)."""
    p_sat = saturation_pressure(t)
    p_w = rh * p_sat
    w = 0.62198 * p_w / (P_ATM - p_w)
    return w * 1000  # g/kg


def wet_bulb_line(t_wb, t_db_range):
    """Approximate humidity ratio along a constant wet-bulb line."""
    w_sat = humidity_ratio_from_rh(t_wb, 1.0)
    slope = -1.006 / 2501  # cp_air / h_fg approximation (kg/kg per C)
    w = w_sat + slope * (t_db_range - t_wb) * 1000  # g/kg
    return w


def specific_volume(t, w_gkg):
    """Specific volume (m3/kg) from dry-bulb temp and humidity ratio."""
    w = w_gkg / 1000  # convert to kg/kg
    return 0.287042 * (t + 273.15) * (1 + 1.6078 * w) / (P_ATM / 1000)


def enthalpy(t, w_gkg):
    """Enthalpy (kJ/kg) from dry-bulb temp and humidity ratio."""
    w = w_gkg / 1000
    return 1.006 * t + w * (2501 + 1.86 * t)


# Data ranges
t_db = np.linspace(-10, 50, 500)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Colors
rh_color = "#306998"
wb_color = "#7B68AE"
enthalpy_color = "#C0392B"
sv_color = "#27AE60"
comfort_color = "#306998"
process_color = "#E67E22"

# Relative humidity curves (10% to 100%)
rh_values = np.arange(0.1, 1.01, 0.1)
for rh in rh_values:
    w = humidity_ratio_from_rh(t_db, rh)
    mask = (w >= 0) & (w <= 30)
    lw = 2.5 if rh == 1.0 else 1.2
    alpha = 1.0 if rh == 1.0 else 0.7
    ax.plot(t_db[mask], w[mask], color=rh_color, linewidth=lw, alpha=alpha)

    # Label RH curves
    label_t = 40 - int(rh * 15)
    if label_t < -10:
        label_t = -5
    w_label = float(humidity_ratio_from_rh(label_t, rh).item())
    if 0 < w_label < 30:
        label_text = f"{int(rh * 100)}%"
        ax.text(
            label_t,
            w_label + 0.3,
            label_text,
            fontsize=9,
            color=rh_color,
            alpha=0.85,
            ha="center",
            va="bottom",
            fontweight="bold",
        )

# Wet-bulb temperature lines
wb_temps = np.arange(0, 35, 5)
for t_wb in wb_temps:
    t_range = np.linspace(t_wb, min(t_wb + 35, 50), 200)
    w_wb = wet_bulb_line(t_wb, t_range)
    w_sat_limit = humidity_ratio_from_rh(t_range, 1.0)
    mask = (w_wb >= 0) & (w_wb <= w_sat_limit) & (w_wb <= 30)
    if np.any(mask):
        ax.plot(t_range[mask], w_wb[mask], color=wb_color, linewidth=0.8, alpha=0.5, linestyle="--")
        valid_t = t_range[mask]
        valid_w = w_wb[mask]
        if len(valid_t) > 0:
            ax.text(
                float(valid_t[-1]),
                max(float(valid_w[-1]) - 0.5, 0.2),
                f"{t_wb}°C",
                fontsize=7,
                color=wb_color,
                alpha=0.7,
                ha="left",
                va="top",
            )

# Specific volume lines
sv_values = np.arange(0.78, 0.96, 0.02)
for sv_target in sv_values:
    t_range = np.linspace(-10, 50, 200)
    w_for_sv = []
    for t in t_range:
        w_trial = np.linspace(0, 30, 200)
        sv_trial = specific_volume(t, w_trial)
        idx = np.argmin(np.abs(sv_trial - sv_target))
        w_for_sv.append(w_trial[idx])
    w_for_sv = np.array(w_for_sv)
    w_sat_limit = humidity_ratio_from_rh(t_range, 1.0)
    mask = (w_for_sv >= 0) & (w_for_sv <= 30) & (w_for_sv <= w_sat_limit)
    if np.sum(mask) > 10:
        ax.plot(t_range[mask], w_for_sv[mask], color=sv_color, linewidth=0.6, alpha=0.4, linestyle=":")
        valid_t = t_range[mask]
        valid_w = w_for_sv[mask]
        mid = len(valid_t) // 3
        if mid > 0:
            ax.text(
                valid_t[mid],
                valid_w[mid],
                f"{sv_target:.2f}",
                fontsize=6,
                color=sv_color,
                alpha=0.6,
                ha="center",
                va="bottom",
                rotation=-75,
            )

# Enthalpy lines
h_values = np.arange(10, 120, 10)
for h_target in h_values:
    t_range = np.linspace(-10, 50, 200)
    w_for_h = (h_target - 1.006 * t_range) / (2.501 + 0.00186 * t_range)
    w_sat_limit = humidity_ratio_from_rh(t_range, 1.0)
    mask = (w_for_h >= 0) & (w_for_h <= 30) & (w_for_h <= w_sat_limit)
    if np.sum(mask) > 5:
        ax.plot(t_range[mask], w_for_h[mask], color=enthalpy_color, linewidth=0.6, alpha=0.35, linestyle="-.")
        valid_t = t_range[mask]
        valid_w = w_for_h[mask]
        if len(valid_t) > 0:
            ax.text(
                valid_t[0],
                valid_w[0] + 0.3,
                f"{h_target}",
                fontsize=6,
                color=enthalpy_color,
                alpha=0.6,
                ha="right",
                va="bottom",
                rotation=-35,
            )

# Comfort zone (20-26°C, 30-60% RH)
comfort_t = np.array([20, 26, 26, 20, 20])
comfort_w = np.array(
    [
        humidity_ratio_from_rh(20, 0.30).item(),
        humidity_ratio_from_rh(26, 0.30).item(),
        humidity_ratio_from_rh(26, 0.60).item(),
        humidity_ratio_from_rh(20, 0.60).item(),
        humidity_ratio_from_rh(20, 0.30).item(),
    ]
)
ax.fill(comfort_t, comfort_w, alpha=0.12, color=comfort_color, zorder=2)
ax.plot(comfort_t, comfort_w, color=comfort_color, linewidth=1.5, alpha=0.5, linestyle="-", zorder=2)
comfort_center_t = 23
comfort_center_w = (comfort_w[0] + comfort_w[2]) / 2
ax.text(
    comfort_center_t,
    comfort_center_w,
    "Comfort\nZone",
    fontsize=10,
    color=comfort_color,
    ha="center",
    va="center",
    fontweight="bold",
    alpha=0.7,
)

# HVAC process path: cooling and dehumidification (35°C, 50% RH → 24°C, 50% RH)
state1_t, state1_rh = 35, 0.50
state2_t, state2_rh = 13, 1.0
state3_t, state3_rh = 24, 0.50

state1_w = humidity_ratio_from_rh(state1_t, state1_rh).item()
state2_w = humidity_ratio_from_rh(state2_t, state2_rh).item()
state3_w = humidity_ratio_from_rh(state3_t, state3_rh).item()

# Cool to saturation, then reheat
ax.annotate(
    "",
    xy=(state2_t, state2_w),
    xytext=(state1_t, state1_w),
    arrowprops={"arrowstyle": "->", "color": process_color, "lw": 2.5},
    zorder=5,
)
ax.annotate(
    "",
    xy=(state3_t, state3_w),
    xytext=(state2_t, state2_w),
    arrowprops={"arrowstyle": "->", "color": process_color, "lw": 2.5},
    zorder=5,
)

ax.plot(state1_t, state1_w, "o", color=process_color, markersize=8, zorder=6)
ax.plot(state2_t, state2_w, "o", color=process_color, markersize=8, zorder=6)
ax.plot(state3_t, state3_w, "o", color=process_color, markersize=8, zorder=6)

ax.text(state1_t + 0.5, state1_w + 0.8, "A (35°C, 50%)", fontsize=9, color=process_color, fontweight="bold")
ax.text(state2_t - 5, state2_w + 0.5, "B (13°C, 100%)", fontsize=9, color=process_color, fontweight="bold")
ax.text(state3_t + 0.5, state3_w + 0.8, "C (24°C, 50%)", fontsize=9, color=process_color, fontweight="bold")

# Legend for line types
legend_elements = [
    Line2D([0], [0], color=rh_color, linewidth=2, label="Relative Humidity"),
    Line2D([0], [0], color=wb_color, linewidth=1, linestyle="--", label="Wet-Bulb Temp"),
    Line2D([0], [0], color=enthalpy_color, linewidth=1, linestyle="-.", label="Enthalpy (kJ/kg)"),
    Line2D([0], [0], color=sv_color, linewidth=1, linestyle=":", label="Specific Volume (m³/kg)"),
    Line2D([0], [0], color=process_color, linewidth=2.5, marker="o", markersize=6, label="HVAC Process Path"),
]
ax.legend(handles=legend_elements, loc="upper left", fontsize=11, framealpha=0.9, edgecolor="#cccccc")

# Style
ax.set_xlim(-10, 50)
ax.set_ylim(0, 30)
ax.set_xlabel("Dry-Bulb Temperature (°C)", fontsize=20)
ax.set_ylabel("Humidity Ratio (g/kg dry air)", fontsize=20)
ax.set_title("psychrometric-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.15, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
