import os
import random
import shutil
import csv
from os import system
from sklearn.model_selection import train_test_split

"""
add stuff here
"""

data_folder = '/Users/81737/work/VisInspection/FrameUploads_Iteration2'                        # input image data
train_folder = '/Users/81737/work/VisInspection/model_train/train_folder_randomly_Iteration2'  # train folder
test_folder  = '/Users/81737/work/VisInspection/model_train/test_folder_randomly_Iteration2'   # test folder
valid_folder = '/Users/81737/work/VisInspection/model_train/valid_folder_randomly_Iteration2'  # validation folder
test_prop = 0.1  # test set part of total (default: 0.1)
valid_prop = 0.1  # val set part of total (default: 0.1)
random_seed = 42  # Random seed

def shuffle_by_class(paths, labels, random_seed):
    comp_class = list(zip(paths, labels))
    random.seed(random_seed)
    random.shuffle(comp_class)
    paths, labels = zip(*comp_class)
    return paths, labels


def create_subfolders(paths, labels, folder):
    for path, label in zip(paths, labels):
        subclass_folder = os.path.basename(os.path.dirname(path))
        class_folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
        class_path = os.path.join(folder, class_folder)
        subclass_path = os.path.join(class_path, subclass_folder)
        os.makedirs(subclass_path, exist_ok=True)
        shutil.copy(path, subclass_path)

def save_images_csv(folder, paths, labels, filename):
    with open(os.path.join(folder, filename), "w", newline="") as f:
        writer = csv.writer(f)
        #writer.writerow(["DATASET", "IMAGE_PATH", "CLASS"])                                                                                                                                        
        for path, label in zip(paths, labels):
            dataset = get_dataset_label(folder, path)
            writer.writerow([dataset, path, label])

def get_dataset_label(folder, image_path):
    if folder == train_folder:
        return "TRAIN"
    elif folder == test_folder:
        return "TEST"
    elif folder == valid_folder:
        return "VALIDATION"

# Create train, test, and validation folders
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)
os.makedirs(valid_folder, exist_ok=True)

# Get list of class folders
class_folders = [folder for folder in os.listdir(data_folder) if
                 os.path.isdir(os.path.join(data_folder, folder))]
print("class_folders", class_folders, " total count: ", len(class_folders))

# List to store image paths and corresponding class labels
image_paths = []

for class_folder in class_folders:
    class_path = os.path.join(data_folder, class_folder)

    # Get list of subclass folders within the class folder
    subclass_folders = [folder for folder in os.listdir(class_path) if
                        os.path.isdir(os.path.join(class_path, folder))]

    for subclass_folder in subclass_folders:
        subclass_path = os.path.join(class_path, subclass_folder)

        # Get list of image files in the subclass folder
        image_files = [file for file in os.listdir(subclass_path) if
                       os.path.isfile(os.path.join(subclass_path, file))]

        # Append image paths and class labels
        image_paths.extend([(os.path.join(subclass_path, file), class_folder) for file in image_files])

# Separate image paths and class labels
paths, labels = zip(*image_paths)

# Perform train, test, validation split
train_paths, test_valid_paths, train_labels, test_valid_labels = train_test_split(paths, labels, test_size=(test_prop + valid_prop),
                                                                                  random_state=random_seed)

test_paths, valid_paths, test_labels, valid_labels = train_test_split(test_valid_paths, test_valid_labels,
                                                                      test_size=(valid_prop / (test_prop + valid_prop)),
                                                                      random_state=random_seed)

# Create train, test, and validation subfolders in the train, test, and validation folders
create_subfolders(train_paths, train_labels, train_folder)
create_subfolders(test_paths, test_labels, test_folder)
create_subfolders(valid_paths, valid_labels, valid_folder)

# Shuffle the paths and labels while maintaining the class-wise order
train_paths, train_labels = shuffle_by_class(train_paths, train_labels, random_seed)
test_paths, test_labels = shuffle_by_class(test_paths, test_labels, random_seed)
valid_paths, valid_labels = shuffle_by_class(valid_paths, valid_labels, random_seed)

# Save train, test, and validation in csv files. 
save_images_csv(train_folder, train_paths, train_labels, "../randomly_train.csv")
save_images_csv(test_folder, test_paths, test_labels, "../randomly_test.csv")
save_images_csv(valid_folder, valid_paths, valid_labels, "../randomly_valid.csv")

# compine them all into one csv file
from os import system 
system("cat randomly_train.csv randomly_test.csv randomly_valid.csv > merge_randomly_Iteration2.csv")

# rename the path to GCP bucket
with open("./merge_randomly_Iteration2.csv", "r") as f1:
    data = f1.read().replace("/Users/81737/work/VisInspection/FrameUploads_Iteration2",
                             "gs://ul-solutions-field-inspection-training/ICP/2024_Frames_v2")
with open("./final_randomly_Iteration2.csv", "w") as f2:
    f2.write(data)

def shuffle_by_class(paths, labels, random_seed):
    comp_class = list(zip(paths, labels))
    random.seed(random_seed)
    random.shuffle(comp_class)
    paths, labels = zip(*comp_class)
    return paths, labels


def create_subfolders(paths, labels, folder):
    for path, label in zip(paths, labels):
        subclass_folder = os.path.basename(os.path.dirname(path))
        class_folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
        class_path = os.path.join(folder, class_folder)
        subclass_path = os.path.join(class_path, subclass_folder)
        os.makedirs(subclass_path, exist_ok=True)
        shutil.copy(path, subclass_path)

def save_images_csv(folder, paths, labels, filename):
    with open(os.path.join(folder, filename), "w", newline="") as f:
        writer = csv.writer(f)
        for path, label in zip(paths, labels):
            dataset = get_dataset_label(folder, path)
            writer.writerow([dataset, path, label])

def get_dataset_label(folder, image_path):
    if folder == train_folder:
        return "TRAIN"
    elif folder == test_folder:
        return "TEST"
    elif folder == valid_folder:
        return "VALIDATION"
        

