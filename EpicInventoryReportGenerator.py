import os
import pandas as pd

spreadsheet_path = "/Users/vikram/Downloads/AAH_March_2025_EpicMetaData - Locked.xlsx"
package_path = "/Users/vikram/Mytonomy Inc Dropbox/Vikram Rao/WE-Tester01/AAH/March 2025 Delivery/AAH 303_03_16_2025-M-S"
report_path = "Report.xlsx"

html_dir = os.path.join(package_path, "HTML Package", "HTML")
pdf_dir = os.path.join(package_path, "PDFs")

df = pd.read_excel(spreadsheet_path)
df['Filepath'] = df['Filepath'].astype(str)
df['Title'] = df['Title'].astype(str)
df = df.sort_values(by='Filepath').reset_index(drop=True)

pdf_files = []
for root, dirs, files in sorted(os.walk(pdf_dir)):
    dirs.sort()  # Sort directories alphabetically to ensure ordered traversal
    files.sort()  # Sort files alphabetically
    
    for file in files:
        if file.endswith(".pdf"):
            filepath = os.path.join(root, file)
            idx = len(pdf_dir)
            pdf_files.append(filepath[idx:])

html_files = []
for root, dirs, files in sorted(os.walk(html_dir)):
    dirs.sort()  # Sort directories alphabetically to ensure ordered traversal
    files.sort()  # Sort files alphabetically
    
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            idx = len(html_dir)
            html_files.append(filepath[idx:])


report_data = []  # List to store the final data
html_filepaths = []

for index, row in df.iterrows():
    spreadsheet_filepath = row['Filepath']
    spreadsheet_title = row['Title']

    html_filepath = os.path.join(os.path.dirname(spreadsheet_filepath), spreadsheet_title + '.html')
    html_filepaths.append(html_filepath)

    # Your custom logic for matching:
    matched_pdf = next((pdf for pdf in pdf_files if spreadsheet_filepath in pdf), None)
    matched_html = next((html for html in html_files if html_filepath in html), None)

    # Append the row as a list
    report_data.append([spreadsheet_filepath, spreadsheet_title, matched_pdf, matched_html])

mismatched_pdfs = [f for f in pdf_files if f not in df['Filepath'].to_list()]
mismatched_htmls = [f for f in html_files if f not in html_filepaths]

for file in mismatched_pdfs:
    report_data.append([None, None, file, None])
for file in mismatched_htmls:
    report_data.append([None, None, None, file])

report_df = pd.DataFrame(report_data, columns=['Spreadsheet Filepath', 'Spreadsheet Title', 'PDF Filepath', 'HTML Filepath'])
report_df.to_excel(report_path)
