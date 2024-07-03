import os


def rename_images(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-image files (you can customize this as needed)
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

    # Sort images to ensure consistent renaming
    images.sort()

    # Rename images
    for i, image in enumerate(images):
        # Get the file extension
        ext = os.path.splitext(image)[1]
        # Create the new file name
        new_name = f"non-fire-{i+1}{ext}"
        # Get the full path for the old and new names
        old_path = os.path.join(folder_path, image)
        new_path = os.path.join(folder_path, new_name)
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}'")


# Specify the folder path
folder_path = r"C:\Users\WALTON\Downloads\non-fire -2"

# Call the rename function
rename_images(folder_path)
