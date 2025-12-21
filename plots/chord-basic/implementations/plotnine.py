""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Migration flows between continents
flows = pd.DataFrame(
    {
        "source": [
            "Asia",
            "Asia",
            "Asia",
            "Europe",
            "Europe",
            "Europe",
            "Africa",
            "Africa",
            "Americas",
            "Americas",
            "Oceania",
        ],
        "target": [
            "Europe",
            "Americas",
            "Oceania",
            "Americas",
            "Asia",
            "Africa",
            "Europe",
            "Americas",
            "Europe",
            "Asia",
            "Asia",
        ],
        "value": [45, 35, 15, 40, 25, 20, 30, 25, 15, 10, 8],
    }
)

# Define entities and their colors (Python Blue primary, then colorblind-safe)
entities = ["Asia", "Europe", "Americas", "Africa", "Oceania"]
colors = {
    "Asia": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Americas": "#4ECDC4",  # Teal
    "Africa": "#E76F51",  # Coral
    "Oceania": "#8338EC",  # Purple
}

# Calculate total flow for each entity (sum of incoming and outgoing)
entity_totals = {}
for entity in entities:
    outgoing = flows[flows["source"] == entity]["value"].sum()
    incoming = flows[flows["target"] == entity]["value"].sum()
    entity_totals[entity] = outgoing + incoming

total_flow = sum(entity_totals.values())

# Calculate arc positions around the circle
gap_angle = 0.05
total_gap = gap_angle * len(entities)
available_angle = 2 * np.pi - total_gap

# Calculate start/end angles for each entity arc
arc_positions = {}
current_angle = 0
for entity in entities:
    arc_size = (entity_totals[entity] / total_flow) * available_angle
    arc_positions[entity] = {
        "start": current_angle,
        "end": current_angle + arc_size,
        "mid": current_angle + arc_size / 2,
        "size": arc_size,
        "flow_offset_out": 0,
        "flow_offset_in": arc_size / 2,
    }
    current_angle += arc_size + gap_angle

# Create figure (16:9 aspect ratio for 4800x2700 at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_aspect("equal")

# Radii for the diagram
outer_radius = 0.95
inner_radius = 0.85
label_radius = 1.08

# Draw outer arcs for each entity
for entity in entities:
    pos = arc_positions[entity]
    theta = np.linspace(pos["start"], pos["end"], 100)

    # Create arc polygon
    x_outer = outer_radius * np.cos(theta)
    y_outer = outer_radius * np.sin(theta)
    x_inner = inner_radius * np.cos(theta[::-1])
    y_inner = inner_radius * np.sin(theta[::-1])

    x_polygon = np.concatenate([x_outer, x_inner])
    y_polygon = np.concatenate([y_outer, y_inner])

    ax.fill(x_polygon, y_polygon, color=colors[entity], alpha=0.9, edgecolor="white", linewidth=2)

    # Add entity label
    label_angle = pos["mid"]
    label_x = label_radius * np.cos(label_angle)
    label_y = label_radius * np.sin(label_angle)

    # Rotate text for readability
    rotation = np.degrees(label_angle)
    if 90 < rotation < 270:
        rotation += 180
        ha = "right"
    else:
        ha = "left"

    ax.text(
        label_x,
        label_y,
        entity,
        fontsize=20,
        fontweight="bold",
        ha=ha,
        va="center",
        rotation=rotation,
        rotation_mode="anchor",
        color=colors[entity],
    )

# Draw all chords
for _, row in flows.iterrows():
    source = row["source"]
    target = row["target"]
    value = row["value"]

    src_pos = arc_positions[source]
    tgt_pos = arc_positions[target]

    # Calculate chord width proportional to value
    src_width = (value / entity_totals[source]) * src_pos["size"] * 0.45
    tgt_width = (value / entity_totals[target]) * tgt_pos["size"] * 0.45

    # Source and target positions on the arcs
    src_start = src_pos["start"] + src_pos["flow_offset_out"]
    src_end = src_start + src_width
    src_pos["flow_offset_out"] += src_width

    tgt_start = tgt_pos["start"] + tgt_pos["flow_offset_in"]
    tgt_end = tgt_start + tgt_width
    tgt_pos["flow_offset_in"] += tgt_width

    # Source and target arc points
    src_angles = np.linspace(src_start, src_end, 20)
    src_x = inner_radius * np.cos(src_angles)
    src_y = inner_radius * np.sin(src_angles)

    tgt_angles = np.linspace(tgt_end, tgt_start, 20)
    tgt_x = inner_radius * np.cos(tgt_angles)
    tgt_y = inner_radius * np.sin(tgt_angles)

    # Bezier curves connecting source and target
    n_bezier = 30
    t = np.linspace(0, 1, n_bezier)
    ctrl_factor = 0.3

    # First bezier: source end to target start
    p0 = np.array([src_x[-1], src_y[-1]])
    p3 = np.array([tgt_x[0], tgt_y[0]])
    p1 = p0 * ctrl_factor
    p2 = p3 * ctrl_factor

    bezier1_x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
    bezier1_y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]

    # Second bezier: target end to source start
    p0 = np.array([tgt_x[-1], tgt_y[-1]])
    p3 = np.array([src_x[0], src_y[0]])
    p1 = p0 * ctrl_factor
    p2 = p3 * ctrl_factor

    bezier2_x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
    bezier2_y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]

    # Combine into chord polygon
    x_chord = np.concatenate([src_x, bezier1_x, tgt_x, bezier2_x])
    y_chord = np.concatenate([src_y, bezier1_y, tgt_y, bezier2_y])

    ax.fill(x_chord, y_chord, color=colors[source], alpha=0.5, edgecolor="none")

# Title
ax.set_title("Migration Flows · chord-basic · plotnine · pyplots.ai", fontsize=28, fontweight="bold", pad=20)

# Set axis limits and remove axes
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.3, 1.3)
ax.axis("off")

# Legend (positioned to avoid overlap with labels)
legend_handles = [mpatches.Patch(color=colors[entity], label=entity, alpha=0.9) for entity in entities]
ax.legend(
    handles=legend_handles,
    loc="upper left",
    fontsize=16,
    framealpha=0.9,
    title="Regions",
    title_fontsize=18,
    bbox_to_anchor=(-0.05, 1.0),
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
