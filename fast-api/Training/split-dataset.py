import os
import shutil

# Source folders (your labeled data)
images_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/labeled/images'
labels_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/labeled/labels'

# Destination folders
train_images_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/training_data/images/train'
val_images_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/training_data/images/val'
train_labels_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/training_data/labels/train'
val_labels_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/training_data/labels/val'

# Create destination folders if they don't exist
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)

# List all image files
image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.jpg')])

for idx, image_file in enumerate(image_files):
    # Image and corresponding label file
    image_path = os.path.join(images_folder, image_file)
    label_file = image_file.replace('.jpg', '.txt')
    label_path = os.path.join(labels_folder, label_file)

    # Decide whether it goes to train or val
    if idx % 5 == 0:
        # Validation set
        dest_image_path = os.path.join(val_images_folder, image_file)
        dest_label_path = os.path.join(val_labels_folder, label_file)
    else:
        # Training set
        dest_image_path = os.path.join(train_images_folder, image_file)
        dest_label_path = os.path.join(train_labels_folder, label_file)

    # Copy files
    shutil.copy2(image_path, dest_image_path)
    shutil.copy2(label_path, dest_label_path)

print("✅ Split complete. Files organized into train/val folders.")
