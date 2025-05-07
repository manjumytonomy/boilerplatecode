import os
import pandas as pd

'''
This script updates the destination Excel file with values from the source Excel file based on a matching column.
The script performs the following steps:
1. Reads the source and destination Excel files into pandas DataFrames.
2. Cleans the file paths in the source DataFrame if necessary.
3. Iterates through the destination DataFrame and checks if the cleaned file path exists in the source DataFrame.
4. If a match is found, it copies the relevant columns from the source row to the destination row.
5. Marks the updated rows in the destination DataFrame.
6. Saves the updated destination DataFrame to a new Excel file.
'''

# Source spreadsheet params
source_path = '/Users/vikram/Downloads/Inova A-B PDFs (1).xlsx'
match_column_source = 'HTML Filepath'
cols_to_copy_source = ['Old Diagnosis Code']

# Destination spreadsheet params
destination_path = '/Users/vikram/Downloads/Mytonomy MASTER All Files 05_05_2025 HTML UPDATED Codes.xlsx'
match_column_destination = 'Filepath'
cols_to_copy_destination = ['Diagnosis Code']

# Program result save path
result_path = '/Users/vikram/Downloads/Mytonomy MASTER All Files 05_05_2025 HTML UPDATED Codes - Updated.xlsx'

# Boolean flag if cleaning is needed (set to True only if using Filepath as match column)
cleaning_needed = True

# Main logic
df_source = pd.read_excel(source_path)
df_destination = pd.read_excel(destination_path)

LANGUAGE_CODES = {
    'English': 'EN',
    'Spanish': 'ES',
    'French': 'FR',
    'Chinese': 'ZH',
    'Korean': 'KO',
    'Vietnamese': 'VI',
    'Russian': 'RU',
}

def clean_filepath(path):
    path = os.path.splitext(path)[0].strip()
    for code in LANGUAGE_CODES.values():
        if path.endswith(code):
            path = path[:-2].strip()
            break
    path = '/'.join(path.split('/')[-2:])
    return path

df_source['Cleaned Filepath'] = df_source[match_column_source]
if cleaning_needed:
    df_source['Cleaned Filepath'] = df_source['Cleaned Filepath'].apply(clean_filepath)

df_destination['Row Updated'] = 'No'
source_match_col_values = []
    
for i, row in df_destination.iterrows():
    cleaned_filepath = row[match_column_destination]
    if cleaning_needed:
        cleaned_filepath = clean_filepath(cleaned_filepath)
    # Check if the cleaned filepath exists in the source DataFrame
    if cleaned_filepath in df_source['Cleaned Filepath'].values:
        # Get the corresponding row from the source DataFrame
        source_row = df_source[df_source['Cleaned Filepath'] == cleaned_filepath].iloc[0]
        
        # Copy the relevant columns from the source row to the destination row
        for j, col in enumerate(cols_to_copy_source):
            df_destination.at[i, cols_to_copy_destination[j]] = source_row[col]

        df_destination.at[i, 'Row Updated'] = 'Yes'
        source_match_col_values.append(source_row[match_column_source])

source_match_col_values = list(set(source_match_col_values))

print(f"Number of rows in source file: {len(df_source)}")
print(f"Number of rows in destination file: {len(df_destination)}")

# Extract the match column destination values that were updated
updated_values = df_destination.loc[df_destination['Row Updated'] == 'Yes', match_column_destination].tolist()
print(f"Updated {len(updated_values)} rows in the destination file, using {len(source_match_col_values)} rows from the source file.")

df_destination.to_excel(result_path, index=False)
print(f"Updated Excel file saved to: {result_path}")