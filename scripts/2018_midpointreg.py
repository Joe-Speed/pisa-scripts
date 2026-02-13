
import os
import pandas as pd
import statsmodels.formula.api as smf
from tabulate import tabulate
from statsmodels.iolib.summary2 import summary_col
import matplotlib.pyplot as plt

BOOKS_ENCODING = "midpoint" 
OPEN_ENDED_VALUE = 600
BOOKS_MIDPOINTS = {
    1: 5,     
    2: 18,    
    3: 63,    
    4: 150,   
    5: 350,   
    6: OPEN_ENDED_VALUE 
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/2018output/newpisa2018_cleaned_all_countries.csv")
df = pd.read_csv(data_path)

df = df.rename(columns={"read_time": "read_time_numeric"})

df["books_home_midpoint"] = pd.to_numeric(df.get("books_home"), errors="coerce").map(BOOKS_MIDPOINTS)

BOOKS_VAR = "books_home_midpoint" if BOOKS_ENCODING.lower() == "midpoint" else "books_home"

BOOKS_DISPLAY_INC = 100 if BOOKS_ENCODING.lower() == "midpoint" else 1
BOOKS_DISPLAY_LABEL = (
    "Books at Home (per 100 books)" if BOOKS_DISPLAY_INC == 100
    else ("Books at Home (Ordinal 1–6)" if BOOKS_ENCODING.lower() == "ordinal" else "Books at Home")
)

base_vars = ["read_time_numeric", BOOKS_VAR, "country"]

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

for col in ["read_time_numeric", BOOKS_VAR] + control_vars:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

effort_vars = ["effort_actual", "effort_ideal"]
goal_vars = ["mastery_goal_orientation", "work_mastery"]

bully_vars = ["bullied_irritates_me", "bullied_help_good", "bullied_wrong_join", "bullied_feel_bad", "bullied_like_defender"]
immigration_vars = ["imm_edu_rights", "imm_voting_rights", "imm_customs", "imm_equal_rights", "attitude_immigrants"]
mindset_vars = ["fixed_mindset"]

metacog_vars = ["metacog_understanding", "metacog_summarising", "metacog_credibility", "cognitive_flexibility", "perspective_taking"]
citizenship_vars = ["global_mindedness", "global_self_efficacy", "global_awareness"]
intercultural_vars = ["interest_other_cultures", "respect_other_cultures", "intercultural_awareness"]

empathy_vars = ["perspective_taking", "global_mindedness"]
cognitiveflex_vars = ["cognitive_flexibility"]
resilience_vars = ["resilience"]
fearfailure_vars = ["general_fear_of_failure"]
meaning_vars = ["eudaemonia_meaning_in_life"]
learning_vars = ["attitude_learning_activities"]

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
    "AUS","AUT","BEL","CAN","CHE","CHL","COL","CRI","CZE","DEU",
    "DNK","EST","FIN","FRA","GBR","GRC","HUN","ISL","IRL","ISR",
    "ITA","JPN","KOR","LTU","LUX","LVA","MEX","NLD","NOR","NZL",
    "POL","PRT","SVK","SVN","ESP","SWE","TUR","USA"
]
df["is_OECD"] = df["country"].isin(oecd_codes)

RUN_GENERAL_REGRESSION = True
SPLIT_BY_OECD = True

USE_CLUSTER_SES = True
USE_COUNTRY_FE = True
CHECK_NONLINEAR = False
CHECK_VIF = False

INTERACT_READTIME_GENDER = False
INTERACT_BOOKS_GENDER = False
INTERACT_READTIME_BOOKS = False

base_predictors = ["read_time_numeric", BOOKS_VAR]
if CHECK_NONLINEAR:
    df["read_time_sq"] = df["read_time_numeric"] ** 2
    if "read_time_sq" not in base_predictors:
        base_predictors.insert(base_predictors.index("read_time_numeric") + 1, "read_time_sq")

interaction_terms = []
if INTERACT_READTIME_GENDER:
    interaction_terms.append("read_time_numeric * gender")
    base_predictors = [v for v in base_predictors if v not in ["read_time_numeric", "gender"]]
if INTERACT_BOOKS_GENDER:
    interaction_terms.append(f"{BOOKS_VAR} * gender")
    base_predictors = [v for v in base_predictors if v not in [BOOKS_VAR, "gender"]]
if INTERACT_READTIME_BOOKS:
    interaction_terms.append(f"read_time_numeric * {BOOKS_VAR}")
    base_predictors = [v for v in base_predictors if v not in ["read_time_numeric", BOOKS_VAR]]

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

            predictors = base_predictors + control_vars
            formula_terms = predictors + interaction_terms
            formula = f"{outcome} ~ {' + '.join(formula_terms)}"
            model_vars = [outcome] + predictors

            if USE_COUNTRY_FE:
                formula += " + C(country)"
                model_vars += ["country"]

            if INTERACT_READTIME_GENDER:
                model_vars += ["read_time_numeric", "gender"]
            if INTERACT_BOOKS_GENDER:
                model_vars += [BOOKS_VAR, "gender"]
            if INTERACT_READTIME_BOOKS:
                model_vars += ["read_time_numeric", BOOKS_VAR]

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

            for pred in ["read_time_numeric", BOOKS_VAR]:
                if pred in results_model.params:
                    pval = results_model.pvalues[pred]
                    scale = BOOKS_DISPLAY_INC if pred == BOOKS_VAR else 1.0
                    results.append({
                        "subset": subset_label,
                        "outcome": outcome,
                        "predictor": ("read_time_numeric" if pred == "read_time_numeric" else BOOKS_DISPLAY_LABEL),
                        "coef_raw": results_model.params[pred],
                        "se_raw": results_model.bse[pred],
                        "coef_disp": results_model.params[pred] * scale,
                        "se_disp": results_model.bse[pred] * scale,
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

    results_df["coef_str"] = results_df.apply(lambda r: f"{r['coef_disp']:.5f}{r['stars']}", axis=1)
    print("\n=== Summary Table of Predictors (display-scaled) ===")
    print(tabulate(
        results_df[["subset", "outcome", "predictor", "coef_str", "se_disp"]],
        headers='keys', tablefmt='github', floatfmt=".5f"
    ))

    predictor_titles = {
        "read_time_numeric": "Time Spent Reading per Day",
        BOOKS_DISPLAY_LABEL: BOOKS_DISPLAY_LABEL
    }

    for label in ["read_time_numeric", BOOKS_DISPLAY_LABEL]:
        subset = results_df[results_df["predictor"] == label]
        if subset.empty:
            continue

        plt.figure(figsize=(10, 6))

        if SPLIT_BY_OECD:
            color_map = {"OECD": "#465759", "non-OECD": "#B77D8F"}
            for group in subset["subset"].unique():
                group_data = subset[subset["subset"] == group]
                plt.errorbar(
                    group_data["coef_disp"], group_data["outcome"],
                    xerr=1.96 * group_data["se_disp"],
                    fmt='o', capsize=4, label=group, color=color_map.get(group, "#999999")
                )
            title_suffix = "by OECD Status"
        else:
            group_data = subset
            plt.errorbar(
                group_data["coef_disp"], group_data["outcome"],
                xerr=1.96 * group_data["se_disp"],
                fmt='o', capsize=4, label="All Countries", color="#003366"
            )
            title_suffix = "(All Countries)"

        plt.axvline(0, linestyle='--', color='gray')
        plt.title(f"Association between {predictor_titles[label]} and Outcome {title_suffix}")
        xlabel = "Coefficient (±95% CI)"
        if label == BOOKS_DISPLAY_LABEL and BOOKS_DISPLAY_INC == 100:
            xlabel += " per 100 books"
        plt.xlabel(xlabel)
        plt.ylabel("Outcomes")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    output_path = os.path.join(BASE_DIR, "../output/2018output/regression_results_summary.csv")
    results_df.to_csv(output_path, index=False)

else:
    results_df = pd.DataFrame()
