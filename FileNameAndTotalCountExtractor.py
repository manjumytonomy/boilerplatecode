import os
import xlsxwriter

# Top-level directory
root_dir = '/Users/Manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Carolina East Nov-1-2024-Delivery/HTML Package/HTML'

# Initialize file count
file_count = 0

# Initialize lists to store data
file_names = []
subdirectories = []

# Recursively traverse directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.pdf'):
            file_names.append(file)
            subdirectories.append(os.path.relpath(root, root_dir))
            file_count += 1

# Get top-level subdirectory name
top_level_dir = os.path.basename(root_dir)

# Create Excel spreadsheet
workbook = xlsxwriter.Workbook(f'{top_level_dir}_file_list.xlsx')
worksheet = workbook.add_worksheet()

# Write header row
worksheet.write(0, 0, 'File Name')
worksheet.write(0, 1, 'Subdirectory')

# Write data rows
for i in range(len(file_names)):
    worksheet.write(i + 1, 0, file_names[i])
    worksheet.write(i + 1, 1, subdirectories[i])

# Write total file count
worksheet.write(len(file_names) + 1, 0, 'Total Files:')
worksheet.write(len(file_names) + 1, 1, file_count)

# Close workbook
workbook.close()
