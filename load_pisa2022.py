import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Define file path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2022/CY08MSP_STU_QQQ.SAV")

# === 2. Load relevant columns: Country + Books at home ===
columns = ["CNT", "ST255Q01JA"]
df = pd.read_spss(data_path, usecols=columns)
df = df.rename(columns={"CNT": "country", "ST255Q01JA": "books_home"})

# === 3. Map book categories and enforce sort order ===
book_map = {
    "There are no books.": "0",
    "1-10 books": "1–10",
    "11-25 books": "11–25",
    "26-100 books": "26–100",
    "101-200 books": "101–200",
    "201-500 books": "201–500",
    "More than 500 books": "500+"
}
category_order = ["0", "1–10", "11–25", "26–100", "101–200", "201–500", "500+"]

df["books_home_label"] = df["books_home"].map(book_map)
df = df[df["books_home_label"].notna()]
df["books_home_label"] = pd.Categorical(df["books_home_label"], categories=category_order, ordered=True)

# === 3a. Sample Size and Country Count Summary ===
num_students = len(df)
num_countries = df["country"].nunique()

print(f"\n✅ Sample size (student records): {num_students:,}")
print(f"🌍 Number of countries in dataset: {num_countries}")


# === 4. Summary: All Countries (corrected sorting)
all_counts = df["books_home_label"].value_counts().reindex(category_order)
all_percent = df["books_home_label"].value_counts(normalize=True).reindex(category_order) * 100
all_df = pd.DataFrame({"Count": all_counts, "Percent": all_percent.round(1)})

print("\n📘 All Countries Book Distribution:")
print(tabulate(all_df, headers="keys", tablefmt="pretty"))

# === 5. Top Countries by Sample Size ===
print("\n📍 Top countries:")
top_countries = df["country"].value_counts().head(20)
print(tabulate(top_countries.reset_index().rename(columns={"index": "country", "country": "count"}), headers="keys", tablefmt="pretty"))

# === 6. UK + US Summary ===
ukus = df[df["country"].isin(["United Kingdom", "United States"])]
print(f"\n✅ UK + US valid samples: {len(ukus):,}")

ukus_counts = ukus["books_home_label"].value_counts().reindex(category_order)
ukus_percent = ukus["books_home_label"].value_counts(normalize=True).reindex(category_order) * 100
ukus_df = pd.DataFrame({"Count": ukus_counts, "Percent": ukus_percent.round(1)})

print("\n📘 UK + US Book Distribution:")
print(tabulate(ukus_df, headers="keys", tablefmt="pretty"))

# === 7. Save cleaned output ===
output_path = os.path.join(BASE_DIR, "../output/pisa2022_books.csv")
df.to_csv(output_path, index=False)
print(f"\n✅ Saved cleaned subset to {output_path}")

# === 8. Bar Chart: Global Distribution of Books at Home (2022) ===
plot_df = all_df.reset_index()
plot_df.columns = ["books_home", "Count", "Percent"]

sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
ax = sns.barplot(x="books_home", y="Percent", data=plot_df)
plt.title(f"PISA 2022 – Global Distribution of Books at Home (n = {df.shape[0]:,})")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home Category")
plt.ylim(0, plot_df["Percent"].max() + 8)  # Headroom for text

# Add n= labels above bars
for i, row in plot_df.iterrows():
    ax.text(i, row["Percent"] + 2.5, f"n={int(row['Count'])}", ha='center')

plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "../output/pisa2022_books_home_chart.png")
plt.savefig(chart_path)
print(f"\n📊 Saved bar chart to: {chart_path}")
plt.show()

# === 9. Save Books Overall Percentages Only ===
books_overall = pd.DataFrame({
    "books_home": category_order,
    "percent": all_percent.round(1)
})
books_overall.to_csv(os.path.join(BASE_DIR, "../output/pisa2022_books_overall.csv"), index=False)
print("✅ Saved books overall percentages to: pisa2022_books_overall.csv")
