from ultralytics import YOLO
import requests
import cv2
import base64
from decouple import config
import time
import numpy as np
from requests.auth import HTTPBasicAuth
from playwright.sync_api import sync_playwright
# Load the pretrained model
model = YOLO('best.pt')

# Times seen
count = 0
threshold = 2
# Define the alarm endpoint
endpoint = config('ENDPOINT')
# Define the image endpoint
imageEndpoint = config('IMAGE_ENDPOINT')
# class to detect
heron_class = 'heron'

# Function to encode image to base64
def img_to_base64(img):
    _, buffer = cv2.imencode('.png', img)
    png_as_text = base64.b64encode(buffer).decode('utf-8')
    return png_as_text

# Function to make an API call
def call_api(image):
    image_data = img_to_base64(image)
    requests.post(endpoint, json={'image': image_data, 'message': 'Heron detected multiple times'})

# Function to fetch and return image
def fetch_image():
    # use playwright to navigate to imageEndpoint and take a screenshot of the image object
    with sync_playwright() as p:
        # try catch around the browser object
        try:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_viewport_size({"width": 1280, "height": 720})
            page.goto(imageEndpoint)
            image = page.locator("img").screenshot()
            browser.close()
            # Convert the image buffer to a numpy array
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
            # resixe image to 640x360
            image = cv2.resize(image, (640, 360))
            return image
        except Exception as e:
            print(f"Error: {e}")
            return None

while True:
    image = fetch_image()
    if image is not None:
        # cv2.imshow('Detection', image)
        # if cv2.waitKey(1) == ord('q'):  # Exit loop if 'q' is pressed
        #     break     
        # Predictions from the model
        results = model(image, conf=0.8, device='mps', verbose=True)
        
        # Process each result
        for r in results:
            # Check if 'heron' is detected
            if heron_class == r.names[0] and r.boxes.conf.numel():
                count += 1

        # If heron is detected multiple times, make an API call
        if count >= threshold:
            frame = r.plot()
            call_api(frame)
            count = 0
    
    # Wait for 5 seconds before making the next request
    time.sleep(5)