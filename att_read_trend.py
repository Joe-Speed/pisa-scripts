import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# === 1. File setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
att_dir = os.path.join(BASE_DIR, "../output/attitudes_readtime")
plot_dir = os.path.join(att_dir, "plots")
os.makedirs(plot_dir, exist_ok=True)

# === 2. File paths ===
att_files = {
    2000: "pisa2000_attitudes.csv",
    2009: "pisa2009_attitudes.csv",
    2018: "pisa2018_attitudes.csv"
}
time_files = {
    2000: "pisa2000_reading_time.csv",
    2009: "pisa2009_reading_time.csv",
    2018: "pisa2018_reading_time.csv"
}

# === 3. Column mapping for attitudes ===
attitude_map = {
    "I read only if I have to": {
        2000: "att_q35a_only_if_have_to",
        2009: "Q1: I read only if I have to",
        2018: "att_1_read_only_if_have_to"
    },
    "Reading is one of my favourite hobbies": {
        2000: "att_q35b_reading_hobby",
        2009: "Q2: Reading is one of my favorite hobbies",
        2018: "att_2_reading_hobby"
    },
    "I like talking about books with other people": {
        2000: "att_q35c_talk_books",
        2009: "Q3: I like talking about books with other people",
        2018: "att_3_talk_books"
    },
    "For me, reading is a waste of time": {
        2000: "att_q35f_waste_of_time",
        2009: "Q6: For me, reading is a waste of time",
        2018: "att_4_reading_waste"
    },
    "I read only to get information that I need": {
        2000: "att_q35h_read_for_info",
        2009: "Q8: I read only to get information that I need",
        2018: "att_5_read_for_info"
    }
}

# === 4. ATTITUDE TREND PLOTS ===
sns.set(style="whitegrid")

for att_label, year_map in attitude_map.items():
    df_plot = pd.DataFrame()
    sample_sizes = {}

    print(f"\n📖 {att_label}")
    for year, file in att_files.items():
        df = pd.read_csv(os.path.join(att_dir, file))  # fixed here
        col = year_map[year]
        if col not in df.columns:
            raise KeyError(f"Column '{col}' not found in {file}")
        total = df[col].sum()
        proportions = (df[col] / total * 100).round(2)
        df_plot[year] = proportions
        sample_sizes[year] = int(total)

        response_str = ", ".join([f"{i}: {proportions.get(i, 0.0)}%" for i in [1, 2, 3, 4]])
        print(f"{year}: [{response_str}]")

    df_plot = df_plot.T[[1, 2, 3, 4]]
    df_plot.index = df_plot.index.astype(int)
    label_lines = [f"{year} (n = {sample_sizes[year]:,})" for year in df_plot.index]

    plt.figure(figsize=(10, 5))
    for col, label in zip(df_plot.columns, ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]):
        plt.plot(df_plot.index, df_plot[col], marker='o', label=label)

    plt.title(f"{att_label} (2000–2018)")
    plt.ylabel("Percent of Students")
    plt.xlabel("Year")
    plt.xticks([2000, 2009, 2018], label_lines)

    min_val = df_plot.min().min()
    max_val = df_plot.max().max()
    margin = 5
    plt.ylim(max(0, min_val - margin), min(100, max_val + margin))

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(title="Response", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    filename = f"{att_label[:30].replace(' ', '_').replace(':','')}_trend.png"
    plt.savefig(os.path.join(plot_dir, filename))
    plt.close()

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


plt.figure(figsize=(10, 5))
for category in read_order:
    plt.plot(df_time_plot.index, df_time_plot[category], marker='o', label=category)

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
