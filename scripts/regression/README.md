# Regression scripts — PISA 2018

Both scripts model the association between a student's reading behaviour and their cognitive /
metacognitive outcomes, using the cleaned 2018 file produced by
[`load_pisa2018.py`](../load/load_pisa2018.py).

**Predictors:** daily leisure-reading time (1–5 ordinal) and books at home.
**Outcomes:** the PISA 2018 metacognition and thinking indices — understanding & remembering
(UNDREM), summarising (METASUM), assessing credibility (METASPAM), cognitive flexibility
(COGFLEX) and perspective taking (PERSPECT).

Model specification (both scripts):

- OLS via `statsmodels` formula API;
- **country fixed effects** (`C(country)`) to absorb between-country differences;
- **standard errors clustered by country**;
- optional **OECD vs non-OECD** split, interaction terms (reading × gender, books × gender,
  reading × books), quadratic reading-time term, and VIF collinearity checks — all toggled by
  the `RUN_*` / `USE_*` / `INTERACT_*` flags near the top of each script;
- a large bank of optional controls (SES, parental education, ICT use, school climate,
  well-being, …) is listed in `control_vars` — individual controls were commented in/out when
  testing robustness, and the list documents everything that was available.

Outputs: full model summaries printed to the console, a compact coefficient table with
significance stars (`* p<0.05, ** p<0.01, *** p<0.001`) saved to
`scripts/output/2018output/regression_results_summary.csv`, and forest plots of each predictor's
coefficient ±95% CI across outcomes.

## The two encodings of "books at home"

| Script | Books encoding | Coefficient reads as |
|---|---|---|
| `2018_reg.py` | ordinal band code 1–6 | change in outcome per one *band* increase |
| `2018_midpointreg.py` | band midpoints (5, 18, 63, 150, 350, 600 books) | change in outcome per **100 books** |

The midpoint version also contains the SES model: books at home regressed on the PISA
socioeconomic index (ESCS), plus a descriptive plot of mean ESCS by books-at-home category —
`2018_reg.py` runs the same SES→books model via the `RUN_SES_BOOKS_*` flags.
