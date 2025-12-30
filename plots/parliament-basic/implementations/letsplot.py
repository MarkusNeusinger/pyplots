# ruff: noqa: F405
"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import os

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()

# Data - Sample parliament composition with generic party names
parties = [
    "Progressive Party",
    "Center Alliance",
    "Liberal Democrats",
    "Green Coalition",
    "Conservative Union",
    "Reform Movement",
]
seats = [85, 72, 58, 35, 95, 55]
colors = ["#306998", "#FFD43B", "#2E8B57", "#32CD32", "#DC143C", "#9370DB"]

total_seats = sum(seats)


# Calculate seat positions in semicircular arrangement
# Seats arranged in multiple concentric arcs
def calculate_parliament_seats(seats_per_party, n_rows=5):
    """Calculate x, y positions for parliament seats in semicircular arcs."""
    total = sum(seats_per_party)

    # Distribute seats across rows (more seats in outer rows)
    row_weights = np.array([i + 1 for i in range(n_rows)])
    seats_per_row = (row_weights / row_weights.sum() * total).astype(int)
    seats_per_row[-1] += total - seats_per_row.sum()  # Adjust for rounding

    x_positions = []
    y_positions = []
    party_labels = []

    party_index = 0
    remaining_in_party = seats_per_party[0]

    for row_idx, row_seats in enumerate(seats_per_row):
        radius = 0.5 + row_idx * 0.12  # Radius increases for outer rows
        angles = np.linspace(np.pi, 0, row_seats)  # Semicircle from left to right

        for angle in angles:
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            x_positions.append(x)
            y_positions.append(y)
            party_labels.append(parties[party_index])

            remaining_in_party -= 1
            if remaining_in_party == 0 and party_index < len(seats_per_party) - 1:
                party_index += 1
                remaining_in_party = seats_per_party[party_index]

    return x_positions, y_positions, party_labels


x_coords, y_coords, party_assignment = calculate_parliament_seats(seats)

# Create DataFrame
df = pd.DataFrame({"x": x_coords, "y": y_coords, "party": party_assignment})

# Create legend labels with seat counts
party_seat_counts = dict(zip(parties, seats, strict=True))
df["party_label"] = df["party"].apply(lambda p: f"{p} ({party_seat_counts[p]})")

# Create color mapping for labels
label_colors = {f"{p} ({s})": c for p, s, c in zip(parties, seats, colors, strict=True)}
color_values = [label_colors[label] for label in df["party_label"].unique()]

# Build the plot
plot = (
    ggplot(df, aes(x="x", y="y", color="party_label"))
    + geom_point(size=5, alpha=0.9)
    + scale_color_manual(values=color_values)
    + coord_fixed(ratio=1)
    + theme_void()
    + labs(title="parliament-basic · letsplot · pyplots.ai", color="Party (Seats)")
    + ggsize(1600, 900)
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        plot_margin=[40, 40, 40, 40],
    )
)

# Add majority line annotation (horizontal line at y=0)
plot = plot + geom_hline(yintercept=0, color="#333333", size=1.5, alpha=0.6)

# Add total seats annotation using geom_text with a data point
annotation_df = pd.DataFrame(
    {"x": [0], "y": [-0.15], "label": [f"Total: {total_seats} seats | Majority: {total_seats // 2 + 1}"]}
)
plot = plot + geom_text(
    data=annotation_df, mapping=aes(x="x", y="y", label="label"), size=14, color="#333333"
)

# Save as PNG and HTML
current_dir = os.getcwd()
ggsave(plot, os.path.join(current_dir, "plot.png"), scale=3)
ggsave(plot, os.path.join(current_dir, "plot.html"))
