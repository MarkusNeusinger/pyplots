"""
sankey-basic: Basic Sankey Diagram
Library: seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.sankey import Sankey


# Apply seaborn styling
sns.set_theme(style="whitegrid")

# Data: Energy flow from sources to end uses (in TWh)
# Flows represent a simplified energy system
sources = ["Coal", "Natural Gas", "Nuclear", "Renewables"]
targets = ["Residential", "Commercial", "Industrial", "Transport"]

# Flow matrix: rows = sources, columns = targets
# Each value represents energy flow from source to target
flows_data = {
    "Coal": {"Residential": 5, "Commercial": 8, "Industrial": 35, "Transport": 2},
    "Natural Gas": {"Residential": 25, "Commercial": 18, "Industrial": 20, "Transport": 5},
    "Nuclear": {"Residential": 12, "Commercial": 10, "Industrial": 8, "Transport": 0},
    "Renewables": {"Residential": 8, "Commercial": 6, "Industrial": 5, "Transport": 3},
}

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create Sankey diagram
# matplotlib's Sankey uses a different approach - flows in/out of nodes
# Positive values = inputs, negative values = outputs

# Calculate total flows for each source and target
source_totals = {s: sum(flows_data[s].values()) for s in sources}
target_totals = {t: sum(flows_data[s][t] for s in sources) for t in targets}

# Create a single Sankey with the main flow
sankey = Sankey(ax=ax, scale=0.008, offset=0.3, head_angle=120, shoulder=0.05, gap=0.4, radius=0.1)

# Input flows (from sources) - positive values
source_flows = [source_totals[s] for s in sources]
# Output flows (to targets) - negative values
target_flows = [-target_totals[t] for t in targets]

# All flows: sources come in (positive), targets go out (negative)
all_flows = source_flows + target_flows
all_labels = sources + targets

# Orientations: sources from left (-1), targets to right (1)
# 0=right, 1=down, -1=up, 2=left
orientations = [-1, -1, 1, 1, 0, 0, 0, 0]

# Path lengths
pathlengths = [0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5]

# Create the diagram
sankey.add(
    flows=all_flows,
    labels=all_labels,
    orientations=orientations,
    pathlengths=pathlengths,
    facecolor="#306998",
    edgecolor="#306998",
    alpha=0.7,
)

# Style the diagram
sankey.finish()

# Update text properties for visibility at 4800x2700
for text in ax.texts:
    text.set_fontsize(18)
    text.set_fontweight("bold")

# Title and labels
ax.set_title(
    "Energy Flow Distribution (TWh) \u00b7 sankey-basic \u00b7 seaborn \u00b7 pyplots.ai",
    fontsize=24,
    fontweight="bold",
    pad=20,
)

# Remove axes
ax.axis("off")

# Adjust layout
plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
