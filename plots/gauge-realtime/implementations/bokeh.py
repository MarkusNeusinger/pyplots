"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure


# Data - Simulated CPU usage with thresholds
np.random.seed(42)
current_value = 67  # Current CPU usage %
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green < 50, Yellow 50-80, Red > 80

# Generate motion trail values to show dynamic nature
trail_values = [62, 65, 67]  # Previous positions leading to current

# Gauge parameters
center_x, center_y = 0, 0
outer_radius = 0.9
inner_radius = 0.55
needle_base_width = 0.05
start_angle = np.pi * 0.8  # Start at ~215 degrees
end_angle = np.pi * 0.2  # End at ~35 degrees
angle_range = start_angle - end_angle  # Sweep clockwise

# Create figure
p = figure(
    width=4800,
    height=2700,
    x_range=(-1.3, 1.3),
    y_range=(-0.8, 1.1),
    title="CPU Monitor · gauge-realtime · bokeh · pyplots.ai",
    tools="",
    toolbar_location=None,
)
p.title.text_font_size = "28pt"
p.title.align = "center"

# Remove grid and axes
p.xgrid.visible = False
p.ygrid.visible = False
p.xaxis.visible = False
p.yaxis.visible = False
p.outline_line_color = None
p.background_fill_color = "#f5f5f5"


def value_to_angle(val):
    """Convert value to angle on the gauge."""
    normalized = (val - min_value) / (max_value - min_value)
    return start_angle - normalized * angle_range


def create_arc_data(start_val, end_val, radius_inner, radius_outer, n_points=50):
    """Create arc wedge data for gauge zones."""
    start_ang = value_to_angle(start_val)
    end_ang = value_to_angle(end_val)
    angles = np.linspace(start_ang, end_ang, n_points)

    # Create closed polygon for the arc
    x_outer = center_x + radius_outer * np.cos(angles)
    y_outer = center_y + radius_outer * np.sin(angles)
    x_inner = center_x + radius_inner * np.cos(angles[::-1])
    y_inner = center_y + radius_inner * np.sin(angles[::-1])

    x = np.concatenate([x_outer, x_inner, [x_outer[0]]])
    y = np.concatenate([y_outer, y_inner, [y_outer[0]]])
    return x, y


# Draw gauge zones
# Green zone: 0 - 50
x_green, y_green = create_arc_data(min_value, thresholds[0], inner_radius, outer_radius)
p.patch(x_green, y_green, fill_color="#27ae60", fill_alpha=0.85, line_color="white", line_width=2)

# Yellow zone: 50 - 80
x_yellow, y_yellow = create_arc_data(thresholds[0], thresholds[1], inner_radius, outer_radius)
p.patch(x_yellow, y_yellow, fill_color="#f39c12", fill_alpha=0.85, line_color="white", line_width=2)

# Red zone: 80 - 100
x_red, y_red = create_arc_data(thresholds[1], max_value, inner_radius, outer_radius)
p.patch(x_red, y_red, fill_color="#e74c3c", fill_alpha=0.85, line_color="white", line_width=2)

# Draw gauge border
border_angles = np.linspace(start_angle, end_angle, 100)
x_border_outer = center_x + outer_radius * np.cos(border_angles)
y_border_outer = center_y + outer_radius * np.sin(border_angles)
p.line(x_border_outer, y_border_outer, line_color="#2c3e50", line_width=4)

x_border_inner = center_x + inner_radius * np.cos(border_angles)
y_border_inner = center_y + inner_radius * np.sin(border_angles)
p.line(x_border_inner, y_border_inner, line_color="#2c3e50", line_width=4)

# Draw tick marks
tick_radius_outer = outer_radius + 0.03
tick_radius_inner = outer_radius - 0.05
for tick_val in range(0, 101, 10):
    tick_angle = value_to_angle(tick_val)
    x1 = center_x + tick_radius_inner * np.cos(tick_angle)
    y1 = center_y + tick_radius_inner * np.sin(tick_angle)
    x2 = center_x + tick_radius_outer * np.cos(tick_angle)
    y2 = center_y + tick_radius_outer * np.sin(tick_angle)

    line_width = 4 if tick_val % 20 == 0 else 2
    p.line([x1, x2], [y1, y2], line_color="#2c3e50", line_width=line_width)

    # Add labels for major ticks
    if tick_val % 20 == 0:
        label_radius = outer_radius + 0.12
        lx = center_x + label_radius * np.cos(tick_angle)
        ly = center_y + label_radius * np.sin(tick_angle)
        label = Label(
            x=lx,
            y=ly,
            text=str(tick_val),
            text_font_size="18pt",
            text_color="#2c3e50",
            text_align="center",
            text_baseline="middle",
        )
        p.add_layout(label)

# Draw motion trail needles (showing previous positions with decreasing opacity)
for i, trail_val in enumerate(trail_values[:-1]):
    trail_angle = value_to_angle(trail_val)
    alpha = 0.15 + i * 0.1  # Increasing opacity

    # Needle tip
    tip_x = center_x + (inner_radius + 0.3) * np.cos(trail_angle)
    tip_y = center_y + (inner_radius + 0.3) * np.sin(trail_angle)

    # Needle base
    base_offset = needle_base_width * 1.5
    base_angle_left = trail_angle + np.pi / 2
    base_angle_right = trail_angle - np.pi / 2

    base_x1 = center_x + base_offset * np.cos(base_angle_left)
    base_y1 = center_y + base_offset * np.sin(base_angle_left)
    base_x2 = center_x + base_offset * np.cos(base_angle_right)
    base_y2 = center_y + base_offset * np.sin(base_angle_right)

    p.patch(
        [tip_x, base_x1, base_x2], [tip_y, base_y1, base_y2], fill_color="#34495e", fill_alpha=alpha, line_color=None
    )

# Draw main needle (current value)
needle_angle = value_to_angle(current_value)
tip_x = center_x + (inner_radius + 0.3) * np.cos(needle_angle)
tip_y = center_y + (inner_radius + 0.3) * np.sin(needle_angle)

base_offset = needle_base_width * 1.5
base_angle_left = needle_angle + np.pi / 2
base_angle_right = needle_angle - np.pi / 2

base_x1 = center_x + base_offset * np.cos(base_angle_left)
base_y1 = center_y + base_offset * np.sin(base_angle_left)
base_x2 = center_x + base_offset * np.cos(base_angle_right)
base_y2 = center_y + base_offset * np.sin(base_angle_right)

needle_source = ColumnDataSource(data={"x": [[tip_x, base_x1, base_x2]], "y": [[tip_y, base_y1, base_y2]]})
p.patches(
    xs="x", ys="y", source=needle_source, fill_color="#2c3e50", fill_alpha=1.0, line_color="#1a252f", line_width=2
)

# Center cap
p.scatter([center_x], [center_y], size=35, fill_color="#2c3e50", line_color="#1a252f", line_width=3)
p.scatter([center_x], [center_y], size=18, fill_color="#ecf0f1", line_color=None)

# Current value display
value_label = Label(
    x=center_x,
    y=center_y - 0.35,
    text=f"{current_value}%",
    text_font_size="48pt",
    text_font_style="bold",
    text_color="#2c3e50",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(value_label)

# Status text based on value
if current_value < thresholds[0]:
    status = "Normal"
    status_color = "#27ae60"
elif current_value < thresholds[1]:
    status = "Warning"
    status_color = "#f39c12"
else:
    status = "Critical"
    status_color = "#e74c3c"

status_label = Label(
    x=center_x,
    y=center_y - 0.52,
    text=status,
    text_font_size="26pt",
    text_color=status_color,
    text_align="center",
    text_baseline="middle",
)
p.add_layout(status_label)

# Min/Max labels
min_label = Label(
    x=-0.95, y=-0.45, text=f"{min_value}%", text_font_size="20pt", text_color="#7f8c8d", text_align="center"
)
p.add_layout(min_label)

max_label = Label(
    x=0.95, y=-0.45, text=f"{max_value}%", text_font_size="20pt", text_color="#7f8c8d", text_align="center"
)
p.add_layout(max_label)

# Subtitle indicating real-time nature
subtitle = Label(
    x=center_x,
    y=-0.7,
    text="Live CPU Usage (motion trail shows recent values)",
    text_font_size="18pt",
    text_color="#95a5a6",
    text_align="center",
)
p.add_layout(subtitle)

# Save static image
export_png(p, filename="plot.png")

# Create interactive HTML version with real-time updates
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Gauge - Bokeh</title>
    <script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.7.0.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #f5f5f5; }
        .container { text-align: center; }
        h1 { color: #2c3e50; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CPU Monitor · gauge-realtime · bokeh · pyplots.ai</h1>
        <canvas id="gauge" width="800" height="500"></canvas>
        <div id="value" style="font-size: 48px; font-weight: bold; color: #2c3e50; margin-top: 20px;">67%</div>
        <div id="status" style="font-size: 24px; color: #f39c12;">Warning</div>
        <p style="color: #95a5a6; margin-top: 10px;">Simulating real-time CPU usage updates</p>
    </div>
    <script>
        const canvas = document.getElementById('gauge');
        const ctx = canvas.getContext('2d');
        const valueDisplay = document.getElementById('value');
        const statusDisplay = document.getElementById('status');

        let currentValue = 67;
        let targetValue = 67;
        const minValue = 0;
        const maxValue = 100;
        const thresholds = [50, 80];

        function drawGauge(value) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2;
            const centerY = canvas.height * 0.65;
            const outerRadius = 180;
            const innerRadius = 110;

            const startAngle = Math.PI * 0.8;
            const endAngle = Math.PI * 0.2;
            const angleRange = startAngle - endAngle;

            function valueToAngle(v) {
                const normalized = (v - minValue) / (maxValue - minValue);
                return startAngle - normalized * angleRange;
            }

            // Draw zones
            function drawArc(startVal, endVal, color) {
                const startAng = valueToAngle(startVal);
                const endAng = valueToAngle(endVal);

                ctx.beginPath();
                ctx.arc(centerX, centerY, outerRadius, -startAng, -endAng, false);
                ctx.arc(centerX, centerY, innerRadius, -endAng, -startAng, true);
                ctx.closePath();
                ctx.fillStyle = color;
                ctx.fill();
            }

            drawArc(minValue, thresholds[0], '#27ae60');
            drawArc(thresholds[0], thresholds[1], '#f39c12');
            drawArc(thresholds[1], maxValue, '#e74c3c');

            // Draw tick marks
            for (let i = 0; i <= 100; i += 10) {
                const angle = valueToAngle(i);
                const cos = Math.cos(angle);
                const sin = Math.sin(angle);
                const innerTick = outerRadius - 10;
                const outerTick = outerRadius + 5;

                ctx.beginPath();
                ctx.moveTo(centerX + innerTick * cos, centerY - innerTick * sin);
                ctx.lineTo(centerX + outerTick * cos, centerY - outerTick * sin);
                ctx.strokeStyle = '#2c3e50';
                ctx.lineWidth = i % 20 === 0 ? 3 : 1;
                ctx.stroke();

                if (i % 20 === 0) {
                    const labelRadius = outerRadius + 25;
                    ctx.font = '16px Arial';
                    ctx.fillStyle = '#2c3e50';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(i.toString(), centerX + labelRadius * cos, centerY - labelRadius * sin);
                }
            }

            // Draw needle
            const needleAngle = valueToAngle(value);
            const needleLength = innerRadius + 50;

            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(-needleAngle + Math.PI / 2);

            ctx.beginPath();
            ctx.moveTo(0, -needleLength);
            ctx.lineTo(-8, 15);
            ctx.lineTo(8, 15);
            ctx.closePath();
            ctx.fillStyle = '#2c3e50';
            ctx.fill();

            ctx.restore();

            // Center cap
            ctx.beginPath();
            ctx.arc(centerX, centerY, 15, 0, Math.PI * 2);
            ctx.fillStyle = '#2c3e50';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
            ctx.fillStyle = '#ecf0f1';
            ctx.fill();

            // Update display
            valueDisplay.textContent = Math.round(value) + '%';

            if (value < thresholds[0]) {
                statusDisplay.textContent = 'Normal';
                statusDisplay.style.color = '#27ae60';
            } else if (value < thresholds[1]) {
                statusDisplay.textContent = 'Warning';
                statusDisplay.style.color = '#f39c12';
            } else {
                statusDisplay.textContent = 'Critical';
                statusDisplay.style.color = '#e74c3c';
            }
        }

        function animate() {
            if (Math.abs(currentValue - targetValue) > 0.5) {
                currentValue += (targetValue - currentValue) * 0.1;
            } else {
                currentValue = targetValue;
            }
            drawGauge(currentValue);
            requestAnimationFrame(animate);
        }

        function updateTarget() {
            // Simulate realistic CPU fluctuations
            const change = (Math.random() - 0.5) * 30;
            targetValue = Math.max(minValue + 10, Math.min(maxValue - 5, targetValue + change));
        }

        drawGauge(currentValue);
        animate();
        setInterval(updateTarget, 2000);
    </script>
</body>
</html>
"""

with open("plot.html", "w") as f:
    f.write(html_content)
