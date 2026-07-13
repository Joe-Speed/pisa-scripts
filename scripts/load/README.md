# Load scripts — one per PISA wave

Each script reads the raw OECD student-questionnaire file for its wave, extracts the variables
used in the dissertation, recodes PISA's special missing-value codes to missing, attaches
readable labels, and writes cleaned output to `scripts/output/`.

Raw data is expected under `scripts/data/<year>/` — see the
[root README](../../README.md#getting-the-data) for filenames and download instructions.

| Script | Input format | Variables extracted | Main output |
|---|---|---|---|
| `load_pisa2000.py` | fixed-width `.txt` | reading time (ST34), 9 attitude items (ST35a–i), books at home (ST37), WEALTH, HISEI, parental education, cultural activities | `pisa2000_cleaned.csv` |
| `load_pisa2003.py` | fixed-width `.txt` | books at home | books-at-home table + bar chart |
| `load_pisa2006.py` | fixed-width `.txt` | books at home | books-at-home table + bar chart |
| `load_pisa2009.py` | fixed-width `.txt` | books at home, reading time (ST23), 11 attitude items (ST24), reading types (ST25), WEALTH, HISEI | `pisa2009_cleaned.csv` |
| `load_pisa2012.py` | fixed-width `.txt` | books at home | books-at-home table + bar chart |
| `load_pisa2015.py` | SPSS `.sav` | books at home (ST013) | `pisa2015_amountbooks.csv` + bar chart |
| `load_pisa2018.py` | SPSS `.sav` | ~130 variables: books at home, reading time, attitudes, reading preferences/format, metacognition indices, SES (ESCS, WEALTH, HISEI), parental education, ICT use, school climate, well-being, global-competence indices, and more | `2018output/newpisa2018_cleaned_all_countries.csv` |
| `load_pisa2022.py` | SPSS `.sav` | books at home (ST255) | `pisa2022_books_overall.csv` + bar chart |

Notes:

- The 2003, 2006, 2012, 2015 and 2022 waves are only used for the **books-at-home trend**
  (the reading-time and attitude questions were asked in the reading-focus waves: 2000, 2009,
  2018), so their load scripts extract just the books variable and also produce the wave's
  descriptive table/chart directly.
- Column positions for the fixed-width waves come from the official OECD codebooks.
- 2018 is the analysis wave for the regressions, hence the much larger variable set: every raw
  PISA variable name is renamed to a self-documenting label (e.g. `ST160Q02IA` →
  `att_2_reading_hobby`) — the rename map inside `load_pisa2018.py` doubles as the codebook.
