"""pyplots.ai
indicator-bollinger: Bollinger Bands Indicator Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Generate realistic stock price data with Bollinger Bands
np.random.seed(42)
n_days = 120

# Generate cumulative price movement (random walk with drift)
dates = pd.date_range(start="2025-07-01", periods=n_days, freq="B")  # Business days
returns = np.random.normal(0.0005, 0.015, n_days)  # Small positive drift, realistic volatility
price_base = 150.0
close = price_base * np.cumprod(1 + returns)

# Calculate Bollinger Bands (20-period SMA, 2 standard deviations)
window = 20
df = pd.DataFrame({"date": dates, "close": close})
df["sma"] = df["close"].rolling(window=window).mean()
df["std"] = df["close"].rolling(window=window).std()
df["upper_band"] = df["sma"] + 2 * df["std"]
df["lower_band"] = df["sma"] - 2 * df["std"]

# Drop NaN values from rolling calculations
df = df.dropna().reset_index(drop=True)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Fill between upper and lower bands
ax.fill_between(
    df["date"], df["lower_band"], df["upper_band"], alpha=0.25, color="#306998", label="Bollinger Bands (±2σ)"
)

# Plot the bands and price using seaborn
sns.lineplot(data=df, x="date", y="upper_band", ax=ax, color="#306998", linewidth=2, linestyle="-", label="Upper Band")
sns.lineplot(data=df, x="date", y="lower_band", ax=ax, color="#306998", linewidth=2, linestyle="-", label="Lower Band")
sns.lineplot(data=df, x="date", y="sma", ax=ax, color="#FFD43B", linewidth=2.5, linestyle="--", label="20-day SMA")
sns.lineplot(data=df, x="date", y="close", ax=ax, color="#1a1a2e", linewidth=3, label="Close Price")

# Styling
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("indicator-bollinger · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Legend
ax.legend(loc="upper left", fontsize=14, framealpha=0.9)

# Format x-axis dates
fig.autofmt_xdate(rotation=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
