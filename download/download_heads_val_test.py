import pandas as pd
import os

# Load the class descriptions
classes = pd.read_csv('oidv7-class-descriptions-boxable.csv', header=None, names=['id', 'name'])

# Find the class ID for "Human head"
head_id = classes[classes['name'] == 'Human head']['id'].values[0]

# Load the bounding boxes annotations
# annotations = pd.read_csv('oidv6-train-annotations-bbox.csv')
annotations_val = pd.read_csv("validation-annotations-bbox.csv")
annotations_test = pd.read_csv("test-annotations-bbox.csv")

# Filter the annotations for "Human head"
# head_annotations = annotations[annotations['LabelName'] == head_id]
head_annotations_val = annotations_val[annotations_val['LabelName'] == head_id]
head_annotations_test = annotations_test[annotations_test['LabelName'] == head_id]

# Get the image IDs for the filtered annotations
# image_ids = head_annotations['ImageID'].unique()
image_ids_val = head_annotations_val['ImageID'].unique()
image_ids_test = head_annotations_test['ImageID'].unique()

# First, we're going to create a list of strings in the format required by the downloader
# We're assuming these are train images
# formatted_image_ids = ['train/' + id for id in image_ids]
formatted_image_ids_val = ['val/' + id for id in image_ids_val]
formatted_image_ids_test = ['test/' + id for id in image_ids_test]

# Then, we write this list to a text file
# with open('image_ids.txt', 'w') as file:
#     for image_id in formatted_image_ids:
#         file.write(f"{image_id}\n" )

with open('image_ids_val.txt', 'w') as file:
    for image_id_val in formatted_image_ids_val:
        file.write(f"{image_id_val}\n")

with open('image_ids_test.txt', 'w') as file:
    for image_id_test in formatted_image_ids_test:
        file.write(f"{image_id_test}\n")


# Replace with the path to the directory where you want to download the images
root_dwnld = "heads"
# download_folders = ["train", "val", "test"]
download_folders = ["val", "test"]

# image_ids_files = ["image_ids.txt", "image_ids_val.txt", "image_ids_test.txt"]
image_ids_files = ["image_ids_val.txt", "image_ids_test.txt"]

for folder, image_ids_file in zip(download_folders, image_ids_files):
    # This will execute the downloader script
    os.system(f"python downloader.py {image_ids_file} --download_folder={os.path.join(root_dwnld, folder)} --num_processes=5")
