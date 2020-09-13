#!/usr/bin/env python3

# script merges data from past event forms to output a csv of everyone involved in tech+

import pandas as pd
import numpy as np

# import all event data from csvs
f20ResumeCritiqueReviewee = pd.read_csv('data/[F20] Resume Critique Reviewee.csv')
f20ResumeCritiqueReviewer = pd.read_csv('data/[F20] Resume Critique Reviewer.csv')
f20KickoffQna = pd.read_csv('data/[F20] Tech+ 101 Kick-off Q&A Panel Sign ups.csv')
f20Mentees = pd.read_csv('data/[F20] Accepted Mentees.csv')
f20Mentors = pd.read_csv('data/[F20] Accepted Mentors.csv')
s20CoffeeChatsMentees = pd.read_csv('data/[S20] Coffee Chats Mentees.csv')
s20CoffeeChatsMentors = pd.read_csv('data/[S20] Coffee Chats Mentors.csv')
mentorshipDatabase = pd.read_csv('data/Mentorship Program Database.csv')

print(f20Mentees.columns)
print(f20Mentors.columns)

# lists of different entries of programs to help with data cleaning
csbba = ['Computer Science and Business Administration Double Degree',
    'Computer Science and Business Double Degree',
    'CS/BBA',
    'Computer Science Business Double Degree',
    'Computer Science & Business Administration Double Degree',
    'Business Administration and Computer Science',
    'Computer Science and Business Administration',
    'CS (UW) and Business (WLU)',
    'BBA BCS',
    'Computer Science and Business Admin.',
    'BBA/BCS Double Degree',
    'Business Administration & Computer Science Double Degree',
    'Computer Science & Business Administration',
    'BCS/BBA',
    'bba/bcs double degree',
    'Double Degree in Computer Science and Business Administration',
    'CS/BBA (WLU) Double Degree' ,
    'CSBBA',
    'CS / BBA',
    'Double Degree CS and BBA',
    'CS/BBA DD',
    'Business and Computer Science Double Degree',
    'Business Administration and Computer Science Double Degree',
    'CS & BBA Double Degree',
    'CS/BBA Double Degree',
    'CS+BBA (uWaterloo side)',
    'UW CS/BBA' 
    ]

cs = ['Computer science',
    'Computer Science',
    'CS',
    'Computer Science Co-op',
    'Computer Science (Co-op)',
    'Computer Science Coop ',
    'Computer Sciece',
    'Computer Science ',
    'computer science',
    'Computer science ',
    'CS Coop',
    "Computer Science '17",
    'Honours Computer Science',
    'Honors Computer Science ',
    'Computer Science co-op',
    'Computer Science (co-op)'
]

ce = ['CE', 'Computer Engineering', 'Computer Engineering ', 'Ce', 'Comp. Eng', 'Computer Engineering (Starting 1A in Fall 2020)', 'Computer engineering' ]

se = [ 'Software Engineering 2024',
    'Software Engineering',
    'Software Engineering ',
    'SE',
    'soft eng'
]

mathbba = ['Double Degree Math/BBA', 'MathBBA Double Degree' , 'BMath/BBA DD']

syde = ['SYDE', 
    'Systems Design Engineering',
    'Systems Design',
    'syde',
    'Systems design engineering ' 
]

mathematics = ['Honours Mathematics', 
    'Mathematics',
    'Bachelors of Mathematics ',
    'Mathematics Honours Co-op',
    'Mathematics ',
    'Honours Mathematics ',
    'Math co-op',
    'Honours Mathematics, Co-op',
    'Honours Math - undecided ' 
]

statcs = ['Statistics & Computer Science',  'Computer Science and Statistics', 'Computer Science & Statistics', 'Statistics and Computer Science Double Major', 'Computer Science/Statistics']

csbus = ['Computer Science and Business',  'Computer Science / Business ']

ece = ['ECE2T2', 'ECE']

mechatronicseng = ['Mechatronics Engineering', 'Mechatronics', 'Mechatronics Engineering ']

afm = ['AFM' ,  'Accounting and Financial Management', 'AFM ' ]

cfm = ['Computing Financial Management',
 'Computing and Financial Management',
 'Computing Financial Management ']

biomedeng = ['Biomedical engineering', 'Biomedical Engineering', 'Biomedical Engineering ']

# combines duplicate columns after merging
# selects non-null value first, if both values are not null, selects left right value (ie. more up-to-date entry)
def combine(merged, col):
    x = col + '_x'
    y = col + '_y'

    merged.loc[(merged[y].isnull() & merged[x].notnull()), col] = merged[x]
    merged.loc[(merged[y].notnull()), col] = merged[y]

    merged.drop([x, y], inplace=True, axis=1)

    return merged

# combines duplicate columns after merging
# selects non-null value first, if both values are not null, concatenates values with a comma
def concatCombine(merged, col):
    x = col + '_x'
    y = col + '_y'

    merged.loc[merged[y].isnull(), col] = merged[x]
    merged.loc[merged[x].isnull(), col] = merged[y]
    merged.loc[merged[x].notnull() & merged[y].notnull(), col] = merged[x] + ', ' + merged[y]

    merged.drop([x, y], inplace=True, axis=1)

    return merged

# cleans CSV data and merges with the final database, mentorshipDatabase, then combines conflicting columns after merge
def cleanData(CSV, role, rename, term):
    # rename relevant columns
    CSV.rename(columns=rename, inplace=True)
    # fill in columns missing from certain sheets to ensure consistency for the merge
    CSV = CSV.reindex(columns=['Email', 'First Name', 'Last Name', 'Pronouns', 'Academic Program', 'Term'])
    # select and create relevant columns
    CSV = CSV[['Email', 'First Name', 'Last Name', 'Pronouns', 'Academic Program', 'Term']]
    CSV["Name"] = CSV["First Name"] + " " + CSV["Last Name"]
    CSV.loc[CSV['First Name'].isnull() & CSV['Last Name'].notnull(), 'Name'] = CSV['Last Name']
    CSV.loc[CSV['First Name'].notnull() & CSV['Last Name'].isnull(), 'Name'] = CSV['First Name']
    CSV.drop(["First Name", "Last Name"], inplace=True, axis=1)

    # drop rows with empty name
    CSV.dropna(subset=['Name'], inplace=True)

    # clean program names to remove response errors and combine different versions of the same program
    # list of conditions to help with cleaning Academic Program
    conditions = [
        (CSV['Academic Program'].isin(csbba)),
        (CSV['Academic Program'].isin(cs)),
        (CSV['Academic Program'].isin(ce)),
        (CSV['Academic Program'].isin(se)),
        (CSV['Academic Program'].isin(mathbba)),
        (CSV['Academic Program'].isin(syde)),
        (CSV['Academic Program'].isin(mathematics)),
        (CSV['Academic Program'].isin(statcs)),
        (CSV['Academic Program'].isin(csbus)),
        (CSV['Academic Program'].isin(ece)),
        (CSV['Academic Program'].isin(mechatronicseng)),
        (CSV['Academic Program'].isin(afm)),
        (CSV['Academic Program'].isin(cfm)),
        (CSV['Academic Program'].isin(biomedeng)),
        (~(CSV['Academic Program'].isin(mathematics)) & ~(CSV['Academic Program'].isin(csbba)) & ~(CSV['Academic Program'].isin(cs)) &
        ~(CSV['Academic Program'].isin(ce)) &
        ~(CSV['Academic Program'].isin(se)) &
        ~(CSV['Academic Program'].isin(mathbba)) &
        ~(CSV['Academic Program'].isin(syde)) &
        ~(CSV['Academic Program'].isin(statcs)) &
        ~(CSV['Academic Program'].isin(csbus)) &
        ~(CSV['Academic Program'].isin(ece)) &
        ~(CSV['Academic Program'].isin(mechatronicseng)) &
        ~(CSV['Academic Program'].isin(afm)) &
        ~(CSV['Academic Program'].isin(cfm)) &
        ~(CSV['Academic Program'].isin(biomedeng)))
        ]

    # final Program name assigned to each condition
    values = ['Computer Science, BBA', 
        'Computer Science', 
        'Computer Engineering', 
        'Software Engineering', 
        'Mathematics, BBA', 
        'Systems Design Engineering', 
        'Mathematics',
        'Computer Science, Statistics', 
        'Computer Science, Business',
        'ECE', 
        'Mechatronics Engineering',
        'Accounting and Financial Management',
        'Computing Financial Management',
        'Biomedical Engineering',
        CSV['Academic Program']]

    # create a new column, Program, and assign values to it using conditions and values defined above
    CSV['Program'] = np.select(conditions, values)

    # cleaning individual programs to match Notion formatting
    CSV.loc[CSV['Program'] == 'CS/CO', 'Program'] = 'Computer Science, Combinatorics and Optimization'
    CSV.loc[CSV['Program'] == 'Math/FARM', 'Program'] = 'Mathematics, FARM'
    CSV.loc[CSV['Program'] == 'Science and Business' , 'Program'] = 'Science, Business'
    CSV.loc[CSV['Program'] == 'Biotechnology/Economics', 'Program'] = 'Biotechnology, Economics'
    CSV.loc[CSV['Program'] == 'Mathematical Finance and Statistics', 'Program'] = 'Mathematical Finance, Statistics'
    CSV.loc[CSV['Program'] == 'Actuarial Science and Statistics', 'Program'] = 'Actuarial Science, Statistics'
    CSV.loc[CSV['Program'] == 'Health Studies, Co-op', 'Program'] = 'Health Studies'
    CSV.loc[CSV['Program'] == 'Computer Science with Business Specialization, Statistics Minor', 'Program'] = 'Computer Science, Business Specialization, Statistics Minor'
    CSV.loc[CSV['Program'] == 'CS with HCI Option', 'Program'] = 'Computer Science, HCI Option'
    CSV.loc[CSV['Program'] == 'Finance and CS', 'Program'] = 'Finance & CS minor'

    # drop old program column
    CSV.drop(['Academic Program'], inplace=True, axis=1)

    # create new columns corresponding to the role and term of the event
    CSV['Role'] = role
    CSV['Terms in Tech+'] = term

    # merge clean data to the final database
    merged = pd.merge(mentorshipDatabase, CSV, on='Name', how='outer')

    # combine any conflicting columns from the merge
    if 'Role_x' in merged.columns and 'Role_y' in merged.columns:
        merged = concatCombine(merged, "Role")

    if 'Program_x' in merged.columns and 'Program_y' in merged.columns:
        merged = combine(merged, "Program")

    if 'Term_x' in merged.columns and 'Term_y' in merged.columns:
        merged = combine(merged, "Term")

    if 'Pronouns_x' in merged.columns and 'Pronouns_y' in merged.columns:
        merged = combine(merged, "Pronouns")

    if 'Email_x' in merged.columns and 'Email_y' in merged.columns:
        merged = concatCombine(merged, "Email")

    if 'Terms in Tech+_x' in merged.columns and 'Terms in Tech+_y' in merged.columns:
        merged.loc[merged['Terms in Tech+_y'].isnull(), 'Terms in Tech+'] = merged['Terms in Tech+_x']
        merged.loc[merged['Terms in Tech+_x'].isnull(), 'Terms in Tech+'] = merged['Terms in Tech+_y']
        merged.loc[(merged['Terms in Tech+_x'].notnull() & merged['Terms in Tech+_y'].notnull() & merged['Terms in Tech+_x'].str.contains(term, regex=False, na=False)), 'Terms in Tech+'] = merged['Terms in Tech+_x']
        merged.loc[(merged['Terms in Tech+_x'].notnull() & merged['Terms in Tech+_y'].notnull() & ~(merged['Terms in Tech+_x'].str.contains(term, regex=False, na=False))), 'Terms in Tech+'] = merged['Terms in Tech+_x'] + ", " + merged['Terms in Tech+_y']
        
        merged.drop(['Terms in Tech+_x', 'Terms in Tech+_y'], inplace=True, axis=1)

    return merged

# dictionaries to rename columns
coffeeChatsRename = {"Email Address":"Email","Preferred First Name":"First Name", "Preferred Pronouns (if you are comfortable sharing)":"Pronouns", "Academic Program ":"Academic Program", "Fall 2020 School Term:":"Term"}
resumeCritiqueRename = {"Username":"Email","First Name:":"First Name", "Last Name:":"Last Name", "What are your pronouns?":"Pronouns", "Academic Program:":"Academic Program", "Fall 2020 School Term:":"Term"}
kickoffRename = {"Email Address:":"Email","First Name:":"First Name", "Last Name:":"Last Name", "Academic program:":"Academic Program"}
mentorshipRename = {"Email Address":"Email", "Fall 2020 School Term:":"Term"}

# clean and merge each dataframe with final dataframe, starting from oldest to newest to ensure newer data replaces older data
mentorshipDatabase = cleanData(s20CoffeeChatsMentees, "S20 Coffee Chat Mentee", coffeeChatsRename, 'S20')
mentorshipDatabase = cleanData(s20CoffeeChatsMentors, "S20 Coffee Chat Mentee", coffeeChatsRename, 'S20')
mentorshipDatabase = cleanData(f20ResumeCritiqueReviewee, "F20 Resume Critique Reviewee", resumeCritiqueRename, 'F20')
mentorshipDatabase = cleanData(f20ResumeCritiqueReviewer, "F20 Resume Critique Reviewer", resumeCritiqueRename, 'F20')
mentorshipDatabase = cleanData(f20KickoffQna, "F20 Tech+ 101 Kickoff Attendee", kickoffRename, 'F20')
mentorshipDatabase = cleanData(f20Mentors, "F20 Mentor", mentorshipRename, 'F20')
mentorshipDatabase = cleanData(f20Mentees, "F20 Mentee", mentorshipRename, 'F20')

# remove any potential duplicates
mentorshipDatabase.drop_duplicates()

# export as csv
mentorshipDatabase.to_csv("mentorshipDatabase.csv")
