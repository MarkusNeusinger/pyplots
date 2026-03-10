""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: plotly 6.6.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-10
"""

import plotly.graph_objects as go


# Data — fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 12, 8]
icons_per_unit = 5
colors = ["#306998", "#E8833A", "#F2C94C", "#7B4F9D", "#4CAF50"]

# Build pictogram grid — one trace per category for tight icon packing
fig = go.Figure()

max_icons = max(v // icons_per_unit + (1 if v % icons_per_unit else 0) for v in values)
spacing = 0.6

for row, (cat, val, color) in enumerate(zip(categories, values, colors, strict=True)):
    full_icons = val // icons_per_unit
    remainder = val % icons_per_unit
    y_pos = row * 1.2

    # Full icons
    if full_icons > 0:
        x_full = [i * spacing for i in range(full_icons)]
        fig.add_trace(
            go.Scatter(
                x=x_full,
                y=[y_pos] * full_icons,
                mode="markers",
                marker={"symbol": "square", "size": 32, "color": color, "line": {"color": "white", "width": 2}},
                hovertext=[f"{cat}: {val}k tonnes"] * full_icons,
                hoverinfo="text",
                showlegend=False,
            )
        )

    # Partial icon for remainder
    if remainder > 0:
        fraction = remainder / icons_per_unit
        fig.add_trace(
            go.Scatter(
                x=[full_icons * spacing],
                y=[y_pos],
                mode="markers",
                marker={
                    "symbol": "square",
                    "size": 32,
                    "color": color,
                    "opacity": max(0.25, fraction),
                    "line": {"color": "white", "width": 2},
                },
                hovertext=[f"{cat}: {val}k tonnes ({remainder}k partial)"],
                hoverinfo="text",
                showlegend=False,
            )
        )

    # Value label at end of row
    total_icons = full_icons + (1 if remainder > 0 else 0)
    fig.add_annotation(
        x=total_icons * spacing + 0.3,
        y=y_pos,
        text=f"<b>{val}k</b>",
        showarrow=False,
        font={"size": 20, "color": "#555555"},
        xanchor="left",
    )

# Legend at bottom
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.06,
    text="<b>▪</b> = 5k tonnes  |  Faded square = partial unit",
    showarrow=False,
    font={"size": 17, "color": "#888888"},
    xanchor="center",
)

# Layout
y_positions = [i * 1.2 for i in range(len(categories))]

fig.update_layout(
    title={
        "text": "Fruit Production · pictogram-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#222222"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
        "showline": False,
        "range": [-0.4, max_icons * spacing + 1.5],
    },
    yaxis={
        "tickvals": y_positions,
        "ticktext": categories,
        "tickfont": {"size": 22, "color": "#333333"},
        "showgrid": False,
        "zeroline": False,
        "showline": False,
        "range": [max(y_positions) + 0.8, -0.8],
    },
    template="plotly_white",
    margin={"t": 100, "b": 80, "l": 140, "r": 80},
    plot_bgcolor="white",
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
