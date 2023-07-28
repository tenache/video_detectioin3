from training import training
from generateYOLO2 import get_yolo_txt
from download_with_random import download_images
EPOCHS = 21
FREEZE = 21

csvs = {
        "train":"oidv6-train-annotations-bbox.csv",
        "validation":"validation-annotations-bbox.csv",
        "test":"test-annotations-bbox.csv"
        }

def download_and_train(epochs=21,freeze=21):
    download_images()
    get_yolo_txt(csvs)
    training(epochs, freeze)

if __name__ == "__main__":
    download_and_train(EPOCHS, FREEZE)
    
