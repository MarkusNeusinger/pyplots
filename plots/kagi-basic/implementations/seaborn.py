"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style and context for large canvas
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.3)

# Generate synthetic stock price data
np.random.seed(42)
n_days = 250

# Simulate realistic stock price movement (starting at $100)
returns = np.random.normal(0.0005, 0.02, n_days)
prices = 100 * np.cumprod(1 + returns)

# Kagi chart parameters
reversal_threshold = 0.04  # 4% reversal

# Build Kagi chart segments from price data
segments = []
direction = None  # 1 = up, -1 = down
current_price = prices[0]
last_high = prices[0]
last_low = prices[0]

for price in prices[1:]:
    if direction is None:
        # Initialize direction
        if price > current_price * (1 + reversal_threshold):
            direction = 1
            segments.append({"start": current_price, "end": price, "yang": price > last_high})
            last_high = max(last_high, price)
            current_price = price
        elif price < current_price * (1 - reversal_threshold):
            direction = -1
            segments.append({"start": current_price, "end": price, "yang": False})
            last_low = min(last_low, price)
            current_price = price
    elif direction == 1:
        # Currently going up
        if price > current_price:
            # Continue up - extend last segment
            if segments:
                segments[-1]["end"] = price
                segments[-1]["yang"] = price > last_high
            current_price = price
            last_high = max(last_high, price)
        elif price < current_price * (1 - reversal_threshold):
            # Reversal down
            direction = -1
            segments.append({"start": current_price, "end": price, "yang": price > last_low})
            current_price = price
            if price < last_low:
                last_low = price
    else:
        # Currently going down
        if price < current_price:
            # Continue down - extend last segment
            if segments:
                segments[-1]["end"] = price
            current_price = price
            last_low = min(last_low, price)
        elif price > current_price * (1 + reversal_threshold):
            # Reversal up
            direction = 1
            segments.append({"start": current_price, "end": price, "yang": price > last_high})
            current_price = price
            if price > last_high:
                last_high = price

# Create figure with seaborn styling
fig, ax = plt.subplots(figsize=(16, 9))

# Colors per specification: green for yang (bullish), red for yin (bearish)
yang_color = "#2E8B57"  # Sea green for bullish
yin_color = "#DC143C"  # Crimson for bearish

# Plot Kagi chart segments
x_pos = 0
for i, seg in enumerate(segments):
    # Determine line properties based on yang/yin
    color = yang_color if seg["yang"] else yin_color
    linewidth = 5 if seg["yang"] else 2  # Thick for yang, thin for yin

    # Draw vertical line for this segment
    ax.plot([x_pos, x_pos], [seg["start"], seg["end"]], color=color, linewidth=linewidth, solid_capstyle="butt")

    # Draw horizontal connector to next segment (shoulder/waist)
    if i < len(segments) - 1:
        ax.plot([x_pos, x_pos + 1], [seg["end"], seg["end"]], color=color, linewidth=linewidth, solid_capstyle="butt")

    x_pos += 1

# Add legend with seaborn-compatible styling
yang_line = plt.Line2D([0], [0], color=yang_color, linewidth=5, label="Yang (Bullish)")
yin_line = plt.Line2D([0], [0], color=yin_color, linewidth=2, label="Yin (Bearish)")
ax.legend(handles=[yang_line, yin_line], loc="upper left", fontsize=16, framealpha=0.9)

# Labels and styling
ax.set_xlabel("Kagi Line Index", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("kagi-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Subtle grid (seaborn whitegrid already provides this)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Set axis limits with padding
y_min = min(min(seg["start"], seg["end"]) for seg in segments)
y_max = max(max(seg["start"], seg["end"]) for seg in segments)
padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - padding, y_max + padding)
ax.set_xlim(-1, len(segments))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
