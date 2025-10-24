import matplotlib.pyplot as plt
import pandas as pd

# --- Inputs ---
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
    for i in range(1, len(lines), 2):           # take every second line
        vals.append(float(lines[i].strip().split()[-1]))
    return vals

# --- Build DataFrame ---
data = {metric: read_sta_file(path) for metric, path in files.items()}
df = pd.DataFrame(data)
df.insert(0, "PVT_CORNER", corners)

# --- Render table ---
fig, ax = plt.subplots(figsize=(14, 3.8))
ax.axis("off")

cell_text = df.round(3).values
nrows, ncols = cell_text.shape

# Alternate row colors without creating a label column
cell_colours = [
    ["#e6f2ff" if i % 2 == 0 else "#ffffff" for _ in range(ncols)]
    for i in range(nrows)
]

table = ax.table(
    cellText=cell_text,
    cellColours=cell_colours,                 # no rowLabels/rowColours -> no blank column
    colLabels=list(df.columns),
    colColours=["#ffcc00"] * ncols,           # header background
    loc="center",
    cellLoc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

# Header bold
for c in range(ncols):
    table[(0, c)].set_text_props(weight="bold")  # header row

# First data column: bold + left aligned
for r in range(1, nrows + 1):
    cell = table[(r, 0)]
    cell.set_text_props(weight="bold", ha="left")  # use Text properties via set_text_props

# Title above the table with a bit of headroom
fig.suptitle("STA Summary Table", fontsize=12, fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])

plt.show()

