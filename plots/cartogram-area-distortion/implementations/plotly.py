"""pyplots.ai
cartogram-area-distortion: Cartogram with Area Distortion by Data Value
Library: plotly 6.6.0 | Python 3.14.3
Quality: 80/100 | Created: 2026-03-13
"""

import numpy as np
import plotly.graph_objects as go


# Data - US states sized by population (2023 estimates, in millions)
states = [
    "CA",
    "TX",
    "FL",
    "NY",
    "PA",
    "IL",
    "OH",
    "GA",
    "NC",
    "MI",
    "NJ",
    "VA",
    "WA",
    "AZ",
    "MA",
    "TN",
    "IN",
    "MO",
    "MD",
    "WI",
    "CO",
    "MN",
    "SC",
    "AL",
    "LA",
    "KY",
    "OR",
    "OK",
    "CT",
    "UT",
    "IA",
    "NV",
    "AR",
    "MS",
    "KS",
    "NM",
    "NE",
    "ID",
    "WV",
    "HI",
    "NH",
    "ME",
    "MT",
    "RI",
    "DE",
    "SD",
    "ND",
    "AK",
    "VT",
    "WY",
]

population = np.array(
    [
        39.03,
        30.03,
        22.24,
        19.57,
        12.97,
        12.55,
        11.78,
        10.91,
        10.70,
        10.04,
        9.29,
        8.64,
        7.81,
        7.36,
        7.00,
        7.05,
        6.83,
        6.18,
        6.18,
        5.89,
        5.84,
        5.71,
        5.28,
        5.07,
        4.59,
        4.53,
        4.24,
        4.00,
        3.62,
        3.42,
        3.20,
        3.18,
        3.05,
        2.94,
        2.94,
        2.11,
        1.97,
        1.94,
        1.77,
        1.44,
        1.40,
        1.39,
        1.12,
        1.10,
        1.02,
        0.91,
        0.78,
        0.74,
        0.65,
        0.58,
    ]
)

# State area in sq miles (for density calculation)
area_sq_miles = np.array(
    [
        163696,
        268596,
        65758,
        54555,
        46054,
        57914,
        44826,
        59425,
        53819,
        96714,
        8723,
        42775,
        71298,
        113990,
        10554,
        42144,
        36420,
        69707,
        12406,
        65496,
        104094,
        86936,
        32020,
        52420,
        52378,
        40408,
        98379,
        69899,
        5543,
        84897,
        56273,
        110572,
        53179,
        48432,
        82278,
        121590,
        77348,
        83569,
        24230,
        10932,
        9349,
        35380,
        147040,
        1545,
        2489,
        77116,
        70698,
        665384,
        9616,
        97813,
    ]
)

# Approximate centroids (latitude, longitude) for each state
lats = np.array(
    [
        36.78,
        31.97,
        27.66,
        42.93,
        41.20,
        40.63,
        40.42,
        32.68,
        35.63,
        44.31,
        40.06,
        37.43,
        47.75,
        34.05,
        42.41,
        35.52,
        40.27,
        38.57,
        39.05,
        43.78,
        39.55,
        46.73,
        33.84,
        32.32,
        31.17,
        37.84,
        43.80,
        35.47,
        41.60,
        39.32,
        41.88,
        38.80,
        35.20,
        32.35,
        39.01,
        34.52,
        41.49,
        44.07,
        38.60,
        19.90,
        43.19,
        45.25,
        46.88,
        41.58,
        38.91,
        43.97,
        47.55,
        63.59,
        44.56,
        43.08,
    ]
)

lons = np.array(
    [
        -119.42,
        -99.90,
        -81.52,
        -75.58,
        -77.19,
        -89.40,
        -82.91,
        -83.54,
        -79.81,
        -84.71,
        -74.41,
        -78.66,
        -120.74,
        -111.09,
        -71.38,
        -86.15,
        -86.13,
        -91.83,
        -76.64,
        -89.62,
        -105.78,
        -94.69,
        -81.16,
        -86.90,
        -91.87,
        -84.27,
        -120.55,
        -97.09,
        -72.76,
        -111.09,
        -93.10,
        -116.42,
        -92.37,
        -89.40,
        -98.48,
        -105.87,
        -99.90,
        -114.74,
        -80.62,
        -155.58,
        -71.57,
        -69.45,
        -110.36,
        -71.48,
        -75.53,
        -99.44,
        -101.00,
        -154.49,
        -72.58,
        -107.29,
    ]
)

density = population * 1e6 / area_sq_miles

# Offset NE states to reduce overlap
ne_offsets = {
    "NJ": (0.8, 1.5),  # push south-east
    "CT": (-0.5, 1.8),  # push east
    "MA": (0.8, 2.0),  # push east
    "RI": (-0.8, 2.5),  # push east more
    "NH": (1.2, 1.0),  # push north-east
    "VT": (1.5, -0.5),  # push north-west
    "DE": (-0.8, 1.8),  # push south-east
    "MD": (-1.2, 0.8),  # push south
    "ME": (1.0, 1.5),  # push north-east
}

for i, s in enumerate(states):
    if s in ne_offsets:
        dlat, dlon = ne_offsets[s]
        lats[i] += dlat
        lons[i] += dlon

# Scale bubble sizes: area proportional to population
max_marker_size = 60
sizes = np.sqrt(population / population.max()) * max_marker_size

# Color values on log scale
log_density = np.log10(density)

# Only show labels on bubbles large enough to read
label_threshold = 3.0  # millions
label_texts = [s if p >= label_threshold else "" for s, p in zip(states, population, strict=False)]

# Plot
fig = go.Figure()

# Background: faint state boundaries using Choropleth for geographic reference
fig.add_trace(
    go.Choropleth(
        locationmode="USA-states",
        locations=states,
        z=[0] * len(states),
        colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
        showscale=False,
        marker={"line": {"color": "#c0c0c0", "width": 0.8}},
        hoverinfo="skip",
    )
)

# Bubble cartogram layer
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=lons,
        lat=lats,
        text=[
            f"<b>{s}</b><br>Pop: {p:.1f}M<br>Density: {d:.0f}/sq mi"
            for s, p, d in zip(states, population, density, strict=False)
        ],
        hoverinfo="text",
        marker={
            "size": sizes,
            "color": log_density,
            "colorscale": "Viridis",
            "cmin": np.log10(5),
            "cmax": np.log10(6000),
            "colorbar": {
                "title": {"text": "Pop. Density<br>(per sq mi)", "font": {"size": 18}},
                "tickfont": {"size": 15},
                "tickvals": np.log10([10, 50, 100, 500, 1000, 5000]),
                "ticktext": ["10", "50", "100", "500", "1k", "5k"],
                "len": 0.55,
                "thickness": 20,
                "x": 0.93,
                "outlinewidth": 0,
            },
            "line": {"width": 1.5, "color": "white"},
            "opacity": 0.9,
            "sizemode": "diameter",
        },
    )
)

# State abbreviation labels (only for larger states)
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=lons,
        lat=lats,
        text=label_texts,
        mode="text",
        textfont={"size": 11, "color": "white", "family": "Arial Black"},
        hoverinfo="skip",
        showlegend=False,
    )
)

# Layout
fig.update_layout(
    title={
        "text": (
            "<b>US States by Population</b>"
            "<br><span style='font-size:16px;color:#888'>"
            "cartogram-area-distortion · plotly · pyplots.ai</span>"
        ),
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
    },
    geo={
        "scope": "usa",
        "showframe": False,
        "showcoastlines": True,
        "coastlinecolor": "#d0d0d0",
        "coastlinewidth": 0.6,
        "showland": True,
        "landcolor": "#f5f5f5",
        "showlakes": True,
        "lakecolor": "white",
        "bgcolor": "white",
        "projection_type": "albers usa",
    },
    template="plotly_white",
    paper_bgcolor="white",
    margin={"l": 10, "r": 90, "t": 85, "b": 40},
    showlegend=False,
    annotations=[
        {
            "text": "Circle area ∝ population  |  Color ∝ density",
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": -0.03,
            "showarrow": False,
            "font": {"size": 16, "color": "#777777"},
        }
    ],
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
