# PISA Analysis Scripts (2000–2022)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Data: OECD PISA](https://img.shields.io/badge/Data-OECD%20PISA-lightgrey.svg)](https://www.oecd.org/en/about/programmes/pisa/pisa-data.html)

Python scripts used in the analysis for an MSc dissertation (University of Glasgow) exploring
**adolescent reading behaviour** through a range of lenses — Economics, Psychology, Neuroscience
and Philosophy.

The scripts process the **student questionnaire** microdata from every PISA wave between 2000 and
2022 to answer three broad questions:

1. **How has reading behaviour changed over two decades?** — daily leisure-reading time, attitudes
   towards reading, and the number of books in the home, tracked across waves.
2. **How does the print environment relate to socioeconomic status?** — the association between a
   student's socioeconomic index (ESCS) and books at home.
3. **Is reading associated with how students think?** — regressions of metacognitive skills
   (understanding, summarising, assessing credibility), cognitive flexibility and perspective
   taking on reading time and books at home, controlling for country and (optionally) a large
   bank of student/home/school covariates.

The dissertation produced with these scripts is available to read at
**[joe-speed.com/dissertation.pdf](https://www.joe-speed.com/dissertation.pdf)** — see
[The dissertation](#the-dissertation) for copyright conditions.

> **Note on data:** the raw PISA microdata is **not included** in this repository (files run to
> several GB). Everything is freely downloadable from the
> [OECD PISA database](https://www.oecd.org/en/about/programmes/pisa/pisa-data.html) — see
> [Getting the data](#getting-the-data) below.

---

## Repository structure

```
pisa-scripts/
├── scripts/
│   ├── load/         # one script per PISA wave: read raw data → cleaned CSV + basic tables
│   ├── analysis/     # descriptive statistics, single-wave breakdowns, cross-wave trend charts
│   └── regression/   # OLS models: reading behaviour → metacognitive outcomes (PISA 2018)
├── requirements.txt
├── LICENSE
└── README.md
```

Each folder has its own README describing every script in detail:

- [`scripts/load/`](scripts/load/) — data cleaning, one script per wave (2000–2022)
- [`scripts/analysis/`](scripts/analysis/) — descriptives and 2000→2018/2022 trend plots
- [`scripts/regression/`](scripts/regression/) — regression models on the 2018 wave

## Pipeline at a glance

```
OECD raw data (.txt fixed-width / .sav SPSS)
        │
        ▼
scripts/load/load_pisaYYYY.py      → scripts/output/pisaYYYY_cleaned.csv (+ summary tables)
        │
        ▼
scripts/analysis/analyse_pisaYYYY.py → per-wave tables & bar charts (books, reading time, attitudes)
scripts/analysis/*_trend.py          → cross-wave trend line charts (2000–2018 / 2003–2022)
        │
        ▼
scripts/regression/2018_reg.py       → OLS coefficient tables & forest plots
scripts/regression/2018_midpointreg.py
```

All paths inside the scripts are **relative to the script's own location**, so they can be run
from anywhere:

```bash
python scripts/load/load_pisa2018.py
```

Outputs (cleaned CSVs, summary tables, PNG charts) are written to `scripts/output/`, which is
git-ignored along with the raw data.

## What the scripts measure

| Construct | PISA variable(s) | Waves used |
|---|---|---|
| Books in the home (6 ordinal bands, `0–10` … `500+`) | ST37 (2000), ST13/ST013 (2003–2018), ST255 (2022) | 2000–2022 |
| Daily leisure-reading time (5 bands, `None` … `>2 hrs`) | ST34 (2000), ST23 (2009), ST175 (2018) | 2000, 2009, 2018 |
| Attitudes to reading (agree/disagree items, e.g. *"Reading is one of my favourite hobbies"*) | ST35 (2000), ST24 (2009), ST160 (2018) | 2000, 2009, 2018 |
| Metacognition: understanding & remembering, summarising, assessing credibility | UNDREM, METASUM, METASPAM | 2018 |
| Cognitive flexibility / perspective taking | COGFLEX, PERSPECT | 2018 |
| Socioeconomic status | ESCS index, WEALTH, HISEI | 2000–2018 |

Only five attitude items are worded identically in 2000, 2009 and 2018 — the trend analysis is
restricted to those five so responses are comparable across waves.

Throughout, PISA's special missing-value codes (e.g. `7/8/9`, `97/98/99`, and the negative and
`999999x` codes in later waves) are recoded to missing before any statistics are computed.

## Getting the data

1. Go to the [OECD PISA data page](https://www.oecd.org/en/about/programmes/pisa/pisa-data.html)
   and download the **student questionnaire** data file for each wave you need.
   - **2000–2012** are distributed as fixed-width text files (with SPSS/SAS control files).
   - **2015–2022** are distributed as SPSS (`.sav`) files.
2. Place the files under `scripts/data/<year>/` so the relative paths in the load scripts resolve:

```
scripts/data/
├── 2000/2000_QU_data.txt
├── 2003/2003_QU_data.txt
├── 2006/2006_QU_data.txt
├── 2009/2009_QU_data.txt
├── 2012/2012_QU_data.txt
├── 2015/PUF_SPSS_COMBINED_CMB_STU_QQQ/CY6_MS_CMB_STU_QQQ.sav
├── 2018/CY07_MSU_STU_QQQ.sav
└── 2022/CY08MSP_STU_QQQ.SAV
```

(The `.txt` files are the raw student-questionnaire text files, renamed to `<year>_QU_data.txt`.)

The column positions used for the fixed-width waves were taken from the official OECD codebooks
for each cycle, which are also available on the PISA data page.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.10+. `pyreadstat` is needed for the `.sav` waves (2015, 2018, 2022).

## Methodological notes

- **Regressions** ([scripts/regression/](scripts/regression/)) are OLS via `statsmodels`, with:
  - **country fixed effects** (`C(country)`) to absorb between-country differences;
  - **standard errors clustered by country**;
  - optional **OECD vs non-OECD** sample splits;
  - optional interaction terms, quadratic reading-time term, and VIF collinearity checks
    (all switchable via the flags at the top of each script).
- `2018_reg.py` treats books at home as an **ordinal 1–6 code**; `2018_midpointreg.py` re-encodes
  each band to its **midpoint count** (5, 18, 63, 150, 350, 600) so coefficients can be read as
  the association *per 100 books*.
- Trend charts report the **percentage distribution of responses per wave** with per-wave sample
  sizes (n) printed on the axis, not regression estimates.
- Analyses are **descriptive/associational**: no causal claims are made, and PISA sampling
  weights are not applied — figures describe the pooled student sample, not population-weighted
  country estimates.

## The dissertation

The full thesis produced with these scripts can be read at
[joe-speed.com/dissertation.pdf](https://www.joe-speed.com/dissertation.pdf).

> © Joe Speed, 2026. This dissertation was submitted in fulfilment of the requirements for an
> MSc degree at the University of Glasgow. In line with University of Glasgow
> [policy on theses](https://www.gla.ac.uk/myglasgow/research/enlighten/theses/), copyright and
> moral rights for the dissertation are retained by the author. It is made available for
> personal, non-commercial research and study; it may be quoted with full acknowledgement, but
> may not be reproduced or published without the author's prior written consent.

The MIT license below applies to the **code in this repository only**, not to the dissertation
text or the PISA data.

## License

Released under the [MIT License](LICENSE). The PISA data itself is © OECD and subject to the
OECD's [terms and conditions](https://www.oecd.org/en/about/terms-conditions.html).

## Citation

If you use these scripts, please cite this repository (see [`CITATION.cff`](CITATION.cff)) and
credit the OECD as the source of the underlying data:

> OECD, *Programme for International Student Assessment (PISA)*, waves 2000–2022,
> https://www.oecd.org/en/about/programmes/pisa/pisa-data.html
