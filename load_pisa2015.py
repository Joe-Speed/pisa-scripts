import pandas as pd
import os
from tabulate import tabulate

# === 1. Load SPSS file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2015/PUF_SPSS_COMBINED_CMB_STU_QQQ/CY6_MS_CMB_STU_QQQ.sav")

columns = ["ST013Q01TA", "CNTRYID"]
df = pd.read_spss(data_path, usecols=columns)
df = df.rename(columns={"ST013Q01TA": "books_home", "CNTRYID": "country"})

# === 2. Clean and map books ===
label_map = {
    "0-10 books": "0–10",
    "11-25 books": "11–25",
    "26-100 books": "26–100",
    "101-200 books": "101–200",
    "201-500 books": "201–500",
    "More than 500 books": "500+"
}
df["books_home_label"] = df["books_home"].map(label_map)
ordered_labels = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df["books_home_label"] = pd.Categorical(df["books_home_label"], categories=ordered_labels, ordered=True)

# Drop missing values
df = df[df["books_home_label"].notna()]
print(f"\n✅ Total valid samples (all countries): {len(df):,}")

# === 2a. Sample Size and Country Coverage ===
num_students = len(df)
num_countries = df["country"].nunique()

print(f"\n✅ Sample size (student records): {num_students:,}")
print(f"🌍 Number of countries in dataset: {num_countries}")

# === 3. Export cleaned version ===
output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "pisa2015_amountbooks.csv"), index=False)

# === 4. All-country distribution ===
all_counts = df["books_home_label"].value_counts(sort=False)
all_percent = (all_counts / all_counts.sum() * 100).round(1)
all_df = pd.DataFrame({"Count": all_counts, "Percent": all_percent})

print("\n📘 Book Distribution (All Countries):")
print(tabulate(all_df, headers="keys", tablefmt="pretty"))
all_df.to_csv(os.path.join(output_dir, "pisa2015_books_overall.csv"))

# === 5. Top reporting countries ===
print("\n📍 Top Countries by Sample Size:")
print(tabulate(df["country"].value_counts().head(20).reset_index().rename(columns={"index": "Country", "country": "N"}), headers="keys", tablefmt="pretty"))

# === 6. UK + US subset ===
ukus = df[df["country"].isin(["United Kingdom", "United States"])]
ukus_counts = ukus["books_home_label"].value_counts(sort=False)
ukus_percent = (ukus_counts / ukus_counts.sum() * 100).round(1)
ukus_df = pd.DataFrame({"Count": ukus_counts, "Percent": ukus_percent})

print(f"\n✅ UK + US valid samples: {ukus_counts.sum():,}")
print("\n📘 Book Distribution (UK + US):")
print(tabulate(ukus_df, headers="keys", tablefmt="pretty"))
ukus_df.to_csv(os.path.join(output_dir, "pisa2015_books_ukus.csv"))

# === 7. Per-Country Breakdown ===
country_summary = (
    df.groupby("country")["books_home_label"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .loc[:, ordered_labels]
    * 100
).round(1)

print("\n📚 Percentage of Students per Book Category by Country:")
print(tabulate(country_summary, headers="keys", tablefmt="pretty"))

country_summary.to_csv(os.path.join(output_dir, "pisa2015_books_by_country.csv"))
print(f"\n📁 Exported to: {output_dir}/pisa2015_books_by_country.csv")

# === 8. Bar Chart: Global Distribution of Books at Home (2015) ===
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare chart data
chart_df = all_df.reset_index()
chart_df.columns = ["books_home", "Count", "percent"]

sns.set(style="whitegrid")
plt.figure(figsize=(8, 5.5))  # Slightly taller for spacing
bars = sns.barplot(x="books_home", y="percent", data=chart_df)

# Annotate bars with n=
for bar, label in zip(bars.patches, chart_df["Count"]):
    height = bar.get_height()
    bars.annotate(f"n = {label:,}", xy=(bar.get_x() + bar.get_width() / 2, height + 1),
                  ha='center', va='bottom', fontsize=9)

# Axis and layout
plt.title("PISA 2015 – Global Distribution of Books at Home")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home Category")
plt.ylim(0, chart_df["percent"].max() + 8)
plt.tight_layout()

# Add total sample size
total_n = len(df)
plt.figtext(0.5, -0.05, f"Total valid responses: n = {total_n:,}", ha="center", fontsize=10)

# Save chart
chart_path = os.path.join(output_dir, "pisa2015_books_home_chart.png")
plt.savefig(chart_path, bbox_inches="tight")
print(f"\n📊 Saved bar chart to: {chart_path}")
plt.show()
