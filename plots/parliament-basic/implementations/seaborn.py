"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data: Generic parliament with 6 parties (neutral naming)
parties = ["Party A", "Party B", "Party C", "Party D", "Party E", "Party F"]
seats = [85, 72, 45, 38, 22, 18]
colors = ["#306998", "#FFD43B", "#2ECC71", "#E74C3C", "#9B59B6", "#F39C12"]
total_seats = sum(seats)

# Set seaborn style
sns.set_style("white")
sns.set_context("talk", font_scale=1.2)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Calculate parliament layout - semicircular arrangement with 5 rows
n_rows = 5
row_proportions = [(i + 1) for i in range(n_rows)]
total_prop = sum(row_proportions)
seats_per_row = [int(total_seats * p / total_prop) for p in row_proportions]
seats_per_row[-1] += total_seats - sum(seats_per_row)  # Adjust for rounding

# Create all seat positions in concentric arcs
all_positions = []
for row_idx, n_seats_row in enumerate(seats_per_row):
    radius = 0.4 + row_idx * 0.15
    angles = np.linspace(np.pi, 0, n_seats_row)
    for angle in angles:
        all_positions.append((radius * np.cos(angle), radius * np.sin(angle)))

# Sort positions left to right for natural party ordering
all_positions.sort(key=lambda p: (p[0], -p[1]))

# Assign seats to parties and collect coordinates
x_coords, y_coords, seat_colors = [], [], []
seat_idx = 0
for party_idx, n_seats in enumerate(seats):
    for _ in range(n_seats):
        if seat_idx < len(all_positions):
            x_coords.append(all_positions[seat_idx][0])
            y_coords.append(all_positions[seat_idx][1])
            seat_colors.append(colors[party_idx])
            seat_idx += 1

# Plot seats using scatter (seaborn styling applied via set_style/set_context)
ax.scatter(x_coords, y_coords, c=seat_colors, s=350, edgecolors="white", linewidths=1.5, zorder=2)

# Add majority threshold line
majority = total_seats // 2 + 1
ax.axhline(y=0, color="#666666", linestyle="--", linewidth=2, alpha=0.5, zorder=1)
ax.text(0.85, 0.02, f"Majority: {majority} seats", fontsize=14, color="#666666", ha="right", transform=ax.transAxes)

# Create legend with seat counts
legend_elements = [
    plt.scatter([], [], c=color, s=200, label=f"{party}: {seat_count}")
    for party, seat_count, color in zip(parties, seats, colors, strict=True)
]
ax.legend(
    handles=legend_elements,
    loc="upper left",
    fontsize=14,
    frameon=True,
    facecolor="white",
    edgecolor="lightgray",
    title="Parties",
    title_fontsize=16,
)

# Style adjustments
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-0.15, 1.0)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("parliament-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Add total seats annotation
ax.text(0.5, -0.08, f"Total: {total_seats} seats", fontsize=18, ha="center", transform=ax.transAxes, color="#333333")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
