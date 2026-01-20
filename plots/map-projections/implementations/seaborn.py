"""pyplots.ai
map-projections: World Map with Different Projections
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Simplified world coastline polygons (major continents outline)
# Coordinates in degrees (longitude, latitude)
WORLD_COASTLINES = [
    # North America
    [
        (-168, 66),
        (-141, 70),
        (-130, 70),
        (-120, 60),
        (-125, 50),
        (-125, 40),
        (-117, 33),
        (-105, 25),
        (-97, 26),
        (-82, 25),
        (-81, 30),
        (-75, 35),
        (-70, 42),
        (-67, 45),
        (-60, 47),
        (-55, 52),
        (-60, 60),
        (-65, 68),
        (-80, 70),
        (-100, 73),
        (-120, 75),
        (-145, 72),
        (-168, 66),
    ],
    # South America
    [
        (-82, 10),
        (-77, 0),
        (-80, -5),
        (-70, -15),
        (-60, -5),
        (-50, 0),
        (-35, -5),
        (-40, -23),
        (-55, -35),
        (-68, -55),
        (-75, -50),
        (-75, -40),
        (-70, -20),
        (-80, -5),
        (-82, 10),
    ],
    # Europe
    [
        (-10, 36),
        (-10, 45),
        (-5, 48),
        (0, 52),
        (5, 55),
        (10, 58),
        (20, 60),
        (28, 70),
        (35, 70),
        (30, 60),
        (25, 55),
        (20, 50),
        (15, 45),
        (20, 40),
        (25, 35),
        (35, 35),
        (28, 42),
        (20, 38),
        (10, 38),
        (-10, 36),
    ],
    # Africa
    [
        (-17, 15),
        (-17, 28),
        (-5, 36),
        (10, 38),
        (20, 33),
        (35, 30),
        (45, 12),
        (52, 12),
        (45, 0),
        (42, -10),
        (35, -25),
        (25, -34),
        (18, -35),
        (12, -20),
        (15, -5),
        (5, 5),
        (-10, 5),
        (-17, 15),
    ],
    # Asia
    [
        (35, 30),
        (45, 42),
        (52, 45),
        (70, 42),
        (80, 30),
        (75, 15),
        (90, 22),
        (100, 15),
        (105, 22),
        (110, 5),
        (120, 25),
        (130, 35),
        (140, 45),
        (145, 55),
        (135, 70),
        (100, 78),
        (70, 75),
        (50, 70),
        (30, 70),
        (35, 50),
        (45, 45),
        (35, 30),
    ],
    # Australia
    [
        (113, -22),
        (120, -18),
        (135, -12),
        (145, -15),
        (152, -25),
        (150, -38),
        (140, -38),
        (130, -33),
        (115, -35),
        (113, -22),
    ],
]


def mercator_project(lon, lat):
    """Mercator projection: preserves angles, distorts area at poles."""
    x = np.radians(lon)
    # Clamp latitude to avoid infinity at poles
    lat_clamped = np.clip(lat, -85, 85)
    y = np.log(np.tan(np.pi / 4 + np.radians(lat_clamped) / 2))
    return x, y


def mollweide_project(lon, lat):
    """Mollweide projection: equal-area, elliptical shape."""
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)
    # Newton-Raphson iteration for theta
    theta = lat_rad.copy() if isinstance(lat_rad, np.ndarray) else lat_rad
    for _ in range(10):
        delta = -(2 * theta + np.sin(2 * theta) - np.pi * np.sin(lat_rad)) / (2 + 2 * np.cos(2 * theta) + 1e-10)
        theta = theta + delta
    x = (2 * np.sqrt(2) / np.pi) * lon_rad * np.cos(theta)
    y = np.sqrt(2) * np.sin(theta)
    return x, y


def robinson_project(lon, lat):
    """Robinson projection: compromise, visually pleasing."""
    # Robinson lookup table (latitude in degrees -> scale factors)
    robinson_table = np.array(
        [
            [0, 1.0000, 0.0000],
            [5, 0.9986, 0.0620],
            [10, 0.9954, 0.1240],
            [15, 0.9900, 0.1860],
            [20, 0.9822, 0.2480],
            [25, 0.9730, 0.3100],
            [30, 0.9600, 0.3720],
            [35, 0.9427, 0.4340],
            [40, 0.9216, 0.4958],
            [45, 0.8962, 0.5571],
            [50, 0.8679, 0.6176],
            [55, 0.8350, 0.6769],
            [60, 0.7986, 0.7346],
            [65, 0.7597, 0.7903],
            [70, 0.7186, 0.8435],
            [75, 0.6732, 0.8936],
            [80, 0.6213, 0.9394],
            [85, 0.5722, 0.9761],
            [90, 0.5322, 1.0000],
        ]
    )
    abs_lat = np.abs(lat)
    # Interpolate X and Y scale factors
    x_scale = np.interp(abs_lat, robinson_table[:, 0], robinson_table[:, 1])
    y_scale = np.interp(abs_lat, robinson_table[:, 0], robinson_table[:, 2])
    x = 0.8487 * np.radians(lon) * x_scale
    y = 1.3523 * y_scale * np.sign(lat)
    return x, y


def sinusoidal_project(lon, lat):
    """Sinusoidal projection: equal-area, pointed poles."""
    lat_rad = np.radians(lat)
    x = np.radians(lon) * np.cos(lat_rad)
    y = lat_rad
    return x, y


# Projection configurations
PROJECTIONS = {
    "Mercator": {"func": mercator_project, "aspect": 1.5, "ylim": (-3.0, 3.0)},
    "Mollweide": {"func": mollweide_project, "aspect": 2.0, "ylim": (-1.6, 1.6)},
    "Robinson": {"func": robinson_project, "aspect": 1.8, "ylim": (-1.5, 1.5)},
    "Sinusoidal": {"func": sinusoidal_project, "aspect": 2.0, "ylim": (-1.8, 1.8)},
}

# Set seaborn theme
sns.set_theme(style="whitegrid", context="talk", font_scale=1.0)

# Create 2x2 subplot figure for comparing projections
fig, axes = plt.subplots(2, 2, figsize=(16, 9))
axes = axes.flatten()

# Generate graticule (latitude/longitude grid lines)
lons_grat = np.linspace(-180, 180, 73)  # Every 5 degrees
lats_grat = np.linspace(-90, 90, 37)  # Every 5 degrees

for idx, (proj_name, proj_config) in enumerate(PROJECTIONS.items()):
    ax = axes[idx]
    proj_func = proj_config["func"]

    # Set ocean background
    ax.set_facecolor("#d4e8f7")

    # Draw graticule lines (every 30 degrees)
    # Longitude lines (meridians)
    for lon in range(-180, 181, 30):
        lats_line = np.linspace(-85, 85, 100)
        lons_line = np.full_like(lats_line, lon)
        x, y = proj_func(lons_line, lats_line)
        ax.plot(x, y, color="#aaaaaa", linewidth=0.5, alpha=0.7, zorder=1)

    # Latitude lines (parallels)
    for lat in range(-60, 61, 30):
        lons_line = np.linspace(-180, 180, 200)
        lats_line = np.full_like(lons_line, lat)
        x, y = proj_func(lons_line, lats_line)
        ax.plot(x, y, color="#aaaaaa", linewidth=0.5, alpha=0.7, zorder=1)

    # Draw coastlines with projection
    for coastline in WORLD_COASTLINES:
        lons = np.array([p[0] for p in coastline])
        lats = np.array([p[1] for p in coastline])
        x, y = proj_func(lons, lats)
        ax.fill(x, y, color="#c8d8c8", edgecolor="#306998", linewidth=1.2, alpha=0.9, zorder=2)

    # Draw Tissot indicatrices (circles that show distortion)
    # Place circles at regular intervals
    tissot_lons = [-120, -60, 0, 60, 120]
    tissot_lats = [-45, 0, 45]

    for t_lon in tissot_lons:
        for t_lat in tissot_lats:
            # Skip if latitude too extreme for Mercator
            if proj_name == "Mercator" and abs(t_lat) > 75:
                continue

            # Create small circle in geographic coordinates
            angles = np.linspace(0, 2 * np.pi, 50)
            radius = 8  # degrees
            circle_lons = t_lon + radius * np.cos(angles) / np.cos(np.radians(t_lat))
            circle_lats = t_lat + radius * np.sin(angles)

            # Clip latitude values
            circle_lats = np.clip(circle_lats, -85, 85)

            # Project the circle
            cx, cy = proj_func(circle_lons, circle_lats)
            ax.fill(cx, cy, color="#FFD43B", edgecolor="#b8940a", linewidth=1.0, alpha=0.5, zorder=3)

    # Styling
    ax.set_title(proj_name, fontsize=20, fontweight="bold", pad=8)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(proj_config["ylim"])
    ax.set_aspect(proj_config["aspect"])
    ax.set_xticks([])
    ax.set_yticks([])

    # Add subtle border
    for spine in ax.spines.values():
        spine.set_edgecolor("#888888")
        spine.set_linewidth(1.5)

# Main title
fig.suptitle("map-projections · seaborn · pyplots.ai", fontsize=26, fontweight="bold", y=0.98)

# Add subtitle explaining the visualization
fig.text(
    0.5,
    0.02,
    "Yellow ellipses (Tissot indicatrices) show how each projection distorts area and shape",
    ha="center",
    fontsize=14,
    color="#555555",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
