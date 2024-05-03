from ultralytics import YOLO
import os
import cv2
from decouple import config

# Load the pretrained model
model = YOLO('best.pt')

# Define the RTSP stream
# stream_url = config('STREAM_URL')
stream_url = 'test.mp4'
# Define the endpoint
endpoint = os.getenv('ENDPOINT')
# Predictions from the model
results = model(stream_url, conf=0.8, device='mps', stream=True, verbose=True)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output/test_output.mp4', fourcc, 30, (1920, 1080))

# Process each result
for r in results:
    frame = r.plot()  # Get the frame with bounding boxes drawn
    # Display the frame
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) == ord('q'):  # Exit loop if 'q' is pressed
        break
    out.write(frame)

out.release()
cv2.destroyAllWindows()