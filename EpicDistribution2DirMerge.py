import os
import shutil

# Paths to the folders to be merged
folder1 = "/Users/vikram/Work/Mytonomy-Official/AAH/Merge Packages/Clinical References Root 1"
folder2 = "/Users/vikram/Work/Mytonomy-Official/AAH/Merge Packages/Clinical References Root 2"
target_folder = "/Users/vikram/Work/Mytonomy-Official/AAH/Merge Packages/Clinical References Root Merged"

if os.path.exists(target_folder):
    shutil.rmtree(target_folder)  # Remove the target folder if it exists

def merge_folders_by_name(folder1, folder2, target_folder):
    """
    Merge files from folder1 and folder2 into target_folder based on unique file names,
    preserving their folder structure.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Set to track file names that have been added
    added_files = set()

    # Loop through both folders to process their files
    for folder in [folder1, folder2]:
        for root, _, files in os.walk(folder):
            for file in files:
                # Get the relative path from the current folder root
                relative_path = os.path.relpath(root, folder)

                # Construct the destination directory path
                dest_dir = os.path.join(target_folder, relative_path)

                # Create the destination directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                # Check if the file has already been added
                if file not in added_files:
                    # Mark the file as added
                    added_files.add(file)

                    # Construct source and destination file paths
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_dir, file)

                    # Copy the file to the destination folder
                    shutil.copy(src_file_path, dest_file_path)
                else:
                    # Log duplicate files that are skipped
                    print(f"Duplicate file name skipped: {file}")

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


# Call the function to merge folders
merge_folders_by_name(folder1, folder2, target_folder)

# Notify the user that the process is complete
print(f"Files from {folder1} and {folder2} have been merged into {target_folder}, preserving folder structure.")


html_subfolder = os.path.join(target_folder, "HTML")  # Define the HTML subfolder path
create_index_html(target_folder, html_subfolder)  # Generate the index file
