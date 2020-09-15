# script merges data from past event forms to output a csv of everyone involved in tech+
# expects the following csvs in the data folder:
# [F20] Resume Critique Reviewee.csv
# [F20] Resume Critique Reviewer.csv
# [F20] Tech+ 101 Kick-off Q&A Panel Sign ups.csv
# [F20] Accepted Mentees.csv
# [F20] Accepted Mentors.csv
# [S20] Coffee Chats Mentees.csv
# [S20] Coffee Chats Mentors.csv
# Mentorship Program Database.csv

import pandas as pd
import numpy as np
from merge_helpers import *
from program_mappings import *
from constants import *

# import all event data from csvs
f20_resume_critique_reviewee = pd.read_csv('data/[F20] Resume Critique Reviewee.csv')
f20_resume_critique_reviewer = pd.read_csv('data/[F20] Resume Critique Reviewer.csv')
f20_kickoff_qna = pd.read_csv('data/[F20] Tech+ 101 Kick-off Q&A Panel Sign ups.csv')
f20_mentees = pd.read_csv('data/[F20] Accepted Mentees.csv')
f20_mentors = pd.read_csv('data/[F20] Accepted Mentors.csv')
s20_coffee_chats_mentees = pd.read_csv('data/[S20] Coffee Chats Mentees.csv')
s20_coffee_chats_mentors = pd.read_csv('data/[S20] Coffee Chats Mentors.csv')
mentorship_database = pd.read_csv('data/Mentorship Program Database.csv')

# cleans CSV data and merges with the final database, mentorshipDatabase, then combines conflicting columns after merge
def clean_data(CSV, role, rename, term):
    # rename relevant columns
    CSV.rename(columns=rename, inplace=True)
    # fill in columns missing from certain sheets to ensure consistency for the merge
    CSV = CSV.reindex(columns=[EMAIL, FIRST_NAME, LAST_NAME, PRONOUNS, ACADEMIC_PROGRAM, TERM])
    # select and create relevant columns
    CSV = CSV[[EMAIL, FIRST_NAME, LAST_NAME, PRONOUNS, ACADEMIC_PROGRAM, TERM]]
    CSV[NAME] = CSV[FIRST_NAME] + " " + CSV[LAST_NAME]
    CSV.loc[CSV[FIRST_NAME].isnull() & CSV[LAST_NAME].notnull(), NAME] = CSV[LAST_NAME]
    CSV.loc[CSV[FIRST_NAME].notnull() & CSV[LAST_NAME].isnull(), NAME] = CSV[FIRST_NAME]
    CSV.drop([FIRST_NAME, LAST_NAME], inplace=True, axis=1)

    # drop rows with empty name
    CSV.dropna(subset=[NAME], inplace=True)

    # clean program names to remove response errors and combine different versions of the same program
    # list of conditions to help with cleaning Academic Program
    conditions = [
        (CSV[ACADEMIC_PROGRAM].isin(csbba)),
        (CSV[ACADEMIC_PROGRAM].isin(cs)),
        (CSV[ACADEMIC_PROGRAM].isin(ce)),
        (CSV[ACADEMIC_PROGRAM].isin(se)),
        (CSV[ACADEMIC_PROGRAM].isin(mathbba)),
        (CSV[ACADEMIC_PROGRAM].isin(syde)),
        (CSV[ACADEMIC_PROGRAM].isin(math)),
        (CSV[ACADEMIC_PROGRAM].isin(statcs)),
        (CSV[ACADEMIC_PROGRAM].isin(csbus)),
        (CSV[ACADEMIC_PROGRAM].isin(ece)),
        (CSV[ACADEMIC_PROGRAM].isin(mte)),
        (CSV[ACADEMIC_PROGRAM].isin(afm)),
        (CSV[ACADEMIC_PROGRAM].isin(cfm)),
        (CSV[ACADEMIC_PROGRAM].isin(bme)),
        (~(CSV[ACADEMIC_PROGRAM].isin(math)) & ~(CSV[ACADEMIC_PROGRAM].isin(csbba)) & ~(CSV[ACADEMIC_PROGRAM].isin(cs)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(ce)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(se)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(mathbba)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(syde)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(statcs)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(csbus)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(ece)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(mte)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(afm)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(cfm)) &
        ~(CSV[ACADEMIC_PROGRAM].isin(bme)))
        ]

    # final Program name assigned to each condition
    values = [CS + ', ' + BBA, 
        CS, 
        CE, 
        SE, 
        MATH + ', ' + BBA, 
        SYDE, 
        MATH,
        CS + ', ' + STAT, 
        CS + ', ' + BUS,
        ECE, 
        MTE,
        AFM,
        CFM,
        BME,
        CSV[ACADEMIC_PROGRAM]]

    # create a new column, Program, and assign values to it using conditions and values defined above
    CSV[PROGRAM] = np.select(conditions, values)

    # cleaning individual programs to match Notion formatting
    CSV.loc[CSV[PROGRAM] == 'CS/CO', PROGRAM] = 'Computer Science, Combinatorics and Optimization'
    CSV.loc[CSV[PROGRAM] == 'Math/FARM', PROGRAM] = 'Mathematics, FARM'
    CSV.loc[CSV[PROGRAM] == 'Science and Business' , PROGRAM] = 'Science, Business'
    CSV.loc[CSV[PROGRAM] == 'Biotechnology/Economics', PROGRAM] = 'Biotechnology, Economics'
    CSV.loc[CSV[PROGRAM] == 'Mathematical Finance and Statistics', PROGRAM] = 'Mathematical Finance, Statistics'
    CSV.loc[CSV[PROGRAM] == 'Actuarial Science and Statistics', PROGRAM] = 'Actuarial Science, Statistics'
    CSV.loc[CSV[PROGRAM] == 'Health Studies, Co-op', PROGRAM] = 'Health Studies'
    CSV.loc[CSV[PROGRAM] == 'Computer Science with Business Specialization, Statistics Minor', PROGRAM] = 'Computer Science, Business Specialization, Statistics Minor'
    CSV.loc[CSV[PROGRAM] == 'CS with HCI Option', PROGRAM] = 'Computer Science, HCI Option'
    CSV.loc[CSV[PROGRAM] == 'Finance and CS', PROGRAM] = 'Finance & CS minor'

    # drop old program column
    CSV.drop([ACADEMIC_PROGRAM], inplace=True, axis=1)

    # create new columns corresponding to the role and term of the event
    CSV[ROLE] = role
    CSV[TERMS_INVOLVED] = term

    # merge clean data to the final database
    merged = pd.merge(mentorship_database, CSV, on=NAME, how='outer')

    # combine any conflicting columns from the merge
    if ROLE + '_x' in merged.columns and ROLE + '_y' in merged.columns:
        merged = concat_combine(merged, ROLE)

    if PROGRAM + '_x' in merged.columns and PROGRAM + '_y' in merged.columns:
        merged = combine(merged, PROGRAM)

    if TERM + '_x' in merged.columns and TERM + '_y' in merged.columns:
        merged = combine(merged, TERM)

    if PRONOUNS + '_x' in merged.columns and PRONOUNS + '_y' in merged.columns:
        merged = combine(merged, PRONOUNS)

    if EMAIL + '_x' in merged.columns and EMAIL + '_y' in merged.columns:
        merged = concat_combine(merged, EMAIL)

    if TERMS_INVOLVED + '_x' in merged.columns and TERMS_INVOLVED + '_y' in merged.columns:
        merged.loc[merged[TERMS_INVOLVED + '_y'].isnull(), TERMS_INVOLVED] = merged[TERMS_INVOLVED + '_x']
        merged.loc[merged[TERMS_INVOLVED + '_x'].isnull(), TERMS_INVOLVED] = merged[TERMS_INVOLVED + '_y']
        merged.loc[(merged[TERMS_INVOLVED + '_x'].notnull() & merged[TERMS_INVOLVED + '_y'].notnull() & merged[TERMS_INVOLVED + '_x'].str.contains(term, regex=False, na=False)), TERMS_INVOLVED] = merged[TERMS_INVOLVED + '_x']
        merged.loc[(merged[TERMS_INVOLVED + '_x'].notnull() & merged[TERMS_INVOLVED + '_y'].notnull() & ~(merged[TERMS_INVOLVED + '_x'].str.contains(term, regex=False, na=False))), TERMS_INVOLVED] = merged[TERMS_INVOLVED + '_x'] + ", " + merged[TERMS_INVOLVED + '_y']
        
        merged.drop([TERMS_INVOLVED + '_x', TERMS_INVOLVED + '_y'], inplace=True, axis=1)

    return merged

# dictionaries to rename columns
coffee_chats_rename = {"Email Address":EMAIL,"Preferred First Name":FIRST_NAME, "Preferred Pronouns (if you are comfortable sharing)":PRONOUNS, "Academic Program ":ACADEMIC_PROGRAM, "Fall 2020 School Term:":TERM}
resume_critique_rename = {"Username":EMAIL,"First Name:":FIRST_NAME, "Last Name:":LAST_NAME, "What are your pronouns?":PRONOUNS, "Academic Program:":ACADEMIC_PROGRAM, "Fall 2020 School Term:":TERM}
kickoff_rename = {"Email Address:":EMAIL,"First Name:":FIRST_NAME, "Last Name:":LAST_NAME, "Academic program:":ACADEMIC_PROGRAM}
mentorship_rename = {"Email Address":EMAIL, "Fall 2020 School Term:":TERM}

# clean and merge each dataframe with final dataframe, starting from oldest to newest to ensure newer data replaces older data
mentorship_database = clean_data(s20_coffee_chats_mentees, "S20 " + COFFEE_CHAT_MENTEE, coffee_chats_rename, 'S20')
mentorship_database = clean_data(s20_coffee_chats_mentors, "S20 " + COFFEE_CHAT_MENTOR, coffee_chats_rename, 'S20')
mentorship_database = clean_data(f20_resume_critique_reviewee, "F20 " + RESUME_CRITIQUE_REVIEWEE, resume_critique_rename, 'F20')
mentorship_database = clean_data(f20_resume_critique_reviewer, "F20 " + RESUME_CRITIQUE_REVIEWER, resume_critique_rename, 'F20')
mentorship_database = clean_data(f20_kickoff_qna, "F20 " + KICKOFF_ATTENDEE, kickoff_rename, 'F20')
mentorship_database = clean_data(f20_mentors, "F20 " + MENTOR, mentorship_rename, 'F20')
mentorship_database = clean_data(f20_mentees, "F20 " + MENTEE, mentorship_rename, 'F20')

# remove any potential duplicates
mentorship_database.drop_duplicates(inplace=True)

# export as csv
mentorship_database.to_csv("mentorship_database.csv", index=False)
