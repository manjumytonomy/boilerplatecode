import os
import shutil
import pandas as pd
from bs4 import BeautifulSoup

# Define the paths for source folder, input Excel file, and destination folder
folder_mapping = {
    #Src Folder Name : give the Path where the src folder located to copy html files  
    "Carolina East Clinical References Root 10-8-24-Shipped": "/home/neualto/Downloads/Carolina East Clinical References Root 10-8-24-Shipped",
    "Carolina East" : "/home/neualto/Downloads/Carolina East",
    "Carolina" : "/home/neualto/Downloads/Carolina"
}  # A dictionary that maps folder names to actual folder paths
input_file_path = '/home/neualto/Desktop/Work/Extract/List of FilesToBeExtracted.xlsx'  # Path to the input Excel file
destination_folder = '/home/neualto/Desktop/Work/Extract/BoilerPlateCodeGitLocal'  # Path to the destination folder where files will be copied

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

# Read the Excel file containing the list of HTML file paths
df = pd.read_excel(input_file_path, header=None)  # Read Excel file without headers

# Function to extract referenced assets (images, CSS files) from an HTML file
def extract_assets_from_html(html_file_path):
    """Extract image and CSS file references from an HTML file."""
    assets = set()  # Use a set to store unique asset paths
    try:
        # Open and parse the HTML file using BeautifulSoup
        with open(html_file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        # Extract all image sources (src attributes in <img> tags)
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            if src:
                assets.add(src)  # Add the image source to the set
        # Extract all CSS file references (href attributes in <link> tags)
        for link_tag in soup.find_all("link", rel="stylesheet"):
            href = link_tag.get("href")
            if href:
                assets.add(href)  # Add the CSS reference to the set
    except Exception as e:
        # Log any errors encountered during parsing
        log_message(f"Error processing HTML file {html_file_path}: {e}", 'error')
    return assets  # Return the set of referenced assets

# Function to copy a file while preserving its folder structure
def copy_file(src_file_path, src_base_folder, dest_base_folder):
    """Copy a file to the destination folder while preserving the folder structure."""
    try:
        # Calculate the relative path of the file
        relative_path = os.path.relpath(src_file_path, src_base_folder)
        # Construct the destination path by preserving folder structure
        dest_path = os.path.join(dest_base_folder, relative_path)
        # Create necessary directories in the target folder
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        # Copy the file to the destination folder
        shutil.copy(src_file_path, dest_path)
        # Log the successful copy operation
        log_message(f"Copied: {src_file_path} to {dest_path}", 'debug')
    except Exception as e:
        # Log any errors during file copy
        log_message(f"Error copying file {src_file_path}: {e}", 'error')

# Process each HTML file listed in the Excel file
for index, row in df.iterrows():
    # Extract folder name and file path from the Excel sheet
    folder_name = row[0].strip()  # Folder column
    relative_path = row[1].strip()  # File column

    # Determine the source folder base path dynamically from the folder_mapping dictionary
    folder_base_path = folder_mapping.get(folder_name)
    if not folder_base_path:
        # Log if the folder name is not found in the mapping
        log_message(f"Folder name not found in mapping: {folder_name}", 'error')
        continue

    # Construct the full path to the HTML file
    src_file_path = os.path.join(folder_base_path, 'HTML', relative_path)

    # Check if the HTML file exists in the source folder
    if os.path.exists(src_file_path):
        # Copy the HTML file to the destination folder
        copy_file(src_file_path, folder_base_path, destination_folder)

        # Extract referenced assets (images, CSS) from the HTML file
        referenced_assets = extract_assets_from_html(src_file_path)
        for asset in referenced_assets:
            # Construct full path for each referenced asset
            asset_path = os.path.join(os.path.dirname(src_file_path), asset)
            # Check if the asset exists and copy it to the destination folder
            if os.path.exists(asset_path):
                copy_file(asset_path, folder_base_path, destination_folder)
            else:
                # Log missing assets
                log_message(f"Referenced asset not found: {asset}", 'error')
    else:
        # Log missing HTML files
        log_message(f"HTML file not found: {relative_path} in folder {folder_name}", 'error')

# Create an index.html file to display the copied files
index_file_path = os.path.join(destination_folder, "EpicDesktopIndex.html")

# Define the HTML structure for the index file
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epic Desktop Index</title>
</head>
<body>
<h1>Epic Desktop Index</h1>
"""
html_footer = """</body></html>"""

# Function to generate HTML links for files in the destination folder
def generate_file_links(folder, base_folder):
    """Recursively generate HTML links for files in the specified folder."""
    def generate_links(current_folder, parent_path=""):
        links = ""  # HTML string for links
        for file in sorted(os.listdir(current_folder)):
            full_path = os.path.join(current_folder, file)
            # Calculate relative path using base_folder to ensure correct links
            relative_path = os.path.relpath(full_path, base_folder).replace("\\", "/")

            # Exclude CSS and Images folders from the links
            if os.path.basename(full_path).lower() in ["css", "images"]:
                continue

            if os.path.isdir(full_path):
                # Add folder name with parent_path for display
                folder_name = f"{parent_path}/{file}" if parent_path else file
                links += f"<li>{folder_name}</li>"
                links += "<ul>" + generate_links(full_path, folder_name) + "</ul>"
            elif file.lower().endswith(".html"):
                # Add hyperlinks for .html files
                file_name = os.path.splitext(file)[0]  # Remove .html extension for display
                links += f'<li><a href="{relative_path}" target="_blank">{file_name}</a></li>'
        return links

    # Start generating links from the folder
    return generate_links(folder)

# Set your base directory here for generating links
html_subfolder = os.path.join(destination_folder, "HTML")  # Subfolder to process

# Initialize base_folder as the top-level folder
base_folder = destination_folder

# Generate the HTML content for the index file
html_content = "<ul>" + generate_file_links(html_subfolder, base_folder) + "</ul>"

# Write the complete index.html file
with open(index_file_path, "w", encoding="utf-8") as f:
    f.write(html_header)
    f.write(html_content)
    f.write(html_footer)

# Output success message
print(f"Index file created: {index_file_path}")
print(f"Extracted Successfully Check {destination_folder}")





















# import os
# import shutil
# import pandas as pd
# from bs4 import BeautifulSoup

# # Define the paths for source folder, input Excel file, and destination folder
# folder_mapping = {
#     "Carolina East Clinical References Root 10-8-24-Shipped": "/home/neualto/Downloads/Carolina East Clinical References Root 10-8-24-Shipped",
#     "Carolina East" : "/home/neualto/Downloads/Carolina East",
#     "Carolina East Clinical " : "/home/neualto/Downloads/Carolina East Clinical "
# } # Source folder containing HTML files
# input_file_path = '/home/neualto/Desktop/Work/Extract/List of FilesToBeExtracted.xlsx'  # Excel file listing HTML files to process
# destination_folder = '/home/neualto/Desktop/Work/Extract/BoilerPlateCodeGitLocal'  # Destination folder for extracted files

# # Create Logs folder outside the destination folder for logging debug and error messages
# log_folder = os.path.join(os.path.dirname(destination_folder), 'Logs')
# os.makedirs(log_folder, exist_ok=True)  # Create the Logs folder if it doesn't exist

# # Define log file paths for debugging and error logs
# debug_log = os.path.join(log_folder, 'debug.log')  # File for debug logs
# error_log = os.path.join(log_folder, 'error.err')  # File for error logs

# # Function to log messages to respective log files
# def log_message(message, level='debug'):
#     # Select appropriate log file based on log level (debug or error)
#     log_path = debug_log if level == 'debug' else error_log
#     with open(log_path, 'a') as log:
#         log.write(message + '\n')  # Append the log message to the file

# # Read the Excel file containing the list of HTML file paths
# df = pd.read_excel(input_file_path, header=None)  # Read Excel file without headers

# # Function to extract referenced assets (images, CSS files) from an HTML file
# def extract_assets_from_html(html_file_path):
#     assets = set()  # Use a set to store unique asset paths
#     try:
#         # Open and parse the HTML file using BeautifulSoup
#         with open(html_file_path, "r", encoding="utf-8") as file:
#             soup = BeautifulSoup(file, "html.parser")
#         # Extract all image sources (src attributes in <img> tags)
#         for img_tag in soup.find_all("img"):
#             src = img_tag.get("src")
#             if src:
#                 assets.add(src)  # Add the image source to the set
#         # Extract all CSS file references (href attributes in <link> tags)
#         for link_tag in soup.find_all("link", rel="stylesheet"):
#             href = link_tag.get("href")
#             if href:
#                 assets.add(href)  # Add the CSS reference to the set
#     except Exception as e:
#         # Log any errors encountered during parsing
#         log_message(f"Error processing HTML file {html_file_path}: {e}", 'error')
#     return assets  # Return the set of referenced assets

# # Function to copy a file while preserving its folder structure
# def copy_file(src_file_path, src_base_folder, dest_base_folder):
#     try:
#         # Calculate the relative path of the file
#         relative_path = os.path.relpath(src_file_path, src_base_folder)
#         # Construct the destination path by preserving folder structure
#         dest_path = os.path.join(dest_base_folder, relative_path)
#         # Create necessary directories in the target folder
#         os.makedirs(os.path.dirname(dest_path), exist_ok=True)
#         # Copy the file to the destination folder
#         shutil.copy(src_file_path, dest_path)
#         # Log the successful copy operation
#         log_message(f"Copied: {src_file_path} to {dest_path}", 'debug')
#     except Exception as e:
#         # Log any errors during file copy
#         log_message(f"Error copying file {src_file_path}: {e}", 'error')

# # Process each HTML file listed in the Excel file
# for index, row in df.iterrows():
#     # Extract folder name and file path from the Excel sheet
#     folder_name = row[0].strip()  # Folder column
#     relative_path = row[1].strip()  # File column

#     # Determine the source folder base path dynamically
#     folder_base_path = folder_mapping.get(folder_name)
#     if not folder_base_path:
#         # Log if the folder name is not found in the mapping
#         log_message(f"Folder name not found in mapping: {folder_name}", 'error')
#         continue

#     # Construct the full path to the HTML file
#     src_file_path = os.path.join(folder_base_path, 'HTML', relative_path)

#     # Check if the HTML file exists in the source folder
#     if os.path.exists(src_file_path):
#         # Copy the HTML file to the target folder
#         copy_file(src_file_path, folder_base_path, destination_folder)

#         # Extract referenced assets (images, CSS) from the HTML file
#         referenced_assets = extract_assets_from_html(src_file_path)
#         for asset in referenced_assets:
#             # Construct full path for each asset based on its reference
#             asset_path = os.path.join(os.path.dirname(src_file_path), asset)
#             # Check if the asset exists and copy it to the target folder
#             if os.path.exists(asset_path):
#                 copy_file(asset_path, folder_base_path, destination_folder)
#             else:
#                 # Log missing assets
#                 log_message(f"Referenced asset not found: {asset}", 'error')
#     else:
#         # Log missing HTML files
#         log_message(f"HTML file not found: {relative_path} in folder {folder_name}", 'error')

# # Create an index.html file to display the copied files
# index_file_path = os.path.join(destination_folder, "EpicDesktopIndex.html")

# # Define the HTML structure for the index file
# html_header = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Epic Desktop Index</title>
# </head>
# <body>
# <h1>Epic Desktop Index</h1>
# """
# html_footer = """</body></html>"""


# def generate_file_links(folder, base_folder):
#     def generate_links(current_folder, parent_path=""):
#         links = ""  # HTML string for links
#         for file in sorted(os.listdir(current_folder)):
#             full_path = os.path.join(current_folder, file)
#             # Calculate relative path using base_folder to ensure correct links
#             relative_path = os.path.relpath(full_path, base_folder).replace("\\", "/")

#             # Exclude CSS and Images folders
#             if os.path.basename(full_path).lower() in ["css", "images"]:
#                 continue

#             if os.path.isdir(full_path):
#                 # Add folder name with parent_path for display
#                 folder_name = f"{parent_path}/{file}" if parent_path else file
#                 links += f"<li>{folder_name}</li>"
#                 links += "<ul>" + generate_links(full_path, folder_name) + "</ul>"
#             elif file.lower().endswith(".html"):
#                 # Add hyperlinks for .html files
#                 file_name = os.path.splitext(file)[0]  # Remove .html extension for display
#                 links += f'<li><a href="{relative_path}" target="_blank">{file_name}</a></li>'
#         return links

#     # Start generating links from the folder
#     return generate_links(folder)

#  # Set your base directory here
# html_subfolder = os.path.join(destination_folder, "HTML")  # Subfolder to process

# # Initialize base_folder as the top-level folder
# base_folder = destination_folder

# # Generate the HTML content for the index file
# html_content = "<ul>" + generate_file_links(html_subfolder, base_folder) + "</ul>"

# # Write the complete index.html file
# with open(index_file_path, "w", encoding="utf-8") as f:
#     f.write(html_header)
#     f.write(html_content)
#     f.write(html_footer)

# print(f"Index file created: {index_file_path}")

