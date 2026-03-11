"""pyplots.ai
probability-weibull: Weibull Probability Plot for Reliability Analysis
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-03-11
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave
from scipy import stats


LetsPlot.setup_html()  # noqa: F405

# Data - Turbine blade fatigue-life (hours) with failures and suspensions
np.random.seed(42)
shape_param = 2.5  # beta (shape)
scale_param = 5000  # eta (scale / characteristic life)
n_failures = 25
n_censored = 5

failure_times = np.sort(stats.weibull_min.rvs(shape_param, scale=scale_param, size=n_failures))
censored_times = np.sort(np.random.uniform(1000, 4500, size=n_censored))

all_times = np.concatenate([failure_times, censored_times])
is_failure = np.concatenate([np.ones(n_failures), np.zeros(n_censored)])

sort_idx = np.argsort(all_times)
all_times = all_times[sort_idx]
is_failure = is_failure[sort_idx]

# Median rank plotting positions for failures only (Bernard's approximation)
failure_rank = np.cumsum(is_failure)
n_total = len(all_times)
median_ranks = (failure_rank - 0.3) / (n_total + 0.4)

# Weibull linearization: y = ln(-ln(1 - F))
weibull_y = np.log(-np.log(1 - median_ranks))
log_times = np.log(all_times)

# Separate failures and censored for plotting
df_all = pd.DataFrame(
    {
        "time": all_times,
        "log_time": log_times,
        "weibull_y": weibull_y,
        "status": np.where(is_failure == 1, "Failure", "Censored"),
    }
)

df_failures = df_all[df_all["status"] == "Failure"].copy()
df_censored = df_all[df_all["status"] == "Censored"].copy()

# Fit line through failure points only
slope, intercept, r_value, _, _ = stats.linregress(df_failures["log_time"], df_failures["weibull_y"])

# Weibull parameters from fit: beta = slope, eta = exp(-intercept/slope)
beta_fit = slope
eta_fit = np.exp(-intercept / slope)

# Fitted line data
fit_x = np.linspace(np.log(np.min(all_times) * 0.7), np.log(np.max(all_times) * 1.3), 100)
fit_y = slope * fit_x + intercept

df_fit = pd.DataFrame({"log_time": fit_x, "weibull_y": fit_y})

# 63.2% reference line (characteristic life)
ref_y = np.log(-np.log(1 - 0.632))

# Annotation data for parameter display
beta_text = f"\u03b2 = {beta_fit:.2f}"
eta_text = f"\u03b7 = {eta_fit:.0f} hrs"
r2_text = f"R\u00b2 = {r_value**2:.4f}"
annotation_label = f"{beta_text}\n{eta_text}\n{r2_text}"

# Y-axis tick positions and labels (cumulative probability)
prob_levels = [0.01, 0.05, 0.10, 0.20, 0.50, 0.632, 0.90, 0.99]
y_ticks = [np.log(-np.log(1 - p)) for p in prob_levels]
y_labels = [f"{p * 100:.1f}%" if p == 0.632 else f"{p * 100:.0f}%" for p in prob_levels]

# X-axis tick positions (log scale, labeled as original hours)
x_tick_vals = [np.log(v) for v in [500, 1000, 2000, 3000, 5000, 8000]]
x_tick_labels = ["500", "1000", "2000", "3000", "5000", "8000"]

# Plot
plot = (
    ggplot()  # noqa: F405
    + geom_line(  # noqa: F405
        data=df_fit,
        mapping=aes(x="log_time", y="weibull_y"),  # noqa: F405
        color="#306998",
        size=1.5,
        alpha=0.8,
    )
    + geom_point(  # noqa: F405
        data=df_failures,
        mapping=aes(x="log_time", y="weibull_y"),  # noqa: F405
        color="#306998",
        size=5,
        shape=16,
        alpha=0.9,
    )
    + geom_point(  # noqa: F405
        data=df_censored,
        mapping=aes(x="log_time", y="weibull_y"),  # noqa: F405
        color="#E74C3C",
        size=5,
        shape=1,
        stroke=2,
        alpha=0.9,
    )
    + geom_hline(  # noqa: F405
        yintercept=ref_y, linetype="dashed", color="#888888", size=0.8
    )
    + geom_text(  # noqa: F405
        data=pd.DataFrame({"x": [max(fit_x) - 0.3], "y": [min(fit_y) + 0.8], "label": [annotation_label]}),
        mapping=aes(x="x", y="y", label="label"),  # noqa: F405
        size=14,
        color="#333333",
        hjust=1,
    )
    + geom_text(  # noqa: F405
        data=pd.DataFrame({"x": [min(fit_x) + 0.1], "y": [ref_y + 0.15], "label": ["63.2% (Characteristic Life)"]}),
        mapping=aes(x="x", y="y", label="label"),  # noqa: F405
        size=11,
        color="#888888",
        hjust=0,
    )
    + scale_x_continuous(  # noqa: F405
        breaks=x_tick_vals, labels=x_tick_labels
    )
    + scale_y_continuous(  # noqa: F405
        breaks=y_ticks, labels=y_labels
    )
    + labs(  # noqa: F405
        x="Time to Failure (hours)",
        y="Cumulative Failure Probability",
        title="probability-weibull \u00b7 letsplot \u00b7 pyplots.ai",
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid_major=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
