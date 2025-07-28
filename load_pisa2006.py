import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Load fixed-width raw file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2006/2006_QU_data.txt")

# Fixed-width columns: COUNTRY (18–21), ST15Q01 (89–90)
colspecs = [(18, 21), (89, 90)]
col_names = ["country", "books_raw"]
df = pd.read_fwf(data_path, colspecs=colspecs, names=col_names)

# === 2. Clean and map countries ===
df["country"] = df["country"].astype(str).str.strip()

country_map = {
    "031": "Azerbaijan", "032": "Argentina", "036": "Australia", "040": "Austria",
    "056": "Belgium", "076": "Brazil", "100": "Bulgaria", "124": "Canada",
    "152": "Chile", "158": "Chinese Taipei", "170": "Colombia", "191": "Croatia",
    "203": "Czech Republic", "208": "Denmark", "233": "Estonia", "246": "Finland",
    "250": "France", "276": "Germany", "300": "Greece", "344": "Hong Kong-China",
    "348": "Hungary", "352": "Iceland", "360": "Indonesia", "372": "Ireland",
    "376": "Israel", "380": "Italy", "392": "Japan", "400": "Jordan", "410": "Korea",
    "417": "Kyrgyzstan", "428": "Latvia", "438": "Liechtenstein", "440": "Lithuania",
    "442": "Luxembourg", "446": "Macao-China", "484": "Mexico", "499": "Montenegro",
    "528": "Netherlands", "554": "New Zealand", "578": "Norway", "616": "Poland",
    "620": "Portugal", "634": "Qatar", "642": "Romania", "643": "Russian Federation",
    "688": "Serbia", "703": "Slovak Republic", "705": "Slovenia", "724": "Spain",
    "752": "Sweden", "756": "Switzerland", "764": "Thailand", "788": "Tunisia",
    "792": "Turkey", "826": "United Kingdom", "840": "United States", "858": "Uruguay"
}
df["country_name"] = df["country"].map(country_map)

# === 3. Clean books and map to categories ===
df["books_raw"] = pd.to_numeric(df["books_raw"], errors="coerce")
df = df[df["books_raw"].between(1, 6)]

book_map = {
    1: "0–10", 2: "11–25", 3: "26–100", 4: "101–200", 5: "201–500", 6: "500+"
}
ordered_labels = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df["books_home"] = df["books_raw"].map(book_map)
df["books_home"] = pd.Categorical(df["books_home"], categories=ordered_labels, ordered=True)

# === 4. Export cleaned file ===
output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "pisa2006_amountbooks.csv"), index=False)

# === 5. Overall Book Distribution (as percent) ===
overall_counts = df["books_home"].value_counts(sort=False)
overall_percent = (overall_counts / len(df) * 100).round(1)
overall_df = pd.DataFrame({
    "books_home": ordered_labels,
    "percent": overall_percent.reindex(ordered_labels).values
})
overall_df.to_csv(os.path.join(output_dir, "pisa2006_books_overall.csv"), index=False)

print("\n📊 Overall Book Distribution (% All Countries):")
print(tabulate(overall_df.set_index("books_home"), headers="keys", tablefmt="pretty"))

# === 6. Per-Country Breakdown ===
summary = (
    df.groupby("country_name")["books_home"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .loc[:, ordered_labels]
    * 100
).round(1)

print("\n🌍 Unique countries in dataset:", df['country_name'].nunique())
print("🧮 Total valid student entries:", len(df))

print("\n📚 Percentage of Students per Book Category by Country:")
print(tabulate(summary, headers="keys", tablefmt="pretty"))

summary.to_csv(os.path.join(output_dir, "pisa2006_books_by_country.csv"))

# === 7. Bar Chart: Global Distribution of Books at Home (2006) ===
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5.5))

# Bar chart
bars = sns.barplot(x="books_home", y="percent", data=overall_df)

# Add labels above bars
for bar, count in zip(bars.patches, overall_counts.reindex(ordered_labels)):
    height = bar.get_height()
    bars.annotate(f"n = {int(count):,}", xy=(bar.get_x() + bar.get_width() / 2, height + 1),
                  ha='center', va='bottom', fontsize=9)

# Titles and axis
plt.title("PISA 2006 – Global Distribution of Books at Home")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home Category")
plt.ylim(0, overall_df["percent"].max() + 8)

# Add total sample size BELOW chart
total_n = len(df)
plt.figtext(0.5, 0.01, f"Total valid responses: n = {total_n:,}", ha="center", fontsize=10)

# Adjust layout *after* figtext
plt.subplots_adjust(bottom=0.15)

# Save figure
chart_path = os.path.join(output_dir, "pisa2006_books_home_chart.png")
plt.savefig(chart_path, bbox_inches="tight")
plt.show()
print(f"\n📊 Saved bar chart to: {chart_path}")

# === 4a. Sample Size and Country Coverage Summary ===
num_students = len(df)
num_countries = df["country_name"].nunique()

print(f"\n✅ Sample size (student records): {num_students:,}")
print(f"🌍 Number of countries in dataset: {num_countries}")
