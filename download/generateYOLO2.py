import pandas as pd
import os
import glob

# Load the bounding boxes annotations
csvs = {
        "train":"oidv6-train-annotations-bbox.csv",
        "validation":"validation-annotations-bbox.csv",
        "test":"test-annotations-bbox.csv"
        }

def get_yolo_txt(csvs):
    for data_type, file_path in csvs.items():
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} not found")
            continue

        print("About to read annotations ...")
        annotations = pd.read_csv(file_path)
        print('Read annotations ... ')

        base_dir_images = os.path.join("heads","images", data_type)  # the base directory where your images are stored

        # List all the images in the directory
        images = glob.glob(os.path.join(base_dir_images, "*.jpg"))
        print(f"len of images is {len(images)}")
        # Extract the image IDs from the file names
        image_ids = [os.path.splitext(os.path.basename(img))[0] for img in images]

        # Filter the annotations for images that are present in the directory
        print(f"len of annotations is {len(annotations)}")
        print(f"len of label name is len {len(annotations['LabelName']== '/m/04hgtk')}")
        print(f"IMAGEID in annotations{annotations['ImageID'][0]}")
        print(f"imageids format{image_ids[0]}")
        annotations = annotations[annotations['ImageID'].isin(image_ids) & (annotations['LabelName'] == "/m/04hgtk")]
        print(f"len of annotations is {len(annotations)}")
        # Check if the DataFrame is not empty
        base_dir_labels = os.path.join("heads","labels", data_type)
        if not annotations.empty:
            print("not empty")
            # Calculate center, width and height of bounding boxes
            x_center = (annotations['XMax'] + annotations['XMin']) / 2
            y_center = (annotations['YMax'] + annotations['YMin']) / 2
            width = annotations['XMax'] - annotations['XMin']
            height = annotations['YMax'] - annotations['YMin']


            for image_id, x_c, y_c, w, h in zip(annotations['ImageID'], x_center, y_center, width, height):
                # Construct the label file path
                label_path = os.path.join(base_dir_labels, image_id + ".txt")

                # Append the bounding box annotation to the label file
                with open(label_path, 'a') as file:
                    file.write(f'0 {x_c} {y_c} {w} {h}\n')  # Assuming 'Human head' is class 0
                # Remove the id from the image_ids list
                try:
                    image_ids.remove(image_id)
                except ValueError:
                    pass

        # make an empty file for those images without human heads
        for image_id in image_ids:
            # Construct the label file path
            label_path_id = os.path.join(base_dir_labels, image_id + ".txt")
            # Write an empty file
            with open(label_path_id, 'a') as file:
                file.write("")

if __name__ == "__main__":
    # print("hi there ... ")
    get_yolo_txt(csvs)
