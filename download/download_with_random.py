import requests
import csv
# import fiftyone as fitty
"""
dataset = fitty.zoo.load_zoo_dataset(
              "open-images-v7",
              split="validation",
              label_types=["detections", "segmentations", "points"],
              classes=["Cat"],
              max_samples=2,
          )

"""
import pandas as pd
import os
import random as rd
import numpy as np
from generateYOLO2 import get_yolo_txt
from training import training
EPOCHS = 50
FREEZE = 21

def download_images():

    PROP_OF_ALL_IMAGES = 0.01

    # Load the class descriptions
    classes = pd.read_csv('oidv7-class-descriptions-boxable.csv', header=None, names=['id', 'name'])

    # Find the class ID for "Human head"
    head_id = classes[classes['name'] == 'Human head']['id'].values[0]

    # Load the bounding boxes annotations
    annotations = pd.read_csv('oidv6-train-annotations-bbox.csv')

    annotations_val = pd.read_csv("validation-annotations-bbox.csv")

    annotations_test = pd.read_csv("test-annotations-bbox.csv")


    # Download some other images, just to confuse the AI a little
    random_mask_train = np.array([rd.random() for x in range(len(annotations))])
    # Filter the annotations for "Human head"
    head_annotations = annotations[(annotations['LabelName'] == head_id) | (random_mask_train < PROP_OF_ALL_IMAGES)]



    random_mask_val = np.array([rd.random() for x in range(len(annotations_val))])
    head_annotations_val = annotations_val[(annotations_val['LabelName'] == head_id) | (random_mask_val < PROP_OF_ALL_IMAGES)]


    random_mask_test = np.array([rd.random() for x in range(len(annotations_test))])
    head_annotations_test = annotations_test[(annotations_test['LabelName'] == head_id )| (random_mask_test < PROP_OF_ALL_IMAGES)]


    # Get the image IDs for the filtered annotations
    image_ids = head_annotations['ImageID'].unique()

    image_ids_val = head_annotations_val['ImageID'].unique()

    image_ids_test = head_annotations_test['ImageID'].unique()


    # Now you can use these image IDs to download the images

    # First, we're going to create a list of strings in the format required by the downloader
    # We're assuming these are train images
    formatted_image_ids = [os.path.join('train',id) for id in image_ids]

    formatted_image_ids_val = [os.path.join('validation',id) for id in image_ids_val]

    formatted_image_ids_test = [os.path.join('test',id) for id in image_ids_test]

    # Then, we write this list to a text file
    with open('image_ids.txt', 'w') as file:
        for image_id in formatted_image_ids:
            file.write(f"{image_id}\n" )
            
    with open('image_ids_val.txt', 'w') as file:
        for image_id_val in formatted_image_ids_val:
            file.write(f"{image_id_val}\n")
            
    with open('image_ids_test.txt', 'w') as file:
        for image_id_test in formatted_image_ids_test:
            file.write(f"{image_id_test}\n")
            



    # Replace with the path to the directory where you want to download the images
    root_dwnld = os.path.join("heads", "images")
    download_folders = ["train", "validation", "test"]
    # download_folders = ["val","test"]

    image_ids_files = ["image_ids.txt", "image_ids_val.txt", "image_ids_test.txt"]
    # image_ids_files = ["image_ids_val.txt", "image_ids_test.txt"]

    for folder, image_ids_file in zip(download_folders, image_ids_files):
        # This will execute the downloader script
        os.system(f"python downloader.py {image_ids_file} --download_folder={os.path.join(root_dwnld, folder)} --num_processes=5")

# Load the bounding boxes annotations
csvs = {
        "train":"oidv6-train-annotations-bbox.csv",
        "validation":"validation-annotations-bbox.csv",
        "test":"test-annotations-bbox.csv"
        }
if __name__ == "__main__":
    download_images()
    # get_yolo_txt(csvs)
    # training


