"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: plotly 6.5.1 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-08
"""

import numpy as np
import plotly.graph_objects as go


# Generate sample price data designed to demonstrate multiple yang/yin transitions
np.random.seed(42)

# Create price series with clear swings that will break through shoulders and waists
# Each phase is designed to create reversal points and yang/yin transitions
prices_list = [100.0]

# Generate data with deliberate swings to create yang/yin transitions
# Key: Price must break above previous shoulder for yang, below previous waist for yin
segments = [
    # (target_price, volatility, n_steps) - target relative to previous end
    (8, 0.5, 20),  # Up to ~108
    (-12, 0.6, 25),  # Down to ~96 (below 100 waist -> YIN)
    (6, 0.5, 20),  # Up to ~102 (not above 108 shoulder yet)
    (-8, 0.5, 18),  # Down to ~94 (below 96 waist -> still YIN)
    (18, 0.6, 30),  # Up to ~112 (above 108 shoulder -> YANG!)
    (-10, 0.5, 22),  # Down to ~102 (above 94 waist -> still YANG)
    (-12, 0.5, 25),  # Down to ~90 (below 94 waist -> YIN!)
    (15, 0.5, 28),  # Up to ~105 (not above 112 shoulder yet)
    (12, 0.6, 25),  # Up to ~117 (above 112 shoulder -> YANG!)
    (-8, 0.5, 20),  # Down to ~109 (above 90 waist -> still YANG)
    (-14, 0.5, 22),  # Down to ~95 (below ~102 waist)
    (20, 0.6, 30),  # Up to ~115 (recovery)
]

for target_move, vol, n_steps in segments:
    start = prices_list[-1]
    end = start + target_move
    # Generate smooth movement with noise
    base_trend = np.linspace(0, target_move, n_steps)
    noise = np.cumsum(np.random.normal(0, vol, n_steps))
    noise = noise - noise[-1] * np.linspace(0, 1, n_steps)  # Trend back to target
    segment_prices = start + base_trend + noise
    prices_list.extend(segment_prices.tolist())

prices = np.array(prices_list)

# Kagi chart parameters - 3% reversal threshold
reversal_pct = 0.03

# Build Kagi chart data with yang/yin tracking at reversal points
# Yang/yin state changes when price breaks above previous shoulder (yang) or below previous waist (yin)
kagi_points = []  # List of (x, y, is_yang) tuples
current_direction = 1  # 1 = up, -1 = down
current_high = prices[0]
current_low = prices[0]
line_index = 0
is_yang = True

# Track shoulders (local highs) and waists (local lows) for yang/yin transitions
prev_shoulder = prices[0]  # Previous local high (reversal point from up to down)
prev_waist = prices[0]  # Previous local low (reversal point from down to up)

# Start with initial point
kagi_points.append((0, prices[0], is_yang))

for price in prices[1:]:
    if current_direction == 1:  # Currently moving up
        if price > current_high:
            # Continue uptrend - extend the line
            current_high = price
            # Check if we break above previous shoulder -> become yang
            if price > prev_shoulder and not is_yang:
                is_yang = True
            # Update last point
            kagi_points[-1] = (kagi_points[-1][0], price, is_yang)
        elif price <= current_high * (1 - reversal_pct):
            # Reversal down - record shoulder and add new descending line
            prev_shoulder = current_high  # This becomes a shoulder
            line_index += 1
            # Add horizontal connector at same y (shoulder)
            kagi_points.append((line_index, kagi_points[-1][1], is_yang))
            # Add new descending point
            kagi_points.append((line_index, price, is_yang))
            current_direction = -1
            current_low = price
    else:  # Currently moving down
        if price < current_low:
            # Continue downtrend - extend the line
            current_low = price
            # Check if we break below previous waist -> become yin
            if price < prev_waist and is_yang:
                is_yang = False
            # Update last point
            kagi_points[-1] = (kagi_points[-1][0], price, is_yang)
        elif price >= current_low * (1 + reversal_pct):
            # Reversal up - record waist and add new ascending line
            prev_waist = current_low  # This becomes a waist
            line_index += 1
            # Add horizontal connector at same y (waist)
            kagi_points.append((line_index, kagi_points[-1][1], is_yang))
            # Add new ascending point
            kagi_points.append((line_index, price, is_yang))
            current_direction = 1
            current_high = price

# Extract x, y coordinates and yang/yin states
kagi_x = [p[0] for p in kagi_points]
kagi_y = [p[1] for p in kagi_points]
yang_yin = [p[2] for p in kagi_points]

# Create figure
fig = go.Figure()

# Draw Kagi lines segment by segment
i = 0
while i < len(kagi_x) - 1:
    x_seg = [kagi_x[i], kagi_x[i + 1]]
    y_seg = [kagi_y[i], kagi_y[i + 1]]

    # Determine if this segment is yang or yin
    is_yang_seg = yang_yin[i]

    # Color and width based on yang/yin (colorblind-accessible colors)
    if is_yang_seg:
        color = "#0077BB"  # Blue for yang (bullish) - colorblind safe
        width = 8
    else:
        color = "#EE7733"  # Orange for yin (bearish) - colorblind safe
        width = 3

    # Add line segment with hover information
    trend_type = "Yang (Bullish)" if is_yang_seg else "Yin (Bearish)"
    fig.add_trace(
        go.Scatter(
            x=x_seg,
            y=y_seg,
            mode="lines",
            line={"color": color, "width": width},
            showlegend=False,
            hovertemplate=f"<b>{trend_type}</b><br>Price: $%{{y:.2f}}<extra></extra>",
        )
    )
    i += 1

# Add legend entries with colorblind-accessible colors
fig.add_trace(
    go.Scatter(x=[None], y=[None], mode="lines", line={"color": "#0077BB", "width": 8}, name="Yang (Bullish)")
)
fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line={"color": "#EE7733", "width": 3}, name="Yin (Bearish)"))

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
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "xanchor": "center",
        "x": 0.5,
        "bgcolor": "rgba(255, 255, 255, 0.9)",
        "bordercolor": "rgba(0, 0, 0, 0.2)",
        "borderwidth": 1,
    },
    margin={"l": 80, "r": 40, "t": 120, "b": 80},
    plot_bgcolor="white",
    hovermode="x unified",
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
