
import csv
from pathlib import Path

import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent

fig, axes = plt.subplots(3, 1, figsize=(10, 9))

for ax, color in zip(axes, ["red", "green", "blue"]):
    path = BASE_DIR / f"histogram_{color}.csv"

    with open(path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    values = [int(row["Value"]) for row in rows]
    counts = [int(row["Count"]) for row in rows]

    ax.plot(values, counts, color=color)
    ax.set_title(f"{color.capitalize()} Channel Histogram")
    ax.set_xlabel("Pixel intensity")
    ax.set_ylabel("Pixel count")
    ax.set_xlim(0, 255)
    ax.grid(alpha=0.3)

plt.tight_layout()
output = BASE_DIR / "rgb_histograms.png"
plt.savefig(output, dpi=150)
print(f"Saved: {output}")
plt.show()

