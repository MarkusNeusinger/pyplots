"""
sankey-basic: Basic Sankey Diagram
Library: matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey


# Data: Energy flow from sources to consumption sectors
# Values in arbitrary units (e.g., TWh or percentage)
flows = [
    # Source flows (positive = into system)
    25,  # Coal
    35,  # Natural Gas
    20,  # Renewables
    20,  # Nuclear
    # Consumption flows (negative = out of system)
    -30,  # Industrial
    -25,  # Residential
    -20,  # Commercial
    -15,  # Transportation
    -10,  # Losses
]

labels = [
    "Coal",
    "Natural Gas",
    "Renewables",
    "Nuclear",
    "Industrial",
    "Residential",
    "Commercial",
    "Transportation",
    "Losses",
]

# Orientations: 1 = up, -1 = down, 0 = right
orientations = [
    1,  # Coal - from top
    1,  # Natural Gas - from top
    -1,  # Renewables - from bottom
    -1,  # Nuclear - from bottom
    0,  # Industrial - to right
    0,  # Residential - to right
    0,  # Commercial - to right
    0,  # Transportation - to right
    -1,  # Losses - to bottom
]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create Sankey diagram
sankey = Sankey(ax=ax, scale=0.01, offset=0.3, head_angle=120, format="%.0f", unit=" units")

# Add flows
sankey.add(
    flows=flows,
    labels=labels,
    orientations=orientations,
    pathlengths=[0.5, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 0.8, 0.5],
    facecolor="#306998",
    edgecolor="#306998",
    alpha=0.7,
)

# Finish the diagram
sankey.finish()

# Style
ax.set_title("Energy Flow: Sources to Consumption Sectors", fontsize=20, pad=20)
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
