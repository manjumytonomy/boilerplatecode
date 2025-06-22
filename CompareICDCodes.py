import pandas as pd
from rapidfuzz import fuzz

def best_fuzzy_match_index_score(df: pd.DataFrame, column_name: str, query: str):
    scores = df[column_name].apply(lambda x: fuzz.ratio(str(x), query))
    best_index = scores.idxmax()
    best_score = scores.loc[best_index]
    return best_index, best_score

match_column = 'Filepath'

mytonomy_spreadsheet = "/Users/vikram/Downloads/test/Mytonomy Merged A-Z HTML Package - May 2025 Release - MetaData Extract (1).xlsx"
df_mytonomy = pd.read_excel(mytonomy_spreadsheet, sheet_name="Sheet1")

inova_spreadsheet = "/Users/vikram/Downloads/test/Written Asset Metatags - Inova_Rev.Aug2024 - New Diagnosis Codes.xlsx"
df_inova = pd.read_excel(inova_spreadsheet, sheet_name="Sheet1")

carolina_east_spreadsheet = "/Users/vikram/Downloads/test/WE Metatags - CarolinaEast_Rev.092724 (1).xlsx"
df_carolina_east = pd.read_excel(carolina_east_spreadsheet, sheet_name="Sheet1")

output_path = "/Users/vikram/Downloads/test/ICD_Comparison.xlsx"

df = pd.DataFrame(columns=[
    'Mytonomy Filepath', 'Mytonomy Title', 'Mytonomy Diagnosis Code', 'Mytonomy New Diagnosis Code',
    'Inova Filepath', 'Inova Title', 'Inova Diagnosis Code', 'Inova New Diagnosis Code', 'Inova Match Score',
    'Carolina East Filepath', 'Carolina East Title', 'Carolina East Diagnosis Code', 'Carolina East New Diagnosis Code', 'Carolina East Match Score'
])

df['Mytonomy Filepath'] = df_mytonomy['Filepath']
df['Mytonomy Title'] = df_mytonomy['Title']
df['Mytonomy Diagnosis Code'] = df_mytonomy['Diagnosis Code']
df['Mytonomy New Diagnosis Code'] = df_mytonomy['New Diagnosis Code']

mytonomy_match_column = None
if match_column == 'Title':
    mytonomy_match_column = 'Mytonomy Title'
elif match_column == 'Filepath':
    mytonomy_match_column = 'Mytonomy Filepath'

for i, row in df.iterrows():
    match_val = df.loc[i, mytonomy_match_column]

    best_index, best_score = best_fuzzy_match_index_score(df_inova, match_column, match_val)
    df.loc[i, 'Inova Filepath'] = df_inova.loc[best_index, 'Filepath']
    df.loc[i, 'Inova Title'] = df_inova.loc[best_index, 'Title']
    df.loc[i, 'Inova Diagnosis Code'] = df_inova.loc[best_index, 'Diagnosis Code']
    df.loc[i, 'Inova New Diagnosis Code'] = df_inova.loc[best_index, 'New Diagnosis Code']
    df.loc[i, 'Inova Match Score'] = best_score

    best_index, best_score = best_fuzzy_match_index_score(df_carolina_east, match_column, match_val)
    df.loc[i, 'Carolina East Filepath'] = df_carolina_east.loc[best_index, 'Filepath']
    df.loc[i, 'Carolina East Title'] = df_carolina_east.loc[best_index, 'Title']
    df.loc[i, 'Carolina East Diagnosis Code'] = df_carolina_east.loc[best_index, 'Diagnosis Code']
    df.loc[i, 'Carolina East New Diagnosis Code'] = df_carolina_east.loc[best_index, 'New Diagnosis Code']
    df.loc[i, 'Carolina East Match Score'] = best_score

df.to_excel(output_path)
