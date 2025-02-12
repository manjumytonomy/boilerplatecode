import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import language_tool
import xlsxwriter
import re

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize language tool
tool = language_tool.LanguageTool('en-US')

# Top-level directory
root_dir = '/Users/Manju/Work/WrittenEdGitLocal/WE Stage/Folder Storage/HTML'

# Initialize lists to store data
file_names = []
errors = []

# Recursively traverse directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            # Extract HTML content
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
                
                # Tokenize sentences
                sentences = sent_tokenize(text)
                
                # Initialize error list for current file
                file_errors = []
                
                # Identify grammar issues
                for sentence in sentences:
                    matches = tool.check(sentence)
                    for match in matches:
                        file_errors.append(f"Issue: {match.msg}, Sentence: {sentence}, Correction: {match.replacements[0]}")
                        
                # Identify word spacing issues
                word_spacing_issues = re.findall(r'\s+', text)
                if word_spacing_issues:
                    file_errors.append(f"Word spacing issue: Multiple spaces found")
                    
                # Identify paragraph spacing issues
                paragraph_spacing_issues = re.findall(r'\n\s*\n', text)
                if paragraph_spacing_issues:
                    file_errors.append(f"Paragraph spacing issue: Inconsistent spacing found")
                    
                # Log errors for current file
                if file_errors:
                    file_names.append(file_path)
                    errors.append('\n'.join(file_errors))

# Create Excel spreadsheet
workbook = xlsxwriter.Workbook('grammar_errors.xlsx')
worksheet = workbook.add_worksheet()

# Write header row
worksheet.write(0, 0, 'File Path')
worksheet.write(0, 1, 'Errors')

# Write data rows
for i in range(len(file_names)):
    worksheet.write(i + 1, 0, file_names[i])
    worksheet.write(i + 1, 1, errors[i])

# Close workbook
workbook.close()
