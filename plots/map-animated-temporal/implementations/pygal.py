""" pyplots.ai
map-animated-temporal: Animated Map over Time
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

import numpy as np
from pygal.style import Style
from pygal_maps_world.maps import World


# Data: Simulated seismic activity spreading over time (6 time periods)
# Shows earthquake activity propagating across Pacific Ring of Fire regions
np.random.seed(42)

# Define regions affected at each time step (simulating wave propagation)
time_periods = ["T1: Initial", "T2: +6h", "T3: +12h", "T4: +24h", "T5: +48h", "T6: +72h"]

# Countries in Pacific Ring of Fire and nearby regions
# Activity spreads outward from initial epicenter (Japan region)
# Values represent seismic intensity index (0-100)
activity_by_time = {
    0: {"jp": 95},  # Initial event in Japan
    1: {"jp": 85, "kr": 55, "ph": 40},  # Spreads to Korea, Philippines
    2: {"jp": 75, "kr": 70, "ph": 65, "id": 50, "tw": 45},  # Further spread
    3: {"jp": 60, "kr": 55, "ph": 75, "id": 80, "tw": 50, "my": 35, "nz": 40},  # Reaches more regions
    4: {"jp": 45, "kr": 40, "ph": 60, "id": 70, "tw": 40, "my": 50, "nz": 65, "au": 35, "cl": 30},  # Wider spread
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
    },  # Maximum extent
}

# Sequential red palette - more distinct color steps for better visibility
# From light (low activity) to dark red (high activity)
colors = ("#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#cb181d")

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=64,
    label_font_size=40,
    legend_font_size=40,
    major_label_font_size=36,
    value_font_size=36,
    tooltip_font_size=32,
    no_data_font_size=32,
)

# Activity level labels and thresholds
activity_labels = [
    ("Minimal (<20)", lambda v: v < 20),
    ("Low (20-35)", lambda v: 20 <= v < 35),
    ("Moderate (35-50)", lambda v: 35 <= v < 50),
    ("High (50-65)", lambda v: 50 <= v < 65),
    ("Severe (65-80)", lambda v: 65 <= v < 80),
    ("Extreme (80+)", lambda v: v >= 80),
]


def bin_activity(data):
    """Bin activity values into categories for legend clarity."""
    bins = {label: {} for label, _ in activity_labels}
    for country, value in data.items():
        for label, condition in activity_labels:
            if condition(value):
                bins[label][country] = value
                break
    return bins


# Create the final time snapshot map (T6: +72 Hours - maximum spread)
# This represents the culmination of the temporal sequence
final_time_idx = 5
final_data = activity_by_time[final_time_idx]
binned_data = bin_activity(final_data)

worldmap = World(
    style=custom_style,
    width=4800,
    height=2700,
    title=f"Seismic Activity ({time_periods[final_time_idx]}) · map-animated-temporal · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    legend_box_size=36,
)

# Add all categories to ensure consistent legend across all snapshots
for label, _ in activity_labels:
    data = binned_data.get(label, {})
    worldmap.add(label, data if data else None)

# Save outputs
# Note: pygal doesn't support animation natively; this shows the final time snapshot
# representing the culmination of the seismic wave propagation across 72 hours
worldmap.render_to_file("plot.html")
worldmap.render_to_png("plot.png")
