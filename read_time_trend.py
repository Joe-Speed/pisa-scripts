import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# === 1. File setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
att_dir = os.path.join(BASE_DIR, "../output/readtime")
plot_dir = os.path.join(att_dir, "plots")
os.makedirs(plot_dir, exist_ok=True)

# === 2. File paths ===

time_files = {
    2000: "pisa2000_reading_time.csv",
    2009: "pisa2009_reading_time.csv",
    2018: "pisa2018_reading_time.csv"
}

# === 5. READING TIME TREND PLOT ===
standard_labels = {
    "don't read": "None",
    "none": "None",
    "<30 min": "<30 min",
    "30–60 min": "30–60 min",
    "31–60 min": "30–60 min",
    "1–2 hrs": "1–2 hrs",
    "2+ hrs": ">2 hrs",
    ">2 hrs": ">2 hrs"
}
read_order = ["None", "<30 min", "30–60 min", "1–2 hrs", ">2 hrs"]

df_time_plot = pd.DataFrame()
sample_sizes = {}

for year, file in time_files.items():
    df = pd.read_csv(os.path.join(att_dir, file), keep_default_na=False)
    time_col = "Time" if "Time" in df.columns else "read_time"
    pct_col = "Percent" if "Percent" in df.columns else "percent"
    n_col = "n"

    df[time_col] = (
        df[time_col]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace("’", "'", regex=False)
        .str.lower()
        .map(standard_labels)
        .fillna(df[time_col])
    )

    df_grouped = df.groupby(time_col).agg({pct_col: 'sum', n_col: 'sum'})
    sample_sizes[year] = int(df_grouped[n_col].sum())

    row = df_grouped[pct_col].reindex(read_order)
    df_time_plot[year] = row

df_time_plot = df_time_plot.T
df_time_plot.index = df_time_plot.index.astype(int)
label_lines = [f"{year} (n = {sample_sizes[year]:,})" for year in df_time_plot.index]

# === Print reading time percentages by year ===
print("\n=== Reading Time Trends ===")
for year in df_time_plot.index:
    year_vals = df_time_plot.loc[year]
    response_str = ", ".join([f"{label}: {year_vals[label]:.1f}%" for label in read_order if pd.notna(year_vals[label])])
    print(f"{year} (n = {sample_sizes[year]:,}): {response_str}")


# === Define color palette for reading time categories ===
read_colors = [
    "#BFD8C6",  # None → mint-sage
    "#B77D8F",  # <30 min → muted burgundy
    "#AAC7D8",  # 30–60 min → intelligent soft blue
    "#D29B85",  # 1–2 hrs → terracotta
    "#9BA9BF",  # >2 hrs → slate blue
]

# === Plot ===
plt.figure(figsize=(10, 5))
for i, category in enumerate(read_order):
    plt.plot(df_time_plot.index, df_time_plot[category],
             marker='o', label=category, color=read_colors[i])

plt.title("Reading Time Distribution (2000–2018)")
plt.ylabel("Percent of Students")
plt.xlabel("Year")
plt.xticks([2000, 2009, 2018], label_lines)

min_val = df_time_plot.min().min()
max_val = df_time_plot.max().max()
margin = 5
plt.ylim(max(0, min_val - margin), min(100, max_val + margin))

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.legend(title="Daily Reading Time", loc="center left", bbox_to_anchor=(1, 0.5))
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, "reading_time_trend.png"))
plt.close()
