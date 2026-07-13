import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "../output")
YEARS = [2003, 2006, 2009, 2012, 2015, 2018, 2022]
BOOK_ORDER = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]

label_map = {
    "1–10": "0–10", "0–10": "0–10", "0-10": "0–10",
    "11–25": "11–25", "11-25": "11–25",
    "26–100": "26–100", "26-100": "26–100",
    "51–100": "26–100", "51-100": "26–100",
    "101–200": "101–200", "101-200": "101–200", "101–250": "101–200",
    "201–500": "201–500", "201-500": "201–500", "251–500": "201–500",
    "500+": "500+", "More than 500 books": "500+"
}

all_dfs = []

for year in YEARS:
    # 2018 comes from analyse_pisa2018.py, which names its output differently
    file_name = "2018_books_all.csv" if year == 2018 else f"pisa{year}_books_overall.csv"
    path = os.path.join(OUTPUT_DIR, file_name)
    if not os.path.exists(path):
        print(f"Missing: {path}")
        continue

    df = pd.read_csv(path)

    if "books_home" in df.columns:
        label_col = "books_home"
    elif "books_home_label" in df.columns:
        label_col = "books_home_label"
    elif "Books" in df.columns:
        label_col = "Books"
    elif "index" in df.columns:
        label_col = "index"
    else:
        raise ValueError(f"No label column found for {year}")

    if "Percent" in df.columns:
        df = df.rename(columns={"Percent": "percent"})
    elif "percent" not in df.columns:
        raise ValueError(f"No percent column found for {year}")

    df["books_home"] = df[label_col].astype(str).map(label_map).fillna(df[label_col])
    df["books_home"] = pd.Categorical(df["books_home"], categories=BOOK_ORDER, ordered=True)
    df = df[df["books_home"].notna() & df["percent"].notna()]
    df["year"] = year

    all_dfs.append(df[["year", "books_home", "percent"]])

combined = pd.concat(all_dfs).sort_values(["books_home", "year"]).reset_index(drop=True)

line_colors = [
    "#BFD8C6", 
    "#B77D8F",  
    "#F1BD78",  
    "#D29B85",  
    "#9BA9BF",  
    "#465759",  
]

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

for i, book_cat in enumerate(BOOK_ORDER):
    df_plot = combined[combined["books_home"] == book_cat]
    plt.plot(df_plot["year"], df_plot["percent"],
             marker="o", label=book_cat, color=line_colors[i])

plt.title("PISA 2003–2022: Change in Global Books at Home")
plt.ylabel("Percent of Students")
plt.xlabel("PISA Year")
plt.xticks(YEARS)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.legend(title="Books at Home", loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()

output_path = os.path.join(OUTPUT_DIR, "pisa_books_over_time_final_noline.png")
plt.savefig(output_path)
plt.show()
print(f"Saved plot to: {output_path}")
