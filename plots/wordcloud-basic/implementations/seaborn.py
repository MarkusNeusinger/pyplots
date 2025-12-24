""" pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-24
"""

import random

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


# Apply seaborn styling - uses seaborn's aesthetic system
sns.set_theme(style="white", context="talk", font_scale=1.2)

# Data - Tech industry survey responses about skills
word_frequencies = {
    "Python": 150,
    "JavaScript": 120,
    "Data": 110,
    "Machine Learning": 100,
    "Cloud": 95,
    "API": 90,
    "Database": 85,
    "Security": 80,
    "DevOps": 75,
    "Docker": 70,
    "Kubernetes": 65,
    "React": 60,
    "SQL": 58,
    "AWS": 55,
    "Git": 52,
    "Agile": 50,
    "Testing": 48,
    "Linux": 45,
    "TypeScript": 42,
    "Node": 40,
    "REST": 38,
    "CI/CD": 35,
    "Microservices": 32,
    "Azure": 30,
    "MongoDB": 28,
    "Redis": 26,
    "GraphQL": 24,
    "Terraform": 22,
    "Spark": 20,
    "Analytics": 18,
    "Frontend": 16,
    "Backend": 15,
    "Scalability": 14,
    "Automation": 13,
    "Architecture": 12,
    "Networking": 11,
    "Performance": 10,
    "Monitoring": 9,
    "Debugging": 8,
    "Documentation": 7,
}

# Use seaborn color palette for word cloud colors
palette = sns.color_palette("muted", n_colors=10)
random.seed(42)


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    color = palette[random.randint(0, len(palette) - 1)]
    r, g, b = [int(c * 255) for c in color[:3]]
    return f"rgb({r}, {g}, {b})"


# Create word cloud with settings optimized for readability
wc = WordCloud(
    width=4800,
    height=2700,
    background_color="white",
    max_words=100,
    min_font_size=24,
    max_font_size=280,
    random_state=42,
    prefer_horizontal=0.8,
    margin=15,
    relative_scaling=0.5,
    collocations=False,
    color_func=color_func,
).generate_from_frequencies(word_frequencies)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")

# Title
fig.suptitle("Tech Skills Survey · wordcloud-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
