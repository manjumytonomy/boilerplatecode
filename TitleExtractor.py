import os
import pandas as pd
from bs4 import BeautifulSoup

#Install the pre-requisite packages to run this python program which extracts the title from all the htmls within a Customer Package
#pip3 install openpyxl
#pip3 install pandas
#pip3 install bs4
#you can also use .venv to create your own virtual environment for python to install the above packages and run the python program
# - refer "Development Notes"   in Google Drive

# Top-level directory
root_dir = '/path/to/your/directory'
root_dir='/Users/Manju/Work/WrittenEducation Project/Carolina East Updated with PI 10-5-2024/HTML'
# Excel file output
output_file = 'title_tags.xlsx'

# Initialize lists to store data
file_names = []
directory_locations = []
title_tags = []

# Recursively traverse directories
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                title = soup.find('title').text.strip() if soup.find('title') else 'No title tag'
                file_names.append(file)
                directory_locations.append(os.path.relpath(root, root_dir))
                title_tags.append(title)

# Create DataFrame and save to Excel
df = pd.DataFrame({
    'File Name': file_names,
    'Directory Location': directory_locations,
    'Value of the <title> tag': title_tags
})

df.to_excel(output_file, index=False)