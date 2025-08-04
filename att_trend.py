import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# === 1. Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_paths = {
    2000: os.path.join(BASE_DIR, "../output/pisa2000_cleaned.csv"),
    2009: os.path.join(BASE_DIR, "../output/pisa2009_cleaned.csv"),
    2018: os.path.join(BASE_DIR, "../output/2018output/newpisa2018_cleaned_all_countries.csv"),
}

plot_dir = os.path.join(BASE_DIR, "../output/attitudes_trend/plots")
os.makedirs(plot_dir, exist_ok=True)

# === 2. Unified variable map ===
attitude_var_map = {
    "I read only if I have to": {
        2000: "att_q35a_only_if_have_to",
        2009: "att_q35a",
        2018: "att_1_read_only_if_have_to"
    },
    "Reading is one of my favourite hobbies": {
        2000: "att_q35b_reading_hobby",
        2009: "att_q35b",
        2018: "att_2_reading_hobby"
    },
    "I like talking about books with other people": {
        2000: "att_q35c_talk_books",
        2009: "att_q35c",
        2018: "att_3_talk_books"
    },
    "For me, reading is a waste of time": {
        2000: "att_q35f_waste_of_time",
        2009: "att_q35f",
        2018: "att_4_reading_waste"
    },
    "I read only to get information that I need": {
        2000: "att_q35h_read_for_info",
        2009: "att_q35h",
        2018: "att_5_read_for_info"
    }
}

# === 3. Style ===
sns.set(style="whitegrid")

attitude_colors = [
    "#B77D8F",  # Strongly Disagree
    "#BFD8C6",  # Disagree
    "#AAC7D8",  # Agree
    "#465759"   # Strongly Agree
]

# === 4. Loop and plot ===
for item_label, year_map in attitude_var_map.items():
    df_plot = pd.DataFrame()
    sample_sizes = {}

    print(f"\n📖 {item_label}")
    for year, var in year_map.items():
        path = file_paths.get(year)
        if not os.path.exists(path):
            print(f"{year}: ❌ File not found at {path}")
            continue

        df = pd.read_csv(path)
        if var not in df.columns:
            print(f"{year}: ❌ Column not found: {var}")
            continue

        series = df[var]
        if year == 2009:
            valid = series[series.isin([1, 2, 3, 4])]
        else:
            valid = series.dropna()
            valid = valid[valid.isin([1, 2, 3, 4])]

        vc = valid.value_counts(normalize=True).sort_index() * 100
        vc = vc.round(2)
        df_plot[year] = vc
        sample_sizes[year] = len(valid)

        response_str = ", ".join([f"{int(k)}: {v:.2f}%" for k, v in vc.items()])
        print(f"{year}: [{response_str}], n = {len(valid):,}")

    # Reformat for plotting
    df_plot = df_plot.T[[1, 2, 3, 4]]
    df_plot.index = df_plot.index.astype(int)
    label_lines = [f"{year} (n = {sample_sizes[year]:,})" for year in df_plot.index]

    plt.figure(figsize=(10, 5))
    for i, (col, label) in enumerate(zip(df_plot.columns, ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"])):
        plt.plot(df_plot.index, df_plot[col], marker='o', label=label, color=attitude_colors[i])

    plt.title(f"{item_label} (2000–2018)")
    plt.ylabel("Percent of Students")
    plt.xlabel("Year")
    plt.xticks([2000, 2009, 2018], label_lines)

    min_val = df_plot.min().min()
    max_val = df_plot.max().max()
    margin = 5
    plt.ylim(max(0, min_val - margin), min(100, max_val + margin))

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(title="Response", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()

    filename = f"{item_label[:40].replace(' ', '_').replace(':','')}_trend.png"
    plt.savefig(os.path.join(plot_dir, filename))
    plt.close()
