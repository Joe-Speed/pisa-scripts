import os
import pandas as pd
import statsmodels.formula.api as smf
from tabulate import tabulate
# For optional regression summary formatting
from statsmodels.iolib.summary2 import summary_col


# === 1. Load numeric-cleaned dataset ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../output/2018output/newpisa2018_cleaned_all_countries.csv")
df = pd.read_csv(data_path)



# === 2. Rename if needed
df = df.rename(columns={"read_time": "read_time_numeric"})

# === 3. Define variables ===
base_vars = ["read_time_numeric", "books_home", "country"]

# === 4. Optional control variables (comment out if you do not want as a control for regression) ===
control_vars = [
    
    
    "age",
    
    "gender",

    # do students value or think cooperation is important
    #"coop_value_cooperation","coop_students_cooperate","coop_coop_important", "coop_encouraged",

    # === school teaches students about culture, conflict resolution etc.
    
    "learn_interconnected_economies", "learn_conflict_resolution", "learn_about_cultures", "learn_current_news", "learn_opinion_on_news", "learn_celebrate_diversity", "learn_world_event_discussion", "learn_global_issues_groupwork", "learn_different_perspectives", "learn_crosscultural_communication",
    # === amount of languages
    #"lang_student", "lang_mother", "lang_father",
    # === cultural contact
    #"contact_family", "contact_school", "contact_neighbourhood", "contact_friends",

    # === taught ditigal skills (eg being critical of phishing)
    "diglit_keywords_search","diglit_trust_info", "diglit_compare_pages", "diglit_privacy_awareness", "diglit_search_snippet", "diglit_subjectivity_bias", "diglit_detect_phishing",

    # reading attitudes to control for
    #"att_1_read_only_if_have_to","att_2_reading_hobby","att_3_talk_books","att_4_reading_waste","att_5_read_for_info",

    # reading preferences to control for 
    #"pref_magazines", "pref_comics", "pref_fiction", "pref_nonfiction", "pref_newspapers", "book_reading_format",



    # === school reads texts
    "school_text_diagrams_maps", "school_text_fiction", "school_text_tables_graphs", "school_text_digital_links",

    # === education
    "mother_edu", "father_edu", "highest_parent_edu", "student_edu_level", "parent_edu_years",

    # === teachers support
    #"teacher_interest", "teacher_support_language","teacher_directed_instruction", "teacher_reading_stimulation",

    # === wealth 

    "family_wealth_index","socioeconomic_index", "parent_occ_status", "home_possessions",  "home_edu_resources", "cultural_possessions",
   


    # === immigration status
    #"immigration_status",

    # === amount of learning in classroom

    "learning_time_mins",

    # === years of childcare

    "ecec_duration",
     
    # === ICT usage
    #"ict_home", "ict_school", "ict_use_leisure", "ict_use_schoolwork_outside_school", "ict_use_in_school", "ict_interest",


    # ===competence beliefs
    #"reading_self_concept_competence", "reading_self_concept_difficulty",

    #"perceived_cooperation_school",

    "subjective_wellbeing_positive_affect",

    "school_discrimination_climate",

    #"school_belonging",

    #"being_bullied",

    # effort
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

    "intercultural_awareness",

    #"attitude_learning_activities",

    #"work_mastery",

    #"general_fear_of_failure",
    #"eudaemonia_meaning_in_life",
    
]

# Coerce only numeric columns — exclude 'country'
for col in ["read_time_numeric", "books_home"] + control_vars:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 6 The testable variables (predictors) that you can block out when running different things

# === Effort and goal orientation ===
effort_vars = [
    "effort_actual", "effort_ideal"
]

goal_vars = [
    "mastery_goal_orientation", "work_mastery"
]

# === Bullying outcome variables ===
bully_vars = [
    "bullied_irritates_me", "bullied_help_good",
    "bullied_wrong_join", "bullied_feel_bad", "bullied_like_defender"
]

# === Immigration attitudes ===
immigration_vars = [
    "imm_edu_rights", "imm_voting_rights",
    "imm_customs", "imm_equal_rights",
    "attitude_immigrants"
]

# === Mindset ===
mindset_vars = ["fixed_mindset"]

# === Metacognition (reading strategies) ===
metacog_vars = [
    "metacog_understanding", "metacog_summarising", "metacog_credibility", "cognitive_flexibility", "perspective_taking", 
]

# === Global citizenship values ===
citizenship_vars = [
    "global_mindedness", "global_self_efficacy", "global_awareness"
]

# === Intercultural respect & openness ===
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

# === Adaptability and resilience ===
resilience_vars = [
    "resilience",
]
fearfailure_vars = [
    "general_fear_of_failure"
]

# === Eudaemonic wellbeing ===
meaning_vars = [
    "eudaemonia_meaning_in_life"
]

# === Attitudes toward learning ===
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



# === Add OECD dummy ===
oecd_codes = [
    "AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU",
    "DNK", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "ISL", "IRL", "ISR",
    "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR", "NZL",
    "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "TUR", "USA"
]

df["is_OECD"] = df["country"].isin(oecd_codes)
import matplotlib.pyplot as plt

# === Toggle to run general regression block ===
RUN_GENERAL_REGRESSION = True
SPLIT_BY_OECD = True  # False = all countries; True = OECD split

# === Robustness settings ===
USE_CLUSTER_SES = True
USE_COUNTRY_FE = True
CHECK_NONLINEAR = False
CHECK_VIF = False

# === Optional interaction switches ===
INTERACT_READTIME_GENDER = False
INTERACT_BOOKS_GENDER = False
INTERACT_READTIME_BOOKS = False

# === Base predictors — expand if CHECK_NONLINEAR is enabled
base_vars = ["read_time_numeric", "books_home"]
if CHECK_NONLINEAR:
    df["read_time_sq"] = df["read_time_numeric"] ** 2
    if "read_time_sq" not in base_vars:
        base_vars.insert(base_vars.index("read_time_numeric") + 1, "read_time_sq")

# === Interaction terms
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

# === Main block
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

            # Add raw variables for interactions
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

    # === Convert to DataFrame
    results_df = pd.DataFrame(results)

    # Map variable names to readable labels
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
        # Custom professional color palette
        color_map = {
            "OECD": "#465759",      # Dusty charcoal-teal
            "non-OECD": "#B77D8F"   # Muted burgundy-rose
        }

        for group in subset["subset"].unique():
            group_data = subset[subset["subset"] == group]
            plt.errorbar(
                group_data["coef"], group_data["outcomes"],
                xerr=1.96 * group_data["se"],
                fmt='o', capsize=4, label=group,
                color=color_map.get(group, "#999999")  # fallback grey
            )
        title_suffix = "by OECD Status"
    else:
        # All Countries – keep consistent dark blue
        group_data = subset
        plt.errorbar(
            group_data["coef"], group_data["outcomes"],
            xerr=1.96 * group_data["se"],
            fmt='o', capsize=4, label="All Countries",
            color="#003366"
        )
        title_suffix = "(All Countries)"

    plt.axvline(0, linestyle='--', color='gray')
    plt.title(f"Association between {predictor_labels[pred]} and Outcome {title_suffix}")
    plt.xlabel("Coefficient (±95% CI)")
    plt.ylabel("Outcome")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    # === Save summary table
    results_df["coef_str"] = results_df.apply(lambda row: f"{row['coef']:.3f}{row['stars']}", axis=1)
    print("\n=== Summary Table of Predictors ===")
    print(tabulate(results_df[["subset", "outcome", "predictor", "coef_str", "se"]],
                   headers='keys', tablefmt='github', floatfmt=".3f"))

    output_path = os.path.join(BASE_DIR, "../output/2018output/regression_results_summary.csv")
    results_df.to_csv(output_path, index=False) 




# === Regression run toggles ===
RUN_WEALTH_MODEL = False
RUN_BOOKS_MODEL = False

# === Additional Regressions===
# === Wealth ➜ Books at Home ===
def run_wealth_to_books_model(df):
    outcome_var = "books_home"
    predictor = "family_wealth_index"
    results = []
    full_models = {}

    subsets = [("All Countries", df)] if not SPLIT_BY_OECD else [
        ("OECD", df[df["is_OECD"] == True]),
        ("non-OECD", df[df["is_OECD"] == False])
    ]

    for subset_label, subset_df in subsets:
        print(f"\n📘 Wealth ➜ Books regression for: {subset_label}")
        predictors = [predictor] + control_vars
        formula = f"{outcome_var} ~ {' + '.join(predictors)}"

        if USE_COUNTRY_FE:
            formula += " + C(country)"
            model_vars = [outcome_var, predictor] + control_vars + ["country"]
        else:
            model_vars = [outcome_var, predictor] + control_vars

        df_model = subset_df[model_vars].copy().dropna()
        print(f"📊 Sample size: {len(df_model)}")

        if df_model[predictor].nunique() < 2:
            print("⚠️ Skipping: not enough variation in predictor")
            continue

        model = smf.ols(formula=formula, data=df_model)
        results_model = model.fit(
            cov_type="cluster", cov_kwds={"groups": df_model["country"]}
        ) if USE_CLUSTER_SES else model.fit()

        print(results_model.summary())
        full_models[subset_label] = results_model

        if predictor in results_model.params:
            pval = results_model.pvalues[predictor]
            results.append({
                "subset": subset_label,
                "outcome": outcome_var,
                "predictor": predictor,
                "coef": results_model.params[predictor],
                "se": results_model.bse[predictor],
                "stars": significance_stars(pval)
            })

    # ⚠️ Add this call here to generate LaTeX table
    if SPLIT_BY_OECD:
        sample_sizes = {
            "OECD": len(df[df["is_OECD"] == True].dropna(subset=model_vars)),
            "non-OECD": len(df[df["is_OECD"] == False].dropna(subset=model_vars))
        }
        generate_latex_wealth_books_table(
            oecd_model=full_models["OECD"],
            non_oecd_model=full_models["non-OECD"],
            sample_sizes=sample_sizes
        )

    return pd.DataFrame(results)


def run_books_to_reading_model(df):
    outcome_var = "read_time_numeric"
    predictor = "books_home"
    results = []

    subsets = [("All Countries", df)] if not SPLIT_BY_OECD else [
        ("OECD", df[df["is_OECD"] == True]),
        ("non-OECD", df[df["is_OECD"] == False])
    ]

    for subset_label, subset_df in subsets:
        print(f"\n📖 Books ➜ Reading regression for: {subset_label}")
        predictors = [predictor] + control_vars
        formula = f"{outcome_var} ~ {' + '.join(predictors)}"

        if USE_COUNTRY_FE:
            formula += " + C(country)"
            model_vars = [outcome_var, predictor] + control_vars + ["country"]
        else:
            model_vars = [outcome_var, predictor] + control_vars

        df_model = subset_df[model_vars].copy().dropna()
        print(f"📊 Sample size: {len(df_model)}")

        if df_model[predictor].nunique() < 2:
            print("⚠️ Skipping: not enough variation in predictor")
            continue

        model = smf.ols(formula=formula, data=df_model)
        results_model = model.fit(
            cov_type="cluster", cov_kwds={"groups": df_model["country"]}
        ) if USE_CLUSTER_SES else model.fit()

        print(results_model.summary())

        if predictor in results_model.params:
            pval = results_model.pvalues[predictor]
            results.append({
                "subset": subset_label,
                "outcome": outcome_var,
                "predictor": predictor,
                "coef": results_model.params[predictor],
                "se": results_model.bse[predictor],
                "stars": significance_stars(pval)
            })

    return pd.DataFrame(results)

# === Generate LaTeX Econometrics Table for Wealth ➜ Books at Home ===
def generate_latex_wealth_books_table(oecd_model, non_oecd_model, sample_sizes):
    def format_coef(p, se, stars):
        return f"{p:.3f}{stars} ({se:.3f})"

    def extract_rows(model, show_countries=False):
        rows = []
        for param in model.params.index:
            if param == "Intercept":
                continue
            if not show_countries and param.startswith("C(country)"):
                continue

            coef = model.params[param]
            se = model.bse[param]
            pval = model.pvalues[param]
            stars = significance_stars(pval)

            name = param.replace("C(country)[T.", "").replace("]", "")
            rows.append((name, coef, se, stars))
        return rows

    oecd_rows = extract_rows(oecd_model)
    non_oecd_rows = extract_rows(non_oecd_model)

    # Create aligned table
    tex_lines = []
    tex_lines.append("\\begin{table}[ht]")
    tex_lines.append("\\centering")
    tex_lines.append("\\small")
    tex_lines.append("\\caption{Regression of Family Wealth on Books at Home}")
    tex_lines.append("\\begin{tabular}{lcc}")
    tex_lines.append("\\toprule")
    tex_lines.append(" & OECD (n = %d) & non-OECD (n = %d) \\" % (sample_sizes['OECD'], sample_sizes['non-OECD']))
    tex_lines.append("\\midrule")

    for (oecd_row, non_row) in zip(oecd_rows, non_oecd_rows):
        name1, coef1, se1, stars1 = oecd_row
        name2, coef2, se2, stars2 = non_row
        assert name1 == name2  # Ensure variable order matches
        line = f"{name1.replace('_', ' ')} & {format_coef(coef1, se1, stars1)} & {format_coef(coef2, se2, stars2)} \\"
        if name1 == "gender":  # Insert break after core variables
            tex_lines.append("\\midrule")
            tex_lines.append("\\underline{Controls} \\")
        tex_lines.append(line)

    tex_lines.append("\\bottomrule")
    tex_lines.append("\\end{tabular}")
    tex_lines.append("\\begin{tablenotes}[flushleft]")
    tex_lines.append("\\small")
    tex_lines.append("\\item Note: Standard errors in parentheses. * p$<$0.05, ** p$<$0.01, *** p$<$0.001")
    tex_lines.append("\\end{tablenotes}")
    tex_lines.append("\\end{table}")

    with open("output/wealth_books_table.tex", "w") as f:
        f.write("\n".join(tex_lines))
    print("✅ Saved LaTeX table to: output/wealth_books_table.tex")




# === Significance formatter ===
def significance_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return ''

# === Run and# === Run and save results for Wealth ➜ Books at Home ===
if RUN_WEALTH_MODEL:
    print("\n Running regression: Wealth ➜ Books at Home")
    wealth_results_df = run_wealth_to_books_model(df)

    if not wealth_results_df.empty:
        # Save summary table
        output_csv_path = "output/wealth_books_summary.csv"
        wealth_results_df.to_csv(output_csv_path, index=False)
        print(f"✅ Saved wealth➜books summary table to: {output_csv_path}")

        # === Plotting (clean version with correct colours) ===
        color_map = {"OECD": "#1f77b4", "non-OECD": "#ff7f0e"}
        plt.figure(figsize=(7, 5))

        for idx, row in wealth_results_df.iterrows():
            x = row["coef"]
            y = row["subset"]
            se = row["se"]
            color = color_map.get(y, "black")

            # Plot error bars and points only
            plt.errorbar(x, y, xerr=1.96 * se, fmt='o', capsize=5, color=color)

        plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
        plt.xlabel("Effect of Family Wealth Index on Books at Home (β)")
        plt.title("Regression: Wealth ➜ Books at Home")
        plt.tight_layout()
        plt.grid(axis='x', linestyle='--', alpha=0.4)

        # Save plot
        output_plot_path = "output/wealth_books_plot.png"
        plt.savefig(output_plot_path, dpi=300)
        print(f"✅ Saved plot to: {output_plot_path}")
        plt.show()

if RUN_BOOKS_MODEL:
    print("\n Running regression: Books at Home ➜ Reading Time")
    run_books_to_reading_model(df)
