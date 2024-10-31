import os
import pandas as pd

# Top-level folder
root_dir = '/Users/Manju/Work/WrittenEducation Project/Customer Releases/Carolina East/166 Carolina East PDFS 10-24-24'

# Excel files
metadata_file = 'WE Metatags - CarolinaEast_Rev.092724.xlsx'
output_file = 'Written QA - CarolinaEast Oct 28 -2024.xlsx'

# Load metadata Excel file
metadata_df = pd.read_excel(metadata_file)

# Initialize output DataFrame
output_df = pd.DataFrame(columns=['File Name', 'Condition Area', 'Metadata'])

# Walk the directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        # Search for file name in metadata Excel file
        metadata_match = metadata_df[metadata_df['Filepath'].str.contains(file)]
        
        if not metadata_match.empty:
            # Retrieve matching metadata and condition area
            metadata = metadata_match.iloc[0]['Filepath']c
            condition_area = metadata_match.iloc[0]['Condition Area']
            
            # Append to output DataFrame
            output_df = pd.concat([output_df, pd.DataFrame({'File Name': [file], 'Condition Area': [condition_area], 'Metadata': [metadata]})], ignore_index=True)

# Save output to Excel file
output_df.to_excel(output_file, index=False)
