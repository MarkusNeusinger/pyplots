""" pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: plotly 6.5.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-07
"""

import numpy as np
import plotly.graph_objects as go
import qrcode


# Data - Generate QR code for pyplots.ai
content = "https://pyplots.ai"
error_correction = qrcode.constants.ERROR_CORRECT_M  # 15% error correction

qr = qrcode.QRCode(
    version=1,
    error_correction=error_correction,
    box_size=1,
    border=4,  # Quiet zone
)
qr.add_data(content)
qr.make(fit=True)

# Convert QR code to numpy array (0=white, 1=black)
qr_matrix = np.array(qr.get_matrix(), dtype=int)

# Invert so black=1, white=0 for proper display
qr_display = 1 - qr_matrix

# Create figure with heatmap
fig = go.Figure(
    data=go.Heatmap(z=qr_display, colorscale=[[0, "#000000"], [1, "#FFFFFF"]], showscale=False, xgap=0, ygap=0)
)

# Layout for square display
fig.update_layout(
    title={
        "text": "qrcode-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#306998"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={"showticklabels": False, "showgrid": False, "zeroline": False, "scaleanchor": "y", "scaleratio": 1},
    yaxis={
        "showticklabels": False,
        "showgrid": False,
        "zeroline": False,
        "autorange": "reversed",  # Flip to show QR code correctly
    },
    template="plotly_white",
    margin={"l": 150, "r": 150, "t": 200, "b": 350},
    paper_bgcolor="white",
    plot_bgcolor="white",
)

# Add annotations below the plot
fig.add_annotation(
    text=f"Content: {content}",
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.05,
    showarrow=False,
    font={"size": 28, "color": "#666666"},
    xanchor="center",
    yanchor="top",
)
fig.add_annotation(
    text="Error Correction: M (15%)",
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.10,
    showarrow=False,
    font={"size": 24, "color": "#888888"},
    xanchor="center",
    yanchor="top",
)

# Save outputs
fig.write_image("plot.png", width=3600, height=3600, scale=1)
fig.write_html("plot.html")
