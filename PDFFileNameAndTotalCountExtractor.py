import os
import xlsxwriter

# Top-level directory
#root_dir = '/Users/Manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Carolina East Nov-1-2024-Delivery/HTML Package/HTML'
#root_dir = '/Users/Manju/Mytonomy Inc Dropbox/Manju Komarlu/4c_CONTENT_FINAL_WE_CUSTOM/5. Advocate Aurora Health - Batch 3.2'
root_dir = '/Users/manju/Work/WrittenEducation Project/Customer Releases/AAH/PDFs/AAH 326_02_11_25-E-J/PDFs/Mytonomy WE/English'


# Initialize file count
file_count = 0

# Initialize lists to store data
pdf_file_paths = []
file_names = []

# Recursively traverse directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.pdf'):
            # Get the relative path from the root_dir
            relative_path = os.path.relpath(root, os.path.dirname(root_dir))
            # Combine the relative path and file name
            pdf_file_path = os.path.join(relative_path, file)
            pdf_file_paths.append(pdf_file_path)
            file_names.append(file)
            file_count += 1

# Get top-level subdirectory name
top_level_dir = os.path.basename(root_dir)

# Create Excel spreadsheet
workbook = xlsxwriter.Workbook(f'{top_level_dir}_file_list.xlsx')
worksheet = workbook.add_worksheet()

# Write header row
worksheet.write(0, 0, 'PDF File Path')
worksheet.write(0, 1, 'PDF File')

# Write data rows
for i in range(len(pdf_file_paths)):
    worksheet.write(i + 1, 0, pdf_file_paths[i])
    worksheet.write(i + 1, 1, file_names[i])

# Write total file count
worksheet.write(len(pdf_file_paths) + 1, 0, 'Total Files:')
worksheet.write(len(pdf_file_paths) + 1, 1, file_count)

# Close workbook
workbook.close()