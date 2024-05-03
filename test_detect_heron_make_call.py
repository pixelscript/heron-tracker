from ultralytics import YOLO
import requests
import cv2
import base64
from decouple import config

# Load the pretrained model
model = YOLO('best.pt')

# Define the RTSP stream
stream_url = 'test.mp4'
print(stream_url)
# Define the endpoint
endpoint = config('ENDPOINT')
results = model(stream_url, conf=0.8, device='mps', stream=True, verbose=True)

# Initialize counter
heron_count = 0
N = 5  # Threshold of consecutive detections

# Function to encode image to base64
def img_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text

# Function to make an API call
def call_api(image):
    image_data = img_to_base64(image)
    requests.post(endpoint, json={'image': image_data, 'message': 'Heron detected multiple times'})

# Process each result
for r in results:
    heron_class = 'heron'
    # Check if 'heron' is detected
    if heron_class == r.names[0] and r.boxes.conf.numel():
        heron_count += 1
        if heron_count >= N:
            frame = r.plot()  # Get the frame with bounding boxes drawn
            call_api(frame)
            heron_count = 0  # Optionally reset the counter after the API call
    else:
        heron_count = 0  # Reset counter if other objects are detected