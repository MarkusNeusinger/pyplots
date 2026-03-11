""" pyplots.ai
scatter-ashby-material: Ashby Material Selection Chart
Library: altair 6.0.0 | Python 3.14.3
Quality: 76/100 | Created: 2026-03-11
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

families = {
    "Metals": {
        "density": (2700, 8900),
        "modulus": (45, 400),
        "materials": [
            "Aluminum",
            "Steel",
            "Titanium",
            "Copper",
            "Nickel",
            "Zinc",
            "Magnesium",
            "Brass",
            "Bronze",
            "Tungsten",
            "Cast Iron",
            "Stainless Steel",
            "Inconel",
            "Tin",
        ],
    },
    "Polymers": {
        "density": (900, 1500),
        "modulus": (0.2, 4.0),
        "materials": [
            "Polyethylene",
            "Polypropylene",
            "PVC",
            "Nylon",
            "Polycarbonate",
            "ABS",
            "PMMA",
            "PET",
            "Polystyrene",
            "PTFE",
            "Epoxy",
            "Polyurethane",
        ],
    },
    "Ceramics": {
        "density": (2200, 6000),
        "modulus": (70, 450),
        "materials": [
            "Alumina",
            "Silicon Carbide",
            "Zirconia",
            "Silicon Nitride",
            "Glass",
            "Porcelain",
            "Boron Carbide",
            "Tungsten Carbide",
            "Silica",
            "Magnesia",
        ],
    },
    "Composites": {
        "density": (1400, 2200),
        "modulus": (15, 200),
        "materials": [
            "CFRP",
            "GFRP",
            "Kevlar Composite",
            "Boron-Epoxy",
            "Wood-Polymer",
            "Metal Matrix",
            "Ceramic Matrix",
            "Carbon-Carbon",
            "Basalt Fiber",
        ],
    },
    "Elastomers": {
        "density": (900, 1300),
        "modulus": (0.001, 0.1),
        "materials": [
            "Natural Rubber",
            "Silicone",
            "Neoprene",
            "Butyl Rubber",
            "EPDM",
            "Nitrile Rubber",
            "Polyisoprene",
            "SBR",
        ],
    },
    "Foams": {
        "density": (20, 500),
        "modulus": (0.001, 1.0),
        "materials": [
            "Polyurethane Foam",
            "Polystyrene Foam",
            "PVC Foam",
            "Metal Foam",
            "Cork",
            "Ceramic Foam",
            "Phenolic Foam",
            "Melamine Foam",
        ],
    },
}

rows = []
for family, props in families.items():
    d_lo, d_hi = props["density"]
    m_lo, m_hi = props["modulus"]
    for mat in props["materials"]:
        log_d = np.random.uniform(np.log10(d_lo), np.log10(d_hi))
        log_m = np.random.uniform(np.log10(m_lo), np.log10(m_hi))
        density = 10**log_d
        modulus = 10**log_m
        rows.append({"material": mat, "family": family, "density": round(density, 1), "modulus": round(modulus, 4)})

df = pd.DataFrame(rows)

family_centers = (
    df.groupby("family")
    .agg(
        density_center=("density", lambda x: 10 ** np.mean(np.log10(x))),
        modulus_center=("modulus", lambda x: 10 ** np.mean(np.log10(x))),
    )
    .reset_index()
)

# Colors
palette = ["#306998", "#E8833A", "#2A9D8F", "#E76F51", "#7B68AE", "#8AB17D"]
family_order = ["Metals", "Polymers", "Ceramics", "Composites", "Elastomers", "Foams"]

# Plot
points = (
    alt.Chart(df)
    .mark_circle(opacity=0.75, stroke="white", strokeWidth=0.8)
    .encode(
        x=alt.X("density:Q", scale=alt.Scale(type="log", domain=[10, 20000]), title="Density (kg/m\u00b3)"),
        y=alt.Y("modulus:Q", scale=alt.Scale(type="log", domain=[0.0005, 1000]), title="Young's Modulus (GPa)"),
        color=alt.Color(
            "family:N",
            scale=alt.Scale(domain=family_order, range=palette),
            legend=alt.Legend(
                title="Material Family", titleFontSize=18, labelFontSize=16, symbolSize=300, orient="right"
            ),
        ),
        size=alt.value(180),
        tooltip=["material:N", "family:N", "density:Q", "modulus:Q"],
    )
)

labels = (
    alt.Chart(family_centers)
    .mark_text(fontSize=16, fontWeight="bold", opacity=0.85)
    .encode(
        x=alt.X("density_center:Q", scale=alt.Scale(type="log", domain=[10, 20000])),
        y=alt.Y("modulus_center:Q", scale=alt.Scale(type="log", domain=[0.0005, 1000])),
        text="family:N",
        color=alt.Color("family:N", scale=alt.Scale(domain=family_order, range=palette), legend=None),
    )
)

chart = (
    (points + labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("scatter-ashby-material \u00b7 altair \u00b7 pyplots.ai", fontSize=28, fontWeight=500),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.2, grid=True)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
