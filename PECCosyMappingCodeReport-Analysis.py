# prints the total number of rows in each tab: code will print the total number of rows in each tab (PPR-Cosy, PPR-Stage, and PPR-Prod) at the end of the report.

import pandas as pd

# Load the Excel file
def load_excel_file(file_path):
    try:
        excel_file = pd.ExcelFile(file_path)
        return excel_file
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# Compare data across tabs and generate a report
def generate_report(excel_file):
    # Define the reference data tab
    reference_tab = 'PPR-COSY'
    
    # Define the column names
    column_names = [
        'PECStageModuleId', 
        'PECStageModuleName', 
        'MappedInboundCode', 
        'MappedModuleOutboundCode', 
        'MappedModuleOutBoundDescription', 
        'PECPlayListId', 
        'PECCPlayListName', 
        'MappedPlaylistOutboundCode', 
        'MappedPlaylistOutboundTitle', 
        'PECVideoId', 
        'PECCVideoId', 
        'MappedVideoOutboundCode', 
        'MappedVideoOutboundTitle'
    ]
    
    # Load the reference data
    reference_data = pd.read_excel(excel_file, sheet_name=reference_tab)
    reference_data.columns = column_names
    
    # Initialize a dictionary to store the report data
    report_data = {}
    
    # Initialize variables to store the total number of missing rows
    total_missing_rows_stage = 0
    total_missing_rows_prod = 0
    
    # Initialize variables to store the total number of rows in each tab
    total_rows_cosy = len(reference_data)
    total_rows_stage = 0
    total_rows_prod = 0
    
    # Iterate over the tabs (excluding the reference tab)
    for tab in ['PPR-Stage', 'PPR-PROD']:
        # Load the data for the current tab
        tab_data = pd.read_excel(excel_file, sheet_name=tab)
        tab_data.columns = column_names
        
        # Update the total number of rows for the current tab
        if tab == 'PPR-Stage':
            total_rows_stage = len(tab_data)
        elif tab == 'PPR-PROD':
            total_rows_prod = len(tab_data)
        
        # Merge the reference data with the current tab's data
        merged_data = pd.merge(reference_data, tab_data, on=column_names, how='outer', indicator=True)
        
        # Highlight mismatched rows
        def highlight_mismatched_rows(row):
            if row['_merge'] == 'left_only':
                return ['background-color: red'] * len(row)
            elif row['_merge'] == 'right_only':
                return ['background-color: red'] * len(row)
            else:
                return [''] * len(row)
        
        # Apply the highlighting function to the merged data
        highlighted_data = merged_data.style.apply(highlight_mismatched_rows, axis=1)
        
        # Add the highlighted data to the report data
        report_data[tab] = highlighted_data
        
        # Calculate the total number of missing rows for the current tab
        if tab == 'PPR-Stage':
            total_missing_rows_stage = len(merged_data[merged_data['_merge'] == 'left_only'])
        elif tab == 'PPR-PROD':
            total_missing_rows_prod = len(merged_data[merged_data['_merge'] == 'left_only'])
    
    # Print the total number of missing rows for each tab
    print(f"Total missing rows in PPR-Stage: {total_missing_rows_stage}")
    print(f"Total missing rows in PPR-Prod: {total_missing_rows_prod}")
    
    # Print the total number of rows in each tab
    print(f"Total rows in PPR-COSY: {total_rows_cosy}")
    print(f"Total rows in PPR-Stage: {total_rows_stage}")
    print(f"Total rows in PPR-PROD: {total_rows_prod}")
    
    # Create a new Excel file for the report
    with pd.ExcelWriter('InovaPECCosyMappingData-Analysis report.xlsx') as writer:
        # Iterate over the report data and write each tab's data to the report file
        for tab, data in report_data.items():
            data.to_excel(writer, sheet_name=tab, engine='openpyxl')

# Main program
def main():
    file_path = 'Inova-COSY-202501024_Updated.xlsx'  # Replace with your file path
    excel_file = load_excel_file(file_path)
    
    if excel_file:
        generate_report(excel_file)
        print("Report generated successfully!")

if __name__ == "__main__":
    main()


