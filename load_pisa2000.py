import pandas as pd
import os

# === 0. Setup paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(BASE_DIR, "../data/2000/2000_QU_data.txt")
output_path = os.path.join(BASE_DIR, "../output/pisa2000_cleaned.csv")


# === 1. Define fixed-width column specs (0-indexed) ===
colspecs = [
    (1, 4),      # COUNTRY
    (164, 165),  # ST34Q01 – reading time
    (165, 174),  # ST35Q01–Q09 – reading attitudes
    (180, 182),  # ST37Q01 – books at home
    (335, 340),  # WEALTH
    (315, 317),  # HISEI

    # Correct cultural/family/education columns from codebook
    (50, 51),    # ST12Q01 – mother's secondary
    (51, 52),    # ST13Q01 – father's secondary
    (52, 53),    # ST14Q01 – mother's tertiary
    (53, 54),    # ST15Q01 – father's tertiary

    (58, 59),    # ST18Q01 – movies
    (59, 60),    # ST18Q02 – art gallery
    (60, 61),    # ST18Q03 – pop music
    (61, 62),    # ST18Q04 – opera
    (62, 63),    # ST18Q05 – theatre

    (64, 65),    # ST19Q01 – discuss politics
    (65, 66),    # ST19Q02 – discuss books
    (66, 67),    # ST19Q03 – listens classics
]

column_names = [
    "country", "read_time_cat", "read_attitudes_raw",
    "books_home", "wealth", "hisei",

    "mother_sec_edu", "father_sec_edu", "mother_ter_edu", "father_ter_edu",

    "cultural_movies", "cultural_art", "cultural_pop", "cultural_opera", "cultural_theatre",

    "discuss_politics", "discuss_books", "listens_classics"
]



# === 2. Load the fixed-width file ===
df = pd.read_fwf(input_path, colspecs=colspecs, names=column_names)
# === 3. Map full country code list ===
df["country"] = pd.to_numeric(df["country"], errors="coerce")

country_map = {
    8: "Albania", 32: "Argentina", 36: "Australia", 40: "Austria", 56: "Belgium",
    76: "Brazil", 100: "Bulgaria", 124: "Canada", 152: "Chile", 203: "Czech Republic",
    208: "Denmark", 246: "Finland", 250: "France", 276: "Germany", 300: "Greece",
    344: "Hong Kong", 348: "Hungary", 352: "Iceland", 360: "Indonesia", 372: "Ireland",
    376: "Israel", 380: "Italy", 392: "Japan", 410: "Korea, Republic of", 428: "Latvia",
    438: "Liechtenstein", 442: "Luxembourg", 484: "Mexico", 528: "Netherlands",
    554: "New Zealand", 578: "Norway", 604: "Peru", 616: "Poland", 620: "Portugal",
    642: "Romania", 643: "Russian Federation", 724: "Spain", 752: "Sweden",
    756: "Switzerland", 764: "Thailand", 807: "Macedonia", 826: "United Kingdom",
    840: "United States"
}

df["country_name"] = df["country"].map(country_map)


# === 4. Clean SES + HISEI values ===
for col in ["wealth", "hisei"]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")

# === 5. Clean reading time category ===
df["read_time_cat"] = pd.to_numeric(df["read_time_cat"], errors="coerce")
df["read_time_cat"] = df["read_time_cat"].replace({7: pd.NA, 8: pd.NA, 9: pd.NA})

# DO NOT map to labels here. Keep it numeric (1–5).
# You will map to labels in the analysis script only.

# === 6. Clean books_home (ST37Q01) and recode missing values ===
df["books_home"] = pd.to_numeric(df["books_home"], errors="coerce")
df["books_home"] = df["books_home"].replace({97: pd.NA, 98: pd.NA, 99: pd.NA})

# === 7. Extract each reading attitude item explicitly (Q35a–Q35i) ===
# ST35Q01–ST35Q09 => positions 165 to 174 (1-indexed)
attitude_colspecs = [(165 + i, 165 + i + 1) for i in range(9)]
attitude_names = [
    "att_q35a_only_if_have_to", "att_q35b_reading_hobby", "att_q35c_talk_books",
    "att_q35d_hard_to_finish", "att_q35e_feel_happy", "att_q35f_waste_of_time",
    "att_q35g_enjoy_library", "att_q35h_read_for_info", "att_q35i_few_minutes_only"
]

att_df = pd.read_fwf(input_path, colspecs=attitude_colspecs, names=attitude_names)

# Convert and clean individual attitude columns
for col in attitude_names:
    att_df[col] = pd.to_numeric(att_df[col], errors="coerce")
    att_df[col] = att_df[col].replace({7: pd.NA, 8: pd.NA, 9: pd.NA})

# Add to main DataFrame
df = pd.concat([df.drop(columns=["read_attitudes_raw"]), att_df], axis=1)

# === 7b. Compute mean reading attitude score ===
df["attitude_mean"] = df[attitude_names].mean(axis=1, skipna=True)



# === 8. Clean cultural and discussion items ===
cultural_discussion_cols = [
    "cultural_movies", "cultural_art", "cultural_pop", "cultural_opera", "cultural_theatre",
    "discuss_politics", "discuss_books", "listens_classics"
]

for col in cultural_discussion_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].replace({7: pd.NA, 8: pd.NA, 9: pd.NA})

# === 9. Clean parental education columns ===
parental_edu_cols = [
    "mother_sec_edu", "father_sec_edu", "mother_ter_edu", "father_ter_edu"
]

for col in parental_edu_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].replace({7: pd.NA, 8: pd.NA, 9: pd.NA})


# === 10. Export cleaned dataset ===
df.to_csv(output_path, index=False)
print("✅ Cleaned UK/US 2000 data saved to:", output_path)
print(df.head())
print("📍 Countries in cleaned data:", df["country_name"].unique())
