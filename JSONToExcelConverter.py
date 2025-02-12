import json
import pandas as pd
import openpyxl
import os
import sys

def json_to_excel(directory):
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            excel_file = os.path.join(dir_path, f"{dir}.xlsx")
            wb = openpyxl.Workbook()
            for file in os.listdir(dir_path):
                if file.endswith(".json"):
                    file_path = os.path.join(dir_path, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    df = pd.json_normalize(data)
                    ws = wb.create_sheet(file.split('.')[0])
                    # Add header row
                    ws.append(df.columns.tolist())
                    for r in df.values.tolist():
                        ws.append(r)
            wb.save(excel_file)
            print(f"Excel file created: {excel_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_excel.py <source_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    json_to_excel(directory)
