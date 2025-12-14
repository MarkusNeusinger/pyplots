"""
polar-basic: Basic Polar Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for aesthetics
sns.set_theme(style="whitegrid")

# Data: Hourly activity pattern (24-hour cycle)
np.random.seed(42)

# Generate hourly data points (activity levels throughout the day)
hours = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])

# Activity levels with realistic daily pattern (low at night, peak in afternoon)
activity = np.array([15, 10, 8, 5, 5, 8, 25, 55, 75, 80, 70, 65, 60, 70, 85, 90, 88, 80, 70, 55, 45, 35, 25, 18])

# Add some variation with additional data points
n_extra = 24
extra_hours = np.random.uniform(0, 24, n_extra)
extra_activity = 40 + 30 * np.sin((extra_hours - 6) * np.pi / 12) + np.random.randn(n_extra) * 15
extra_activity = np.clip(extra_activity, 5, 100)

# Combine all data
all_hours = np.concatenate([hours, extra_hours])
all_activity = np.concatenate([activity, extra_activity])

# Convert hours to radians (clock-like: 0h at top, clockwise)
theta = (all_hours / 24) * 2 * np.pi

# Create polar plot (figsize 16x9 at dpi=300 gives 4800x2700)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, polar=True)

# Set clock-like orientation: 0 at top, clockwise
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# Plot data points using scatter with seaborn styling
ax.scatter(theta, all_activity, c="#306998", s=200, alpha=0.7, edgecolors="white", linewidths=1.5)

# Configure angular axis (hours) at standard clock positions
hour_labels = ["0h", "3h", "6h", "9h", "12h", "15h", "18h", "21h"]
hour_angles = [(h / 24) * 2 * np.pi for h in [0, 3, 6, 9, 12, 15, 18, 21]]
ax.set_xticks(hour_angles)
ax.set_xticklabels(hour_labels, fontsize=18)

# Configure radial axis (activity level)
ax.set_ylim(0, 110)
ax.set_yticks([25, 50, 75, 100])
ax.set_yticklabels(["25", "50", "75", "100"], fontsize=14, color="gray")

# Subtle gridlines
ax.grid(True, alpha=0.3, linestyle="--")

# Title
ax.set_title("polar-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300)
