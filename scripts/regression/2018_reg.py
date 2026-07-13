import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from tabulate import tabulate
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/2018output/newpisa2018_cleaned_all_countries.csv")
df = pd.read_csv(data_path)

df = df.rename(columns={"read_time": "read_time_numeric"})

base_vars = ["read_time_numeric", "books_home", "country"]

control_vars = [
    
    #"age",
    
    #"gender",

    #"coop_value_cooperation","coop_students_cooperate","coop_coop_important", "coop_encouraged",
    
    #"learn_interconnected_economies", "learn_conflict_resolution", "learn_about_cultures", "learn_current_news", "learn_opinion_on_news", "learn_celebrate_diversity", "learn_world_event_discussion", "learn_global_issues_groupwork", "learn_different_perspectives", "learn_crosscultural_communication",
    
    #"lang_student", "lang_mother", "lang_father",

    #"contact_family", "contact_school", "contact_neighbourhood", "contact_friends",

    #"diglit_keywords_search","diglit_trust_info", "diglit_compare_pages", "diglit_privacy_awareness", "diglit_search_snippet", "diglit_subjectivity_bias", "diglit_detect_phishing",

    #"att_1_read_only_if_have_to","att_2_reading_hobby","att_3_talk_books","att_4_reading_waste","att_5_read_for_info",

    #"pref_magazines", "pref_comics", "pref_fiction", "pref_nonfiction", "pref_newspapers", "book_reading_format",

    #"school_text_diagrams_maps", "school_text_fiction", "school_text_tables_graphs", "school_text_digital_links",

    #"mother_edu", "father_edu", "highest_parent_edu", "student_edu_level", "parent_edu_years",

    #"teacher_interest", "teacher_support_language","teacher_directed_instruction", "teacher_reading_stimulation",

    #"family_wealth_index","socioeconomic_index", "parent_occ_status", "home_possessions",  "home_edu_resources", "cultural_possessions",
   
    #"immigration_status",

    #"learning_time_mins",

    #"ecec_duration",
     
    #"ict_home", "ict_school", "ict_use_leisure", "ict_use_schoolwork_outside_school", "ict_use_in_school", "ict_interest",

    #"reading_self_concept_competence", "reading_self_concept_difficulty",

    #"perceived_cooperation_school",

    #"subjective_wellbeing_positive_affect",

    #"school_discrimination_climate",

    #"school_belonging",

    #"being_bullied",

    #"effort_actual", "effort_ideal",

    #"bullied_irritates_me","bullied_help_good","bullied_wrong_join", "bullied_feel_bad", "bullied_like_defender",

    #"imm_edu_rights","imm_voting_rights","imm_customs","imm_equal_rights",

    #"fixed_mindset",

    # "metacog_understanding", "metacog_summarising", "metacog_credibility",

    #"global_mindedness","global_self_efficacy","global_awareness",

    #"resilience",

    #"mastery_goal_orientation",

    #"attitude_immigrants",

    #"interest_other_cultures",

    #"perspective_taking",

    #"cognitive_flexibility",

    #"respect_other_cultures",

    #"intercultural_awareness",

    #"attitude_learning_activities",

    #"work_mastery",

    #"general_fear_of_failure",

    #"eudaemonia_meaning_in_life",
]

for col in ["read_time_numeric", "books_home"] + control_vars:
    df[col] = pd.to_numeric(df[col], errors="coerce")

effort_vars = [
    "effort_actual", "effort_ideal"
]

goal_vars = [
    "mastery_goal_orientation", "work_mastery"
]

bully_vars = [
    "bullied_irritates_me", "bullied_help_good",
    "bullied_wrong_join", "bullied_feel_bad", "bullied_like_defender"
]

immigration_vars = [
    "imm_edu_rights", "imm_voting_rights",
    "imm_customs", "imm_equal_rights",
    "attitude_immigrants"
]

mindset_vars = ["fixed_mindset"]

metacog_vars = [
    "metacog_understanding", "metacog_summarising", "metacog_credibility", "cognitive_flexibility", "perspective_taking", 
]

citizenship_vars = [
    "global_mindedness", "global_self_efficacy", "global_awareness"
]

intercultural_vars = [
    "interest_other_cultures",
    "respect_other_cultures",
    "intercultural_awareness"
]

empathy_vars = [
    "perspective_taking", "global_mindedness",
]

cognitiveflex_vars = [
    "cognitive_flexibility", 
]

resilience_vars = [
    "resilience",
]
fearfailure_vars = [
    "general_fear_of_failure"
]

meaning_vars = [
    "eudaemonia_meaning_in_life"
]

learning_vars = [
    "attitude_learning_activities"
]

def significance_stars(pval):
    if pval < 0.001:
        return '***'   
    elif pval < 0.01:
        return '**'    
    elif pval < 0.05:
        return '*'   
    else:
        return ''

oecd_codes = [
    "AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU",
    "DNK", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "ISL", "IRL", "ISR",
    "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR", "NZL",
    "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "TUR", "USA"
]

df["is_OECD"] = df["country"].isin(oecd_codes)

RUN_GENERAL_REGRESSION = False
SPLIT_BY_OECD = False

USE_CLUSTER_SES = True
USE_COUNTRY_FE = True
CHECK_NONLINEAR = False
CHECK_VIF = False

INTERACT_READTIME_GENDER = False
INTERACT_BOOKS_GENDER = False
INTERACT_READTIME_BOOKS = False

base_vars = ["read_time_numeric", "books_home"]
if CHECK_NONLINEAR:
    df["read_time_sq"] = df["read_time_numeric"] ** 2
    if "read_time_sq" not in base_vars:
        base_vars.insert(base_vars.index("read_time_numeric") + 1, "read_time_sq")

interaction_terms = []
if INTERACT_READTIME_GENDER:
    interaction_terms.append("read_time_numeric * gender")
    base_vars = [v for v in base_vars if v not in ["read_time_numeric", "gender"]]
if INTERACT_BOOKS_GENDER:
    interaction_terms.append("books_home * gender")
    base_vars = [v for v in base_vars if v not in ["books_home", "gender"]]
if INTERACT_READTIME_BOOKS:
    interaction_terms.append("read_time_numeric * books_home")
    base_vars = [v for v in base_vars if v not in ["read_time_numeric", "books_home"]]

if RUN_GENERAL_REGRESSION:
    subsets = [("All Countries", df)] if not SPLIT_BY_OECD else [
        ("OECD", df[df["is_OECD"] == True]),
        ("non-OECD", df[df["is_OECD"] == False])
    ]

    results = []

    for subset_label, subset_df in subsets:
        print(f"\n=== Running regressions for: {subset_label} ===")

        for outcome in metacog_vars:
            print(f"\n=== Regression for: {outcome} ===")

            predictors = base_vars + control_vars
            formula_terms = predictors + interaction_terms
            formula = f"{outcome} ~ {' + '.join(formula_terms)}"
            model_vars = [outcome] + predictors
            if USE_COUNTRY_FE:
                formula += " + C(country)"
                model_vars += ["country"]

            if INTERACT_READTIME_GENDER:
                model_vars += ["read_time_numeric", "gender"]
            if INTERACT_BOOKS_GENDER:
                model_vars += ["books_home", "gender"]
            if INTERACT_READTIME_BOOKS:
                model_vars += ["read_time_numeric", "books_home"]

            df_model = subset_df[model_vars].copy().dropna()
            print(f"📊 Sample size: {len(df_model)}")

            if df_model["read_time_numeric"].nunique() < 2:
                print(f"⚠️ Skipping {outcome}: not enough variation")
                continue

            model = smf.ols(formula=formula, data=df_model)
            results_model = model.fit(
                cov_type="cluster", cov_kwds={"groups": df_model["country"]}
            ) if USE_CLUSTER_SES else model.fit()

            print(results_model.summary())

            for pred in ["read_time_numeric", "books_home"]:
                if pred in results_model.params:
                    pval = results_model.pvalues[pred]
                    results.append({
                        "subset": subset_label,
                        "outcome": outcome,
                        "predictor": pred,
                        "coef": results_model.params[pred],
                        "se": results_model.bse[pred],
                        "stars": significance_stars(pval)
                    })

            if CHECK_VIF:
                from statsmodels.stats.outliers_influence import variance_inflation_factor
                from patsy import dmatrix
                print("\n Checking VIFs...")
                rhs = formula.split('~')[1].strip()
                X_vif = dmatrix(rhs, data=df_model, return_type='dataframe')
                vif_df = pd.DataFrame({
                    'Variable': X_vif.columns,
                    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
                })
                print(tabulate(vif_df, headers='keys', tablefmt='github', floatfmt=".2f"))

    results_df = pd.DataFrame(results)

    predictor_labels = {
        "read_time_numeric": "Time Spent Reading per Day",
        "books_home": "Number of Books at Home"
    }

    for pred in ["read_time_numeric", "books_home"]:
        subset = results_df[results_df["predictor"] == pred]
        if subset.empty:
            continue

        plt.figure(figsize=(10, 6))

        if SPLIT_BY_OECD:
            color_map = {"OECD": "#465759", "non-OECD": "#B77D8F"}
            for group in subset["subset"].unique():
                group_data = subset[subset["subset"] == group]
                plt.errorbar(
                    group_data["coef"], group_data["outcome"],
                    xerr=1.96 * group_data["se"],
                    fmt='o', capsize=4, label=group,
                    color=color_map.get(group, "#999999")
                )
            title_suffix = "by OECD Status"
        else:
            group_data = subset
            plt.errorbar(
                group_data["coef"], group_data["outcome"],
                xerr=1.96 * group_data["se"],
                fmt='o', capsize=4, label="All Countries",
                color="#003366"
            )
            title_suffix = "(All Countries)"

        plt.axvline(0, linestyle='--', color='gray')
        plt.title(f"Association between {predictor_labels[pred]} and Outcome {title_suffix}")
        plt.xlabel("Coefficient (±95% CI)")
        plt.ylabel("Outcomes")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    results_df["coef_str"] = results_df.apply(lambda row: f"{row['coef']:.3f}{row['stars']}", axis=1)
    print("\n=== Summary Table of Predictors ===")
    print(tabulate(results_df[["subset", "outcome", "predictor", "coef_str", "se"]],
                   headers='keys', tablefmt='github', floatfmt=".3f"))

    output_path = os.path.join(BASE_DIR, "../output/2018output/regression_results_summary.csv")
    results_df.to_csv(output_path, index=False)

else:
    results_df = pd.DataFrame()



RUN_SES_BOOKS_MODEL     = True   
RUN_SES_BOOKS_LINEPLOT  = True   

SES_VAR = "socioeconomic_index"
book_labels = ["0–10", "11–25", "26–100", "101–200", "201–500", "500+"]
book_code_to_label = {1:"0–10", 2:"11–25", 3:"26–100", 4:"101–200", 5:"201–500", 6:"500+"}

if "books_home_cat" in df.columns:
    df["books_home_cat"] = pd.Categorical(df["books_home_cat"], categories=book_labels, ordered=True)

_subsets = [("All Countries", df)] if not SPLIT_BY_OECD else [
    ("OECD", df[df["is_OECD"] == True]),
    ("non-OECD", df[df["is_OECD"] == False]),
]

def run_ses_to_books_model(df_in):
    outcome_var = "books_home"
    predictor = SES_VAR
    results = []

    for subset_label, subset_df in _subsets:
        print(f"\n📘 SES ➜ Books association for: {subset_label}")
        predictors = [predictor] + control_vars
        formula = f"{outcome_var} ~ {' + '.join(predictors)}"

        if USE_COUNTRY_FE:
            formula += " + C(country)"
            model_vars = [outcome_var, predictor] + control_vars + ["country"]
        else:
            model_vars = [outcome_var, predictor] + control_vars

        df_model = subset_df[model_vars].copy().dropna()
        print(f"Sample size: {len(df_model)}")

        if df_model[predictor].nunique() < 2:
            print("⚠️ Skipping: not enough variation in SES")
            continue

        model = smf.ols(formula=formula, data=df_model)
        if USE_CLUSTER_SES:
            results_model = model.fit(cov_type="cluster", cov_kwds={"groups": df_model["country"]})
        else:
            results_model = model.fit()

        print(results_model.summary())

        if predictor in results_model.params:
            results.append({
                "subset": subset_label,
                "coef": results_model.params[predictor],
                "se": results_model.bse[predictor],
            })

    return pd.DataFrame(results)

if RUN_SES_BOOKS_MODEL:
    ses_books_results_df = run_ses_to_books_model(df)
    if not ses_books_results_df.empty:
        color_map = {"OECD": "#1f77b4", "non-OECD": "#ff7f0e", "All Countries": "#003366"}
        plt.figure(figsize=(7, 5))
        for _, row in ses_books_results_df.iterrows():
            x = row["coef"]; y = row["subset"]; se = row["se"]
            color = color_map.get(y, "black")
            plt.errorbar(x, y, xerr=1.96 * se, fmt='o', capsize=5, color=color)
        plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
        plt.xlabel("Association (β) with Socioeconomic Index")
        plt.title("Association between Socioeconomic Index and Books at Home")
        plt.tight_layout(); plt.grid(axis='x', linestyle='--', alpha=0.4)
        plt.show()

def _safe_subset_name(s): return s.lower().replace(" ", "_").replace("-", "")

if RUN_SES_BOOKS_LINEPLOT:
    for subset_label, subset_df in _subsets:
        if "books_home_cat" not in subset_df.columns:
            print(f"⚠️ Skipping Books line plot for {subset_label}: 'books_home_cat' not found."); continue

        d = subset_df.dropna(subset=["books_home_cat", SES_VAR]).copy()
        d[SES_VAR] = pd.to_numeric(d[SES_VAR], errors="coerce")
        d = d.dropna(subset=[SES_VAR])
        if d.empty:
            print(f"⚠️ Skipping Books line plot for {subset_label}: no data after cleaning."); continue

        g = (d.groupby("books_home_cat")[SES_VAR]
               .agg(["mean", "count", "std"])
               .reindex(book_labels))
        g["se"] = g["std"] / np.sqrt(g["count"])

        y_pos = np.arange(len(g.index))
        plt.figure(figsize=(8, 5.5))
        plt.errorbar(
            x=g["mean"].values,
            y=y_pos,
            xerr=1.96 * g["se"].values,
            fmt='o-',
            capsize=4,
            ecolor="gray",
            color="#003366",
            linewidth=1.6,
            markersize=6,
        )
        plt.yticks(y_pos, g.index)
        plt.xlabel("Mean Socioeconomic Index")
        plt.ylabel("Number of Books at Home (category)")
        plt.title("Mean Socioeconomic Index by Books at Home Category")
        plt.grid(axis='x', linestyle='--', alpha=0.5); plt.tight_layout()
        out_path = os.path.join(BASE_DIR, f"../output/ses_vs_books_line_{_safe_subset_name(subset_label)}.png")
        plt.savefig(out_path, dpi=300); print(f"Saved descriptive plot ➜ {out_path}")
        plt.show()
