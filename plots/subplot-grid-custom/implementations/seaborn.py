"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)

# Time series data for main plot (spanning 2 columns)
dates = pd.date_range("2024-01-01", periods=120, freq="D")
price = 100 + np.cumsum(np.random.randn(120) * 2)
df_main = pd.DataFrame({"Date": dates, "Price": price})

# Volume bar data
volume = np.random.randint(1000, 5000, size=12)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
df_volume = pd.DataFrame({"Month": months, "Volume": volume})

# Returns histogram data
returns = np.diff(price) / price[:-1] * 100
df_returns = pd.DataFrame({"Returns": returns})

# Scatter plot data
x_scatter = np.random.randn(80) * 15 + 50
y_scatter = x_scatter * 0.8 + np.random.randn(80) * 10 + 20
df_scatter = pd.DataFrame({"Variable_X": x_scatter, "Variable_Y": y_scatter})

# Category boxplot data
categories = np.repeat(["Q1", "Q2", "Q3", "Q4"], 30)
values = np.concatenate(
    [
        np.random.normal(50, 10, 30),
        np.random.normal(55, 12, 30),
        np.random.normal(60, 8, 30),
        np.random.normal(65, 15, 30),
    ]
)
df_box = pd.DataFrame({"Quarter": categories, "Performance": values})

# Create figure with GridSpec layout
fig = plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.30)

# Main plot: Time series spanning 2 columns (top-left 2x2 area)
ax_main = fig.add_subplot(gs[0:2, 0:2])
sns.lineplot(data=df_main, x="Date", y="Price", ax=ax_main, linewidth=3, color="#306998")
ax_main.set_title("Daily Price Trend", fontsize=20, fontweight="bold")
ax_main.set_xlabel("Date", fontsize=16)
ax_main.set_ylabel("Price ($)", fontsize=16)
ax_main.tick_params(axis="both", labelsize=12)
ax_main.tick_params(axis="x", rotation=0)
ax_main.grid(True, alpha=0.3, linestyle="--")
ax_main.fill_between(df_main["Date"], df_main["Price"], alpha=0.2, color="#306998")
ax_main.xaxis.set_major_locator(plt.MaxNLocator(5))
ax_main.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

# Top-right: Scatter plot
ax_scatter = fig.add_subplot(gs[0, 2])
sns.scatterplot(data=df_scatter, x="Variable_X", y="Variable_Y", ax=ax_scatter, s=120, alpha=0.7, color="#FFD43B")
ax_scatter.set_title("Correlation Analysis", fontsize=16, fontweight="bold")
ax_scatter.set_xlabel("Variable X", fontsize=14)
ax_scatter.set_ylabel("Variable Y", fontsize=14)
ax_scatter.tick_params(axis="both", labelsize=12)
ax_scatter.grid(True, alpha=0.3, linestyle="--")

# Middle-right: Boxplot (spanning vertically)
ax_box = fig.add_subplot(gs[1, 2])
sns.boxplot(data=df_box, x="Quarter", y="Performance", hue="Quarter", ax=ax_box, palette="Set2", legend=False)
ax_box.set_title("Quarterly Performance", fontsize=16, fontweight="bold")
ax_box.set_xlabel("Quarter", fontsize=14)
ax_box.set_ylabel("Performance Score", fontsize=14)
ax_box.tick_params(axis="both", labelsize=12)

# Bottom-left: Volume bar chart
ax_volume = fig.add_subplot(gs[2, 0])
sns.barplot(data=df_volume, x="Month", y="Volume", hue="Month", ax=ax_volume, palette="viridis", legend=False)
ax_volume.set_title("Monthly Volume", fontsize=16, fontweight="bold")
ax_volume.set_xlabel("Month", fontsize=14)
ax_volume.set_ylabel("Volume (Units)", fontsize=14)
ax_volume.tick_params(axis="x", labelsize=10, rotation=45)
ax_volume.tick_params(axis="y", labelsize=12)

# Bottom-center: Returns histogram
ax_hist = fig.add_subplot(gs[2, 1])
sns.histplot(data=df_returns, x="Returns", kde=True, ax=ax_hist, color="#306998", alpha=0.7, bins=20)
ax_hist.set_title("Returns Distribution", fontsize=16, fontweight="bold")
ax_hist.set_xlabel("Daily Returns (%)", fontsize=14)
ax_hist.set_ylabel("Frequency", fontsize=14)
ax_hist.tick_params(axis="both", labelsize=12)
ax_hist.axvline(x=0, color="#FFD43B", linewidth=2, linestyle="--", alpha=0.8)

# Bottom-right: Summary heatmap (correlation-style)
correlation_data = np.array([[1.0, 0.65, 0.42], [0.65, 1.0, 0.58], [0.42, 0.58, 1.0]])
labels = ["Price", "Volume", "Returns"]
ax_heatmap = fig.add_subplot(gs[2, 2])
sns.heatmap(
    correlation_data,
    annot=True,
    fmt=".2f",
    xticklabels=labels,
    yticklabels=labels,
    ax=ax_heatmap,
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    annot_kws={"size": 14},
    cbar_kws={"shrink": 0.8},
)
ax_heatmap.set_title("Correlation Matrix", fontsize=16, fontweight="bold")
ax_heatmap.tick_params(axis="both", labelsize=12)

# Main title
fig.suptitle("subplot-grid-custom · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
