import os
import pandas as pd

print("✅ Script started...")


# === 1. Load PISA 2018 SPSS .sav file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/2018/CY07_MSU_STU_QQQ.sav")

columns = [

    # indepedent/categorical variables


    "CNT", "ST013Q01TA", "ST175Q01IA",

    # reading attitudes

    "ST160Q01IA", "ST160Q02IA", "ST160Q03IA", "ST160Q04IA", "ST160Q05IA",

    # reading preference 

    "ST167Q01IA", "ST167Q02IA", "ST167Q03IA", "ST167Q04IA", "ST167Q05IA", 
    
    # reading format

    "ST168Q01HA",

    # amount of cell phones and computers (want to see if this impacts reading times)
    "ST012Q05NA", "ST012Q06NA",

    "AGE",

    # school values cooperation

    "ST206Q01HA", "ST206Q02HA", "ST206Q03HA", "ST206Q04HA",

    #what school teaches (eg resolving conflict)
    "ST221Q01HA", "ST221Q02HA", "ST221Q03HA", "ST221Q04HA", "ST221Q05HA",
    "ST221Q06HA", "ST221Q07HA", "ST221Q08HA", "ST221Q09HA", "ST221Q11HA",

    #languages spoken
    "ST177Q01HA", "ST177Q02HA", "ST177Q03HA",

    #contact with culture
    "ST220Q01HA", "ST220Q02HA", "ST220Q03HA", "ST220Q04HA",


    # schools teaching digital literacy 
    "ST158Q01HA", "ST158Q02HA", "ST158Q03HA",
    "ST158Q04HA", "ST158Q05HA", "ST158Q06HA", "ST158Q07HA",
    #reading tasks in school
    "ST150Q01IA", "ST150Q02IA", "ST150Q03IA", "ST150Q04HA",

    # gender
    "ST004D01T",
    
    # wealth 
    "WEALTH",
    # parent year of schooling
    "PARED",

    # parents highest occupation
    "HISEI",


    # parent education 

    "MISCED", "FISCED", "HISCED",

    # student level of education
    "ISCEDL", 
    # immigrant status
    "IMMIG",
    # duration in childhood care
    "DURECEC",
     
    # cultural and socioeconomic score

    "ESCS",
    
    # perceived competence and reading difficulty

   "SCREADCOMP",
   "SCREADDIFF",

    # empathy with bullying
    "ST207Q01HA", "ST207Q02HA", "ST207Q03HA", "ST207Q04HA", "ST207Q05HA",
    # views on immigration
    "ST204Q02HA", "ST204Q03HA", "ST204Q04HA", "ST204Q05HA",
  
    # belief that intelligence is fixed  
    "ST184Q01HA", 
    
    # student effort
    "EFFORT1", "EFFORT2", 

    # time spent learning
    "TMINS",
    
    # meta cognitive understanding, summarising, critical thinking
    "UNDREM", "METASUM", "METASPAM",

    # ICT usage 
    "ICTHOME", "ICTSCH", 

    # home wealth
    
    "HOMEPOS", "CULTPOSS", "HEDRES",

    # teacher support

    "TEACHSUP",

    # teacher instruction 

    "DIRINS",


    "STIMREAD",

    "TEACHINT",

    "PERCOOP",

    "ATTLNACT",

    "WORKMAST",

    "GFOFAIL",
    "EUDMO",

    "SWBP",
    "RESILIENCE",
    "MASTGOAL",   

    "GCSELFEFF",
    "GCAWARE",
    "ATTIMM",
    "INTCULT",

    "PERSPECT",
    "COGFLEX",
    "RESPECT",
    "AWACOM",

    "GLOBMIND",
    "DISCRIM",
    "BELONG",
    "BEINGBULLIED",

    "ENTUSE",
    "HOMESCH",
    "USESCH",
    "INTICT",

    "CURSUPP",
    "EMOSUPP",
    "PQSCHOOL",

    "JOYREADP",
    "ATTIMMP",
    "INTCULTP",
    "GCAWAREP",

    "SOCONPA",

]

df = pd.read_spss(data_path, usecols=columns, convert_categoricals=False)


# === 2. Rename columns ===
df = df.rename(columns={
    

    "CNT": "country",

    # READING VARIABLES
    "ST013Q01TA": "books_home",
    "ST175Q01IA": "read_time",
    "ST160Q01IA": "att_1_read_only_if_have_to",
    "ST160Q02IA": "att_2_reading_hobby",
    "ST160Q03IA": "att_3_talk_books",
    "ST160Q04IA": "att_4_reading_waste",
    "ST160Q05IA": "att_5_read_for_info",
    "ST167Q01IA": "pref_magazines",
    "ST167Q02IA": "pref_comics",
    "ST167Q03IA": "pref_fiction",
    "ST167Q04IA": "pref_nonfiction",
    "ST167Q05IA": "pref_newspapers",
    "ST168Q01HA": "book_reading_format",
    "ST012Q05NA": "home_smartphones",
    "ST012Q06NA": "home_computers",

    #CONTROLS:
    #gender
    "ST004D01T": "gender",
    # ST206 school values cooperation items
    "ST206Q01HA": "coop_value_cooperation",
    "ST206Q02HA": "coop_students_cooperate",
    "ST206Q03HA": "coop_coop_important",
    "ST206Q04HA": "coop_encouraged",
   
    # what school teaches 
    "ST221Q01HA": "learn_interconnected_economies",
    "ST221Q02HA": "learn_conflict_resolution",
    "ST221Q03HA": "learn_about_cultures",
    "ST221Q04HA": "learn_current_news",
    "ST221Q05HA": "learn_opinion_on_news",
    "ST221Q06HA": "learn_celebrate_diversity",
    "ST221Q07HA": "learn_world_event_discussion",
    "ST221Q08HA": "learn_global_issues_groupwork",
    "ST221Q09HA": "learn_different_perspectives",
    "ST221Q11HA": "learn_crosscultural_communication",


    # languages spoken
    "ST177Q01HA": "lang_student",
    "ST177Q02HA": "lang_mother",
    "ST177Q03HA": "lang_father",

    # control for contact with other culture
    "ST220Q01HA": "contact_family",
    "ST220Q02HA": "contact_school",
    "ST220Q03HA": "contact_neighbourhood",
    "ST220Q04HA": "contact_friends",

    # control for schools teaching digital literacy and critical thinking skills 
    "ST158Q01HA": "diglit_keywords_search",
    "ST158Q02HA": "diglit_trust_info",
    "ST158Q03HA": "diglit_compare_pages",
    "ST158Q04HA": "diglit_privacy_awareness",
    "ST158Q05HA": "diglit_search_snippet",
    "ST158Q06HA": "diglit_subjectivity_bias",
    "ST158Q07HA": "diglit_detect_phishing",

    # reading tasks in school
    "ST150Q01IA": "school_text_diagrams_maps",
    "ST150Q02IA": "school_text_fiction",
    "ST150Q03IA": "school_text_tables_graphs",
    "ST150Q04HA": "school_text_digital_links",

    # education
    "MISCED": "mother_edu",
    "FISCED": "father_edu",
    "HISCED": "highest_parent_edu",   
    "ISCEDL": "student_edu_level",
    "PARED": "parent_edu_years",

    # teachers interest (could be interpreted as support)
   "TEACHINT": "teacher_interest",

    # wealth items 

    "WEALTH": "family_wealth_index",
    # age

    "AGE": "age",

    # highest occupation of parent
    "HISEI": "parent_occ_status",
    # immigration status
    "IMMIG": "immigration_status",

    # learning time (minutes per week)
    "TMINS": "learning_time_mins",

    "ESCS": "socioeconomic_index",

    "DURECEC": "ecec_duration",

    
    "ICTHOME": "ict_home",
    "ICTSCH": "ict_school",
    "HOMEPOS": "home_possessions",
    "CULTPOSS": "cultural_possessions",
    "HEDRES": "home_edu_resources",

    "TEACHSUP": "teacher_support_language",

    "DIRINS": "teacher_directed_instruction",
     

    "STIMREAD": "teacher_reading_stimulation",

    "SCREADCOMP": "reading_self_concept_competence",
    "SCREADDIFF": "reading_self_concept_difficulty",

    "PERCOOP": "perceived_cooperation_school",

    "SWBP": "subjective_wellbeing_positive_affect",
   
    "DISCRIM": "school_discrimination_climate",

    "BELONG": "school_belonging",

    "BEINGBULLIED": "being_bullied",

    "ENTUSE": "ict_use_leisure",
    "HOMESCH": "ict_use_schoolwork_outside_school",

    "USESCH": "ict_use_in_school",

    "INTICT": "ict_interest",


    "CURSUPP": "parental_learning_support",
    
    "EMOSUPP": "parental_emotional_support",

    "PQSCHOOL": "parental_school_quality",

    "JOYREADP": "parent_enjoy_reading",

    "ATTIMMP": "parent_immigration_attitude",

    "INTCULTP": "parent_culture_interest",
    
    "GCAWAREP": "parent_global_awareness",

    "SOCONPA": "parent_social_connection",

    
    #  TESTABLE VARIABLES (that will also be controlled for): 
    "EFFORT1": "effort_actual",
    "EFFORT2": "effort_ideal",

    "ST207Q01HA": "bullied_irritates_me",
    "ST207Q02HA": "bullied_help_good",
    "ST207Q03HA": "bullied_wrong_join",
    "ST207Q04HA": "bullied_feel_bad",
    "ST207Q05HA": "bullied_like_defender",

    "ST204Q02HA": "imm_edu_rights",
    "ST204Q03HA": "imm_voting_rights",
    "ST204Q04HA": "imm_customs",
    "ST204Q05HA": "imm_equal_rights",

    "ST184Q01HA": "fixed_mindset",

    "UNDREM": "metacog_understanding",
    "METASUM": "metacog_summarising",
    "METASPAM": "metacog_credibility",

    "GLOBMIND": "global_mindedness",

    "RESILIENCE": "resilience",
    "MASTGOAL": "mastery_goal_orientation",

    "GCSELFEFF": "global_self_efficacy",
    "GCAWARE": "global_awareness",
    "ATTIMM": "attitude_immigrants",
    "INTCULT": "interest_other_cultures",

    "PERSPECT": "perspective_taking",
    "COGFLEX": "cognitive_flexibility",
    "RESPECT": "respect_other_cultures",
    "AWACOM": "intercultural_awareness",

    "ATTLNACT": "attitude_learning_activities",

    "WORKMAST": "work_mastery",

    "GFOFAIL": "general_fear_of_failure",
    "EUDMO": "eudaemonia_meaning_in_life",

})

# === 6. Clean known special codes ===

# General codes used across many categorical/ordinal items
GENERIC_SPECIAL_CODES = [97, 98, 99, -9, -8, -5, -4, -3, -2, -1]

# PISA-specific extended numeric missing codes
EXTENDED_SPECIAL_CODES = [9999995, 9999997, 9999998, 9999999]

# Combine all known codes into a master list
ALL_SPECIAL_CODES = GENERIC_SPECIAL_CODES + EXTENDED_SPECIAL_CODES

# Apply to all numeric-looking columns
for col in df.columns:
    if df[col].dtype in ["float64", "int64"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].where(~df[col].isin(ALL_SPECIAL_CODES))

df["immigration_status"] = pd.to_numeric(df["immigration_status"], errors="coerce")
df["immigration_status"] = df["immigration_status"].where(~df["immigration_status"].isin([5, 7, 8, 9]))

df["ecec_duration"] = pd.to_numeric(df["ecec_duration"], errors="coerce")
df["ecec_duration"] = df["ecec_duration"].where(~df["ecec_duration"].isin([95, 97, 98, 99]))


# === 3. Recode books_home ===
books_map = {
    1: "0–10", 2: "11–25", 3: "26–100",
    4: "101–200", 5: "201–500", 6: "500+"
}
df["books_home_cat"] = df["books_home"].replace(books_map)

# === 4. Recode reading time ===
read_map = {
    1: "None",
    2: "<30 min",
    3: "30–60 min",
    4: "1–2 hrs",
    5: ">2 hrs"
}
df["read_time_cat"] = df["read_time"].replace(read_map)


ecec_duration_map = {
    0: "Less than 1 year",
    1: "1–2 years",
    2: "2–3 years",
    3: "3–4 years",
    4: "4–5 years",
    5: "5–6 years",
    6: "6–7 years",
    7: "7–8 years",
    8: "8+ years"
}

df["ecec_duration_label"] = df["ecec_duration"].replace(ecec_duration_map)


# === Value labels for cooperation vars ===
coop_map = {
    1: "Not at all true",
    2: "Slightly true",
    3: "Very true",
    4: "Extremely true"
}
for var in ["coop_value_cooperation", "coop_students_cooperate", "coop_coop_important", "coop_encouraged"]:
    df[var + "_label"] = df[var].map(coop_map)

    # === ST207: Anti-Bullying Attitudes Label Mapping ===
bully_map = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Agree",
    4: "Strongly agree"
}

for var in [
    "bullied_irritates_me", "bullied_help_good", "bullied_wrong_join",
    "bullied_feel_bad", "bullied_like_defender"
]:
    df[var + "_label"] = df[var].map(bully_map)

effort_scale = {
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5",
    6: "6", 7: "7", 8: "8", 9: "9", 10: "10"
}
df["effort_actual_cat"] = df["effort_actual"].map(effort_scale)
df["effort_ideal_cat"] = df["effort_ideal"].map(effort_scale)

immigration_map = {
    1: "Native",
    2: "Second-Generation",
    3: "First-Generation"
}
df["immigration_status_label"] = df["immigration_status"].replace(immigration_map)



# === Recode parental education levels (ISCED) ===
isced_parent_map = {
    0: "None",
    1: "ISCED 1",
    2: "ISCED 2",
    3: "ISCED 3B/C",
    4: "ISCED 3A/4",
    5: "ISCED 5B",
    6: "ISCED 5A/6"
}

df["mother_edu_label"] = df["mother_edu"].replace(isced_parent_map)
df["father_edu_label"] = df["father_edu"].replace(isced_parent_map)
df["highest_parent_edu_label"] = df["highest_parent_edu"].replace(isced_parent_map)


# === ST221: Global Competence Learning at School (Yes/No) ===
yes_no_map = {
    1: "Yes",
    2: "No"
}

for var in [
    "learn_interconnected_economies",
    "learn_conflict_resolution",
    "learn_about_cultures",
    "learn_current_news",
    "learn_opinion_on_news",
    "learn_celebrate_diversity",
    "learn_world_event_discussion",
    "learn_global_issues_groupwork",
    "learn_different_perspectives",
    "learn_crosscultural_communication"
]:
    df[var + "_label"] = df[var].map(yes_no_map)


# === ST177: Number of Languages Spoken (Student, Mother, Father) ===
lang_map = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four or more"
}

for var in ["lang_student", "lang_mother", "lang_father"]:
    df[var + "_label"] = df[var].map(lang_map)

# === ST204: Attitudes Toward Immigrants ===
imm_map = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Agree",
    4: "Strongly agree"
}

for var in [
    "imm_edu_rights", "imm_voting_rights", 
    "imm_customs", "imm_equal_rights"
]:
    df[var + "_label"] = df[var].map(imm_map)


# === ST220: Contact with People from Other Countries ===
contact_map = {
    1: "Yes",
    2: "No"
}

for var in [
    "contact_family", "contact_school", "contact_neighbourhood", "contact_friends"
]:
    df[var + "_label"] = df[var].map(contact_map)



# === Recode ISCEDL (student education level) ===
isced_map = {
    1: "ISCED 1 (Primary)",        # Rare
    2: "ISCED 2 (Lower Secondary)",
    3: "ISCED 3 (Upper Secondary)",
    4: "ISCED 4 (Post-sec non-tertiary)",
    5: "ISCED 5 (Tertiary)"
}

df["student_edu_level_label"] = df["student_edu_level"].replace(isced_map)


# === ST184: Fixed Mindset Statement ===
mindset_map = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Agree",
    4: "Strongly agree"
}

df["fixed_mindset_label"] = df["fixed_mindset"].map(mindset_map)


# === ST168: Book Reading Format Preference ===
format_map = {
    1: "Rarely or never read books",
    2: "Mostly paper format",
    3: "Mostly digital format",
    4: "Equal paper and digital"
}

df["book_reading_format_label"] = df["book_reading_format"].map(format_map)


# reading preference
reading_pref_map = {
    1: "Never or almost never",
    2: "A few times a year",
    3: "About once a month",
    4: "Several times a month",
    5: "Several times a week"
}

reading_pref_vars = [
    "pref_magazines",
    "pref_comics",
    "pref_fiction",
    "pref_nonfiction",
    "pref_newspapers"
]

for col in reading_pref_vars:
    df[col + "_label"] = df[col].map(reading_pref_map)

# === ST158: Taught Digital Literacy Skills at School (Yes/No) ===
yes_no_map = {
    1: "Yes",
    2: "No"
}

for var in [
    "diglit_keywords_search", "diglit_trust_info", "diglit_compare_pages",
    "diglit_privacy_awareness", "diglit_search_snippet",
    "diglit_subjectivity_bias", "diglit_detect_phishing"
]:
    df[var + "_label"] = df[var].map(yes_no_map)

# === ST150: Frequency of Reading Text Types in School ===
frequency_map = {
    1: "Many times",
    2: "Two or three times",
    3: "Once",
    4: "Not at all"
}

for var in [
    "school_text_diagrams_maps", "school_text_fiction",
    "school_text_tables_graphs", "school_text_digital_links"
]:
    df[var + "_label"] = df[var].map(frequency_map)

# === ST004: Gender ===
gender_map = {
    1: "Female",
    2: "Male"
}
df["gender_label"] = df["gender"].map(gender_map)

# how many devices

device_count_map = {
    1: "None",
    2: "One",
    3: "Two",
    4: "Three or more"
}

df["home_smartphones_label"] = df["home_smartphones"].map(device_count_map)
df["home_computers_label"] = df["home_computers"].map(device_count_map)


# ===#  7. Export cleaned data ===
output_path = os.path.join(BASE_DIR, "../output/2018output/newpisa2018_cleaned_all_countries.csv")
df.to_csv(output_path, index=False)
print(f"📁 Exported cleaned file to: {output_path}")
