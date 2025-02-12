import os
import shutil
import fitz  # PyMuPDF
import pandas as pd

# INPUT 1
folder_path = "/Users/vikram/Work/Mytonomy/Latest/LogoReplacement/Mytonomy_WE"
#folder_path = "/Users/manju/Work/WrittenEducation Project/Customer Releases/AAH/PDFs/AAH 401_02_07_25-A-D/Mytonomy WE/English/A"
#folder_path = "/Users/manju/Work/WrittenEducation Project/Customer Releases/AAH/PDFs/Test batch 113_01_17_25 Epic Ready/Clara Project/ENGLISH"

# INPUT 2
logo_file = "/Users/vikram/Work/Mytonomy/Latest/LogoReplacement/Mytonomy_logo.jpeg"
#logo_file = "/Users/manju/Work/WrittenEducation Project/Customer Releases/Inova/Clinical References Root_FULL_August_21_24/HTML/Images/Inova logo.png"
#logo_file = "/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Nov1-EpicTesting-HTML Package/HTML/Images/Mytonomy_logo.png"

# INPUT 3
output_folder_path = os.path.join(os.path.dirname(folder_path), os.path.basename(folder_path) + "Mytonomy-Updated")
#output_folder_path = os.path.join(os.path.dirname(folder_path), os.path.basename(folder_path) + "Inova-Updated")

# INPUT 4
customer = 'Mytonomy'

config = {
    "Inova": {
        'logo_coords': [68.6, 47.5, 248.35, 81.5],
        'scale': 0.75
    },
    "Mytonomy": {
        'logo_coords': [25.6, 38, 205.35, 72],
        'scale': 1
    }
}

def replace_image_at_coordinates(pdf_file, logo_file, output_file, target_rect):
    doc = fitz.open(pdf_file)

    num_pages = len(doc)
    num_errors = 0
    for i, page in enumerate(doc):
        try:
            # Convert given coordinates to a fitz.Rect object
            rect = fitz.Rect(*target_rect)

            # Get the area to be whitened out (horizontal stripe at the y-level of the logo)
            whiten_rect = fitz.Rect(0, 38, 575, 72)

            # Draw a white rectangle (whiten out) over the existing image area at the specified y-level
            page.draw_rect(whiten_rect, color=(1, 1, 1), fill=(1, 1, 1))  # White color (1, 1, 1)

            # Overlay the new logo at the specified position
            page.insert_image(rect, filename=logo_file)
        except Exception as e:
            print(f'Error replacing logo in page {i+1} in file {pdf_file}: {e}')
            num_errors += 1

    doc.save(output_file)
    doc.close()
    return num_pages, num_errors

def main():
    # Validate inputs (Error handling)
    if not os.path.isdir(folder_path):
        print(f"Folder path {folder_path} is not a directory")
        return 1
    if not os.path.isfile(logo_file):
        print(f"Logo filepath {logo_file} is invalid")
        return 1
    if customer not in config:
        print(f'Invalid customer: {customer}')
        return 1
    

    folder = folder_path.split(os.sep)[-1]
    
    # Apply scaling to the logo image to adjust the size
    target_rect = config[customer]['logo_coords']
    target_rect = [x*config[customer]['scale'] for x in target_rect]

    df = pd.DataFrame(columns=['Filepath', 'Total Pages', 'Total Images Replaced', 'Match'])

    # If the output directory exists, delete its contents
    if os.path.exists(output_folder_path):
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
                
    # Make the output directory if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)

    filepaths = []
    total_pages = []
    total_images_replaced = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        relative_dir_path = os.path.relpath(dirpath, folder_path)
        output_dir = os.path.join(output_folder_path, relative_dir_path)
        
        os.makedirs(output_dir, exist_ok=True)

        for filename in filenames:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(dirpath, filename)
                idx = pdf_path.find(folder)
                filepaths.append(os.sep + pdf_path[idx:])

                output_file_path = os.path.join(output_dir, filename)

                num_pages, num_errors = replace_image_at_coordinates(pdf_path, logo_file, output_file_path, target_rect)     
                total_pages.append(num_pages)
                total_images_replaced.append(num_pages - num_errors)

    df["Filepath"] = filepaths
    df["Total Pages"] = total_pages
    df["Total Images Replaced"] = total_images_replaced
    df["Match"] = df["Total Pages"] == df["Total Images Replaced"]
    error_count = (df["Match"] == "FALSE").sum()
    print(f'Number of files with errors: {error_count}')
    df.to_excel(f'{folder}-PDFLogoReplacement.xlsx')
    

if __name__ == '__main__':
    main()
