import os
import random
import shutil
from sklearn.model_selection import train_test_split

def split_images(data_folder, train_folder, test_folder, test_size=0.2, random_state=42):
    # Create train and test folders
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # Get list of class folders
    class_folders = [os.path.join(data_folder, folder) for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]
    print("class_folders", class_folders, len(class_folders))

    class_counts_train = {}  # Class counts in the train set
    class_counts_test = {}  # Class counts in the test set

    for class_folder in class_folders:
        # Get class name
        class_name = os.path.basename(class_folder)
        print("class_name", class_name)

        # Get list of subclass folders (video titles) within the class folder
        subclass_folders = [folder for folder in os.listdir(class_folder) if os.path.isdir(os.path.join(class_folder, folder))]
        print("subclass_folders", subclass_folders, len(subclass_folders))

        for subclass_folder in subclass_folders:
            subclass_path = os.path.join(class_folder, subclass_folder)
            print("subclass_path", subclass_path)

            # Get list of image files in the subclass folder with the full path
            image_files = [os.path.join(subclass_path, file) for file in os.listdir(subclass_path) if os.path.isfile(os.path.join(subclass_path, file))]
            print("image_files", image_files, len(image_files))

            # Split image files into train and test sets
            train_files, test_files = train_test_split(image_files, test_size=test_size, random_state=random_state)
            print("train_files", train_files)

            # Create train and test subfolders if they don't exist
            train_subfolder = os.path.join(train_folder, class_name, subclass_folder)
            os.makedirs(train_subfolder, exist_ok=True)

            test_subfolder = os.path.join(test_folder, class_name, subclass_folder)
            os.makedirs(test_subfolder, exist_ok=True)

            # Move train and test images to subfolders
            for file in train_files:
                dest_path = os.path.join(train_subfolder, os.path.basename(file))
                shutil.copy(file, dest_path)
                class_counts_train[subclass_folder] = class_counts_train.get(subclass_folder, 0) + 1

            # Move test image files
            for file in test_files:
                dest_path = os.path.join(test_subfolder, os.path.basename(file))
                shutil.copy(file, dest_path)
                class_counts_test[subclass_folder] = class_counts_test.get(subclass_folder, 0) + 1

    print("Train set composition:")
    for subclass_folder, count in class_counts_train.items():
        print(f"{subclass_folder}: {count} images")

    print("\nTest set composition:")
    for subclass_folder, count in class_counts_test.items():
        print(f"{subclass_folder}: {count} images")

# Pathes
data_folder = '/Users/81737/work/VisInspection/FrameUploads_Update2'  # images
train_folder = '/Users/81737/work/VisInspection/model_train/train_folder' # train set 
test_folder  = '/Users/81737/work/VisInspection/model_train/test_folder'  # test set
test_size = 0.2  # Fraction of data in test set
random_state = 42  # Random state

split_images(data_folder, train_folder, test_folder, test_size, random_state)
