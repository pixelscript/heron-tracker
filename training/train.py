from ultralytics import YOLO

# Loading pretrained model
model = YOLO('yolov8n.pt')

# Train the model using M1 M2 Macs
results = model.train(data='heron_yolov8/data.yaml', epochs=100, imgsz=640, device='mps')
