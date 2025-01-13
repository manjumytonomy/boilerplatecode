import docx
import os
import pandas as pd

word_docs_path = "/Users/vikram/Work/Mytonomy/WE Stage/Folder Storage/super_admin/Word Docs"
excel_save_path = "/Users/vikram/Work/Mytonomy/WE Stage/Folder Storage/super_admin/EpicMetaTagSpreadsheet/customer-epic-ready.xlsx"

column_titles = ["Customer", "Logo", "Condition Area", "Filepath", "Title", "Unique Name", "Keyword", "Diagnosis Code", "CPT Code", 
                "Language", "Corresponding Language", "Language Index", "Source", "Document Type", "QR Code", "Short URL", "Customer Disclaimer"]
column_titles_lower = [title.lower() for title in column_titles]
df = pd.DataFrame(columns=column_titles)

for root, dirs, files in os.walk(word_docs_path):
    for file in files:
        if file.endswith(".docx"):
            doc_filepath = os.path.join(root, file)
            print(doc_filepath)
            # Load the Word document
            doc = docx.Document(doc_filepath)

            # Get the first table in the document
            table = doc.tables[0]

            # Extract the column value pairs
            data = {}
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text)

                cell_type = row_data[0].lower()
                if cell_type == 'icd 10 codes':
                    row_data[0] = 'Diagnosis Code'
                elif cell_type == 'cpt codes':
                    row_data[0] = 'CPT Code'
                elif cell_type == 'metatags':
                    row_data[0] = 'Keyword'
                
                if row_data[0] in column_titles:
                    data[row_data[0]] = row_data[1]
                elif cell_type in column_titles_lower:
                    loc = column_titles_lower.index(cell_type)
                    data[column_titles[loc]] = row_data[1]

            data['Filepath'] = doc_filepath[len(word_docs_path):].replace('.docx', '.pdf')
            data['Document Type'] = 'Patient Education'
            data['Source'] = 'Mytonomy'

            if 'ES' in data['Filepath']:
                data['Language'] = 'Spanish'
            else:
                data['Language'] = 'English'

            # Check if the Filepath exists in the dataframe
            if data['Filepath'] in df['Filepath'].values:
                # Update the existing row
                df.loc[df['Filepath'] == data['Filepath'], list(data.keys())] = list(data.values())
            else:
                # Append a new row
                df = pd.concat([df, pd.DataFrame([data], columns=column_titles)], ignore_index=True)

df.to_excel(excel_save_path, index=False)