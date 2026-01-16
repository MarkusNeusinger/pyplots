"""pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-01-16
"""

import matplotlib.pyplot as plt


# Hierarchical data: Sales by Region -> Country -> City
# Root level (regions)
regions = ["North America", "Europe", "Asia Pacific"]
region_values = [4500, 3200, 2800]

# Second level (countries within each region)
countries = {
    "North America": ["USA", "Canada", "Mexico"],
    "Europe": ["Germany", "UK", "France"],
    "Asia Pacific": ["Japan", "Australia", "India"],
}
country_values = {"North America": [2800, 1100, 600], "Europe": [1400, 1000, 800], "Asia Pacific": [1200, 900, 700]}

# Colors for regions (Python palette + complementary)
colors = ["#306998", "#FFD43B", "#4B8BBE"]

# Create figure with 2 rows: top shows all levels, bottom shows drilldown example
fig, axes = plt.subplots(2, 2, figsize=(16, 9))

# Top-left: Root level (all regions)
ax1 = axes[0, 0]
bars1 = ax1.bar(regions, region_values, color=colors, edgecolor="white", linewidth=2)
ax1.set_ylabel("Sales (M$)", fontsize=16)
ax1.set_title("Level 1: Regions", fontsize=18, fontweight="bold")
ax1.tick_params(axis="both", labelsize=14)
ax1.set_ylim(0, max(region_values) * 1.2)

# Add value labels on bars
for bar, val in zip(bars1, region_values, strict=True):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 100,
        f"${val}M",
        ha="center",
        va="bottom",
        fontsize=14,
        fontweight="bold",
    )

# Add click indicator arrows
for bar in bars1:
    ax1.annotate(
        "↓",
        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() * 0.5),
        ha="center",
        va="center",
        fontsize=20,
        color="white",
        fontweight="bold",
    )

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Top-right: Drilldown into North America
ax2 = axes[0, 1]
na_countries = countries["North America"]
na_values = country_values["North America"]
bars2 = ax2.bar(na_countries, na_values, color="#306998", edgecolor="white", linewidth=2, alpha=0.85)
ax2.set_ylabel("Sales (M$)", fontsize=16)
ax2.set_title("Level 2: North America → Countries", fontsize=18, fontweight="bold")
ax2.tick_params(axis="both", labelsize=14)
ax2.set_ylim(0, max(na_values) * 1.2)

for bar, val in zip(bars2, na_values, strict=True):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 80,
        f"${val}M",
        ha="center",
        va="bottom",
        fontsize=14,
        fontweight="bold",
    )

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# Bottom-left: Drilldown into Europe
ax3 = axes[1, 0]
eu_countries = countries["Europe"]
eu_values = country_values["Europe"]
bars3 = ax3.bar(eu_countries, eu_values, color="#FFD43B", edgecolor="white", linewidth=2, alpha=0.85)
ax3.set_ylabel("Sales (M$)", fontsize=16)
ax3.set_title("Level 2: Europe → Countries", fontsize=18, fontweight="bold")
ax3.tick_params(axis="both", labelsize=14)
ax3.set_ylim(0, max(eu_values) * 1.2)

for bar, val in zip(bars3, eu_values, strict=True):
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 50,
        f"${val}M",
        ha="center",
        va="bottom",
        fontsize=14,
        fontweight="bold",
    )

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

# Bottom-right: Drilldown into Asia Pacific
ax4 = axes[1, 1]
ap_countries = countries["Asia Pacific"]
ap_values = country_values["Asia Pacific"]
bars4 = ax4.bar(ap_countries, ap_values, color="#4B8BBE", edgecolor="white", linewidth=2, alpha=0.85)
ax4.set_ylabel("Sales (M$)", fontsize=16)
ax4.set_title("Level 2: Asia Pacific → Countries", fontsize=18, fontweight="bold")
ax4.tick_params(axis="both", labelsize=14)
ax4.set_ylim(0, max(ap_values) * 1.2)

for bar, val in zip(bars4, ap_values, strict=True):
    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 30,
        f"${val}M",
        ha="center",
        va="bottom",
        fontsize=14,
        fontweight="bold",
    )

ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

# Add main title with breadcrumb-style navigation indicator
fig.suptitle("bar-drilldown · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

# Add annotation explaining the static drilldown visualization
fig.text(
    0.5,
    0.02,
    "Static representation of hierarchical drilldown: Top-left shows root level, other panels show drilldown views",
    ha="center",
    fontsize=12,
    style="italic",
    color="#666666",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
