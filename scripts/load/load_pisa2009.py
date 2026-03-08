import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(BASE_DIR, "../data/2009/2009_QU_data.txt")
output_path = os.path.join(BASE_DIR, "../output/pisa2009_cleaned.csv")

colspecs = [
    (3, 6),      # COUNTRY
    (114, 115),  # ST22Q01 
    (115, 116),  # ST23Q01 
    (116, 127),  # ST24Q01–Q11 
    (127, 132),  # ST25Q01–Q05
    (408, 416),  # HISEI
    (700, 709),  # WEALTH
]

column_names = [
    "country", "books_raw", "read_time_cat",
    "read_attitudes_raw", "read_types_raw",
    "hisei", "wealth"
]

df = pd.read_fwf(input_path, colspecs=colspecs, names=column_names)

df["country"] = df["country"].astype(str).str.zfill(3)
country_map = {
    "826": "United Kingdom", "840": "United States"
}
df["country_name"] = df["country"].map(country_map)

for col in ["wealth", "hisei"]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")

df["books_raw"] = pd.to_numeric(df["books_raw"], errors="coerce")
df = df[df["books_raw"].between(1, 6)]

book_map = {
    1: "0–10", 2: "11–25", 3: "26–100",
    4: "101–200", 5: "201–500", 6: "500+"
}
df["books_home"] = df["books_raw"].map(book_map)
df["books_home"] = pd.Categorical(
    df["books_home"],
    categories=["0–10", "11–25", "26–100", "101–200", "201–500", "500+"],
    ordered=True
)

df["read_time_cat"] = pd.to_numeric(df["read_time_cat"], errors="coerce")
df["read_time_cat"] = df["read_time_cat"].replace({7: pd.NA, 8: pd.NA, 9: pd.NA})

att_cols = [f"att_q35{chr(97 + i)}" for i in range(11)]  
att_colspecs = [(116 + i, 117 + i) for i in range(11)] 

att_df = pd.read_fwf(input_path, colspecs=att_colspecs, names=att_cols)
att_df = att_df.apply(pd.to_numeric, errors="coerce")

df = pd.concat([df.reset_index(drop=True), att_df.reset_index(drop=True)], axis=1)

types = df["read_types_raw"].astype(str).str.pad(5, fillchar='0')
for i, label in enumerate(["magazines", "comics", "fiction", "nonfiction", "newspapers"]):
    df[f"voluntary_read_{label}"] = pd.to_numeric(types.str[i], errors="coerce")

os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print("Cleaned ALL COUNTRY 2009 data saved to:", output_path)
print(df["books_home"].value_counts(sort=False))
print(df["books_home"].value_counts(normalize=True).round(3) * 100)

ukus = df[df["country"].isin(["826", "840"])].copy()
ukus["books_home"] = pd.Categorical(
    ukus["books_home"],
    categories=["0–10", "11–25", "26–100", "101–200", "201–500", "500+"],
    ordered=True
)

print("\nUK + US book counts:")
print(ukus["books_home"].value_counts(sort=False))

print("\nUK + US book proportions (%):")
print((ukus["books_home"].value_counts(normalize=True, sort=False) * 100).round(1))
