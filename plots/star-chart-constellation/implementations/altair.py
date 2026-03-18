""" pyplots.ai
star-chart-constellation: Star Chart with Constellations
Library: altair 6.0.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-18
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Stars and constellations for a northern sky view
np.random.seed(42)

# Major constellation stars with RA (hours) and Dec (degrees)
stars_data = [
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
    ("Merak", 11.03, 56.38, 2.37, "UMa"),
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
    ("Algieba", 10.33, 19.84, 2.28, "Leo"),
    ("Zosma", 11.24, 20.52, 2.56, "Leo"),
    ("Chertan", 11.24, 15.43, 3.34, "Leo"),
    # Cygnus
    ("Deneb", 20.69, 45.28, 1.25, "Cyg"),
    ("Sadr", 20.37, 40.26, 2.20, "Cyg"),
    ("Gienah Cyg", 20.77, 33.97, 2.46, "Cyg"),
    ("Albireo", 19.51, 27.96, 3.08, "Cyg"),
    ("Delta Cyg", 19.75, 45.13, 2.87, "Cyg"),
    # Lyra
    ("Vega", 18.62, 38.78, 0.03, "Lyr"),
    ("Sheliak", 18.83, 33.36, 3.45, "Lyr"),
    ("Sulafat", 18.98, 32.69, 3.24, "Lyr"),
    # Gemini
    ("Castor", 7.58, 31.89, 1.58, "Gem"),
    ("Pollux", 7.76, 28.03, 1.14, "Gem"),
    ("Alhena", 6.63, 16.40, 1.93, "Gem"),
    ("Wasat", 7.07, 21.98, 3.53, "Gem"),
    ("Mebsuta", 6.73, 25.13, 2.98, "Gem"),
    # Taurus
    ("Aldebaran", 4.60, 16.51, 0.85, "Tau"),
    ("Elnath", 5.44, 28.61, 1.65, "Tau"),
    ("Alcyone", 3.79, 24.11, 2.87, "Tau"),
    ("Tianguan", 5.63, 21.14, 3.00, "Tau"),
    # Bootes
    ("Arcturus", 14.26, 19.18, -0.05, "Boo"),
    ("Izar", 14.75, 27.07, 2.37, "Boo"),
    ("Muphrid", 13.91, 18.40, 2.68, "Boo"),
    ("Nekkar", 15.03, 40.39, 3.50, "Boo"),
    # Aquila
    ("Altair", 19.85, 8.87, 0.76, "Aql"),
    ("Tarazed", 19.77, 10.61, 2.72, "Aql"),
    ("Alshain", 19.92, 6.41, 3.71, "Aql"),
    # Scorpius
    ("Antares", 16.49, -26.43, 1.09, "Sco"),
    ("Shaula", 17.56, -37.10, 1.63, "Sco"),
    ("Sargas", 17.62, -43.00, 1.87, "Sco"),
    ("Dschubba", 16.01, -22.62, 2.32, "Sco"),
    ("Acrab", 16.09, -19.81, 2.62, "Sco"),
    # Canis Major
    ("Sirius", 6.75, -16.72, -1.46, "CMa"),
    ("Adhara", 6.98, -28.97, 1.50, "CMa"),
    ("Wezen", 7.14, -26.39, 1.84, "CMa"),
    ("Mirzam", 6.38, -17.96, 1.98, "CMa"),
    ("Aludra", 7.40, -29.30, 2.45, "CMa"),
    # Perseus
    ("Mirfak", 3.41, 49.86, 1.80, "Per"),
    ("Algol", 3.14, 40.96, 2.12, "Per"),
    ("Zeta Per", 3.90, 31.88, 2.85, "Per"),
    ("Epsilon Per", 3.96, 40.01, 2.89, "Per"),
    # Auriga
    ("Capella", 5.27, 46.00, 0.08, "Aur"),
    ("Menkalinan", 5.99, 44.95, 1.90, "Aur"),
    ("Theta Aur", 5.99, 37.21, 2.62, "Aur"),
]

# Background filler stars
n_filler = 200
filler_ra = np.random.uniform(0, 24, n_filler)
filler_dec = np.random.uniform(-45, 70, n_filler)
filler_mag = np.random.uniform(3.5, 5.5, n_filler)

stars = pd.DataFrame(stars_data, columns=["star_id", "ra", "dec", "magnitude", "constellation"])
filler = pd.DataFrame(
    {
        "star_id": [f"HIP{i}" for i in range(n_filler)],
        "ra": filler_ra,
        "dec": filler_dec,
        "magnitude": filler_mag,
        "constellation": "field",
    }
)
stars = pd.concat([stars, filler], ignore_index=True)

# Convert RA to degrees for plotting (RA hours * 15 = degrees)
stars["ra_deg"] = stars["ra"] * 15.0

# Invert magnitude for sizing: brighter stars get larger points
mag_min, mag_max = stars["magnitude"].min(), stars["magnitude"].max()
stars["size"] = ((mag_max - stars["magnitude"]) / (mag_max - mag_min)) * 450 + 20

# Constellation line edges (pairs of star_id)
edges_list = [
    # Orion
    ("Betelgeuse", "Bellatrix"),
    ("Bellatrix", "Mintaka"),
    ("Mintaka", "Alnilam"),
    ("Alnilam", "Alnitak"),
    ("Betelgeuse", "Alnitak"),
    ("Bellatrix", "Rigel"),
    ("Betelgeuse", "Saiph"),
    ("Rigel", "Saiph"),
    ("Mintaka", "Saiph"),
    # Ursa Major (Big Dipper)
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
    ("Chertan", "Zosma"),
    ("Zosma", "Denebola"),
    ("Regulus", "Algieba"),
    ("Algieba", "Zosma"),
    # Cygnus (Northern Cross)
    ("Deneb", "Sadr"),
    ("Sadr", "Gienah Cyg"),
    ("Gienah Cyg", "Albireo"),
    ("Sadr", "Delta Cyg"),
    # Lyra
    ("Vega", "Sheliak"),
    ("Sheliak", "Sulafat"),
    ("Sulafat", "Vega"),
    # Gemini
    ("Castor", "Pollux"),
    ("Pollux", "Wasat"),
    ("Wasat", "Alhena"),
    ("Castor", "Mebsuta"),
    # Taurus
    ("Aldebaran", "Tianguan"),
    ("Tianguan", "Elnath"),
    ("Aldebaran", "Alcyone"),
    # Bootes
    ("Arcturus", "Izar"),
    ("Arcturus", "Muphrid"),
    ("Izar", "Nekkar"),
    # Aquila
    ("Altair", "Tarazed"),
    ("Altair", "Alshain"),
    # Scorpius
    ("Antares", "Dschubba"),
    ("Dschubba", "Acrab"),
    ("Antares", "Shaula"),
    ("Shaula", "Sargas"),
    # Canis Major
    ("Sirius", "Mirzam"),
    ("Sirius", "Adhara"),
    ("Adhara", "Wezen"),
    ("Wezen", "Aludra"),
    # Perseus
    ("Mirfak", "Algol"),
    ("Mirfak", "Epsilon Per"),
    ("Epsilon Per", "Zeta Per"),
    # Auriga
    ("Capella", "Menkalinan"),
    ("Menkalinan", "Theta Aur"),
]

# Build edge dataframe with coordinates
star_lookup = stars.set_index("star_id")[["ra_deg", "dec"]].to_dict("index")
edge_rows = []
for s1, s2 in edges_list:
    if s1 in star_lookup and s2 in star_lookup:
        edge_rows.append(
            {
                "x": star_lookup[s1]["ra_deg"],
                "y": star_lookup[s1]["dec"],
                "x2": star_lookup[s2]["ra_deg"],
                "y2": star_lookup[s2]["dec"],
            }
        )
edges_df = pd.DataFrame(edge_rows)

# Constellation label positions (centroid of named stars)
named_stars = stars[stars["constellation"] != "field"]
label_df = named_stars.groupby("constellation").agg(ra_deg=("ra_deg", "mean"), dec=("dec", "mean")).reset_index()
constellation_names = {
    "Ori": "Orion",
    "UMa": "Ursa Major",
    "Cas": "Cassiopeia",
    "Leo": "Leo",
    "Cyg": "Cygnus",
    "Lyr": "Lyra",
    "Gem": "Gemini",
    "Tau": "Taurus",
    "Boo": "Boötes",
    "Aql": "Aquila",
    "Sco": "Scorpius",
    "CMa": "Canis Major",
    "Per": "Perseus",
    "Aur": "Auriga",
}
label_df["name"] = label_df["constellation"].map(constellation_names)

# Plot - Stars layer
star_points = (
    alt.Chart(stars)
    .mark_circle(opacity=0.9)
    .encode(
        x=alt.X("ra_deg:Q", title="Right Ascension (°)", scale=alt.Scale(domain=[0, 360], reverse=True)),
        y=alt.Y("dec:Q", title="Declination (°)", scale=alt.Scale(domain=[-50, 70])),
        size=alt.Size("size:Q", legend=None, scale=alt.Scale(range=[8, 500])),
        color=alt.condition(alt.datum.magnitude < 2.0, alt.value("#FFFDE7"), alt.value("#B0BEC5")),
        tooltip=["star_id:N", "magnitude:Q", "constellation:N"],
    )
)

# Constellation lines layer
lines = (
    alt.Chart(edges_df)
    .mark_rule(strokeWidth=1.2, opacity=0.35)
    .encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q", color=alt.value("#5C9DC8"))
)

# Constellation labels layer
labels = (
    alt.Chart(label_df)
    .mark_text(fontSize=16, fontWeight="bold", dy=-18, opacity=0.7)
    .encode(x="ra_deg:Q", y="dec:Q", text="name:N", color=alt.value("#80CBC4"))
)

# RA grid lines
ra_grid_values = list(range(0, 360, 30))
ra_grid_df = pd.DataFrame({"ra_deg": ra_grid_values})
ra_grid = (
    alt.Chart(ra_grid_df)
    .mark_rule(strokeDash=[4, 4], strokeWidth=0.5, opacity=0.15)
    .encode(x="ra_deg:Q", color=alt.value("#546E7A"))
)

# Dec grid lines
dec_grid_values = list(range(-30, 70, 15))
dec_grid_df = pd.DataFrame({"dec": dec_grid_values})
dec_grid = (
    alt.Chart(dec_grid_df)
    .mark_rule(strokeDash=[4, 4], strokeWidth=0.5, opacity=0.15)
    .encode(y="dec:Q", color=alt.value("#546E7A"))
)

# Combine all layers
chart = (
    (ra_grid + dec_grid + lines + star_points + labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="star-chart-constellation · altair · pyplots.ai", fontSize=28, anchor="middle", color="#E0E0E0"
        ),
    )
    .configure_view(fill="#0A1628", strokeWidth=0)
    .configure_axis(
        labelFontSize=16,
        titleFontSize=20,
        labelColor="#78909C",
        titleColor="#90A4AE",
        gridColor="#1A2A3A",
        gridOpacity=0.3,
        domainColor="#37474F",
    )
    .configure_title(color="#E0E0E0")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
