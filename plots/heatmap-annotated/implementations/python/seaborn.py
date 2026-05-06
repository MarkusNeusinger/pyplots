"""anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-05-06
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data - Correlation matrix for realistic financial variables
np.random.seed(42)

variables = ["Stocks", "Bonds", "Gold", "Real Estate", "Crypto", "Commodities", "Cash"]

# Create a realistic correlation matrix with meaningful relationships
n = len(variables)
corr_matrix = np.eye(n)

# Define some realistic correlations
correlations = {
    (0, 1): -0.25,  # Stocks-Bonds (negative)
    (0, 2): 0.10,  # Stocks-Gold (weak positive)
    (0, 3): 0.55,  # Stocks-Real Estate (moderate positive)
    (0, 4): 0.65,  # Stocks-Crypto (positive)
    (0, 5): 0.40,  # Stocks-Commodities (moderate)
    (0, 6): 0.05,  # Stocks-Cash (near zero)
    (1, 2): 0.35,  # Bonds-Gold (positive)
    (1, 3): 0.20,  # Bonds-Real Estate (weak positive)
    (1, 4): -0.15,  # Bonds-Crypto (weak negative)
    (1, 5): 0.15,  # Bonds-Commodities (weak positive)
    (1, 6): 0.60,  # Bonds-Cash (positive)
    (2, 3): 0.10,  # Gold-Real Estate (weak)
    (2, 4): 0.30,  # Gold-Crypto (moderate)
    (2, 5): 0.50,  # Gold-Commodities (positive)
    (2, 6): 0.25,  # Gold-Cash (weak positive)
    (3, 4): 0.35,  # Real Estate-Crypto (moderate)
    (3, 5): 0.30,  # Real Estate-Commodities (moderate)
    (3, 6): -0.10,  # Real Estate-Cash (weak negative)
    (4, 5): 0.45,  # Crypto-Commodities (moderate)
    (4, 6): -0.20,  # Crypto-Cash (negative)
    (5, 6): 0.05,  # Commodities-Cash (near zero)
}

# Fill symmetric matrix
for (i, j), val in correlations.items():
    corr_matrix[i, j] = val
    corr_matrix[j, i] = val

# Create DataFrame
df_corr = pd.DataFrame(corr_matrix, index=variables, columns=variables)

# Plot - Square format (3600x3600 px at 300 DPI = 12x12 inches)
fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAGE_BG)

# Use seaborn's heatmap with annotations
sns.heatmap(
    df_corr,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    square=True,
    linewidths=0.5,
    linecolor=INK_SOFT,
    cbar_kws={"shrink": 0.75, "label": "Correlation", "ticks": [-1, -0.5, 0, 0.5, 1]},
    annot_kws={"size": 16, "weight": "bold"},
    ax=ax,
)

# Style
ax.set_facecolor(PAGE_BG)
ax.set_title("heatmap-annotated · seaborn · anyplot.ai", fontsize=24, pad=20, weight="bold", color=INK)
ax.set_xlabel("Asset Class", fontsize=20, color=INK)
ax.set_ylabel("Asset Class", fontsize=20, color=INK)
ax.tick_params(axis="both", labelsize=16, colors=INK_SOFT)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

# Adjust colorbar label size and colors
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14, colors=INK_SOFT)
cbar.ax.set_ylabel("Correlation", fontsize=16, color=INK)
cbar.outline.set_edgecolor(INK_SOFT)

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
