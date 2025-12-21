""" pyplots.ai
sunburst-basic: Basic Sunburst Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import plotly.graph_objects as go


# Data - Company budget breakdown by department, team, and project
# Using leaf node values with branchvalues="remainder" for auto-summing parents
labels = [
    # Level 1 - Root (innermost)
    "Company",
    # Level 2 - Departments
    "Engineering",
    "Sales",
    "Marketing",
    "Operations",
    # Level 3 - Teams/Areas (leaf nodes)
    "Backend",
    "Frontend",
    "DevOps",  # Engineering
    "Enterprise",
    "SMB",  # Sales
    "Digital",
    "Brand",  # Marketing
    "HR",
    "Finance",  # Operations
]

parents = [
    # Company has no parent
    "",
    # Departments report to Company
    "Company",
    "Company",
    "Company",
    "Company",
    # Teams report to departments
    "Engineering",
    "Engineering",
    "Engineering",
    "Sales",
    "Sales",
    "Marketing",
    "Marketing",
    "Operations",
    "Operations",
]

# Values - only leaf nodes have values, parents auto-sum
values = [
    48,  # Company total
    18,
    15,
    7,
    8,  # Department totals
    # Individual team budgets (in millions)
    8,
    6,
    4,  # Engineering teams
    10,
    5,  # Sales teams
    4,
    3,  # Marketing teams
    3,
    5,  # Operations teams
]

# Colors - Python Blue and Yellow as primary, variations for children
colors = [
    "#306998",  # Company - Python Blue
    # Departments
    "#306998",  # Engineering - Python Blue
    "#FFD43B",  # Sales - Python Yellow
    "#4B8BBE",  # Marketing - Light Blue
    "#FFE873",  # Operations - Light Yellow
    # Engineering teams (blue variations)
    "#1e4f7a",
    "#306998",
    "#4B8BBE",
    # Sales teams (yellow variations)
    "#e6be00",
    "#FFD43B",
    # Marketing teams (blue variations)
    "#5a9fd4",
    "#7ab8e6",
    # Operations teams (yellow variations)
    "#fff3b8",
    "#FFE873",
]

# Create sunburst chart
fig = go.Figure(
    go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textfont=dict(size=20),
        insidetextorientation="radial",
    )
)

# Update layout for 4800x2700 px
fig.update_layout(
    title=dict(text="sunburst-basic · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    template="plotly_white",
    margin=dict(t=100, l=50, r=50, b=50),
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
