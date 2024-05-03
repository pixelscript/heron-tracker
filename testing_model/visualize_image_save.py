from ultralytics import YOLO
import cv2

# Load the pretrained model
model = YOLO('../best.pt')

# test image
image = './samples/evil2.png'

# Predictions from the model
results = model(image, conf=0.5, device='mps', stream=True, verbose=True)

for r in results:
    frame = r.plot()  # Get the frame with bounding boxes drawn
    # write the frame to a png
    cv2.imwrite('output/test_output.png', frame)