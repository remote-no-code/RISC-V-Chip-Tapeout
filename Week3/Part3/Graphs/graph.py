import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle

# --- Inputs (same as before) ---
files = {
    "WNS (ns)": "sta_wns.txt",
    "TNS (ns)": "sta_tns.txt",
    "Worst Max Slack (ns)": "sta_worst_max_slack.txt",
    "Worst Min Slack (ns)": "sta_worst_min_slack.txt",
}

corners = [
    "tt_025C_1v80", "ff_100C_1v65", "ff_100C_1v95",
    "ff_n40C_1v56", "ff_n40C_1v65", "ff_n40C_1v76",
    "ss_100C_1v40", "ss_100C_1v60", "ss_n40C_1v28",
    "ss_n40C_1v35", "ss_n40C_1v40", "ss_n40C_1v44",
    "ss_n40C_1v76",
]

def read_sta_file(filename):
    vals = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for i in range(1, len(lines), 2):
        vals.append(float(lines[i].strip().split()[-1]))
    return vals

# --- DataFrame ---
data = {metric: read_sta_file(path) for metric, path in files.items()}
df = pd.DataFrame(data)
df.insert(0, "PVT_CORNER", corners)

# --- Plot 2x2 connected-scatter (markers + line) ---
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("STA Metrics Across PVT Corners", fontsize=14, fontweight="bold")

metrics = ["WNS (ns)", "TNS (ns)", "Worst Max Slack (ns)", "Worst Min Slack (ns)"]
colors = ["#3b82f6", "#ef4444", "#22c55e", "#eab308"]
markers = cycle(["o", "s", "D", "^"])

for idx, metric in enumerate(metrics):
    r, c = divmod(idx, 2)
    ax = axes[r, c]
    color = colors[idx]
    marker = next(markers)
    
    # Line + markers on categorical x
    ax.plot(
        df["PVT_CORNER"], df[metric],
        color=color, marker=marker, linestyle="-", linewidth=2, markersize=6,
    )  # categorical x is supported directly [web:91][web:83]
    
    # Scatter call (optional) if you want explicit marker layering
    # ax.scatter(df["PVT_CORNER"], df[metric], color=color, s=30, zorder=3)  # [web:86]
    
    # Annotate each point with its value
    for x, y in zip(df["PVT_CORNER"], df[metric]):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7)  # [web:96][web:93]
    
    ax.set_title(f"{metric} vs PVT Corners", fontsize=11, fontweight="bold")
    ax.set_xlabel("PVT Corner", fontsize=10, fontweight="bold")
    ax.set_ylabel(metric, fontsize=10, fontweight="bold")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

