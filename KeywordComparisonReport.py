import pandas as pd
import xlsxwriter

# --- CONFIGURATION ---
# Set your spreadsheet paths here
# path_june26 = '/mnt/c/Users/bhoom/Downloads/Mytonomy Consolidated Package MetaData Extract June 26 2025 Snapshot (1).xlsx'
# path_nlp = '/mnt/c/Users/bhoom/Downloads/Batch 1 - 3 Metadata Updated with Integrated Tool (1).xlsx'
# path_imo = '/mnt/c/Users/bhoom/Downloads/Sep-06-2025-English 1631 PDFs Epic Metadata (1).xlsx'
path_june26 = '/Users/vikram/Downloads/Mytonomy Consolidated Package MetaData Extract June 26 2025 Snapshot English.xlsx'
path_nlp = '/Users/vikram/Downloads/Batch 1 - 3 Metadata Updated with Integrated Tool English.xlsx'
path_imo = '/Users/vikram/Downloads/Sep-08-2025-English 1631 PDFs Epic Metadata.xlsx'

# --- UTILITY FUNCTIONS ---


def get_match_key(row, is_imo=False):
    # Use 'HTML Filepath' for IMO spreadsheet, 'Filepath' for others
    #column_name = 'HTML Filepath' if is_imo else 'Filepath'
    column_name = 'Unique Name'
    return str(row[column_name]).strip() if column_name in row else ''

def get_keywords_str(row):
    # Return the raw keyword string from the 'Keyword' column
    return str(row['Keyword']).strip() if 'Keyword' in row else ''

def get_keywords_set(keyword_str):
    # Convert a keyword string to a set of keywords
    return set([kw.strip() for kw in keyword_str.split(',') if kw.strip()])

def get_filepath(row, is_imo=False):
    # Extract the Filepath or HTML Filepath from your spreadsheet row
    column_name = 'HTML Filepath' if is_imo else 'Filepath'
    return str(row[column_name]).strip() if column_name in row else ''

# --- READ SPREADSHEETS ---
df_june26 = pd.read_excel(path_june26)
df_imo = pd.read_excel(path_imo)
df_nlp = pd.read_excel(path_nlp)

# --- BUILD LOOKUPS ---


def build_lookup(df, is_imo=False):
    lookup = {}
    for _, row in df.iterrows():
        match_key = get_match_key(row, is_imo)
        keywords_str = get_keywords_str(row)
        filepath = get_filepath(row, is_imo)
        lookup[match_key] = {
            'keywords_str': keywords_str,
            'keywords_set': get_keywords_set(keywords_str),
            'filepath': filepath
        }
    return lookup


lookup_june26 = build_lookup(df_june26)
lookup_imo = build_lookup(df_imo, is_imo=True)
lookup_nlp = build_lookup(df_nlp)

# Use Filepath as the match key
all_match_keys = set(lookup_june26.keys()) | set(lookup_imo.keys()) | set(lookup_nlp.keys())

# --- COMPARISON FUNCTION ---


def make_comparison_sheet(main_lookup, compare_lookup, main_label, compare_label):
    output_rows = []
    for match_key in all_match_keys:
        main_info = main_lookup.get(match_key, {'keywords_str': '', 'keywords_set': set(), 'filepath': ''})
        compare_info = compare_lookup.get(match_key, {'keywords_str': '', 'keywords_set': set(), 'filepath': ''})
        main_keywords_set = main_info['keywords_set']
        compare_keywords_set = compare_info['keywords_set']
        addition = main_keywords_set - compare_keywords_set
        deletion = compare_keywords_set - main_keywords_set
        output_rows.append({
            f'File Name {main_label}': main_info['filepath'],
            f'Keywords {main_label}': main_info['keywords_str'],
            f'File Name {compare_label}': compare_info['filepath'],
            f'Keywords {compare_label}': compare_info['keywords_str'],
            'Addition': ', '.join(sorted(addition)),
            'Addition Count': len(addition),
            'Deletion': ', '.join(sorted(deletion)),
            'Deletion Count': len(deletion),
            'Difference Count': len(addition) + len(deletion),
        })
    columns = [
        f'File Name {main_label}',
        f'Keywords {main_label}',
        f'File Name {compare_label}',
        f'Keywords {compare_label}',
        'Addition',
        'Addition Count',
        'Deletion',
        'Deletion Count',
        'Difference Count',
    ]
    df = pd.DataFrame(output_rows, columns=columns)
    df.sort_values(by=f'File Name {main_label}', ascending=True, inplace=True)
    return df

# --- CREATE DATAFRAMES FOR EACH COMPARISON ---
df_june26_imo_sheet = make_comparison_sheet(
    lookup_june26, lookup_imo, 'June26', 'IMO')
df_nlp_imo_sheet = make_comparison_sheet(
    lookup_nlp, lookup_imo, 'NLP_CDC_Alex', 'IMO')
df_june26_nlp_sheet = make_comparison_sheet(
    lookup_june26, lookup_nlp, 'June26', 'NLP_CDC_Alex')

# --- WRITE TO EXCEL WITH FORMATTING ---
with pd.ExcelWriter('KeywordComparisonReport.xlsx', engine='xlsxwriter') as writer:
    # Add summary sheet as the first sheet
    summary_data = [
        {'File Name': 'June26', 'File Path': path_june26},
        {'File Name': 'NLP_CDC_Alex', 'File Path': path_nlp},
        {'File Name': 'IMO', 'File Path': path_imo},
    ]

    df_summary = pd.DataFrame(summary_data, columns=['File Name', 'File Path'])
    df_summary.to_excel(writer, sheet_name='Summary', index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Summary']
    wrap_format = workbook.add_format({'text_wrap': True})
    worksheet.set_column(0, 0, 20, wrap_format)
    worksheet.set_column(1, 1, 80, wrap_format)

    # Add hyperlinks for file paths in summary sheet
    for row_num, file_path in enumerate(df_summary['File Path'], start=1):
        worksheet.write_url(row_num, 1, f'file:///{file_path}', string=file_path, cell_format=wrap_format)

    # Now add the three comparison sheets
    for df, sheet_name in [
        (df_june26_imo_sheet, 'June26 vs IMO'),
        (df_nlp_imo_sheet, 'NLP_CDC_Alex vs IMO'),
        (df_june26_nlp_sheet, 'June26 vs NLP_CDC_Alex')
    ]:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        # Formatting
        add_format = workbook.add_format({'bg_color': '#C6EFCE', 'border': 1, 'text_wrap': True})  # Green for Addition
        del_format = workbook.add_format({'bg_color': '#FFC7CE', 'border': 1, 'text_wrap': True})  # Red for Deletion
        wrap_format = workbook.add_format({'text_wrap': True})
        # Set fixed column widths for readability
        col_widths = {
            'File Name June26': 30,
            'File Name IMO': 30,
            'File Name NLP_CDC_Alex': 30,
            'Keywords June26': 40,
            'Keywords IMO': 40,
            'Keywords NLP_CDC_Alex': 40,
            'Addition': 30,
            'Addition Count': 15,
            'Deletion': 30,
            'Deletion Count': 15,
            'Difference Count': 18,
        }
        for idx, col in enumerate(df.columns):
            width = col_widths.get(col, 20)
            worksheet.set_column(idx, idx, width, wrap_format)
        # Apply green to Addition and red to Deletion columns for all rows
        if 'Addition' in df.columns:
            addition_col = df.columns.get_loc('Addition')
            for row_num in range(1, len(df) + 1):
                worksheet.write(row_num, addition_col, df.iloc[row_num - 1, addition_col], add_format)
        if 'Deletion' in df.columns:
            deletion_col = df.columns.get_loc('Deletion')
            for row_num in range(1, len(df) + 1):
                worksheet.write(row_num, deletion_col, df.iloc[row_num - 1, deletion_col], del_format)
print("Report generated: KeywordComparisonReport.xlsx")

