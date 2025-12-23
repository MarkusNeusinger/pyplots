""" pyplots.ai
sankey-basic: Basic Sankey Diagram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 45/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.sankey import Sankey


# Apply seaborn styling
sns.set_theme(style="white", context="talk", font_scale=1.2)

# Data - Energy flow from sources to sectors (in arbitrary units)
# Sources flow into a central node which distributes to end-use sectors
# The diagram must balance: total inputs = total outputs

# Input flows (energy sources) - total: 165 units
coal_in = 60
gas_in = 60
nuclear_in = 45

# Output flows (energy sectors) - total: 165 units
residential_out = 50
commercial_out = 45
industrial_out = 70

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn color palette - using Python Blue as primary
palette = sns.color_palette(["#306998", "#FFD43B", "#4CAF50"])

# Create Sankey diagram
# Flows must sum to zero for a balanced diagram
sankey = Sankey(
    ax=ax, scale=0.004, offset=0.3, head_angle=110, format="%.0f", unit=" units", gap=0.4, radius=0.1, shoulder=0.03
)

# Define flows: positive = input (from left), negative = output (to right)
flows = [coal_in, gas_in, nuclear_in, -residential_out, -commercial_out, -industrial_out]
labels = ["Coal", "Gas", "Nuclear", "Residential", "Commercial", "Industrial"]
orientations = [-1, 0, 1, -1, 0, 1]  # -1=down, 0=horizontal, 1=up
pathlengths = [0.5, 0.25, 0.5, 0.5, 0.25, 0.5]

# Add the main Sankey diagram with seaborn-style colors
sankey.add(
    flows=flows,
    labels=labels,
    orientations=orientations,
    pathlengths=pathlengths,
    facecolor=palette[0],  # Python Blue
    alpha=0.75,
    edgecolor="#1a3a52",
    linewidth=2.5,
)

# Finish and apply styling
diagrams = sankey.finish()

# Style the labels with larger fonts for visibility at 4800x2700
for diagram in diagrams:
    for text in diagram.texts:
        text.set_fontsize(20)
        text.set_fontweight("bold")
        text.set_color("#333333")

# Set title using the required format
ax.set_title("Energy Flow Distribution · sankey-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Remove axis decorations
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
