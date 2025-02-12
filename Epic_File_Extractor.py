import os
import shutil
import pandas as pd
from bs4 import BeautifulSoup

# input_file_path

# Define the paths
src_folder = '/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East Clinical References Root 10-8-24-Shipped'  # Source folder where files are located and not include the HTML directory

# Define the paths for source folder, input Excel file, and destination folder
# folder_mapping = {
#     #Src Folder Name : give the Path where the src folder located to copy html files  
#     '/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East Clinical References Root 10-8-24-Shipped'  # Source folder where files are located and not include the HTML directory
#    '/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East 11-1-24 Epic Desktop-Shipped',
#     '/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East Clinical References Q4-2024-Shipped'
# }  # A dictionary that maps folder names to actual folder paths


source_html_folder_locations = {
    'Carolina East Clinical References Root 10-8-24-Shipped': '/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Carolina East Clinical References Root 10-8-24-Shipped',
    'Carolina East 11-1-24 Epic Desktop-Shipped': '/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Carolina East 11-1-24 Epic Desktop-Shipped',
    'Carolina East Clinical References Q4-2024-Shipped': '/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Carolina East Clinical References Q4-2024-Shipped'
}
source_html_folder_locations = dict(source_html_folder_locations)  # Convert the list of tuples to a dictionary

input_file_path = '/Users/manju/Work/BoilerPlateCodeGitLocal/CE_QRCodeIssues_Jan-25-Files_to_extract_no_dupes.xlsx'  # Path to the Excel file containing HTML file paths
destination_folder = '/Users/manju/Work/BoilerPlateCodeGitLocal/EpicPackageDestDir' # Destination folder where files will be copied

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
                log_message(f"Image processed : {src}")
        # Extract all CSS file references (href attributes in <link> tags)
        for link_tag in soup.find_all("link", rel="stylesheet"):
            href = link_tag.get("href")
            if href:
                assets.add(href)  # Add the CSS reference to the set
                log_message(f"HREF processed : {href}")
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
    folder_base_path = source_html_folder_locations.get(folder_name)
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
        index += 1  # Increment the row index for logging purposes
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
                log_message(f"Referenced asset {asset} for the html file {src_file_path} not found ", 'error')
    else:
        # Log missing HTML files
        log_message(f"HTML file not found: {relative_path} in folder {folder_name}", 'error')


log_message(f"Total number of HTML Files copied: {index}") # Log the total number of HTML files copied

# Define the HTML structure for the index file
HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EpicDesktopIndex</title>
    <script type="text/javascript" src="EpicVendorCommunication.js"></script>
</head>
<body>
<h1>EpicDesktopIndex</h1>
"""
# HTML_FOOTER: This is the closing portion of the HTML document.
HTML_FOOTER = """
</body>
</html>
"""

# Function to generate file links in an HTML format
def generate_file_links(folder, base_folder, exclude_folders=None, include_extensions=None):
    if exclude_folders is None:
        exclude_folders = ["CSS", "Images"]  # Default folders to exclude
    if include_extensions is None:
        include_extensions = [".html"]  # Default file extensions to include

    def generate_links(current_folder, parent_path=""):
        links = []  # List to store HTML strings for links
        for item in sorted(os.listdir(current_folder)):  # Sort items for consistent ordering
            full_path = os.path.join(current_folder, item)  # Full path of the item
            relative_path = os.path.relpath(full_path, base_folder).replace("\\", "/")  # Relative path for linking

            if os.path.isdir(full_path):  # If the item is a folder
                if os.path.basename(full_path).lower() in [folder.lower() for folder in exclude_folders]:
                    continue  # Skip excluded folders
                # Add folder name and recursively generate its contents
                folder_name = f"{parent_path}/{item}" if parent_path else item
                links.append(f"<li>{folder_name}</li>")  # Add the folder name as a list item
                links.append("<ul>")  # Start a new nested list
                links.append(generate_links(full_path, folder_name))  # Recurse into the folder
                links.append("</ul>")  # Close the nested list
            elif os.path.isfile(full_path):  # If the item is a file
                if any(item.lower().endswith(ext) for ext in include_extensions):  # Check for valid extensions
                    file_name = os.path.splitext(item)[0]  # Extract the file name without extension
                    links.append(f'<li><a href="{relative_path}">{file_name}</a></li>')  # Add a link to the file
        return "\n".join(links)  # Join all links into a single string

    return generate_links(folder)  # Start generating links from the base folder

# Function to create the index.html file
def create_index_html(destination_folder, html_subfolder, index_file_name="EpicDesktopIndex.html"):
    index_file_path = os.path.join(destination_folder, index_file_name)  # Path for the index file
    # Generate HTML content with links
    html_content = "<ul>\n" + generate_file_links(html_subfolder, destination_folder) + "\n</ul>"

    # Write the content to the index file
    with open(index_file_path, "w", encoding="utf-8") as f:
        f.write(HTML_HEADER)  # Write the header
        f.write(html_content)  # Write the generated links
        f.write(HTML_FOOTER)  # Write the footer

    # Notify the user of the created file
    print(f"Index file created: {index_file_path}")
    print(f"Extracted Successfully. Check {destination_folder}")

# Example usage
html_subfolder = os.path.join(destination_folder, "HTML")  # Define the HTML subfolder path
create_index_html(destination_folder, html_subfolder)  # Generate the index file
