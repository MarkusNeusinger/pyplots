""" pyplots.ai
phase-diagram-pt: Thermodynamic Phase Diagram (Pressure-Temperature)
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-14
"""

import matplotlib.pyplot as plt
import numpy as np


# Data — Water phase diagram (representative real data)
# Triple point: 273.16 K, 611.73 Pa
# Critical point: 647.1 K, 22.064 MPa = 22064000 Pa

triple_T, triple_P = 273.16, 611.73
critical_T, critical_P = 647.1, 22.064e6

# Solid-gas boundary (sublimation curve) — Clausius-Clapeyron approximation
T_solid_gas = np.linspace(200, triple_T, 80)
L_sub = 51059  # J/mol (sublimation enthalpy approx)
R = 8.314
P_solid_gas = triple_P * np.exp((L_sub / R) * (1 / triple_T - 1 / T_solid_gas))

# Liquid-gas boundary (vaporization curve) — from triple point to critical point
T_liquid_gas = np.linspace(triple_T, critical_T, 100)
L_vap = 40670  # J/mol (vaporization enthalpy approx)
P_liquid_gas = triple_P * np.exp((L_vap / R) * (1 / triple_T - 1 / T_liquid_gas))

# Solid-liquid boundary (melting curve) — water has negative slope
# Using Simon equation approximation for ice Ih
T_solid_liquid = np.linspace(triple_T, 250, 80)
P_solid_liquid = triple_P + (T_solid_liquid - triple_T) * (-1.4e7)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(T_solid_gas, P_solid_gas, color="#306998", linewidth=3, zorder=3)
ax.plot(T_liquid_gas, P_liquid_gas, color="#306998", linewidth=3, zorder=3)
ax.plot(T_solid_liquid, P_solid_liquid, color="#306998", linewidth=3, zorder=3)

# Mark triple point and critical point
ax.scatter(triple_T, triple_P, s=250, color="#E74C3C", edgecolors="white", linewidth=1.5, zorder=5)
ax.scatter(critical_T, critical_P, s=250, color="#E74C3C", edgecolors="white", linewidth=1.5, zorder=5)

# Annotate triple point
ax.annotate(
    "Triple Point\n(273.16 K, 611.73 Pa)",
    xy=(triple_T, triple_P),
    xytext=(80, -60),
    textcoords="offset points",
    fontsize=14,
    fontweight="medium",
    color="#333333",
    arrowprops={"arrowstyle": "->", "color": "#666666", "lw": 1.5},
    zorder=6,
)

# Annotate critical point
ax.annotate(
    "Critical Point\n(647.1 K, 22.06 MPa)",
    xy=(critical_T, critical_P),
    xytext=(-120, 50),
    textcoords="offset points",
    fontsize=14,
    fontweight="medium",
    color="#333333",
    arrowprops={"arrowstyle": "->", "color": "#666666", "lw": 1.5},
    zorder=6,
)

# Phase region labels
ax.text(220, 5e6, "SOLID", fontsize=22, fontweight="bold", color="#306998", alpha=0.5, ha="center")
ax.text(400, 5e6, "LIQUID", fontsize=22, fontweight="bold", color="#306998", alpha=0.5, ha="center")
ax.text(550, 50, "GAS", fontsize=22, fontweight="bold", color="#306998", alpha=0.5, ha="center")
ax.text(710, 1.5e8, "SUPERCRITICAL\nFLUID", fontsize=16, fontweight="bold", color="#306998", alpha=0.4, ha="center")

# Style
ax.set_yscale("log")
ax.set_xlim(180, 750)
ax.set_ylim(10, 5e8)
ax.set_xlabel("Temperature (K)", fontsize=20)
ax.set_ylabel("Pressure (Pa)", fontsize=20)
ax.set_title("Water Phase Diagram · phase-diagram-pt · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.15, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
