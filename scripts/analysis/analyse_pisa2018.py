import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/2018output/oldpisa2018_cleaned_all_countries.csv")
df = pd.read_csv(data_path)

df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)

book_order = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df["books_home_cat"] = pd.Categorical(df["books_home_cat"], categories=book_order, ordered=True)

book_counts = df["books_home_cat"].value_counts().reindex(book_order)
book_percents = (book_counts / book_counts.sum() * 100).round(1)
book_df = pd.DataFrame({"Books": book_order, "Percent": book_percents.values, "n": book_counts.values})

print("\n📚 Books at Home (All Countries):")
print(tabulate(book_df, headers="keys", tablefmt="pretty"))
book_df.to_csv(os.path.join(output_dir, "2018_books_all.csv"), index=False)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x="Books", y="Percent", data=book_df)
plt.title(f"PISA 2018 – Global Distribution of Books at Home (n = {int(book_counts.sum()):,})")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home")
plt.ylim(0, book_df["Percent"].max() + 8)
for i, row in book_df.iterrows():
    ax.text(i, row["Percent"] + 2.5, f"n={int(row['n'])}", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "2018_books_all.png"))
plt.close()

oecd_codes = [
    "AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU",
    "DNK", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "ISL", "IRL", "ISR",
    "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR", "NZL",
    "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "TUR", "USA"
]

df["is_OECD"] = df["country"].isin(oecd_codes)

read_map = {1.0: "None", 2.0: "<30 min", 3.0: "30–60 min", 4.0: "1–2 hrs", 5.0: ">2 hrs"}
read_order = ["None", "<30 min", "30–60 min", "1–2 hrs", ">2 hrs"]
df["read_time_cat"] = df["read_time"].replace(read_map)
df["read_time_cat"] = pd.Categorical(df["read_time_cat"], categories=read_order, ordered=True)

read_counts = df["read_time_cat"].value_counts().reindex(read_order)
read_percents = (read_counts / read_counts.sum() * 100).round(1)
read_df = pd.DataFrame({"Time": read_order, "Percent": read_percents.values, "n": read_counts.values})

print("\nReading Time (All Countries):")
print(tabulate(read_df, headers="keys", tablefmt="pretty"))
read_df.to_csv(os.path.join(output_dir, "2018_readingtime_all.csv"), index=False)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x="Time", y="Percent", data=read_df)
plt.title(f"PISA 2018 – Global Distribution of Reading Time (n = {int(read_counts.sum()):,})")
plt.ylabel("Percent of Students")
plt.xlabel("Reading Time")
plt.ylim(0, read_df["Percent"].max() + 8)
for i, row in read_df.iterrows():
    ax.text(i, row["Percent"] + 2.5, f"n={int(row['n'])}", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "2018_readingtime_all.png"))
plt.close()

comp_read_df = []
for label, group_df in [("OECD", df[df["is_OECD"]]), ("non-OECD", df[~df["is_OECD"]])]:
    vc = group_df["read_time_cat"].value_counts().reindex(read_order)
    pct = (vc / vc.sum() * 100).round(1)
    temp = pd.DataFrame({"Reading Time": read_order, "Percent": pct.values, "Group": label})
    comp_read_df.append(temp)
comp_read_df = pd.concat(comp_read_df)

plt.figure(figsize=(10, 5))
ax = sns.barplot(
    x="Reading Time",
    y="Percent",
    hue="Group",
    data=comp_read_df,
    palette={
        "OECD": "#465759",     
        "non-OECD": "#B77D8F"
    }
)

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f'{height:.1f}%', 
                    (p.get_x() + p.get_width() / 2., height + 1),
                    ha='center', va='bottom', fontsize=9, color='black')

plt.title("PISA 2018 – Daily Reading Time by OECD Status")
plt.ylabel("Percent of Students")
plt.xlabel("Reading Time per Day")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.ylim(0, comp_read_df["Percent"].max() + 10)
plt.legend(title="Group")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "2018_readingtime_by_OECD.png"))
plt.close()

for group in comp_read_df["Group"].unique():
    summary = comp_read_df[comp_read_df["Group"] == group]
    summary.to_csv(os.path.join(output_dir, f"2018_readingtime_{group}.csv"), index=False)

df["book_reading_format_label"] = df["book_reading_format_label"].astype(str).str.strip()
format_counts = df["book_reading_format_label"].value_counts(dropna=True).sort_index()
format_percents = (format_counts / format_counts.sum() * 100).round(1)

format_df = pd.DataFrame({
    "Format": format_counts.index,
    "Percent": format_percents.values,
    "n": format_counts.values
})

print("\nBook Format Preference (All Countries):")
print(tabulate(format_df, headers="keys", tablefmt="pretty"))
format_df.to_csv(os.path.join(output_dir, "2018_format_all.csv"), index=False)

plt.figure(figsize=(8, 5))
format_palette = ["#BFD8C6", "#D5C9C0", "#B5C2CA", "#E5D8CB", "#68747A"]
ax = sns.barplot(x="Format", y="Percent", data=format_df, palette=format_palette)

plt.title(f"PISA 2018 – Book Format Preference (n = {int(format_counts.sum()):,})", fontsize=13)
plt.ylabel("Percent of Students")
plt.xlabel("Preferred Format")
plt.xticks(rotation=15)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())

for i, row in format_df.iterrows():
    ax.text(i, row["Percent"] + 2.5, f"{row['Percent']}%\n(n={int(row['n'])})", ha='center', fontsize=9)

plt.ylim(0, format_df["Percent"].max() + 10)
plt.tight_layout()
chart_path = os.path.join(output_dir, "2018_format_all.png")
plt.savefig(chart_path, bbox_inches="tight")
print(f"\nSaved improved format bar chart to: {chart_path}")
plt.close()

attitude_labels = {
    "att_1_read_only_if_have_to": "I read only if I have to",
    "att_2_reading_hobby": "Reading is one of my favourite hobbies",
    "att_3_talk_books": "I like talking about books with other people",
    "att_4_reading_waste": "For me, reading is a waste of time",
    "att_5_read_for_info": "I read only to get information that I need"
}

att_output_dir = os.path.join(BASE_DIR, "../output/attitudes_readtime")
os.makedirs(att_output_dir, exist_ok=True)

att_counts = {}
for col, label in attitude_labels.items():
    vc = df[col].value_counts(dropna=False).sort_index()
    att_counts[col] = vc
    print(f"\nQ: {label} [{col}] value counts:")
    print(vc)

att_df = pd.DataFrame(att_counts).fillna(0).astype(int)
att_df.index.name = "Response"
att_df.to_csv(os.path.join(att_output_dir, "pisa2018_attitudes.csv"))

print(f"\nSaved attitude response breakdown ➜ pisa2018_attitudes.csv")

oecd_codes = [
    "AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU",
    "DNK", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "ISL", "IRL", "ISR",
    "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR", "NZL",
    "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "TUR", "USA"
]

df["is_OECD"] = df["country"].isin(oecd_codes)
df_bh = df.dropna(subset=["books_home_cat"])

for group_label, group_df in [("OECD", df_bh[df_bh["is_OECD"]]), ("non-OECD", df_bh[~df_bh["is_OECD"]])]:
    counts = group_df["books_home_cat"].value_counts().reindex(book_order)
    percents = (counts / counts.sum() * 100).round(1)
    summary = pd.DataFrame({"Books": book_order, "Percent": percents.values, "n": counts.values})
    summary.to_csv(os.path.join(output_dir, f"2018_books_{group_label}.csv"), index=False)
    print(f"\n{group_label} Books at Home:")
    print(tabulate(summary, headers="keys", tablefmt="pretty"))

comp_df = []
for label, group_df in [("OECD", df_bh[df_bh["is_OECD"]]), ("non-OECD", df_bh[~df_bh["is_OECD"]])]:
    vc = group_df["books_home_cat"].value_counts().reindex(book_order)
    pct = (vc / vc.sum() * 100).round(1)
    temp = pd.DataFrame({"Books": book_order, "Percent": pct.values, "Group": label})
    comp_df.append(temp)
comp_df = pd.concat(comp_df)

plt.figure(figsize=(10, 5))
ax = sns.barplot(
    x="Books",
    y="Percent",
    hue="Group",
    data=comp_df,
    palette={
        "OECD": "#465759",     
        "non-OECD": "#B77D8F" 
    }
)

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f'{height:.1f}%', 
                    (p.get_x() + p.get_width() / 2., height + 1),
                    ha='center', va='bottom', fontsize=9, color='black')

plt.title("PISA 2018 – Books at Home by OECD Status")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.ylim(0, comp_df["Percent"].max() + 10)
plt.legend(title="Group")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "2018_books_by_OECD.png"))
plt.close()