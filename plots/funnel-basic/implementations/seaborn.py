""" pyplots.ai
funnel-basic: Basic Funnel Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import seaborn as sns


# Apply seaborn styling
sns.set_theme(style="white")

# Data - Sales funnel example
stages = ["Awareness", "Interest", "Consideration", "Intent", "Purchase"]
values = [1000, 600, 400, 200, 100]

# Use seaborn color palette (Blues reversed, with Python Yellow for last stage)
blue_colors = sns.color_palette("Blues_r", n_colors=4)
colors = [blue_colors[i] for i in range(4)] + ["#FFD43B"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Calculate widths proportional to values (relative to max)
max_value = max(values)
widths = [v / max_value for v in values]

# Funnel parameters
n_stages = len(stages)
stage_height = 0.8 / n_stages  # Height of each stage
gap = 0.02  # Gap between stages
y_start = 0.9  # Starting y position (top)

# Draw funnel segments as trapezoids
for i, (stage, value, width, color) in enumerate(zip(stages, values, widths, colors, strict=True)):
    y_top = y_start - i * (stage_height + gap)
    y_bottom = y_top - stage_height

    # Current width and next width (for trapezoid shape)
    current_width = width
    next_width = widths[i + 1] if i < n_stages - 1 else width * 0.6

    # Calculate trapezoid corners (centered)
    x_left_top = 0.5 - current_width / 2
    x_right_top = 0.5 + current_width / 2
    x_left_bottom = 0.5 - next_width / 2
    x_right_bottom = 0.5 + next_width / 2

    # Create trapezoid
    trapezoid = patches.Polygon(
        [(x_left_top, y_top), (x_right_top, y_top), (x_right_bottom, y_bottom), (x_left_bottom, y_bottom)],
        closed=True,
        facecolor=color,
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(trapezoid)

    # Add stage label on the left
    ax.text(
        0.02, (y_top + y_bottom) / 2, stage, fontsize=20, fontweight="bold", va="center", ha="left", color="#333333"
    )

    # Add value and percentage on the segment
    percentage = (value / max_value) * 100
    ax.text(
        0.5,
        (y_top + y_bottom) / 2,
        f"{value:,}\n({percentage:.0f}%)",
        fontsize=18,
        fontweight="bold",
        va="center",
        ha="center",
        color="white" if i < len(colors) - 1 else "#333333",
    )

# Set axis limits and remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Title
ax.set_title("funnel-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
