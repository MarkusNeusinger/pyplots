""" pyplots.ai
tree-phylogenetic: Phylogenetic Tree Diagram
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-31
"""

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure, output_file, save


# Phylogenetic tree data - Primate species (mitochondrial DNA based)
# Manually define tree structure with node positions and branch connections
# Structure: ((((Human, Chimp), Gorilla), Orangutan), Gibbon)
# Using rectangular cladogram layout

# Node positions (x = evolutionary distance, y = vertical position)
species = ["Human", "Chimpanzee", "Gorilla", "Orangutan", "Gibbon"]

# Leaf node positions (x based on cumulative branch lengths, y evenly spaced)
leaf_y = [5, 4, 3, 2, 1]
leaf_x = [0.95, 0.95, 0.85, 0.65, 0.45]

# Internal node positions
# Node 1: Human-Chimp ancestor (x=0.80, y=4.5)
# Node 2: Node1-Gorilla ancestor (x=0.60, y=3.75)
# Node 3: Node2-Orangutan ancestor (x=0.40, y=2.875)
# Node 4: Root - Node3-Gibbon ancestor (x=0.20, y=1.9375)

internal_x = [0.80, 0.60, 0.40, 0.20]
internal_y = [4.5, 3.75, 2.875, 1.9375]

# Branch lines (horizontal and vertical segments)
# Format: lists of x and y coordinates for each branch segment

# Horizontal branches from leaves to their ancestors
h_branch_x = [
    [internal_x[0], leaf_x[0]],  # Human
    [internal_x[0], leaf_x[1]],  # Chimp
    [internal_x[1], leaf_x[2]],  # Gorilla
    [internal_x[2], leaf_x[3]],  # Orangutan
    [internal_x[3], leaf_x[4]],  # Gibbon
    [internal_x[1], internal_x[0]],  # Node1 to Node2
    [internal_x[2], internal_x[1]],  # Node2 to Node3
    [internal_x[3], internal_x[2]],  # Node3 to Root
]

h_branch_y = [
    [leaf_y[0], leaf_y[0]],  # Human
    [leaf_y[1], leaf_y[1]],  # Chimp
    [leaf_y[2], leaf_y[2]],  # Gorilla
    [leaf_y[3], leaf_y[3]],  # Orangutan
    [leaf_y[4], leaf_y[4]],  # Gibbon
    [internal_y[0], internal_y[0]],  # Node1 to Node2
    [internal_y[1], internal_y[1]],  # Node2 to Node3
    [internal_y[2], internal_y[2]],  # Node3 to Root
]

# Vertical branches connecting nodes
v_branch_x = [
    [internal_x[0], internal_x[0]],  # Node1 vertical (Human-Chimp)
    [internal_x[1], internal_x[1]],  # Node2 vertical (Node1-Gorilla)
    [internal_x[2], internal_x[2]],  # Node3 vertical (Node2-Orangutan)
    [internal_x[3], internal_x[3]],  # Root vertical (Node3-Gibbon)
]

v_branch_y = [
    [leaf_y[0], leaf_y[1]],  # Node1 vertical
    [internal_y[0], leaf_y[2]],  # Node2 vertical
    [internal_y[1], leaf_y[3]],  # Node3 vertical
    [internal_y[2], leaf_y[4]],  # Root vertical
]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Primate Evolution · tree-phylogenetic · bokeh · pyplots.ai",
    x_axis_label="Evolutionary Distance (substitutions per site)",
    y_axis_label="",
    x_range=(-0.05, 1.25),
    y_range=(0.3, 5.7),
)

# Style the figure
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Draw horizontal branches
for hx, hy in zip(h_branch_x, h_branch_y, strict=True):
    p.line(hx, hy, line_width=4, line_color="#306998")

# Draw vertical branches
for vx, vy in zip(v_branch_x, v_branch_y, strict=True):
    p.line(vx, vy, line_width=4, line_color="#306998")

# Draw leaf nodes
leaf_source = ColumnDataSource(data={"x": leaf_x, "y": leaf_y, "species": species})
p.scatter("x", "y", source=leaf_source, size=20, color="#FFD43B", line_color="#306998", line_width=3)

# Draw internal nodes
internal_source = ColumnDataSource(data={"x": internal_x, "y": internal_y})
p.scatter("x", "y", source=internal_source, size=16, color="#306998")

# Add species labels
for i, sp in enumerate(species):
    label = Label(
        x=leaf_x[i] + 0.02, y=leaf_y[i], text=sp, text_font_size="20pt", text_baseline="middle", text_color="#333333"
    )
    p.add_layout(label)

# Add scale bar
scale_bar_y = 0.6
p.line([0, 0.1], [scale_bar_y, scale_bar_y], line_width=4, line_color="#333333")
scale_label = Label(
    x=0.0, y=scale_bar_y - 0.15, text="0.1 substitutions/site", text_font_size="16pt", text_color="#333333"
)
p.add_layout(scale_label)

# Add clade annotations
clade_labels = [
    {"x": 0.78, "y": 4.5, "text": "Hominini"},
    {"x": 0.58, "y": 3.75, "text": "Homininae"},
    {"x": 0.38, "y": 2.875, "text": "Hominidae"},
]

for clade in clade_labels:
    bracket_label = Label(
        x=clade["x"] - 0.15,
        y=clade["y"],
        text=clade["text"],
        text_font_size="16pt",
        text_font_style="italic",
        text_color="#666666",
        text_baseline="middle",
    )
    p.add_layout(bracket_label)

# Save PNG
export_png(p, filename="plot.png")

# Save HTML for interactivity
output_file("plot.html")
save(p)
