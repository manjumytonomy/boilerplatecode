import os
import shutil

# Paths to the folders to be merged
folder1 = "/Users/Manju/Downloads/Clinical References Root - Dir2"
folder2 = "/Users/Manju/Downloads/Clinical References Root - Dir1"
target_folder = "/Users/Manju/Downloads/Clinical References Root -Merged Dir"

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



# Call the function to merge folders
merge_folders_by_name(folder1, folder2, target_folder)

# Notify the user that the process is complete
print(f"Files from {folder1} and {folder2} have been merged into {target_folder}, preserving folder structure.")
