# Analysis scripts — descriptives and cross-wave trends

These scripts run on the cleaned CSVs produced by [`scripts/load/`](../load/) and produce the
descriptive tables and figures used in the dissertation. All tables are printed to the console
(via `tabulate`) and saved as CSV; all charts are saved as PNG under `scripts/output/`.

## Single-wave descriptives

| Script | Wave | What it produces |
|---|---|---|
| `analyse_pisa2000.py` | 2000 | Books-at-home and reading-time distributions (all countries and UK+US subset), bar charts, and response counts for all 9 reading-attitude items |
| `analyse_pisa2009.py` | 2009 | Books-at-home and reading-time distributions with bar charts, cleaned response counts for the 11 reading-attitude items |
| `analyse_pisa2018.py` | 2018 | Books-at-home, reading-time and book-format (paper vs digital) distributions; each also split **OECD vs non-OECD**; attitude-item response counts |

All distributions are reported as the percentage of valid student responses, with sample sizes
(n) shown on the charts.

## Cross-wave trends

| Script | Waves | What it measures |
|---|---|---|
| `books_trend.py` | 2003–2022 (7 waves) | Change in the global distribution of books at home. Harmonises the slightly different band labels across waves into six categories (`0–10` … `500+`) and plots one line per category |
| `read_time_trend.py` | 2000, 2009, 2018 | Change in daily leisure-reading time, harmonised into five bands (`None` … `>2 hrs`), one line per band |
| `att_trend.py` | 2000, 2009, 2018 | Change in agreement with the five reading-attitude statements asked identically in all three reading-focus waves (e.g. *"Reading is one of my favourite hobbies"*, *"For me, reading is a waste of time"*). One chart per statement, one line per response category (Strongly disagree … Strongly agree) |

The trend scripts read the per-wave summary CSVs written by the load/analysis scripts, so run
those first for every wave you want on the chart.
