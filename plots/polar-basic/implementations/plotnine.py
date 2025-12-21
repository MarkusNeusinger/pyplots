""" pyplots.ai
polar-basic: Basic Polar Chart
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - hourly activity pattern (24-hour cycle)
np.random.seed(42)
hours = np.arange(0, 24)
# Simulate activity with peaks in morning and evening
activity = 30 + 25 * np.sin((hours - 6) * np.pi / 12) + np.random.randn(24) * 5
activity = np.clip(activity, 5, 100)

df = pd.DataFrame({"hour": hours, "activity": activity})

# Convert hours to radians (full circle = 24 hours)
theta = (df["hour"] / 24) * 2 * np.pi
radius = df["activity"]

# Close the loop by appending first point at the end
theta_closed = np.append(theta, theta.iloc[0])
radius_closed = np.append(radius, radius.iloc[0])

# Create polar plot with plotnine-style sizing
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"polar": True})

# Start at top (12 o'clock position) and go clockwise
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw line and points with Python Blue
ax.plot(theta_closed, radius_closed, color="#306998", linewidth=3, alpha=0.8)
ax.scatter(theta, radius, color="#306998", s=200, alpha=0.9, zorder=5)

# Set angular labels (24-hour clock, starting at top)
hour_labels = ["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"]
hour_positions = np.array([0, 3, 6, 9, 12, 15, 18, 21]) / 24 * 2 * np.pi
ax.set_xticks(hour_positions)
ax.set_xticklabels(hour_labels, fontsize=18)

# Set radial gridlines and labels
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75])
ax.set_yticklabels(["25", "50", "75"], fontsize=14, color="gray")

# Grid styling - subtle, not dominant
ax.grid(True, linestyle="--", alpha=0.4, linewidth=1.5)

# Title in pyplots format
ax.set_title("polar-basic · plotnine · pyplots.ai", fontsize=24, pad=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
