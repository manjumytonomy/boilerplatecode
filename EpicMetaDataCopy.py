import os
import pandas as pd

def clean_filepath(path):
    idx = 0
    for i, char in enumerate(path):
        if i < len(path) - 2:
            if (path[i].isdigit() and path[i+1].isdigit() and path[i+2] == '-') or (path[i].isdigit() and path[i+1] == '-'):
                idx = i-1
                break
    return path[:idx].strip()

destination_path = "/Users/vikram/Downloads/EpicMetaTagSpreadsheet/Mytonomy WE Epic Metadata.xlsx"
source_path = "/Users/vikram/Downloads/AAH_March_2025_EpicMetaData - Locked.xlsx"

df1 = pd.read_excel(destination_path)
df2 = pd.read_excel(source_path)

df1['Cleaned Filepath'] = df1['Filepath'].apply(clean_filepath)
df2['Cleaned Filepath'] = df2['Filepath'].apply(clean_filepath)

match_column = 'Cleaned Filepath'

columns_to_copy = ['Title', 'Unique Name', 'Keyword', 'Diagnosis Code', 'CPT Code']

# Merge df1 with df2 on the match column (using a left join to preserve df1 structure)
df1_updated = df1.merge(df2[[match_column] + columns_to_copy], on=match_column, how="left", suffixes=("", "_new"))

# Update the original columns in df1 with values from df2 (avoiding NaN overwrites)
for col in columns_to_copy:
    df1_updated[col] = df1_updated[col + "_new"].combine_first(df1_updated[col])
    df1_updated.drop(columns=[col + "_new"], inplace=True)

df1_updated.drop(columns=['Cleaned Filepath'], inplace=True)
# Save the updated DataFrame to Excel
output_path = 'AAH Spanish 103_03_17_2025.xlsx'
df1_updated.to_excel(output_path, index=False)
