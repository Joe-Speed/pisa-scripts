import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/pisa2009_cleaned.csv")
df = pd.read_csv(data_path)

df["country"] = df["country"].astype(str).str.zfill(3)
df["read_time_cat"] = pd.to_numeric(df["read_time_cat"], errors="coerce")

num_students = len(df)
num_countries = df["country"].nunique()

print(f"\nSample size (student records): {num_students:,}")
print(f"Number of countries in dataset (based on 'country' codes): {num_countries}")

ukus_df = df[df["country"].isin(["826", "840"])]

category_order_books = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
df = df[df["books_home"].isin(category_order_books)]
df["books_home_label"] = pd.Categorical(df["books_home"], categories=category_order_books, ordered=True)

print("\nBooks at Home (All Countries):")
print(tabulate(df["books_home_label"].value_counts().reindex(category_order_books).reset_index().rename(columns={"index": "Books", "books_home_label": "Count"}), headers="keys", tablefmt="pretty"))

book_counts = df["books_home_label"].value_counts(normalize=True).reindex(category_order_books) * 100
book_counts = book_counts.round(1)
book_n = df["books_home_label"].value_counts().reindex(category_order_books)
book_df = pd.DataFrame({"books_home": category_order_books, "percent": book_counts.values, "n": book_n.values})

output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
books_csv_path = os.path.join(output_dir, "pisa2009_books_overall.csv")
book_df.to_csv(books_csv_path, index=False)
print(f"\nSaved books at home % breakdown to: {books_csv_path}")

sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
ax = sns.barplot(x="books_home", y="percent", data=book_df)
plt.title(f"PISA 2009 – Global Distribution of Books at Home (n = {df.shape[0]:,})")
plt.ylabel("Percent of Students")
plt.xlabel("No. of Books at Home")
plt.ylim(0, book_df["percent"].max() + 8)

for i, row in book_df.iterrows():
    ax.text(i, row["percent"] + 2.5, f"n={int(row['n'])}", ha='center')

chart_path = os.path.join(output_dir, "pisa2009_books_home_chart.png")
plt.savefig(chart_path)
print(f"Saved books at home chart to: {chart_path}")
plt.show()

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

print("\nReading Time (All Countries):")
print(tabulate(df["read_time_label"].value_counts().reindex(category_order_read).reset_index().rename(columns={"index": "Read Time", "read_time_label": "Count"}), headers="keys", tablefmt="pretty"))

read_counts = df["read_time_label"].value_counts(normalize=True).reindex(category_order_read) * 100
read_counts = read_counts.round(1)
read_n = df["read_time_label"].value_counts().reindex(category_order_read)
read_df = pd.DataFrame({"read_time": category_order_read, "percent": read_counts.values, "n": read_n.values})

plt.figure(figsize=(8, 5))
ax = sns.barplot(x="read_time", y="percent", data=read_df)
plt.title(f"PISA 2009 – Global Distribution of Reading Time (n = {df.shape[0]:,})")
plt.ylabel("Percent of Students")
plt.xlabel("Reading Time")
plt.ylim(0, read_df["percent"].max() + 8)

for i, row in read_df.iterrows():
    ax.text(i, row["percent"] + 2.5, f"n={int(row['n'])}", ha='center')

read_chart_path = os.path.join(output_dir, "pisa2009_reading_time_chart.png")
plt.savefig(read_chart_path)
print(f"Saved reading time chart to: {read_chart_path}")
plt.show()

attitudes_output_dir = os.path.join(BASE_DIR, "../output/attitudes_readtime")
os.makedirs(attitudes_output_dir, exist_ok=True)

read_csv_path = os.path.join(attitudes_output_dir, "pisa2009_reading_time.csv")
read_df.to_csv(read_csv_path, index=False)
print(f"Saved reading time % breakdown to: {read_csv_path}")

attitude_items = {
    "att_q35a": "Q1: I read only if I have to",
    "att_q35b": "Q2: Reading is one of my favorite hobbies",
    "att_q35c": "Q3: I like talking about books with other people",
    "att_q35d": "Q4: I find it hard to finish books",
    "att_q35e": "Q5: I feel happy if I receive a book as a present",
    "att_q35f": "Q6: For me, reading is a waste of time",
    "att_q35g": "Q7: I enjoy going to a bookstore or a library",
    "att_q35h": "Q8: I read only to get information that I need",
    "att_q35i": "Q9: I cannot sit still and read for more than a few minutes",
    "att_q35j": "Q10: I like to express my opinions about books I read",
    "att_q35k": "Q11: I like to exchange books with my friends"
}

for col in attitude_items:
    if col in df.columns:
        df[col + "_clean"] = df[col].where(df[col].isin([1, 2, 3, 4]))


print("\nCleaned Attitude Value Counts (1–4 only):")
cleaned_counts = {}
for col, label in attitude_items.items():
    col_clean = col + "_clean"
    if col_clean in df.columns:
        counts = df[col_clean].value_counts(dropna=False).sort_index()
        cleaned_counts[label] = counts
        print(f"\n{label} value counts:")
        print(counts)


attitudes_df = pd.DataFrame(cleaned_counts).fillna(0).astype(int)
attitudes_df.index.name = "Response"

attitudes_path = os.path.join(attitudes_output_dir, "pisa2009_attitudes_cleaned_labeled.csv")
attitudes_df.to_csv(attitudes_path)

print(f"\nSaved labeled cleaned attitudes to: {attitudes_path}")
