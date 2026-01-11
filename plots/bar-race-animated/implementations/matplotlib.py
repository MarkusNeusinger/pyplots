""" pyplots.ai
bar-race-animated: Animated Bar Chart Race
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-11
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation


# Data: Tech company revenue growth over 10 years (in billions USD)
np.random.seed(42)

companies = [
    "TechCorp",
    "DataSoft",
    "CloudNet",
    "AppWorks",
    "NetBase",
    "ByteFlow",
    "CodeLabs",
    "DigiCore",
    "InfoSys",
    "WebScale",
]
years = list(range(2015, 2025))
n_companies = len(companies)
n_years = len(years)

# Generate realistic revenue data with different growth patterns
base_revenues = np.array([45, 38, 32, 28, 25, 22, 18, 15, 12, 10])
growth_rates = np.array([1.15, 1.22, 1.18, 1.25, 1.12, 1.30, 1.20, 1.16, 1.28, 1.19])

revenues = np.zeros((n_years, n_companies))
revenues[0] = base_revenues

for i in range(1, n_years):
    noise = np.random.uniform(0.9, 1.1, n_companies)
    revenues[i] = revenues[i - 1] * growth_rates * noise

# Create DataFrame for easier manipulation
data = []
for i, year in enumerate(years):
    for j, company in enumerate(companies):
        data.append({"year": year, "company": company, "revenue": revenues[i, j]})
df = pd.DataFrame(data)

# Assign consistent colors to each company
colors = ["#306998", "#FFD43B", "#E74C3C", "#2ECC71", "#9B59B6", "#F39C12", "#1ABC9C", "#E67E22", "#3498DB", "#95A5A6"]
color_map = dict(zip(companies, colors, strict=True))

# Create animation
fig, ax = plt.subplots(figsize=(16, 9))


def animate(frame):
    ax.clear()
    year = years[frame]
    year_data = df[df["year"] == year].copy()
    year_data = year_data.sort_values("revenue", ascending=True)

    # Create horizontal bars
    bar_colors = [color_map[c] for c in year_data["company"]]
    ax.barh(range(n_companies), year_data["revenue"], color=bar_colors, height=0.7, edgecolor="white", linewidth=1)

    # Add company labels and values
    for i, (_idx, row) in enumerate(year_data.iterrows()):
        ax.text(
            row["revenue"] + 2, i, f"${row['revenue']:.1f}B", va="center", ha="left", fontsize=14, fontweight="bold"
        )
        ax.text(5, i, row["company"], va="center", ha="left", fontsize=14, color="white", fontweight="bold")

    # Year indicator
    ax.text(
        0.98,
        0.02,
        str(year),
        transform=ax.transAxes,
        fontsize=72,
        fontweight="bold",
        ha="right",
        va="bottom",
        color="#306998",
        alpha=0.3,
    )

    # Styling
    ax.set_xlim(0, df["revenue"].max() * 1.15)
    ax.set_ylim(-0.5, n_companies - 0.5)
    ax.set_yticks([])
    ax.set_xlabel("Revenue (Billion USD)", fontsize=20)
    ax.set_title("bar-race-animated · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
    ax.tick_params(axis="x", labelsize=16)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")

    plt.tight_layout()


# Create animation
anim = FuncAnimation(fig, animate, frames=n_years, interval=500, repeat=True)

# Save as animated GIF and static PNG
anim.save("plot.gif", writer="pillow", fps=2, dpi=169)

# Save final frame as PNG
animate(n_years - 1)
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
