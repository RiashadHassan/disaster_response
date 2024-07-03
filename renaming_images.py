import os


# Function to rename images in a folder starting from a specified index
def rename_images_in_folder(folder_path, start_index):
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter out non-image files (adjust extensions as needed)
    image_files = [
        file
        for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

    # Rename each image sequentially starting from start_index
    for index, old_name in enumerate(image_files, start=start_index):
        extension = os.path.splitext(old_name)[1]  # Get the file extension
        new_name = f"image-{index}{extension}"

        # Construct full paths
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")

    # Return the next index for the next folder
    return start_index + len(image_files)


# Main function to process all folders
def rename_images_in_all_folders(parent_folder):
    # List all folders in the parent folder
    folders = [
        folder
        for folder in os.listdir(parent_folder)
        if os.path.isdir(os.path.join(parent_folder, folder))
    ]

    # Initialize the starting index for renaming
    current_index = 1

    # Rename images in each folder
    for folder in folders:
        folder_path = os.path.join(parent_folder, folder)
        current_index = rename_images_in_folder(folder_path, current_index)


# Example usage:
if __name__ == "__main__":

    parent_folder = r"C:\Users\WALTON\Downloads\Large-Fire-2"  # Replace with your parent folder path
    rename_images_in_all_folders(parent_folder)
