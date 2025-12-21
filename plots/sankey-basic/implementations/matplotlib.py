""" pyplots.ai
sankey-basic: Basic Sankey Diagram
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey


# Data - Energy flow example (in arbitrary units)
# A single balanced flow: Total input = Total output
# Sources flow into a central node, which distributes to sectors

# Flow values
coal_in = 60
gas_in = 60
nuclear_in = 45
total_in = coal_in + gas_in + nuclear_in  # 165

residential_out = 50
commercial_out = 45
industrial_out = 70
total_out = residential_out + commercial_out + industrial_out  # 165

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create Sankey diagram
# Flows: positive = input, negative = output
# They must sum to zero for a balanced diagram
sankey = Sankey(
    ax=ax, scale=0.004, offset=0.3, head_angle=110, format="%.0f", unit=" units", gap=0.4, radius=0.1, shoulder=0.03
)

# Add the main diagram
# Inputs (positive) come from left, outputs (negative) go to right
flows = [coal_in, gas_in, nuclear_in, -residential_out, -commercial_out, -industrial_out]
labels = ["Coal", "Gas", "Nuclear", "Residential", "Commercial", "Industrial"]
orientations = [-1, 0, 1, -1, 0, 1]  # -1=down, 0=horizontal, 1=up
pathlengths = [0.5, 0.25, 0.5, 0.5, 0.25, 0.5]

sankey.add(
    flows=flows,
    labels=labels,
    orientations=orientations,
    pathlengths=pathlengths,
    facecolor="#306998",
    alpha=0.7,
    edgecolor="#1a3a52",
    linewidth=2,
)

# Finish and style the diagram
diagrams = sankey.finish()

# Increase text sizes for all labels
for diagram in diagrams:
    for text in diagram.texts:
        text.set_fontsize(20)
        text.set_fontweight("bold")

# Set title and style
ax.set_title(
    "Energy Flow Distribution · sankey-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
