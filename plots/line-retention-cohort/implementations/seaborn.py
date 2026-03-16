"""pyplots.ai
line-retention-cohort: User Retention Curve by Cohort
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-16
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)

cohorts = {"Jan 2025": 1245, "Feb 2025": 1380, "Mar 2025": 1510, "Apr 2025": 1420, "May 2025": 1605}

weeks = np.arange(0, 13)
records = []

decay_rates = [0.18, 0.16, 0.14, 0.12, 0.10]
floors = [8, 10, 14, 18, 22]

for (cohort_label, cohort_size), decay, floor in zip(cohorts.items(), decay_rates, floors, strict=True):
    retention = 100 * np.exp(-decay * weeks) + floor * (1 - np.exp(-0.3 * weeks))
    retention[0] = 100.0
    retention = np.clip(retention, 0, 100)
    noise = np.random.normal(0, 0.8, len(weeks))
    noise[0] = 0
    retention = np.clip(retention + noise, 0, 100)
    for w, r in zip(weeks, retention, strict=True):
        records.append({"week": w, "retention": r, "cohort": f"{cohort_label} (n={cohort_size:,})"})

df = pd.DataFrame(records)

# Plot
palette = ["#8FAABC", "#7B9EA8", "#306998", "#2A7F62", "#1B9E77"]
linewidths = [1.8, 2.0, 2.5, 2.8, 3.2]

fig, ax = plt.subplots(figsize=(16, 9))

for i, cohort_label in enumerate(df["cohort"].unique()):
    cohort_data = df[df["cohort"] == cohort_label]
    sns.lineplot(
        data=cohort_data,
        x="week",
        y="retention",
        label=cohort_label,
        color=palette[i],
        linewidth=linewidths[i],
        marker="o",
        markersize=6 + i,
        ax=ax,
    )

ax.axhline(y=20, color="#999999", linestyle="--", linewidth=1.2, alpha=0.6)
ax.text(12.2, 20, "20% target", fontsize=13, color="#999999", va="center")

# Style
ax.set_title("line-retention-cohort · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=20)
ax.set_xlabel("Weeks Since Signup", fontsize=20)
ax.set_ylabel("Retained Users (%)", fontsize=20)
ax.tick_params(axis="both", labelsize=16)

ax.set_xlim(-0.3, 12.5)
ax.set_ylim(0, 105)
ax.set_xticks(weeks)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

ax.legend(fontsize=14, frameon=False, loc="upper right", title="Signup Cohort", title_fontsize=15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
