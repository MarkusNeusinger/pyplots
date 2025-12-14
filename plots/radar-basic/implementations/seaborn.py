"""
radar-basic: Basic Radar Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for aesthetics
sns.set_theme(style="whitegrid")

# Data: Employee performance metrics
categories = ["Communication", "Technical Skills", "Teamwork", "Problem Solving", "Leadership", "Creativity"]
values = [85, 90, 75, 88, 70, 82]

# Close the polygon by repeating the first value
values_closed = values + [values[0]]
num_vars = len(categories)

# Calculate angles for each axis (in radians)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

# Create polar plot (figsize adjusted for tight_layout to achieve 4800x2700)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, polar=True)

# Plot the radar area
ax.fill(angles, values_closed, color="#306998", alpha=0.25)
ax.plot(angles, values_closed, color="#306998", linewidth=3, marker="o", markersize=12)

# Configure the axes
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=18)

# Set radial limits and gridlines
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=14, color="gray")

# Subtle gridlines
ax.grid(True, alpha=0.3, linestyle="--")

# Title
ax.set_title("radar-basic · seaborn · pyplots.ai", fontsize=24, pad=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300)
