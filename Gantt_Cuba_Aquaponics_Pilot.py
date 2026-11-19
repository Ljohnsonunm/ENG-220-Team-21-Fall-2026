import matplotlib.pyplot as plt
import numpy as np

# Tasks ordered from bottom to top in the chart
tasks = [
    "Full Steady-State (Fish + Greens)",
    "First Greens/Herb Harvests",
    "Fingerling & Crop Stocking",
    "Biofilter Cycling (Fishless)",
    "Tanks, Rafts & Plumbing",
    "Site Prep & High Tunnel Build",
    "Local Lead Training (SFCC)",
    "Grants, MOUs & Permits"
]

# Start month (0-indexed: 0 = Start, 8 = M8) and duration in months
# Stocking runs 6.5 -> 8.0 (1.5 mo), meeting First Greens/Herb Harvests right at 8.0 (M8)
starts = np.array([12.0, 8.0, 6.5, 5.0, 4.0, 2.0, 1.0, 0.0])
durations = np.array([1.5, 4.5, 1.5, 1.5, 1.5, 2.0, 3.0, 2.0])

colors = [
    "#1b5e20",  # Full steady-state
    "#43a047",  # First greens/herb harvests
    "#0288d1",  # Stocking
    "#00acc1",  # Biofilter cycling
    "#5e35b1",  # Plumbing/tanks/rafts
    "#fb8c00",  # Site prep & hoop house
    "#8e24aa",  # SFCC lead training
    "#546e7a",  # Grants, MOUs & permits
]

fig, ax = plt.subplots(figsize=(10, 5.5))

y_pos = np.arange(len(tasks))
ax.barh(
    y_pos,
    durations,
    left=starts,
    height=0.55,
    color=colors,
    edgecolor="black",
    linewidth=0.6
)

# Formatting axes
ax.set_yticks(y_pos)
ax.set_yticklabels(tasks, fontsize=10)
ax.set_xlim(0, 13.5)
ax.set_xticks(np.arange(0, 14, 1))
ax.set_xticklabels([f"M{i}" if i > 0 else "Start" for i in range(14)], fontsize=9)
ax.set_xlabel(
    "Project Timeline (Months Desert Verde Pace)",
    fontsize=10,
    fontweight="bold"
)
ax.set_title(
    "Cuba Aquaponics Pilot Gantt Chart",
    fontsize=12,
    fontweight="bold",
    pad=12
)

# Grid and clean spines
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotate milestone at M8 for first greens
ax.axvline(8.0, color="#2e7d32", linestyle=":", linewidth=1.2)
ax.text(8.15, 0.3, "First Greens (M8)", color="#1b5e20", fontsize=8.5, fontweight="bold")

plt.tight_layout()
plt.savefig("cuba_aquaponics_gantt.png", dpi=300)
plt.show()
