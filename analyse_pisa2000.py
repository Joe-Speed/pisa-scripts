import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Load Cleaned Dataset ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/pisa2000_cleaned.csv")
df = pd.read_csv(data_path)

# === 2. Minimal Cleaning ===
df["books_home"] = pd.to_numeric(df["books_home"], errors="coerce")
df["read_time_cat"] = pd.to_numeric(df["read_time_cat"], errors="coerce")

# === 3. Country Subset for UK + US ===
ukus_df = df[df["country_name"].isin(["United Kingdom", "United States"])]

# === 4. BOOKS AT HOME: Mapping + Summary ===
book_map = {
    1: "0",
    2: "1–10",
    3: "11–25",
    4: "26–100",
    5: "101–200",
    6: "201–500",
    7: "500+"
}
category_order_books = ["0", "1–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df["books_home_label"] = df["books_home"].map(book_map)
df = df[df["books_home_label"].notna()]
df["books_home_label"] = pd.Categorical(df["books_home_label"], categories=category_order_books, ordered=True)

print("\n📚 Books at Home (All Countries):")
print(tabulate(df["books_home_label"].value_counts().reindex(category_order_books).reset_index().rename(columns={"index": "Books", "books_home_label": "Count"}), headers="keys", tablefmt="pretty"))

print("\n📚 Books at Home (UK + US):")
print(tabulate(ukus_df["books_home"].map(book_map).value_counts().reindex(category_order_books).reset_index().rename(columns={"index": "Books", "books_home": "Count"}), headers="keys", tablefmt="pretty"))

# === 4b. Save Books at Home % Breakdown ===
book_counts = df["books_home_label"].value_counts(normalize=True).reindex(category_order_books) * 100
book_counts = book_counts.round(1)
book_n = df["books_home_label"].value_counts().reindex(category_order_books)
book_df = pd.DataFrame({"books_home": category_order_books, "percent": book_counts.values, "n": book_n.values})

# Save CSV
output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
books_csv_path = os.path.join(output_dir, "pisa2000_books_overall.csv")
book_df.to_csv(books_csv_path, index=False)
print(f"\n✅ Saved books at home % breakdown to: {books_csv_path}")

# === 4c. Bar Chart – Books at Home ===
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
ax = sns.barplot(x="books_home", y="percent", data=book_df)
plt.title(f"PISA 2000 – Global Distribution of Books at Home (n = {df.shape[0]:,})")
plt.ylabel("Percent of Students")
plt.xlabel("No. of Books at Home")
plt.ylim(0, book_df["percent"].max() + 8)  # Add headroom for n labels

for i, row in book_df.iterrows():
    ax.text(i, row["percent"] + 2.5, f"n={int(row['n'])}", ha='center')

chart_path = os.path.join(output_dir, "pisa2000_books_home_chart.png")
plt.savefig(chart_path)
print(f"📊 Saved books at home chart to: {chart_path}")
plt.show()

# === 5. READING TIME: Correct Mapping + Chart ===
read_map = {
    1: "Don't read",
    2: "<30 min",
    3: "31–60 min",
    4: "1–2 hrs",
    5: "2+ hrs"
}
category_order_read = ["Don't read", "<30 min", "31–60 min", "1–2 hrs", "2+ hrs"]
df["read_time_label"] = df["read_time_cat"].map(read_map)
df = df[df["read_time_label"].notna()]
df["read_time_label"] = pd.Categorical(df["read_time_label"], categories=category_order_read, ordered=True)

print("\n📖 Reading Time (All Countries):")
print(tabulate(df["read_time_label"].value_counts().reindex(category_order_read).reset_index().rename(columns={"index": "Read Time", "read_time_label": "Count"}), headers="keys", tablefmt="pretty"))

print("\n📖 Reading Time (UK + US):")
print(tabulate(ukus_df["read_time_cat"].map(read_map).value_counts().reindex(category_order_read).reset_index().rename(columns={"index": "Read Time", "read_time_cat": "Count"}), headers="keys", tablefmt="pretty"))

# === 5b. Bar Chart – Reading Time ===
read_counts = df["read_time_label"].value_counts(normalize=True).reindex(category_order_read) * 100
read_counts = read_counts.round(1)
read_n = df["read_time_label"].value_counts().reindex(category_order_read)
read_df = pd.DataFrame({"read_time": category_order_read, "percent": read_counts.values, "n": read_n.values})

plt.figure(figsize=(8, 5))
ax = sns.barplot(x="read_time", y="percent", data=read_df)
plt.title(f"PISA 2000 – Global Distribution of Reading Time (n = {df.shape[0]:,})")
plt.ylabel("Percent of Students")
plt.xlabel("Reading Time")
plt.ylim(0, read_df["percent"].max() + 8)

for i, row in read_df.iterrows():
    ax.text(i, row["percent"] + 2.5, f"n={int(row['n'])}", ha='center')

chart_path = os.path.join(output_dir, "pisa2000_reading_time_chart.png")
plt.savefig(chart_path)
print(f"📊 Saved reading time chart to: {chart_path}")
plt.show()

# === 5c. Save Reading Time Breakdown ===
attitudes_output_dir = os.path.join(BASE_DIR, "../output/attitudes_readtime")
os.makedirs(attitudes_output_dir, exist_ok=True)

read_csv_path = os.path.join(attitudes_output_dir, "pisa2000_reading_time.csv")
read_df.to_csv(read_csv_path, index=False)
print(f"✅ Saved reading time % breakdown to: {read_csv_path}")


# === 6. Reading Attitude Item Distributions ===
attitude_items = [
    "att_q35a_only_if_have_to", "att_q35b_reading_hobby", "att_q35c_talk_books",
    "att_q35d_hard_to_finish", "att_q35e_feel_happy", "att_q35f_waste_of_time",
    "att_q35g_enjoy_library", "att_q35h_read_for_info", "att_q35i_few_minutes_only"
]

print("\n🧠 Reading Attitude Responses (All Countries):")
for item in attitude_items:
    if item in df.columns:
        print(f"\n{item} response counts:")
        print(tabulate(df[item].value_counts(dropna=False).sort_index().reset_index().rename(columns={"index": "Response", item: "Count"}), headers="keys", tablefmt="pretty"))

# === 6b. Save Reading Attitudes ===
attitudes_data = {}

for item in attitude_items:
    if item in df.columns:
        counts = df[item].value_counts(dropna=False).sort_index()
        attitudes_data[item] = counts

# Combine into a DataFrame (long format)
attitudes_df = pd.DataFrame(attitudes_data).fillna(0).astype(int)
attitudes_df.index.name = "Response"

attitudes_path = os.path.join(attitudes_output_dir, "pisa2000_attitudes.csv")
attitudes_df.to_csv(attitudes_path)
print(f"✅ Saved reading attitude response table to: {attitudes_path}")

# === Quick Check: Sample Size and Countries ===
print(f"\n✅ Sample size (student records): {df.shape[0]:,}")

# Try detecting the country column
possible_country_cols = ["country", "CNT", "cnt", "country_name"]
found_country_col = None

for col in possible_country_cols:
    if col in df.columns:
        found_country_col = col
        break

if found_country_col:
    num_countries = df[found_country_col].nunique()
    print(f"🌍 Number of countries in dataset (using '{found_country_col}'): {num_countries}")
else:
    print("⚠️ Could not detect a country column automatically. Columns available:")
    print(df.columns.tolist())
