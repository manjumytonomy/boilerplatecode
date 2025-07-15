from bs4 import BeautifulSoup
import os

def remove_images(html_folder):
    images_folder = os.path.join(html_folder, 'Images')
    target_folder = os.path.join(html_folder, 'Mytonomy WE')
    existing_images = set()
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                
                img_tags = soup.find_all('img')
                src_list = [os.path.basename(img.get('src')) for img in img_tags if img.get('src')]
                existing_images.update(src_list)

    for file in os.listdir(images_folder):
        if file not in existing_images:
            os.remove(os.path.join(images_folder, file))

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

html_folder = "/Users/vikram/Downloads/test/HTML"
remove_images(html_folder)  # Remove images not referenced in HTML files

destination_folder = os.path.dirname(html_folder)
create_index_html(destination_folder, html_folder)  # Create the index.html file