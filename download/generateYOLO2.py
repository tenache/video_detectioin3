import pandas as pd
import os
import glob

# Load the bounding boxes annotations
csvs = {
        "train":"oidv6-train-annotations-bbox.csv",
        "val":"validation-annotations-bbox.csv",
        "test":"test-annotations-bbox.csv"
        }

def get_yolo_txt(csvs):
    for data_type, file_path in csvs.items():
        print("About to read annotations ...")
        annotations = pd.read_csv(file_path)
        print('Read annotations ... ')

        base_dir = os.path.join("heads", data_type)  # the base directory where your images are stored

        # List all the images in the directory
        images = glob.glob(os.path.join(base_dir, "*.jpg"))
        # Extract the image IDs from the file names
        image_ids = [os.path.splitext(os.path.basename(img))[0] for img in images]

        # Filter the annotations for images that are present in the directory
        annotations = annotations[annotations['ImageID'].isin(image_ids)]

        # Further filter the annotations for "Human head"
        annotations = annotations[annotations['LabelName'] == "/m/04hgtk"]

        # Calculate center, width and height of bounding boxes
        x_center = (annotations['XMax'] + annotations['XMin']) / 2
        y_center = (annotations['YMax'] + annotations['YMin']) / 2
        width = annotations['XMax'] - annotations['XMin']
        height = annotations['YMax'] - annotations['YMin']

        for image_id, x_c, y_c, w, h in zip(annotations['ImageID'], x_center, y_center, width, height):
            # Construct the label file path
            label_path = os.path.join(base_dir, image_id + ".txt")

            # Append the bounding box annotation to the label file
            with open(label_path, 'a') as file:
                file.write(f'0 {x_c} {y_c} {w} {h}\n')  # Assuming 'Human head' is class 0

if __name__ == "__main__":
    print("hi there ... ")
    get_yolo_txt(csvs)
