""" pyplots.ai
histogram-epidemic: Epidemic Curve (Epi Curve)
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 68/100 | Created: 2026-03-05
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

dates_range = pd.date_range("2024-01-15", periods=120, freq="D")

confirmed_base = np.concatenate(
    [
        np.linspace(2, 35, 30),
        np.linspace(35, 80, 15),
        np.linspace(80, 120, 10),
        np.linspace(120, 60, 20),
        np.linspace(60, 25, 15),
        np.linspace(25, 45, 10),
        np.linspace(45, 15, 20),
    ]
)
confirmed_counts = np.maximum(0, confirmed_base + np.random.normal(0, 8, 120)).astype(int)

probable_counts = np.maximum(0, confirmed_counts * 0.25 + np.random.normal(0, 3, 120)).astype(int)
suspect_counts = np.maximum(0, confirmed_counts * 0.12 + np.random.normal(0, 2, 120)).astype(int)

df = pd.DataFrame(
    {
        "onset_date": np.tile(dates_range, 3),
        "case_count": np.concatenate([confirmed_counts, probable_counts, suspect_counts]),
        "case_type": (["Confirmed"] * 120 + ["Probable"] * 120 + ["Suspect"] * 120),
    }
)

pivot = df.pivot_table(index="onset_date", columns="case_type", values="case_count", aggfunc="sum")
pivot = pivot[["Confirmed", "Probable", "Suspect"]]
cumulative = pivot.sum(axis=1).cumsum()

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

colors = {"Confirmed": "#306998", "Probable": "#E8A838", "Suspect": "#A8D8A8"}

ax.bar(
    pivot.index,
    pivot["Confirmed"],
    width=1.0,
    label="Confirmed",
    color=colors["Confirmed"],
    edgecolor="white",
    linewidth=0.3,
)
ax.bar(
    pivot.index,
    pivot["Probable"],
    width=1.0,
    bottom=pivot["Confirmed"],
    label="Probable",
    color=colors["Probable"],
    edgecolor="white",
    linewidth=0.3,
)
ax.bar(
    pivot.index,
    pivot["Suspect"],
    width=1.0,
    bottom=pivot["Confirmed"] + pivot["Probable"],
    label="Suspect",
    color=colors["Suspect"],
    edgecolor="white",
    linewidth=0.3,
)

ax2 = ax.twinx()
ax2.plot(pivot.index, cumulative, color="#C04040", linewidth=2.5, alpha=0.85, label="Cumulative Cases")
ax2.set_ylabel("Cumulative Cases", fontsize=20, color="#C04040")
ax2.tick_params(axis="y", labelsize=16, colors="#C04040")
ax2.spines["top"].set_visible(False)

intervention_dates = [
    (pd.Timestamp("2024-02-20"), "Travel\nRestrictions"),
    (pd.Timestamp("2024-03-25"), "Vaccination\nCampaign"),
]
for date, label in intervention_dates:
    ax.axvline(date, color="#555555", linewidth=1.5, linestyle="--", alpha=0.7, zorder=5)
    ax.text(
        date,
        ax.get_ylim()[1] * 0.92,
        label,
        fontsize=13,
        ha="center",
        va="top",
        color="#555555",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#CCCCCC", "alpha": 0.85},
    )

# Style
ax.set_xlabel("Date of Symptom Onset", fontsize=20)
ax.set_ylabel("New Cases", fontsize=20)
ax.set_title("histogram-epidemic · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=20)
ax.tick_params(axis="both", labelsize=16)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

lines_1, labels_1 = ax.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax.legend(lines_1 + lines_2, labels_1 + labels_2, fontsize=14, loc="upper left", framealpha=0.9)

# Save
plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
