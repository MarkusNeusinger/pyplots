"""pyplots.ai
tree-decision: Decision Tree Visualization with Probabilities
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-06
"""

import cairosvg
import pygal
from pygal.style import Style


# Data - New Product Launch Decision Tree
# Decision: Launch Product vs. Sell License vs. Do Nothing
# EMV (Expected Monetary Value) rollback:
#   C1 (Launch):  0.6 x $500K + 0.4 x (-$100K) = $260K  [OPTIMAL]
#   C2 (License): 0.7 x $250K + 0.3 x $50K     = $190K  [PRUNED]
#   T5 (Nothing): $0K                                     [PRUNED]
#   D1 (Root):    max($260K, $190K, $0K)         = $260K

nodes = {
    "D1": {"type": "decision", "x": 550, "y": 1200, "emv": 260, "label": "Strategy\nChoice"},
    "C1": {"type": "chance", "x": 2000, "y": 520, "emv": 260, "label": "Market\nOutcome"},
    "C2": {"type": "chance", "x": 2000, "y": 1650, "emv": 190, "label": "License\nResult"},
    "T1": {"type": "terminal", "x": 3500, "y": 280, "payoff": 500},
    "T2": {"type": "terminal", "x": 3500, "y": 760, "payoff": -100},
    "T3": {"type": "terminal", "x": 3500, "y": 1430, "payoff": 250},
    "T4": {"type": "terminal", "x": 3500, "y": 1870, "payoff": 50},
    "T5": {"type": "terminal", "x": 2000, "y": 2250, "payoff": 0},
}

branches = [
    ("D1", "C1", "Launch Product", None, False),
    ("D1", "C2", "Sell License", None, True),
    ("D1", "T5", "Do Nothing", None, True),
    ("C1", "T1", "High Demand", 0.6, False),
    ("C1", "T2", "Low Demand", 0.4, False),
    ("C2", "T3", "Accepted", 0.7, True),
    ("C2", "T4", "Rejected", 0.3, True),
]

# Colors
DECISION_COLOR = "#306998"
CHANCE_COLOR = "#E8833A"
TERMINAL_POS = "#2CA02C"
TERMINAL_NEG = "#DC3545"
TERMINAL_ZERO = "#7F8C8D"
OPTIMAL_LINE = "#306998"
PRUNED_LINE = "#AAAAAA"
TEXT_COLOR = "#333333"
TEXT_LIGHT = "#666666"

# Node sizes
DECISION_SIZE = 70
CHANCE_RADIUS = 55
TRIANGLE_SIZE = 40

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    title_font_size=72,
)

# Create minimal chart as SVG base
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="tree-decision \u00b7 pygal \u00b7 pyplots.ai",
    show_legend=False,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    dots_size=0,
    stroke=False,
    range=(0, 100),
    xrange=(0, 100),
)
chart.add("", [(50, 50)])

# Render base SVG
base_svg = chart.render().decode("utf-8")

# Build custom SVG for decision tree
tree_svg = '<g id="decision-tree">'

# Draw branches (behind nodes)
for parent_id, child_id, label, prob, pruned in branches:
    p = nodes[parent_id]
    c = nodes[child_id]
    px, py = p["x"], p["y"]
    cx, cy = c["x"], c["y"]

    line_color = PRUNED_LINE if pruned else OPTIMAL_LINE
    line_width = 3 if pruned else 5
    dash = ' stroke-dasharray="20,12"' if pruned else ""
    opacity = "0.5" if pruned else "1.0"

    # Elbow connector: horizontal from parent, then vertical to child
    mid_x = px + (cx - px) * 0.55
    tree_svg += f'''
    <path d="M {px},{py} L {mid_x},{py} L {mid_x},{cy} L {cx},{cy}"
          fill="none" stroke="{line_color}" stroke-width="{line_width}"
          opacity="{opacity}"{dash}/>'''

    # Branch label on the vertical segment, offset to the left
    vert_mid_y = py + (cy - py) * 0.45
    label_color = TEXT_LIGHT if pruned else TEXT_COLOR
    font_weight = "normal" if pruned else "bold"
    tree_svg += f'''
    <text x="{mid_x - 22}" y="{vert_mid_y}" text-anchor="end"
          font-size="36" font-family="DejaVu Sans, sans-serif"
          fill="{label_color}" font-weight="{font_weight}">{label}</text>'''

    # Probability label on vertical segment (for chance branches), offset right
    if prob is not None:
        prob_y = py + (cy - py) * 0.45
        prob_color = TEXT_LIGHT if pruned else CHANCE_COLOR
        tree_svg += f'''
    <text x="{mid_x + 22}" y="{prob_y}" text-anchor="start"
          font-size="34" font-family="DejaVu Sans, sans-serif"
          fill="{prob_color}" font-style="italic">p = {prob}</text>'''

    # Pruned mark (X cross) on vertical segment
    if pruned:
        strike_x = mid_x
        strike_y = py + (cy - py) * 0.2
        tree_svg += f'''
    <line x1="{strike_x - 16}" y1="{strike_y - 14}" x2="{strike_x + 16}" y2="{strike_y + 14}"
          stroke="#DC3545" stroke-width="4" opacity="0.8"/>
    <line x1="{strike_x - 16}" y1="{strike_y + 14}" x2="{strike_x + 16}" y2="{strike_y - 14}"
          stroke="#DC3545" stroke-width="4" opacity="0.8"/>'''

# Draw nodes on top of branches
for _node_id, node in nodes.items():
    x, y = node["x"], node["y"]
    ntype = node["type"]

    if ntype == "decision":
        half = DECISION_SIZE
        tree_svg += f'''
    <rect x="{x - half}" y="{y - half}" width="{half * 2}" height="{half * 2}"
          fill="{DECISION_COLOR}" stroke="white" stroke-width="4" rx="8"/>'''
        tree_svg += f'''
    <text x="{x}" y="{y - 8}" text-anchor="middle" dominant-baseline="auto"
          font-size="30" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="white">EMV</text>
    <text x="{x}" y="{y + 30}" text-anchor="middle" dominant-baseline="auto"
          font-size="34" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="white">${node["emv"]}K</text>'''
        label_lines = node["label"].split("\n")
        for i, line in enumerate(label_lines):
            tree_svg += f'''
    <text x="{x}" y="{y + half + 42 + i * 44}" text-anchor="middle"
          font-size="38" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="{DECISION_COLOR}">{line}</text>'''

    elif ntype == "chance":
        tree_svg += f'''
    <circle cx="{x}" cy="{y}" r="{CHANCE_RADIUS}"
            fill="{CHANCE_COLOR}" stroke="white" stroke-width="4"/>'''
        tree_svg += f'''
    <text x="{x}" y="{y - 8}" text-anchor="middle" dominant-baseline="auto"
          font-size="28" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="white">EMV</text>
    <text x="{x}" y="{y + 28}" text-anchor="middle" dominant-baseline="auto"
          font-size="30" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="white">${node["emv"]}K</text>'''
        label_lines = node["label"].split("\n")
        for i, line in enumerate(label_lines):
            tree_svg += f'''
    <text x="{x}" y="{y + CHANCE_RADIUS + 40 + i * 40}" text-anchor="middle"
          font-size="34" font-family="DejaVu Sans, sans-serif"
          fill="{CHANCE_COLOR}" font-weight="bold">{line}</text>'''

    elif ntype == "terminal":
        payoff = node["payoff"]
        if payoff > 0:
            fill_color = TERMINAL_POS
        elif payoff < 0:
            fill_color = TERMINAL_NEG
        else:
            fill_color = TERMINAL_ZERO
        s = TRIANGLE_SIZE
        points = f"{x - s},{y - s} {x - s},{y + s} {x + s},{y}"
        tree_svg += f'''
    <polygon points="{points}"
             fill="{fill_color}" stroke="white" stroke-width="3"/>'''
        payoff_str = f"${payoff}K" if payoff >= 0 else f"\u2212${abs(payoff)}K"
        tree_svg += f'''
    <text x="{x + s + 25}" y="{y + 10}" text-anchor="start"
          font-size="40" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="{fill_color}">{payoff_str}</text>'''

# Legend
legend_x = 3850
legend_y = 2150
legend_items = [
    ("rect", DECISION_COLOR, "Decision Node"),
    ("circle", CHANCE_COLOR, "Chance Node"),
    ("triangle", TERMINAL_POS, "Terminal Node"),
    ("line_solid", OPTIMAL_LINE, "Optimal Path"),
    ("line_dash", PRUNED_LINE, "Pruned Branch"),
]

tree_svg += f'''
    <rect x="{legend_x - 30}" y="{legend_y - 30}" width="880" height="360"
          fill="white" stroke="#dddddd" stroke-width="2" rx="10"/>'''

for i, (shape, color, text) in enumerate(legend_items):
    ly = legend_y + i * 62
    if shape == "rect":
        tree_svg += f'''
    <rect x="{legend_x}" y="{ly - 14}" width="28" height="28"
          fill="{color}" rx="4"/>'''
    elif shape == "circle":
        tree_svg += f'''
    <circle cx="{legend_x + 14}" cy="{ly}" r="14" fill="{color}"/>'''
    elif shape == "triangle":
        tree_svg += f'''
    <polygon points="{legend_x},{ly - 14} {legend_x},{ly + 14} {legend_x + 28},{ly}"
             fill="{color}"/>'''
    elif shape == "line_solid":
        tree_svg += f'''
    <line x1="{legend_x}" y1="{ly}" x2="{legend_x + 28}" y2="{ly}"
          stroke="{color}" stroke-width="5"/>'''
    elif shape == "line_dash":
        tree_svg += f'''
    <line x1="{legend_x}" y1="{ly}" x2="{legend_x + 28}" y2="{ly}"
          stroke="{color}" stroke-width="3" stroke-dasharray="6,4"/>'''
    tree_svg += f'''
    <text x="{legend_x + 52}" y="{ly + 8}" text-anchor="start"
          font-size="34" font-family="DejaVu Sans, sans-serif"
          fill="{TEXT_COLOR}">{text}</text>'''

tree_svg += "\n</g>"

# Insert tree elements before closing </svg> tag
svg_output = base_svg.replace("</svg>", f"{tree_svg}\n</svg>")

# Save SVG
with open("plot.svg", "w") as f:
    f.write(svg_output)

# Save PNG
cairosvg.svg2png(bytestring=svg_output.encode("utf-8"), write_to="plot.png")

# Save HTML
with open("plot.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>tree-decision &middot; pygal &middot; pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; text-align: center; }
        object { width: 100%; max-width: 4800px; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Decision tree not supported
        </object>
    </div>
</body>
</html>""")
