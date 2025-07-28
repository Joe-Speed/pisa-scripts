import pandas as pd
import os

# === 1. Load raw fixed-width text file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2012/2012_QU_data.txt")

# Define column specs: CNT (3-char ISO), ST28Q01 (books at home)
colspecs = [(0, 3), (124, 125)]
col_names = ["CNT", "books_raw"]
df = pd.read_fwf(data_path, colspecs=colspecs, names=col_names)

# === 2. Clean country codes and book responses ===
df["CNT"] = df["CNT"].str.strip()
df["books_raw"] = pd.to_numeric(df["books_raw"], errors="coerce")
df = df[df["books_raw"].between(1, 6)]

# === 3. Map books_raw to categories ===
book_map = {
    1: "0–10", 2: "11–25", 3: "26–100",
    4: "101–200", 5: "201–500", 6: "500+"
}
df["books_home"] = df["books_raw"].map(book_map)
df["books_home"] = pd.Categorical(df["books_home"],
    categories=["0–10", "11–25", "26–100", "101–200", "201–500", "500+"],
    ordered=True
)

# === 4. Country label map ===
country_map = {
    "ALB": "Albania", "ARG": "Argentina", "AUS": "Australia", "AUT": "Austria",
    "BEL": "Belgium", "BRA": "Brazil", "BGR": "Bulgaria", "CAN": "Canada",
    "CHL": "Chile", "QCN": "Shanghai-China", "TAP": "Chinese Taipei", "COL": "Colombia",
    "CRI": "Costa Rica", "HRV": "Croatia", "CZE": "Czech Republic", "DNK": "Denmark",
    "EST": "Estonia", "FIN": "Finland", "FRA": "France", "DEU": "Germany",
    "GRC": "Greece", "HKG": "Hong Kong-China", "HUN": "Hungary", "ISL": "Iceland",
    "IDN": "Indonesia", "IRL": "Ireland", "ISR": "Israel", "ITA": "Italy",
    "JPN": "Japan", "JOR": "Jordan", "KAZ": "Kazakhstan", "KOR": "Korea",
    "LVA": "Latvia", "LIE": "Liechtenstein", "LTU": "Lithuania", "LUX": "Luxembourg",
    "MAC": "Macao-China", "MYS": "Malaysia", "MEX": "Mexico", "MNE": "Montenegro",
    "NLD": "Netherlands", "NZL": "New Zealand", "NOR": "Norway", "QRS": "Perm (Russia)",
    "PER": "Peru", "POL": "Poland", "PRT": "Portugal", "QAT": "Qatar",
    "ROU": "Romania", "RUS": "Russian Federation", "SRB": "Serbia", "SGP": "Singapore",
    "SVK": "Slovak Republic", "SVN": "Slovenia", "ESP": "Spain", "SWE": "Sweden",
    "CHE": "Switzerland", "THA": "Thailand", "TUN": "Tunisia", "TUR": "Turkey",
    "GBR": "United Kingdom", "ARE": "United Arab Emirates", "USA": "United States",
    "URY": "Uruguay", "VNM": "Viet Nam", "QUA": "Florida (USA)",
    "QUB": "Connecticut (USA)", "QUC": "Massachusetts (USA)"
}
df["country_name"] = df["CNT"].map(country_map)

# === 4a. Sample Size and Country Count Summary ===
num_students = len(df)
num_countries = df["country_name"].nunique()

print(f"\n✅ Sample size (student records): {num_students:,}")
print(f"🌍 Number of countries in dataset: {num_countries}")


# === 5. Export cleaned dataset ===
output_dir = os.path.join(BASE_DIR, "../output")
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "pisa2012_amountbooks.csv"), index=False)

# === 6. Summary stats ===
print("✅ PISA 2012 data loaded and saved.")
print("\n🔢 Number of observations per country:")
print(df["country_name"].value_counts())

print("\n📚 Book category distribution by country:")
dist = df.groupby("country_name")["books_home"].value_counts(normalize=True).unstack().round(3) * 100
print(dist.fillna(0).sort_index())

print("\n📊 Overall distribution across UK + US only:")
ukus = df[df["CNT"].isin(["GBR", "USA"])]
print(ukus["books_home"].value_counts(sort=False))
print(ukus["books_home"].value_counts(normalize=True, sort=False).round(3) * 100)

print("\n🌍 Overall global distribution (all countries):")
print(df["books_home"].value_counts(sort=False))
print(df["books_home"].value_counts(normalize=True, sort=False).round(3) * 100)

# === Save overall percentages to CSV ===
overall_percent = df["books_home"].value_counts(normalize=True).sort_index() * 100
overall_df = overall_percent.reset_index()
overall_df.columns = ["books_home", "percent"]

overall_df.to_csv(os.path.join(output_dir, "pisa2012_books_overall.csv"), index=False)
print("📁 Saved overall book distribution to: pisa2012_books_overall.csv")


# === 7. Bar Chart: Global Distribution of Books at Home (2012) ===
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare counts and percentages
counts = df["books_home"].value_counts().reindex(overall_df["books_home"])
overall_df["n"] = counts.values

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5.5))  # Slightly taller for spacing
bars = sns.barplot(x="books_home", y="percent", data=overall_df)

# Annotate each bar with n=
for bar, label in zip(bars.patches, overall_df["n"]):
    height = bar.get_height()
    bars.annotate(f"n = {label:,}", xy=(bar.get_x() + bar.get_width() / 2, height + 1),
                  ha='center', va='bottom', fontsize=9)

# Title and axis labels
plt.title("PISA 2012 – Global Distribution of Books at Home")
plt.ylabel("Percent of Students")
plt.xlabel("Books at Home Category")
plt.ylim(0, overall_df["percent"].max() + 8)
plt.tight_layout()

# Add total sample size under the chart
total_n = len(df)
plt.figtext(0.5, -0.05, f"Total valid responses: n = {total_n:,}", ha="center", fontsize=10)

# Save figure
chart_path = os.path.join(output_dir, "pisa2012_books_home_chart.png")
plt.savefig(chart_path, bbox_inches="tight")
print(f"\n📊 Saved bar chart to: {chart_path}")
plt.show()
