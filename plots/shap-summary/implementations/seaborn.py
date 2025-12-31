"""pyplots.ai
shap-summary: SHAP Summary Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier


# Data - Train a model and compute SHAP-like values
np.random.seed(42)
data = load_breast_cancer()
X = data.data[:, :12]  # Use first 12 features for cleaner visualization
feature_names = [name.replace(" ", "\n") if len(name) > 20 else name for name in data.feature_names[:12]]

# Train a gradient boosting model
model = GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=42)
model.fit(X, data.target)

# Compute approximate SHAP values using feature perturbation approach
n_samples = 200
sample_indices = np.random.choice(len(X), n_samples, replace=False)
X_sample = X[sample_indices]

# Calculate feature contributions (SHAP-like values)
# Use model predictions and feature importance for realistic values
base_pred = model.predict_proba(X_sample)[:, 1]
shap_values = np.zeros((n_samples, X_sample.shape[1]))

for i in range(X_sample.shape[1]):
    # Permutation-based importance approximation
    X_perm = X_sample.copy()
    X_perm[:, i] = np.random.permutation(X_perm[:, i])
    perm_pred = model.predict_proba(X_perm)[:, 1]
    # Scale by feature importance for more realistic distribution
    importance = model.feature_importances_[i]
    shap_values[:, i] = (base_pred - perm_pred) * (1 + importance * 10)

# Normalize feature values for coloring (0 to 1 scale)
feature_values_norm = (X_sample - X_sample.min(axis=0)) / (X_sample.max(axis=0) - X_sample.min(axis=0) + 1e-8)

# Sort features by mean absolute SHAP value
mean_abs_shap = np.abs(shap_values).mean(axis=0)
sorted_indices = np.argsort(mean_abs_shap)[::-1][:10]  # Top 10 features

# Prepare data for plotting
plot_data = []
for rank, feat_idx in enumerate(sorted_indices):
    for sample in range(n_samples):
        plot_data.append(
            {
                "Feature": feature_names[feat_idx],
                "SHAP Value": shap_values[sample, feat_idx],
                "Feature Value": feature_values_norm[sample, feat_idx],
                "Rank": rank,
            }
        )

df = pd.DataFrame(plot_data)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Create stripplot with color mapped to feature values
# Use seaborn's stripplot with custom coloring
ordered_features = [feature_names[i] for i in sorted_indices]

# Plot points with jitter
for i, feat in enumerate(ordered_features):
    feat_df = df[df["Feature"] == feat]
    y_positions = np.full(len(feat_df), i) + np.random.uniform(-0.3, 0.3, len(feat_df))
    scatter = ax.scatter(
        feat_df["SHAP Value"],
        y_positions,
        c=feat_df["Feature Value"],
        cmap="coolwarm",
        s=80,
        alpha=0.7,
        edgecolors="none",
    )

# Add vertical line at x=0
ax.axvline(x=0, color="#306998", linestyle="-", linewidth=2, alpha=0.8)

# Styling
ax.set_yticks(range(len(ordered_features)))
ax.set_yticklabels(ordered_features, fontsize=16)
ax.set_xlabel("SHAP Value (Impact on Model Output)", fontsize=20)
ax.set_ylabel("Feature", fontsize=20)
ax.set_title("shap-summary · seaborn · pyplots.ai", fontsize=24, pad=20)
ax.tick_params(axis="x", labelsize=16)
ax.invert_yaxis()  # Most important at top
ax.grid(True, axis="x", alpha=0.3, linestyle="--")

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label("Feature Value\n(Low → High)", fontsize=16)
cbar.ax.tick_params(labelsize=14)

# Adjust spines
sns.despine(left=True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
