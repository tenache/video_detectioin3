from ultralytics import YOLO
EPOCHS = 19
FREEZE = 21  # replace this with the number of layers you want to freeze (23 is the maximum)
# Load a model
# this is just the architecture/model 
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# guy removes next line ... 
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Freeze the first n layers


for i, (name, param) in enumerate(model.model.named_parameters()):
    if i < FREEZE:
        param.requires_grad = False

# Use the model
model.train(data="config.yaml", epochs=EPOCHS)  # train the model

## guy removes everthing from here ... 
metrics = model.val()  # evaluate model performance on the validation set
results = model("/home/thibbard/video_detectioin2/photo-1517732306149-e8f829eb588a.avif")  # predict on an image
path = model.export(format="onnx")  # export the model to ONNX format