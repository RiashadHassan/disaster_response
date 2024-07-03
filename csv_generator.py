import os
import pandas as pd

# Base directory containing the fire severity folders
base_dir = r"C:\Users\WALTON\Downloads\Large-Fire-2"

# Initialize an empty DataFrame for labels
labels_df = pd.DataFrame(columns=["filename", "label", "severity"])

# List to collect rows for the DataFrame
rows = []

# Iterate over all severity folders in the base directory
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)

    # Check if the folder name starts with 'fire-' and is a directory
    if folder_name.startswith("Fire-") and os.path.isdir(folder_path):
        # Extract severity level from the folder name
        severity_level = int(folder_name.split("-")[1])

        # Iterate over all files in the severity folder
        for filename in os.listdir(folder_path):
            if (
                filename.endswith(".jpg")
                or filename.endswith(".jpeg")
                or filename.endswith(".png")
            ):
                # Full path of the image file
                file_path = os.path.join(folder_path, filename)

                # Collect row data
                rows.append(
                    {"filename": filename, "label": 1, "severity": severity_level}
                )

# Create a DataFrame from the collected rows
labels_df = pd.concat([labels_df, pd.DataFrame(rows)], ignore_index=True)

# Path to save the labels CSV file
labels_csv = os.path.join(base_dir, "labels.csv")

# Save DataFrame to CSV
labels_df.to_csv(labels_csv, index=False)

print(f"Labels CSV file saved successfully at: {labels_csv}")
