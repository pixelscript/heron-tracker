from ultralytics import YOLO
import requests
import cv2
import base64
from decouple import config
import numpy as np

# Load the model
model = YOLO('best.pt')

# Initialize counter
count = 0
# Threshold of consecutive detections
threshold = 5

# Define the alarm endpoint
endpoint = config('ENDPOINT')
# Define the image endpoint
imageEndpoint = config('IMAGE_ENDPOINT')
# class to detect
detection_class = 'heron'


# Function to encode image to base64
def img_to_base64(img):
    _, buffer = cv2.imencode('.png', img)
    png_as_text = base64.b64encode(buffer).decode('utf-8')
    return png_as_text

# Function to make an API call
def call_api(image):
    try:
        image_data = img_to_base64(image)
        requests.post(endpoint, json={'image': image_data, 'message': 'Heron detected multiple times'})
    except Exception as e:
        print(f"Error: {e}")
        return None   

# Function to fetch and return image
def fetch_image():
    # try catch around the browser object
    try:
        image = requests.get(imageEndpoint)
        image = cv2.imdecode(np.frombuffer(image.content, np.uint8), cv2.IMREAD_COLOR)
        width = 640
        height = 384
        image = cv2.resize(image, (width, height))
        return [image, width, height]
    except Exception as e:
        print(f"Error: {e}")
        return [None, 0, 0]
    
def test_image(image, width, height):
    global count
    try:
        results = model(image, conf=0.8, device='mps', verbose=True, imgsz=(height, width))
        # Process each result
        for r in results:
            # Check if 'heron' is detected
            if detection_class == r.names[0] and r.boxes.conf.numel():
                count += 1
                return r
    except Exception as e:
        print(f"Error: {e}")
        return None
    
# Calculate time main loop took
while True:
    # Calculate time loop took
    time_start = cv2.getTickCount()
    [image, width, height] = fetch_image()
    if image is not None:
        # Predictions from the model
        r = test_image(image, width, height)
        # If heron is detected multiple times, make an API call
        time_end = cv2.getTickCount()
        time_loop = (time_end - time_start) / cv2.getTickFrequency()
        print(f"Loop took {time_loop} seconds")
        if count >= threshold:
            if (r is not None):
                frame = r.plot()
                call_api(frame)
            count = 0
