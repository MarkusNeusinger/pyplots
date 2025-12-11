"""
sankey-basic: Basic Sankey Diagram
Library: plotly
"""

import plotly.graph_objects as go


# Color palette from style guide
COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Data - Energy flow from sources through conversion to end uses
# Nodes: 0-3 Sources, 4-6 Conversion, 7-10 End Uses
node_labels = [
    # Sources (0-3)
    "Coal",
    "Natural Gas",
    "Nuclear",
    "Renewables",
    # Conversion (4-6)
    "Power Plants",
    "Direct Use",
    "Heat Plants",
    # End Uses (7-10)
    "Residential",
    "Commercial",
    "Industrial",
    "Transport",
]

# Flows: source index, target index, value
flows = [
    # Coal flows
    (0, 4, 150),  # Coal -> Power Plants
    (0, 6, 30),  # Coal -> Heat Plants
    # Natural Gas flows
    (1, 4, 100),  # Natural Gas -> Power Plants
    (1, 5, 80),  # Natural Gas -> Direct Use
    (1, 6, 50),  # Natural Gas -> Heat Plants
    # Nuclear flows
    (2, 4, 120),  # Nuclear -> Power Plants
    # Renewables flows
    (3, 4, 60),  # Renewables -> Power Plants
    (3, 5, 20),  # Renewables -> Direct Use
    # Power Plants to End Uses
    (4, 7, 100),  # Power Plants -> Residential
    (4, 8, 120),  # Power Plants -> Commercial
    (4, 9, 150),  # Power Plants -> Industrial
    (4, 10, 60),  # Power Plants -> Transport
    # Direct Use to End Uses
    (5, 7, 40),  # Direct Use -> Residential
    (5, 9, 60),  # Direct Use -> Industrial
    # Heat Plants to End Uses
    (6, 7, 30),  # Heat Plants -> Residential
    (6, 8, 25),  # Heat Plants -> Commercial
    (6, 9, 25),  # Heat Plants -> Industrial
]

sources = [f[0] for f in flows]
targets = [f[1] for f in flows]
values = [f[2] for f in flows]

# Assign colors to nodes based on their category
node_colors = (
    [COLORS[0]] * 4  # Sources - Python Blue
    + [COLORS[3]] * 3  # Conversion - Teal Green
    + [COLORS[4]] * 4  # End Uses - Violet
)

# Link colors with transparency (based on source node)
link_colors = [
    node_colors[src]
    .replace("#", "rgba(")
    .replace("306998", "48, 105, 152, 0.4)")
    .replace("FFD43B", "255, 212, 59, 0.4)")
    .replace("DC2626", "220, 38, 38, 0.4)")
    .replace("059669", "5, 150, 105, 0.4)")
    .replace("8B5CF6", "139, 92, 246, 0.4)")
    .replace("F97316", "249, 115, 22, 0.4)")
    for src in sources
]

# Create Sankey diagram
fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(pad=20, thickness=30, line=dict(color="black", width=0.5), label=node_labels, color=node_colors),
            link=dict(source=sources, target=targets, value=values, color=link_colors),
        )
    ]
)

# Layout
fig.update_layout(
    title=dict(text="Energy Flow: Sources to End Uses", font=dict(size=48), x=0.5, xanchor="center"),
    font=dict(size=28),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=50, r=50, t=100, b=50),
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
