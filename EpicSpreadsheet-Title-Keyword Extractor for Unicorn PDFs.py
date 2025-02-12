import os
import fitz
import re
import numpy as np
import pandas as pd

#Flag to determine if the PDFs are from Unicorn template
IS_UNICORN_TEMPLATE = True

#folder_path="/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/4b_CONTENT_FINAL_WE"
#folder_path="/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East 10-4-24 PDFs"
folder_path = "/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/4c_CONTENT_FINAL_WE_CUSTOM/Mytonomy WE for AAH Published 01.31.2025"

destination_folder = '/Users/manju/Work/BoilerPlateCodeGitLocal/EpicSpreadsheetTitleKeywordExtractor' # Destination folder where files will be copied

# Create a Logs folder outside the destination folder to log debug and error messages
log_folder = os.path.join(os.path.dirname(destination_folder), 'Logs')
os.makedirs(log_folder, exist_ok=True)  # Create the Logs folder if it doesn't exist

# Define log file paths for debugging and error logs
debug_log = os.path.join(log_folder, 'debug.log')  # File to log debug messages
error_log = os.path.join(log_folder, 'error.err')  # File to log error messages

# Function to log messages to respective log files
def log_message(message, level='debug'):
    """Log messages to appropriate log files (debug or error)."""
    log_path = debug_log if level == 'debug' else error_log
    with open(log_path, 'a') as log:
        log.write(message + '\n')  # Append the log message to the respective log file

def generate_span_df(doc):
    # Open the PDF document

    # Extract text blocks only from the first page
    page = doc[0]
    output = page.get_text("blocks", flags=1+2+8)

    previous_block_id = 0
    plain_text_list = []

    # Extract and clean text using Unidecode
    for block in output:
        if block[6] == 0:  # Only take the text
            plain_text = block[4]
            plain_text_list.append(plain_text)

    # Span extraction for deeper text analysis
    block_dict = {}
    page_num = 1

    # Create a block dictionary for 1st page
    file_dict = page.get_text('dict', flags = 1+2+8)
    blocks = file_dict['blocks']
    block_dict[page_num] = blocks

    # Iterate over blocks, lines, and spans
    rows = []
    for page_num, blocks in block_dict.items():
        for block in blocks:
            if block['type'] == 0:  # Only text blocks
                block_id = block['number'] 
                for line in block['lines']:
                    for span in line['spans']:
                        xmin, ymin, xmax, ymax = list(span['bbox'])
                        font_size = span['size']
                        text = span['text']
                        span_font = span['font']

                        is_upper = False
                        is_bold = False

                        if "bold" in span_font.lower():
                            is_bold = True
                        if re.sub(r"[\(\[].*?[\)\]]", "", text).isupper():
                            is_upper = True

                        if text.replace(" ", "") != "":
                            rows.append((page_num, block_id, xmin, ymin, xmax, ymax, text, is_upper, is_bold, span_font, font_size))

    span_df = pd.DataFrame(rows, columns=['page_num', 'block_id', 'xmin', 'ymin', 'xmax', 'ymax', 'text', 'is_upper', 'is_bold', 'span_font', 'font_size'])

    # Determine 'p' (paragraph) size based on text style frequencies
    span_scores = []
    special = '[(_:/,#%\\=@)]'

    for index, span_row in span_df.iterrows():
        score = round(span_row.font_size)
        text = span_row.text

        if not re.search(special, text):
            if span_row.is_bold:
                score += 1
            if span_row.is_upper:
                score += 1
        span_scores.append(score)

    values, counts = np.unique(span_scores, return_counts=True)
    style_dict = {value: count for value, count in zip(values, counts)}

    p_size = max(style_dict, key=style_dict.get)

    # Assign tags to different text styles
    tag = {}
    idx = 0

    for size in sorted(values, reverse=True):
        idx += 1
        if size == p_size:
            idx = 0
            tag[size] = 'p'
        elif size > p_size:
            tag[size] = f'h{idx}'
        else:
            tag[size] = f's{idx}'

    span_tags = [tag[score] for score in span_scores]
    span_df['tag'] = span_tags
    return span_df

def main(): 
    folder = folder_path.split(os.sep)[-1]
    df = pd.DataFrame(columns=["Customer", "Logo", "Logo", "Condition Area", "Filepath", "Title", "Unique Name", "Keyword", "Diagnosis Code", "CPT Code", 
                               "Language", "Corresponding Language", "Language Index", "Source", "Document Type", "QR Code", "Short URL", "Customer Disclaimer"])
    
    filepaths = []
    titles = []
    keywords = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            try:
                if filename.endswith('.pdf'):
                    pdf_path = os.path.join(dirpath, filename)
                    idx = pdf_path.find(folder)
                    filepaths.append(os.sep + pdf_path[idx:])
                    
                    doc = fitz.open(pdf_path)
                    if IS_UNICORN_TEMPLATE:
                        span_df = generate_span_df(doc)
                        # Find the first instance where page_num is 1 and tag is 'h1', then return only the text
                        first_h1_text = span_df.loc[(span_df['page_num'] == 1) & (span_df['tag'] == 'h1'), 'text'].iloc[0]
                        titles.append(first_h1_text)
                    else:
                        titles.append(doc.metadata.get('title'))
                        keywords.append(doc.metadata.get('keywords'))
            except Exception as e:
                log_message(f"Error processing file: {pdf_path} - {e}", level='error')
                titles.append(f"Unable to convert PDF file to HTML!")
    
    df["Filepath"] = filepaths
    df["Title"] = titles
    if not IS_UNICORN_TEMPLATE:
        df["Keyword"] = keywords

    df.to_excel(f'{folder}.xlsx')

if __name__ == "__main__":
    main()
