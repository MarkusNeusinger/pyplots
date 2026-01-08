""" pyplots.ai
kagi-basic: Basic Kagi Chart
Library: plotly 6.5.1 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import numpy as np
import plotly.graph_objects as go


# Generate sample price data (simulated stock prices over 200 days)
np.random.seed(42)
n_days = 200
returns = np.random.normal(0.001, 0.02, n_days)
prices = 100 * np.cumprod(1 + returns)

# Kagi chart parameters
reversal_pct = 0.04  # 4% reversal threshold

# Build Kagi chart data
kagi_x = [0]
kagi_y = [prices[0]]
directions = [1]  # 1 = up (yang), -1 = down (yin)
current_direction = 1
current_high = prices[0]
current_low = prices[0]
line_index = 0

for price in prices[1:]:
    if current_direction == 1:  # Currently in uptrend
        if price > current_high:
            # Continue uptrend - extend the line
            current_high = price
            kagi_y[-1] = price
        elif price <= current_high * (1 - reversal_pct):
            # Reversal down - add shoulder and new descending line
            line_index += 1
            kagi_x.extend([line_index, line_index])
            kagi_y.extend([kagi_y[-1], price])
            directions.extend([directions[-1], -1])
            current_direction = -1
            current_low = price
    else:  # Currently in downtrend
        if price < current_low:
            # Continue downtrend - extend the line
            current_low = price
            kagi_y[-1] = price
        elif price >= current_low * (1 + reversal_pct):
            # Reversal up - add waist and new ascending line
            line_index += 1
            kagi_x.extend([line_index, line_index])
            kagi_y.extend([kagi_y[-1], price])
            directions.extend([directions[-1], 1])
            current_direction = 1
            current_high = price

# Determine yang/yin based on breaking previous highs/lows
yang_yin = []  # True = yang (thick/green), False = yin (thin/red)
prev_high = kagi_y[0]
prev_low = kagi_y[0]
is_yang = True

for i in range(len(kagi_y)):
    if kagi_y[i] > prev_high:
        is_yang = True
        prev_high = kagi_y[i]
    elif kagi_y[i] < prev_low:
        is_yang = False
        prev_low = kagi_y[i]
    yang_yin.append(is_yang)

# Create figure
fig = go.Figure()

# Draw Kagi lines segment by segment
i = 0
while i < len(kagi_x) - 1:
    x_seg = [kagi_x[i], kagi_x[i + 1]]
    y_seg = [kagi_y[i], kagi_y[i + 1]]

    # Determine if this segment is yang or yin
    is_yang_seg = yang_yin[i]

    # Color and width based on yang/yin
    if is_yang_seg:
        color = "#2E8B57"  # Sea green for yang (bullish)
        width = 6
    else:
        color = "#DC3545"  # Red for yin (bearish)
        width = 2

    # Add line segment (vertical or horizontal)
    fig.add_trace(
        go.Scatter(
            x=x_seg, y=y_seg, mode="lines", line={"color": color, "width": width}, showlegend=False, hoverinfo="skip"
        )
    )
    i += 1

# Add legend entries
fig.add_trace(
    go.Scatter(x=[None], y=[None], mode="lines", line={"color": "#2E8B57", "width": 6}, name="Yang (Bullish)")
)
fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line={"color": "#DC3545", "width": 2}, name="Yin (Bearish)"))

# Layout
fig.update_layout(
    title={
        "text": "kagi-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Line Index", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.3)",
    },
    yaxis={
        "title": {"text": "Price ($)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.3)",
    },
    template="plotly_white",
    legend={
        "font": {"size": 18},
        "x": 0.02,
        "y": 0.98,
        "bgcolor": "rgba(255, 255, 255, 0.8)",
        "bordercolor": "rgba(0, 0, 0, 0.3)",
        "borderwidth": 1,
    },
    margin={"l": 80, "r": 40, "t": 100, "b": 80},
    plot_bgcolor="white",
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
