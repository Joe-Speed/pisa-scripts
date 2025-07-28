import pandas as pd
import os
from tabulate import tabulate

# === 1. Load raw fixed-width text file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2003/2003_QU_data.txt")

# COUNTRY (cols 1–3), ST19Q01 (col 96)
colspecs = [(0, 3), (95, 96)]
col_names = ["country", "books_raw"]
df = pd.read_fwf(data_path, colspecs=colspecs, names=col_names)

df["country"] = pd.to_numeric(df["country"], errors="coerce")

# === 2. Country mapping ===
country_map = {
    8: "Albania", 32: "Argentina", 36: "Australia", 40: "Austria", 56: "Belgium",
    76: "Brazil", 100: "Bulgaria", 124: "Canada", 152: "Chile", 203: "Czech Republic",
    208: "Denmark", 246: "Finland", 250: "France", 276: "Germany", 300: "Greece",
    344: "Hong Kong (China)", 348: "Hungary", 352: "Iceland", 360: "Indonesia",
    372: "Ireland", 376: "Israel", 380: "Italy", 392: "Japan", 410: "Korea",
    428: "Latvia", 438: "Liechtenstein", 442: "Luxembourg", 446: "Macao (China)",
    484: "Mexico", 528: "Netherlands", 554: "New Zealand", 578: "Norway", 604: "Peru",
    616: "Poland", 620: "Portugal", 643: "Russia", 703: "Slovakia",
    724: "Spain", 752: "Sweden", 756: "Switzerland", 764: "Thailand", 788: "Tunisia",
    792: "Turkey", 807: "Macedonia", 826: "United Kingdom", 840: "United States",
    858: "Uruguay", 891: "Yugoslavia"
}
df["country_name"] = df["country"].map(country_map)

# === 3. Convert and filter book responses ===
df["books_raw"] = pd.to_numeric(df["books_raw"], errors="coerce")
df = df[df["books_raw"].between(1, 6)]

# === 4. Map to labels and enforce order ===
book_map = {
    1: "0–10", 2: "11–25", 3: "26–100", 4: "101–200", 5: "201–500", 6: "500+"
}
df["books_home"] = df["books_raw"].map(book_map)
ordered_labels = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df["books_home"] = pd.Categorical(df["books_home"], categories=ordered_labels, ordered=True)

# === 5. Save cleaned data ===
output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "pisa2003_amountbooks.csv"), index=False)
print(f"\n✅ Cleaned data saved to: {output_dir}/pisa2003_amountbooks.csv")

# === 6. Summary: Sample Checks ===
print("\n🔍 Sample preview:")
print(tabulate(df.head(10), headers="keys", tablefmt="pretty"))

print(f"\n🌍 Unique countries in dataset: {df['country_name'].nunique()}")
print(f"🧮 Total valid book entries: {len(df)}")

# === 7. Percentage of students per book category by country ===
summary = (
    df.groupby("country_name")["books_home"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .loc[:, ordered_labels]
    * 100
).round(1)

print("\n📚 Percentage of Students per Book Category by Country:")
print(tabulate(summary, headers="keys", tablefmt="pretty"))

summary.to_csv(os.path.join(output_dir, "pisa2003_books_by_country.csv"))
print(f"\n📁 Exported to: {output_dir}/pisa2003_books_by_country.csv")

# === 8. Overall Book Distribution ===
overall = df["books_home"].value_counts(normalize=True).sort_index() * 100
overall = overall.reindex(ordered_labels).round(1)

print("\n📊 Overall Book Distribution (% All Countries):")
overall_df = pd.DataFrame({"Percent": overall})
print(tabulate(overall_df, headers="keys", tablefmt="pretty"))

overall_df.to_csv(os.path.join(output_dir, "pisa2003_books_overall.csv"))
print(f"\n📁 Exported to: {output_dir}/pisa2003_books_overall.csv")

# === 9. Bar Chart: Global Distribution of Books at Home (2003) ===
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
overall_df = overall.reset_index()
overall_df.columns = ["books_home", "percent"]
counts = df["books_home"].value_counts().reindex(ordered_labels)
overall_df["n"] = counts.values

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5.5))  # Slightly taller for label space
bars = sns.barplot(x="books_home", y="percent", data=overall_df)

# Add value labels above bars
for bar, label in zip(bars.patches, overall_df["n"]):
    height = bar.get_height()
    bars.annotate(f"n = {label:,}", xy=(bar.get_x() + bar.get_width() / 2, height + 1),
                  ha='center', va='bottom', fontsize=9)

# Title and labels
plt.title("PISA 2003 – Global Distribution of Books at Home")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home Category")
plt.ylim(0, overall_df["percent"].max() + 8)
plt.tight_layout()

# Add total n label
total_n = len(df)
plt.figtext(0.5, -0.05, f"Total valid responses: n = {total_n:,}", ha="center", fontsize=10)

# Save chart
chart_path = os.path.join(output_dir, "pisa2003_books_home_chart.png")
plt.savefig(chart_path, bbox_inches='tight')
print(f"\n📊 Saved bar chart to: {chart_path}")
plt.show()

# === 6a. Sample Size and Country Coverage ===
num_students = len(df)
num_countries = df['country_name'].nunique()

print(f"\n✅ Sample size (student records): {num_students:,}")
print(f"🌍 Number of countries in dataset: {num_countries}")
