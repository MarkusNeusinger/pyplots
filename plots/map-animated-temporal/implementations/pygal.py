"""pyplots.ai
map-animated-temporal: Animated Map over Time
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style
from pygal_maps_world.maps import World


# Data: Simulated seismic activity spreading over time (6 time periods)
# Shows earthquake activity propagating across Pacific Ring of Fire regions
time_periods = ["T1: Initial", "T2: +6h", "T3: +12h", "T4: +24h", "T5: +48h", "T6: +72h"]

# Countries in Pacific Ring of Fire and nearby regions
# Activity spreads outward from initial epicenter (Japan region)
# Values represent seismic intensity index (0-100)
activity_by_time = {
    0: {"jp": 95},
    1: {"jp": 85, "kr": 55, "ph": 40},
    2: {"jp": 75, "kr": 70, "ph": 65, "id": 50, "tw": 45},
    3: {"jp": 60, "kr": 55, "ph": 75, "id": 80, "tw": 50, "my": 35, "nz": 40},
    4: {"jp": 45, "kr": 40, "ph": 60, "id": 70, "tw": 40, "my": 50, "nz": 65, "au": 35, "cl": 30},
    5: {
        "jp": 35,
        "kr": 30,
        "ph": 45,
        "id": 55,
        "tw": 30,
        "my": 45,
        "nz": 55,
        "au": 50,
        "cl": 60,
        "pe": 40,
        "mx": 35,
        "ec": 25,
    },
}

# Activity level labels and thresholds (for binning)
activity_bins = [
    ("Minimal (<20)", 0, 20),
    ("Low (20-35)", 20, 35),
    ("Moderate (35-50)", 35, 50),
    ("High (50-65)", 50, 65),
    ("Severe (65-80)", 65, 80),
    ("Extreme (80+)", 80, 101),
]

# Sequential red palette - from light (low activity) to dark red (high activity)
colors = ("#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#cb181d")

# Custom style for individual maps (smaller for grid layout)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=48,
    label_font_size=28,
    legend_font_size=28,
    major_label_font_size=24,
    value_font_size=24,
    tooltip_font_size=24,
    no_data_font_size=24,
)

# Generate small multiples: 2 rows x 3 columns grid for 6 time periods
# Each individual map: 1600 x 1200 px → Combined: 4800 x 2400 px + title area
individual_width = 1600
individual_height = 1200
grid_cols = 3
grid_rows = 2

map_images = []
for time_idx in range(6):
    data = activity_by_time[time_idx]

    # Inline binning: group countries by activity level
    binned = {label: {} for label, _, _ in activity_bins}
    for country, value in data.items():
        for label, low, high in activity_bins:
            if low <= value < high:
                binned[label][country] = value
                break

    worldmap = World(
        style=custom_style,
        width=individual_width,
        height=individual_height,
        title=time_periods[time_idx],
        show_legend=True,
        legend_at_bottom=True,
        legend_at_bottom_columns=3,
        legend_box_size=24,
    )

    # Add all categories for consistent legend across all maps
    for label, _, _ in activity_bins:
        category_data = binned.get(label, {})
        worldmap.add(label, category_data if category_data else None)

    # Render to PNG bytes
    png_bytes = worldmap.render_to_png()
    map_images.append(Image.open(BytesIO(png_bytes)))

# Create combined image with title area
title_height = 300
combined_width = individual_width * grid_cols
combined_height = individual_height * grid_rows + title_height
combined = Image.new("RGB", (combined_width, combined_height), "white")

# Add title at top center
draw = ImageDraw.Draw(combined)
title_text = "Seismic Activity Temporal Progression · map-animated-temporal · pygal · pyplots.ai"
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
except OSError:
    title_font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), title_text, font=title_font)
text_width = bbox[2] - bbox[0]
title_x = (combined_width - text_width) // 2
draw.text((title_x, 100), title_text, fill="#111111", font=title_font)

# Paste individual maps in grid
for idx, img in enumerate(map_images):
    row = idx // grid_cols
    col = idx % grid_cols
    x = col * individual_width
    y = row * individual_height + title_height
    combined.paste(img, (x, y))

combined.save("plot.png", dpi=(300, 300))

# Also save individual HTML for interactivity (final snapshot for web viewing)
final_map = World(
    style=custom_style,
    width=4800,
    height=2700,
    title="Seismic Activity (T6: +72h) · map-animated-temporal · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    legend_box_size=36,
)
final_data = activity_by_time[5]
final_binned = {label: {} for label, _, _ in activity_bins}
for country, value in final_data.items():
    for label, low, high in activity_bins:
        if low <= value < high:
            final_binned[label][country] = value
            break
for label, _, _ in activity_bins:
    category_data = final_binned.get(label, {})
    final_map.add(label, category_data if category_data else None)
final_map.render_to_file("plot.html")
