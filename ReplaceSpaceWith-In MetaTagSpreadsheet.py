import pandas as pd

def replace_spaces_in_excel(file_path, file_name):
    # Read the Excel file
    df = pd.read_excel(f"{file_path}/{file_name}")

    # Replace spaces with underscores in the "Unique Name" column
    df["Unique Name"] = df["Unique Name"].str.replace(" ", "_")

    # Save the updated DataFrame to the original Excel file
    df.to_excel(f"{file_path}/{file_name}", index=False)

# Example usage:
file_path = "/Users/manju/Work/WrittenEdGitEpicPro/WE Stage/EpicHtmlRequirements"
file_name = "AAH_Test batch 113_01_17_25 Epic Ready.xlsx"
replace_spaces_in_excel(file_path, file_name)