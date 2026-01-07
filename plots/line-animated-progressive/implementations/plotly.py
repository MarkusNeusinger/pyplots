"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - Monthly sales figures over 3 years
np.random.seed(42)
dates = pd.date_range(start="2021-01-01", periods=36, freq="ME")
base_trend = np.linspace(100, 180, 36)
seasonality = 15 * np.sin(np.linspace(0, 6 * np.pi, 36))
noise = np.random.normal(0, 5, 36)
values = base_trend + seasonality + noise

# Create static figure with progressive visual indicator
fig = go.Figure()

# Main line with gradient-like effect using multiple segments
# Create color gradient from light to dark blue to show progression
n_points = len(dates)
colors = [f"rgba(48, 105, 152, {0.3 + 0.7 * i / n_points})" for i in range(n_points)]

# Add the full line first (light background line)
fig.add_trace(
    go.Scatter(
        x=dates,
        y=values,
        mode="lines",
        line=dict(color="rgba(48, 105, 152, 0.2)", width=4),
        showlegend=False,
        hoverinfo="skip",
    )
)

# Add progressive segments with increasing opacity
for i in range(1, n_points):
    fig.add_trace(
        go.Scatter(
            x=[dates[i - 1], dates[i]],
            y=[values[i - 1], values[i]],
            mode="lines",
            line=dict(color=colors[i], width=4),
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Add markers with gradient - small markers at start, larger at end
marker_sizes = [8 + 12 * (i / n_points) for i in range(n_points)]
marker_colors = colors

fig.add_trace(
    go.Scatter(
        x=dates,
        y=values,
        mode="markers",
        marker=dict(size=marker_sizes, color=marker_colors, line=dict(color="white", width=2)),
        showlegend=False,
        customdata=np.column_stack((dates.strftime("%b %Y"), values)),
        hovertemplate="<b>%{customdata[0]}</b><br>Sales: $%{customdata[1]:.1f}K<extra></extra>",
    )
)

# Add emphasis on the final point (current position)
fig.add_trace(
    go.Scatter(
        x=[dates[-1]],
        y=[values[-1]],
        mode="markers",
        marker=dict(size=25, color="#306998", line=dict(color="#FFD43B", width=4), symbol="circle"),
        showlegend=False,
        hoverinfo="skip",
    )
)

# Add an arrow annotation pointing to the progression direction
fig.add_annotation(
    x=dates[-1],
    y=values[-1] + 15,
    text="Latest",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor="#306998",
    font=dict(size=18, color="#306998"),
    ax=0,
    ay=-40,
)

# Add a subtle starting point indicator
fig.add_trace(
    go.Scatter(
        x=[dates[0]],
        y=[values[0]],
        mode="markers",
        marker=dict(size=18, color="rgba(48, 105, 152, 0.3)", line=dict(color="#306998", width=2), symbol="circle"),
        showlegend=False,
        hoverinfo="skip",
    )
)

fig.add_annotation(
    x=dates[0], y=values[0] - 15, text="Start", showarrow=False, font=dict(size=16, color="rgba(48, 105, 152, 0.6)")
)

# Layout
fig.update_layout(
    title=dict(
        text="line-animated-progressive · plotly · pyplots.ai",
        font=dict(size=28, color="#333333"),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Date", font=dict(size=22)),
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
        dtick="M6",
        tickformat="%b %Y",
    ),
    yaxis=dict(
        title=dict(text="Monthly Sales ($K)", font=dict(size=22)),
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=100, r=80, t=100, b=80),
)

# Save static PNG - 4800x2700 px
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Create animated version for HTML
fig_animated = go.Figure()

# Build frames for animation - progressively reveal the line
frames = []
for k in range(1, n_points + 1):
    frame_data = [
        go.Scatter(
            x=dates[:k],
            y=values[:k],
            mode="lines+markers",
            line=dict(color="#306998", width=4),
            marker=dict(size=12, color="#306998", line=dict(color="white", width=2)),
            hovertemplate="<b>%{x|%b %Y}</b><br>Sales: $%{y:.1f}K<extra></extra>",
        )
    ]
    # Add emphasis on current point
    if k > 0:
        frame_data.append(
            go.Scatter(
                x=[dates[k - 1]],
                y=[values[k - 1]],
                mode="markers",
                marker=dict(size=20, color="#FFD43B", line=dict(color="#306998", width=3)),
                hoverinfo="skip",
            )
        )
    frames.append(go.Frame(data=frame_data, name=str(k)))

# Initial state - just the first point
fig_animated.add_trace(
    go.Scatter(
        x=[dates[0]],
        y=[values[0]],
        mode="lines+markers",
        line=dict(color="#306998", width=4),
        marker=dict(size=12, color="#306998", line=dict(color="white", width=2)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Sales: $%{y:.1f}K<extra></extra>",
    )
)

fig_animated.add_trace(
    go.Scatter(
        x=[dates[0]],
        y=[values[0]],
        mode="markers",
        marker=dict(size=20, color="#FFD43B", line=dict(color="#306998", width=3)),
        hoverinfo="skip",
    )
)

fig_animated.frames = frames

# Animation controls
fig_animated.update_layout(
    title=dict(
        text="line-animated-progressive · plotly · pyplots.ai",
        font=dict(size=28, color="#333333"),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        title=dict(text="Date", font=dict(size=22)),
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
        range=[dates[0] - pd.Timedelta(days=30), dates[-1] + pd.Timedelta(days=30)],
        tickformat="%b %Y",
    ),
    yaxis=dict(
        title=dict(text="Monthly Sales ($K)", font=dict(size=22)),
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
        range=[min(values) - 20, max(values) + 20],
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=100, r=80, t=100, b=80),
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            y=1.15,
            x=0.5,
            xanchor="center",
            buttons=[
                dict(
                    label="▶ Play",
                    method="animate",
                    args=[
                        None,
                        dict(frame=dict(duration=100, redraw=True), fromcurrent=True, transition=dict(duration=50)),
                    ],
                ),
                dict(
                    label="⏸ Pause",
                    method="animate",
                    args=[
                        [None],
                        dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0)),
                    ],
                ),
                dict(
                    label="⏮ Reset",
                    method="animate",
                    args=[
                        ["1"],
                        dict(frame=dict(duration=0, redraw=True), mode="immediate", transition=dict(duration=0)),
                    ],
                ),
            ],
            font=dict(size=16),
        )
    ],
    sliders=[
        dict(
            active=0,
            yanchor="top",
            xanchor="left",
            currentvalue=dict(font=dict(size=16), prefix="Month: ", visible=True, xanchor="center"),
            transition=dict(duration=50),
            pad=dict(b=10, t=50),
            len=0.9,
            x=0.05,
            y=0,
            steps=[
                dict(
                    args=[
                        [str(k)],
                        dict(frame=dict(duration=100, redraw=True), mode="immediate", transition=dict(duration=50)),
                    ],
                    label=dates[k - 1].strftime("%b %Y"),
                    method="animate",
                )
                for k in range(1, n_points + 1)
            ],
        )
    ],
    showlegend=False,
)

# Save interactive HTML
fig_animated.write_html("plot.html", include_plotlyjs="cdn")
