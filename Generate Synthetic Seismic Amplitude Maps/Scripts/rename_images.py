import os
import glob

def rename_images(folder_path, identifier):
    # Get a list of all image files in the specified folder
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
    image_files = []
    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, extension)))

    # Sort the files for consistent renaming
    image_files.sort()

    # Rename each image file
    for index, filepath in enumerate(image_files, start=1):
        # Get the file extension
        file_extension = os.path.splitext(filepath)[1]
        
        # Construct the new filename
        new_filename = f"{identifier} ({index}){file_extension}"
        
        # Get the full new filepath
        new_filepath = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(filepath, new_filepath)
        print(f"Renamed: {filepath} -> {new_filepath}")

# Example usage
# folder_path = 'path_to_your_folder'
folder_path = 'C:/Users/your path'
identifier = 'seismic'
rename_images(folder_path, identifier)
