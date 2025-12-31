"""pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import plotly.graph_objects as go


# Hierarchical data structure for company budget breakdown
# Structure: Department -> Team -> Expense Category
# Leaf nodes have direct values, parent nodes derive values from children
hierarchy = {
    "All": {"children": ["Engineering", "Marketing", "Operations", "Sales"], "parent": None},
    "Engineering": {"children": ["Backend", "Frontend", "DevOps", "QA"], "parent": "All"},
    "Marketing": {"children": ["Digital", "Content", "Events", "Brand"], "parent": "All"},
    "Operations": {"children": ["HR", "Finance", "Legal", "Facilities"], "parent": "All"},
    "Sales": {"children": ["Enterprise", "SMB", "Partnerships"], "parent": "All"},
    # Engineering subcategories (leaf nodes with values)
    "Backend": {"value": 850000, "parent": "Engineering"},
    "Frontend": {"value": 620000, "parent": "Engineering"},
    "DevOps": {"value": 480000, "parent": "Engineering"},
    "QA": {"value": 350000, "parent": "Engineering"},
    # Marketing subcategories
    "Digital": {"value": 420000, "parent": "Marketing"},
    "Content": {"value": 280000, "parent": "Marketing"},
    "Events": {"value": 350000, "parent": "Marketing"},
    "Brand": {"value": 180000, "parent": "Marketing"},
    # Operations subcategories
    "HR": {"value": 320000, "parent": "Operations"},
    "Finance": {"value": 290000, "parent": "Operations"},
    "Legal": {"value": 410000, "parent": "Operations"},
    "Facilities": {"value": 250000, "parent": "Operations"},
    # Sales subcategories
    "Enterprise": {"value": 680000, "parent": "Sales"},
    "SMB": {"value": 420000, "parent": "Sales"},
    "Partnerships": {"value": 300000, "parent": "Sales"},
}

# Pre-compute parent values (sum of children)
hierarchy["Engineering"]["value"] = sum(hierarchy[c]["value"] for c in hierarchy["Engineering"]["children"])
hierarchy["Marketing"]["value"] = sum(hierarchy[c]["value"] for c in hierarchy["Marketing"]["children"])
hierarchy["Operations"]["value"] = sum(hierarchy[c]["value"] for c in hierarchy["Operations"]["children"])
hierarchy["Sales"]["value"] = sum(hierarchy[c]["value"] for c in hierarchy["Sales"]["children"])

# Color palette for main categories (colorblind-safe)
colors = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Operations": "#2CA02C",  # Green
    "Sales": "#FF7F0E",  # Orange
}

# Lighter shades for subcategories
sub_colors = {
    "Backend": "#4A8BBE",
    "Frontend": "#6BA3D6",
    "DevOps": "#8CBBEE",
    "QA": "#ADD3F5",
    "Digital": "#FFE066",
    "Content": "#FFEB99",
    "Events": "#FFF5CC",
    "Brand": "#FFFAE6",
    "HR": "#4DC04D",
    "Finance": "#70D070",
    "Legal": "#93E093",
    "Facilities": "#B6F0B6",
    "Enterprise": "#FF9F40",
    "SMB": "#FFBF73",
    "Partnerships": "#FFDFA6",
}

# Get data for top level view
current_level = "All"
children = hierarchy[current_level]["children"]
values = [hierarchy[child]["value"] for child in children]
total = sum(values)
slice_colors = [colors[child] for child in children]

# Create pie chart
fig = go.Figure()

# Main pie chart
fig.add_trace(
    go.Pie(
        labels=children,
        values=values,
        hole=0.3,  # Donut style for modern look
        textinfo="label+percent",
        textposition="outside",
        textfont={"size": 20},
        hovertemplate="<b>%{label}</b><br>"
        + "Value: $%{value:,.0f}<br>"
        + "Percentage: %{percent}<br>"
        + "<extra>Click to drill down</extra>",
        marker={"colors": slice_colors, "line": {"color": "white", "width": 3}},
        pull=[0.02] * len(children),  # Slight separation
    )
)

# Add center text showing current view
fig.add_annotation(
    text="<b>Company Budget</b><br>FY 2024",
    x=0.5,
    y=0.5,
    font={"size": 24, "color": "#333333"},
    showarrow=False,
    xref="paper",
    yref="paper",
)

# Add breadcrumb navigation at the top
fig.add_annotation(
    text="📍 All Departments",
    x=0.02,
    y=0.98,
    xanchor="left",
    yanchor="top",
    font={"size": 22, "color": "#306998"},
    showarrow=False,
    xref="paper",
    yref="paper",
    bgcolor="rgba(255,255,255,0.9)",
    borderpad=8,
)

# Add click instruction
fig.add_annotation(
    text="👆 Click any slice to drill down into subcategories",
    x=0.5,
    y=0.02,
    xanchor="center",
    yanchor="bottom",
    font={"size": 18, "color": "#666666"},
    showarrow=False,
    xref="paper",
    yref="paper",
)

# Update layout
fig.update_layout(
    title={
        "text": "pie-drilldown · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    showlegend=True,
    legend={
        "orientation": "v",
        "yanchor": "middle",
        "y": 0.5,
        "xanchor": "left",
        "x": 1.02,
        "font": {"size": 18},
        "title": {"text": "Departments", "font": {"size": 20}},
    },
    template="plotly_white",
    margin={"l": 60, "r": 200, "t": 100, "b": 80},
)

# Custom JavaScript for drilldown functionality (in HTML output)
# Creates the interactive experience with animations
drilldown_js = """
<script>
var hierarchyData = %s;
var colors = %s;
var subColors = %s;
var currentPath = ['All'];

function getValue(nodeName) {
    return hierarchyData[nodeName].value;
}

function updateChart(level) {
    var node = hierarchyData[level];
    if (!node.children) return;

    var children = node.children;
    var values = children.map(c => getValue(c));
    var sliceColors = children.map(c => subColors[c] || colors[c] || '#306998');

    Plotly.animate('plotly-chart', {
        data: [{
            labels: children,
            values: values,
            marker: {colors: sliceColors}
        }],
        layout: {}
    }, {
        transition: {duration: 500, easing: 'cubic-in-out'},
        frame: {duration: 500}
    });
}

document.getElementById('plotly-chart').on('plotly_click', function(data) {
    var clickedLabel = data.points[0].label;
    if (hierarchyData[clickedLabel] && hierarchyData[clickedLabel].children) {
        currentPath.push(clickedLabel);
        updateChart(clickedLabel);
    }
});
</script>
""" % (
    str(hierarchy).replace("'", '"').replace("None", "null"),
    str(colors).replace("'", '"'),
    str(sub_colors).replace("'", '"'),
)

# Save as PNG (static image for main output)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML (interactive version with drilldown)
html_content = fig.to_html(
    full_html=True,
    include_plotlyjs=True,
    div_id="plotly-chart",
    config={
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "toImageButtonOptions": {"format": "png", "width": 4800, "height": 2700},
    },
)

# Inject drilldown JavaScript before closing body tag
html_content = html_content.replace("</body>", drilldown_js + "</body>")

with open("plot.html", "w") as f:
    f.write(html_content)
