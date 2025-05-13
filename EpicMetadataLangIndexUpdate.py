import pandas as pd
import os

spreadsheet_path = '/Users/vikram/Downloads/Mytonomy MASTER All Files 05_05_2025 HTML UPDATED Codes.xlsx'
result_path = '/Users/vikram/Downloads/Mytonomy MASTER All Files 05_05_2025 HTML UPDATED Codes - Updated.xlsx'

df = pd.read_excel(spreadsheet_path)
df = df.rename(columns={'Language Index': 'Language Index Old'})
loc = df.columns.get_loc('Language Index Old')
df.insert(loc, 'Language Index', '')

for i, row in df.iterrows():
    li = row['Language Index Old']
    if li and type(li) == str and li != 'nan':
        li_list = li.split('\n')
        unique_name_list = []
        for item in li_list:
            filename = os.path.basename(item)
            title, ext = os.path.splitext(filename)
            filtered_df = df[df['Title'] == title]
            if filtered_df.empty:
                print(f'Error: No matched row found for Language Index: {item} at row {i}')
                continue
            matched_row = filtered_df.iloc[0]
            unique_name_list.append(matched_row['Unique Name'])
        df.at[i, 'Language Index'] = '\n'.join(unique_name_list)

df.to_excel(result_path)
