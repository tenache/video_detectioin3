# Video detectioin

This project contains necessary code for training, and fine-tuning YOLO from personal datasets, and applying the model to videos for counting people, making heatmaps, etc. 

## Install packaged

You can install the required packages with 
    ```bash
    pip install -r requirements.txt
    ```

## Training

1. Navigate to the 'downloads' directory:

    ```bash
    cd downloads
    ```

2. Download or decompress the folder `heads` within downloads

3. Go to config.yaml, change the root directory. It has to be the full path. 

4. Run the following command from the terminal:


```bash
python3 training.py

```

### Changing parameters

Inside `training.py`, you can change some parameters, namely: 

1. You can change the number of ***epochs*** by changing the variable EPOCHS to whatever you want. 

You can change the number of ***layers*** you want to ***freeze*** from YOLO, by changing the parameter FREEZE. YOLO has 24 layers, so the maximum number of layers you can freeze is 23. 

You can load a different ***model***, as long as it is a valid ultralytics model. [ultralytics models](https://github.com/ultralytics/ultralytics)
Change it with `model = YOLO("yolov8n.pt") ` by default. 

By default, we have YOLOv8n, which is the smallest. 

If you want to build a new model from scratch: 
`model = YOLO("yolov8n.yaml")`

## People detection

Run the following command from the terminal:

Inside the main foler `video_detectioin3`, run the command `main2.py`

The program will ask you to delimit areas, so as to count people that move from one area to the other. 

## Generate heatmap

To generate a heatmap of the most visited or transited areas, you can run from the terminal:

`get_heatmap2.py`





