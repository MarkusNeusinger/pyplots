"""pyplots.ai
area-basic: Basic Area Chart
Library: seaborn 0.13.2 | Python 3.14.2
Quality: 86/100 | Created: 2025-12-23
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import PathPatch
from matplotlib.path import Path


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

# Simulate realistic web traffic with weekly pattern, trend, and a traffic spike
base_visitors = 5000
trend = np.linspace(0, 1500, 30)
weekly_pattern = np.array([1.0, 1.1, 1.15, 1.2, 1.1, 0.7, 0.65] * 5)[:30]
noise = np.random.randn(30) * 300
visitors = (base_visitors + trend) * weekly_pattern + noise
visitors[17] *= 1.45  # Traffic spike from a viral post on day 18
visitors = np.maximum(visitors, 1000)

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Plot - use seaborn's theme management for coherent styling
sns.set_theme(
    style="white",
    context="talk",
    font_scale=1.2,
    rc={"axes.spines.top": False, "axes.spines.right": False, "grid.alpha": 0.2, "grid.linewidth": 0.8},
)

fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn's lineplot for the area boundary
sns.lineplot(data=df, x="date", y="visitors", ax=ax, color="#306998", linewidth=3)

# Gradient fill using imshow clipped to the area
y_max = df["visitors"].max() * 1.12
x_num = mdates.date2num(df["date"])
gradient = np.linspace(0, 1, 256).reshape(-1, 1)
gradient = np.hstack([gradient, gradient])
ax.imshow(
    gradient,
    aspect="auto",
    extent=[x_num[0], x_num[-1], 0, y_max],
    origin="lower",
    cmap=sns.light_palette("#306998", as_cmap=True),
    alpha=0.5,
    zorder=1,
)
# Clip the gradient to the area under the curve
vertices = list(zip(x_num, df["visitors"], strict=True)) + [(x_num[-1], 0), (x_num[0], 0)]
codes = [Path.MOVETO] + [Path.LINETO] * (len(vertices) - 1)
clip_path = Path(vertices, codes)
patch = PathPatch(clip_path, transform=ax.transData, facecolor="none", edgecolor="none")
ax.add_patch(patch)
for im in ax.images:
    im.set_clip_path(patch)

# Annotate the traffic spike with deliberate positioning
spike_idx = 17
spike_val = df["visitors"].iloc[spike_idx]
ax.annotate(
    "Viral post",
    xy=(df["date"].iloc[spike_idx], spike_val),
    xytext=(df["date"].iloc[spike_idx - 9], spike_val * 0.82),
    fontsize=16,
    fontweight="semibold",
    color="#1a3a5c",
    arrowprops={"arrowstyle": "->", "color": "#1a3a5c", "lw": 2, "connectionstyle": "arc3,rad=-0.2"},
    ha="center",
    va="top",
)

# Style - axis labels and title
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Visitors (count)", fontsize=20)
ax.set_title("area-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, pad=16)
ax.tick_params(axis="both", labelsize=16)

# Use seaborn's despine for idiomatic spine removal
sns.despine(ax=ax)

# Enable y-axis grid below data
ax.yaxis.grid(True)
ax.set_axisbelow(True)

# Y-axis: thousands separator formatting
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# X-axis: clean date formatting ("Jan 01" style)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_minor_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# Set y-axis to start at 0
ax.set_ylim(bottom=0, top=y_max)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
