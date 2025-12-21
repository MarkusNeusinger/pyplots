""" pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-16
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Programming language popularity (word frequencies)
# Using diverse frequencies to show size variation
word_frequencies = {
    "Python": 100,
    "JavaScript": 90,
    "Java": 80,
    "TypeScript": 70,
    "SQL": 65,
    "Rust": 58,
    "Go": 52,
    "Kotlin": 46,
    "Swift": 42,
    "Ruby": 38,
    "PHP": 35,
    "Scala": 32,
    "Perl": 28,
    "Haskell": 25,
    "Lua": 22,
    "Julia": 20,
    "Dart": 18,
    "Elixir": 16,
    "Clojure": 14,
    "Erlang": 12,
}

# Set seaborn style for consistent aesthetics
sns.set_theme(style="white")

# Sort words by frequency (descending)
sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
frequencies = np.array([w[1] for w in sorted_words])

# Normalize frequencies to font sizes (scaled for 4800x2700 canvas)
min_freq, max_freq = frequencies.min(), frequencies.max()
font_sizes = 28 + (frequencies - min_freq) / (max_freq - min_freq) * 72

# Create color palette using seaborn (Blues_d for better contrast)
n_colors = len(sorted_words)
palette = sns.color_palette("Blues_d", n_colors=n_colors)
# Reverse so larger words get darker (more prominent) colors
colors = palette[::-1]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Seed for reproducibility
np.random.seed(42)

# Handcrafted positions for word cloud aesthetic (no overlap)
# Words spread across canvas with more space for larger words
positions = [
    # Large words (frequency 100-70) - need more spacing
    (0.50, 0.80),  # Python (center)
    (0.15, 0.72),  # JavaScript (left)
    (0.85, 0.72),  # Java (right)
    (0.35, 0.60),  # TypeScript
    (0.68, 0.58),  # SQL
    # Medium words (frequency 58-38)
    (0.12, 0.45),  # Rust
    (0.50, 0.45),  # Go
    (0.88, 0.45),  # Kotlin
    (0.30, 0.32),  # Swift
    (0.70, 0.32),  # Ruby
    # Smaller words (frequency 35-22)
    (0.12, 0.22),  # PHP
    (0.35, 0.18),  # Scala
    (0.55, 0.22),  # Perl
    (0.78, 0.18),  # Haskell
    (0.92, 0.22),  # Lua
    # Smallest words (frequency 20-12)
    (0.08, 0.08),  # Julia
    (0.28, 0.06),  # Dart
    (0.48, 0.08),  # Elixir
    (0.68, 0.06),  # Clojure
    (0.88, 0.08),  # Erlang
]

# Place words on the canvas
for i, (word, _freq) in enumerate(sorted_words):
    x, y = positions[i]
    fontsize = font_sizes[i]
    color = colors[i]

    ax.text(
        x, y, word, fontsize=fontsize, color=color, fontweight="bold", ha="center", va="center", transform=ax.transAxes
    )

# Remove axes for clean word cloud look
ax.axis("off")

# Add title with proper formatting
ax.set_title(
    "Programming Languages · wordcloud-basic · seaborn · pyplots.ai",
    fontsize=24,
    pad=20,
    color="#306998",
    fontweight="bold",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
