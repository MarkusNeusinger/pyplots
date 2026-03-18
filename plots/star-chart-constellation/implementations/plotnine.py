""" pyplots.ai
star-chart-constellation: Star Chart with Constellations
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 80/100 | Created: 2026-03-18
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_rect,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_identity,
    scale_size_identity,
    theme,
    theme_void,
    xlim,
    ylim,
)


# Data — real star positions (RA in hours, Dec in degrees) for prominent constellations
np.random.seed(42)

stars_raw = [
    # Orion
    ("Betelgeuse", 5.92, 7.41, 0.42, "Ori"),
    ("Rigel", 5.24, -8.20, 0.13, "Ori"),
    ("Bellatrix", 5.42, 6.35, 1.64, "Ori"),
    ("Mintaka", 5.53, -0.30, 2.23, "Ori"),
    ("Alnilam", 5.60, -1.20, 1.69, "Ori"),
    ("Alnitak", 5.68, -1.94, 1.77, "Ori"),
    ("Saiph", 5.80, -9.67, 2.09, "Ori"),
    # Ursa Major (Big Dipper)
    ("Dubhe", 11.06, 61.75, 1.79, "UMa"),
    ("Merak", 11.02, 56.38, 2.37, "UMa"),
    ("Phecda", 11.90, 53.69, 2.44, "UMa"),
    ("Megrez", 12.26, 57.03, 3.31, "UMa"),
    ("Alioth", 12.90, 55.96, 1.77, "UMa"),
    ("Mizar", 13.40, 54.93, 2.27, "UMa"),
    ("Alkaid", 13.79, 49.31, 1.86, "UMa"),
    # Cassiopeia
    ("Schedar", 0.68, 56.54, 2.23, "Cas"),
    ("Caph", 0.15, 59.15, 2.27, "Cas"),
    ("Gamma Cas", 0.95, 60.72, 2.47, "Cas"),
    ("Ruchbah", 1.36, 60.24, 2.68, "Cas"),
    ("Segin", 1.91, 63.67, 3.37, "Cas"),
    # Leo
    ("Regulus", 10.14, 11.97, 1.35, "Leo"),
    ("Denebola", 11.82, 14.57, 2.14, "Leo"),
    ("Algieba", 10.33, 19.84, 2.08, "Leo"),
    ("Zosma", 11.24, 20.52, 2.56, "Leo"),
    ("Chertan", 11.24, 15.43, 3.34, "Leo"),
    # Cygnus
    ("Deneb", 20.69, 45.28, 1.25, "Cyg"),
    ("Sadr", 20.37, 40.26, 2.20, "Cyg"),
    ("Gienah Cyg", 20.77, 33.97, 2.46, "Cyg"),
    ("Albireo", 19.51, 27.96, 3.08, "Cyg"),
    ("Delta Cyg", 19.75, 45.13, 2.87, "Cyg"),
    # Scorpius
    ("Antares", 16.49, -26.43, 0.96, "Sco"),
    ("Shaula", 17.56, -37.10, 1.63, "Sco"),
    ("Sargas", 17.62, -42.99, 1.87, "Sco"),
    ("Dschubba", 16.01, -22.62, 2.32, "Sco"),
    ("Graffias", 16.09, -19.81, 2.62, "Sco"),
    ("Wei", 16.84, -34.29, 2.29, "Sco"),
    ("Lesath", 17.53, -37.29, 2.69, "Sco"),
    # Gemini
    ("Pollux", 7.76, 28.03, 1.14, "Gem"),
    ("Castor", 7.58, 31.89, 1.58, "Gem"),
    ("Alhena", 6.63, 16.40, 1.93, "Gem"),
    ("Tejat", 6.38, 22.51, 2.88, "Gem"),
    ("Mebsuta", 6.73, 25.13, 3.06, "Gem"),
    # Lyra
    ("Vega", 18.62, 38.78, 0.03, "Lyr"),
    ("Sheliak", 18.83, 33.36, 3.45, "Lyr"),
    ("Sulafat", 18.98, 32.69, 3.24, "Lyr"),
    # Aquila
    ("Altair", 19.85, 8.87, 0.77, "Aql"),
    ("Tarazed", 19.77, 10.61, 2.72, "Aql"),
    ("Alshain", 19.92, 6.41, 3.71, "Aql"),
    # Taurus
    ("Aldebaran", 4.60, 16.51, 0.85, "Tau"),
    ("Elnath", 5.44, 28.61, 1.65, "Tau"),
    ("Alcyone", 3.79, 24.11, 2.87, "Tau"),
    ("Tianguan", 5.63, 21.14, 3.00, "Tau"),
]

# Constellation edges (pairs of star names)
edges_raw = [
    # Orion
    ("Betelgeuse", "Bellatrix"),
    ("Bellatrix", "Mintaka"),
    ("Mintaka", "Alnilam"),
    ("Alnilam", "Alnitak"),
    ("Betelgeuse", "Alnilam"),
    ("Rigel", "Alnitak"),
    ("Rigel", "Saiph"),
    ("Saiph", "Alnitak"),
    # Ursa Major
    ("Dubhe", "Merak"),
    ("Merak", "Phecda"),
    ("Phecda", "Megrez"),
    ("Megrez", "Alioth"),
    ("Alioth", "Mizar"),
    ("Mizar", "Alkaid"),
    ("Megrez", "Dubhe"),
    # Cassiopeia
    ("Caph", "Schedar"),
    ("Schedar", "Gamma Cas"),
    ("Gamma Cas", "Ruchbah"),
    ("Ruchbah", "Segin"),
    # Leo
    ("Regulus", "Chertan"),
    ("Chertan", "Denebola"),
    ("Denebola", "Zosma"),
    ("Zosma", "Algieba"),
    ("Algieba", "Regulus"),
    # Cygnus
    ("Deneb", "Sadr"),
    ("Sadr", "Gienah Cyg"),
    ("Sadr", "Delta Cyg"),
    ("Sadr", "Albireo"),
    # Scorpius
    ("Graffias", "Dschubba"),
    ("Dschubba", "Antares"),
    ("Antares", "Wei"),
    ("Wei", "Shaula"),
    ("Shaula", "Lesath"),
    ("Wei", "Sargas"),
    # Gemini
    ("Castor", "Pollux"),
    ("Castor", "Tejat"),
    ("Pollux", "Alhena"),
    ("Tejat", "Mebsuta"),
    ("Mebsuta", "Castor"),
    # Lyra
    ("Vega", "Sheliak"),
    ("Sheliak", "Sulafat"),
    ("Sulafat", "Vega"),
    # Aquila
    ("Altair", "Tarazed"),
    ("Altair", "Alshain"),
    # Taurus
    ("Aldebaran", "Elnath"),
    ("Aldebaran", "Alcyone"),
    ("Elnath", "Tianguan"),
]

# Add fainter background stars
n_bg = 250
bg_ra = np.random.uniform(0, 24, n_bg)
bg_dec = np.random.uniform(-50, 70, n_bg)
bg_mag = np.random.uniform(3.5, 5.5, n_bg)
bg_stars = [(f"BG{i}", bg_ra[i], bg_dec[i], bg_mag[i], "bg") for i in range(n_bg)]

all_stars = stars_raw + bg_stars

# Build star dataframe
star_names = [s[0] for s in all_stars]
ra_hours = np.array([s[1] for s in all_stars])
dec_deg = np.array([s[2] for s in all_stars])
magnitudes = np.array([s[3] for s in all_stars])
constellations = [s[4] for s in all_stars]

# Convert RA hours to degrees, then to radians for projection
ra_deg = ra_hours * 15.0
ra_rad = np.radians(ra_deg)
dec_rad = np.radians(dec_deg)

# Stereographic projection (centered on RA=12h, Dec=30° for northern sky view)
ra0 = np.radians(180.0)
dec0 = np.radians(30.0)

# Stereographic projection formulas
cos_c = np.sin(dec0) * np.sin(dec_rad) + np.cos(dec0) * np.cos(dec_rad) * np.cos(ra_rad - ra0)
k = 2.0 / (1.0 + cos_c)
proj_x = k * np.cos(dec_rad) * np.sin(ra_rad - ra0)
proj_y = k * (np.cos(dec0) * np.sin(dec_rad) - np.sin(dec0) * np.cos(dec_rad) * np.cos(ra_rad - ra0))

# Flip x so RA increases right-to-left (as seen on sky)
proj_x = -proj_x

# Size mapping: brighter stars (lower mag) get larger points
max_mag = 5.5
min_mag = -0.5
star_sizes = np.clip((max_mag - magnitudes) / (max_mag - min_mag), 0.05, 1.0)
star_sizes = star_sizes**1.5 * 8.0 + 0.3

# Star colors based on magnitude (brighter = more yellow-white, dimmer = blueish-white)
star_colors = []
for mag in magnitudes:
    if mag < 1.0:
        star_colors.append("#FFFDE7")
    elif mag < 2.0:
        star_colors.append("#FFF9C4")
    elif mag < 3.0:
        star_colors.append("#E8EAF6")
    else:
        star_colors.append("#B0BEC5")

df_stars = pd.DataFrame(
    {
        "x": proj_x,
        "y": proj_y,
        "magnitude": magnitudes,
        "size": star_sizes,
        "color": star_colors,
        "name": star_names,
        "constellation": constellations,
    }
)

# Filter to visible region (within projection circle)
radius_limit = 3.5
df_stars = df_stars[np.sqrt(df_stars["x"] ** 2 + df_stars["y"] ** 2) < radius_limit].copy()

# Build edges dataframe
star_lookup = {row["name"]: (row["x"], row["y"]) for _, row in df_stars.iterrows()}
edge_data = []
for s1, s2 in edges_raw:
    if s1 in star_lookup and s2 in star_lookup:
        x1, y1 = star_lookup[s1]
        x2, y2 = star_lookup[s2]
        edge_data.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

df_edges = pd.DataFrame(edge_data)

# Constellation labels at centroid of each group
named_stars = df_stars[df_stars["constellation"] != "bg"].copy()
constellation_names = {
    "Ori": "ORION",
    "UMa": "URSA MAJOR",
    "Cas": "CASSIOPEIA",
    "Leo": "LEO",
    "Cyg": "CYGNUS",
    "Sco": "SCORPIUS",
    "Gem": "GEMINI",
    "Lyr": "LYRA",
    "Aql": "AQUILA",
    "Tau": "TAURUS",
}
label_data = []
for abbr, full_name in constellation_names.items():
    group = named_stars[named_stars["constellation"] == abbr]
    if len(group) > 0:
        label_data.append({"x": group["x"].mean(), "y": group["y"].min() - 0.12, "label": full_name})

df_labels = pd.DataFrame(label_data)

# Coordinate grid circles (declination rings)
grid_circles = []
for dec_grid in [0, 20, 40, 60]:
    theta = np.linspace(0, 2 * np.pi, 200)
    dec_g = np.radians(dec_grid)
    cos_c_g = np.sin(dec0) * np.sin(dec_g) + np.cos(dec0) * np.cos(dec_g) * np.cos(theta)
    k_g = 2.0 / (1.0 + cos_c_g)
    gx = -k_g * np.cos(dec_g) * np.sin(theta)
    gy = k_g * (np.cos(dec0) * np.sin(dec_g) - np.sin(dec0) * np.cos(dec_g) * np.cos(theta))
    mask = np.sqrt(gx**2 + gy**2) < radius_limit
    gx[~mask] = np.nan
    gy[~mask] = np.nan
    for i in range(len(theta) - 1):
        if not (np.isnan(gx[i]) or np.isnan(gx[i + 1])):
            grid_circles.append({"x": gx[i], "y": gy[i], "xend": gx[i + 1], "yend": gy[i + 1]})

df_grid = pd.DataFrame(grid_circles) if grid_circles else pd.DataFrame(columns=["x", "y", "xend", "yend"])

# RA grid lines (meridians)
ra_grid_segs = []
for ra_h in range(0, 24, 3):
    ra_g = np.radians(ra_h * 15.0)
    dec_range = np.linspace(np.radians(-50), np.radians(70), 150)
    cos_c_g = np.sin(dec0) * np.sin(dec_range) + np.cos(dec0) * np.cos(dec_range) * np.cos(ra_g - ra0)
    k_g = 2.0 / (1.0 + cos_c_g)
    gx = -k_g * np.cos(dec_range) * np.sin(ra_g - ra0)
    gy = k_g * (np.cos(dec0) * np.sin(dec_range) - np.sin(dec0) * np.cos(dec_range) * np.cos(ra_g - ra0))
    mask = np.sqrt(gx**2 + gy**2) < radius_limit
    gx[~mask] = np.nan
    gy[~mask] = np.nan
    for i in range(len(dec_range) - 1):
        if not (np.isnan(gx[i]) or np.isnan(gx[i + 1])):
            ra_grid_segs.append({"x": gx[i], "y": gy[i], "xend": gx[i + 1], "yend": gy[i + 1]})

df_ra_grid = pd.DataFrame(ra_grid_segs) if ra_grid_segs else pd.DataFrame(columns=["x", "y", "xend", "yend"])

# Combine all grid segments
df_all_grid = pd.concat([df_grid, df_ra_grid], ignore_index=True)

# Plot
plot = (
    ggplot()
    + geom_segment(
        data=df_all_grid, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#1a2744", size=0.3, alpha=0.5
    )
    + geom_segment(
        data=df_edges, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#4a6fa5", size=0.6, alpha=0.55
    )
    + geom_point(data=df_stars, mapping=aes(x="x", y="y", size="size", color="color"), alpha=0.92)
    + scale_size_identity()
    + scale_color_identity()
    + geom_text(data=df_labels, mapping=aes(x="x", y="y", label="label"), color="#6a8cba", size=8, alpha=0.7)
    + annotate(
        "text",
        x=0,
        y=-radius_limit - 0.25,
        label="star-chart-constellation · plotnine · pyplots.ai",
        color="#8899aa",
        size=12,
        ha="center",
    )
    + xlim(-radius_limit - 0.2, radius_limit + 0.2)
    + ylim(-radius_limit - 0.5, radius_limit + 0.2)
    + labs(x="", y="")
    + theme_void()
    + theme(
        figure_size=(16, 16),
        plot_background=element_rect(fill="#060d1f", color="#060d1f"),
        panel_background=element_rect(fill="#060d1f", color="#060d1f"),
        text=element_text(color="#aabbcc"),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
