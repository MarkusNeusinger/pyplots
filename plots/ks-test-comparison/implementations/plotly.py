""" pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: plotly 6.5.2 | Python 3.14.3
Quality: 81/100 | Created: 2026-02-17
"""

import numpy as np
import plotly.graph_objects as go
from scipy import stats


# Data
np.random.seed(42)
good_customers = np.random.beta(5, 2, size=500) * 100
bad_customers = np.random.beta(2, 5, size=500) * 100

good_sorted = np.sort(good_customers)
bad_sorted = np.sort(bad_customers)

good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# K-S test
ks_stat, p_value = stats.ks_2samp(good_customers, bad_customers)

# Find the point of maximum divergence
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_cdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_cdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
diff = np.abs(good_cdf_at_all - bad_cdf_at_all)
max_idx = np.argmax(diff)
max_x = all_values[max_idx]
max_good_y = good_cdf_at_all[max_idx]
max_bad_y = bad_cdf_at_all[max_idx]

# Plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=good_sorted,
        y=good_ecdf,
        mode="lines",
        name="Good Customers",
        line={"color": "#306998", "width": 3, "shape": "hv"},
    )
)

fig.add_trace(
    go.Scatter(
        x=bad_sorted,
        y=bad_ecdf,
        mode="lines",
        name="Bad Customers",
        line={"color": "#E8590C", "width": 3, "shape": "hv"},
    )
)

# Maximum divergence line
fig.add_trace(
    go.Scatter(
        x=[max_x, max_x],
        y=[min(max_good_y, max_bad_y), max(max_good_y, max_bad_y)],
        mode="lines",
        name=f"K-S Statistic = {ks_stat:.3f}",
        line={"color": "#2B8A3E", "width": 3, "dash": "dash"},
    )
)

# Annotation for K-S statistic and p-value
fig.add_annotation(
    x=max_x,
    y=(max_good_y + max_bad_y) / 2,
    text=f"D = {ks_stat:.3f}<br>p < 0.001",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=2,
    arrowcolor="#2B8A3E",
    ax=80,
    ay=-40,
    font={"size": 18, "color": "#2B8A3E"},
    bordercolor="#2B8A3E",
    borderwidth=2,
    borderpad=8,
    bgcolor="rgba(255,255,255,0.9)",
)

# Style
fig.update_layout(
    title={"text": "ks-test-comparison · plotly · pyplots.ai", "font": {"size": 28}},
    xaxis={
        "title": {"text": "Credit Score", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": False,
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Cumulative Proportion", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "range": [0, 1.05],
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.08)",
        "gridwidth": 1,
        "zeroline": False,
    },
    template="plotly_white",
    legend={
        "font": {"size": 18},
        "x": 0.02,
        "y": 0.98,
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "rgba(0,0,0,0.1)",
        "borderwidth": 1,
    },
    plot_bgcolor="white",
    margin={"l": 80, "r": 40, "t": 80, "b": 80},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
