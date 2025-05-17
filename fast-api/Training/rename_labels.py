import os
import re

# Path to your folder
labels_folder_path = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/labeled/labels'
images_folder_path = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/labeled/images'

# List all files in the folder
for filename in os.listdir(labels_folder_path):
    if filename.endswith('.txt'):
        # Use regex to extract "frame-#" part
        match = re.search(r'frame_\d+\.txt', filename)
        if match:
            new_filename = match.group()
            old_path = os.path.join(labels_folder_path, filename)
            new_path = os.path.join(labels_folder_path, new_filename)
            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} -> {new_filename}')

for filename in os.listdir(images_folder_path):
    if filename.endswith('.jpg'):
        # Use regex to extract "frame-#" part
        match = re.search(r'frame_\d+\.jpg', filename)
        if match:
            new_filename = match.group()
            old_path = os.path.join(images_folder_path, filename)
            new_path = os.path.join(images_folder_path, new_filename)
            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} -> {new_filename}')