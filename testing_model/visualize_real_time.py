from ultralytics import YOLO
import cv2

# Load the pretrained model
model = YOLO('../best.pt')

# test video
stream_url = './samples/false-positive-convert.mp4'

# Predictions from the model
results = model(stream_url, conf=0.8, device='mps', stream=True, verbose=True)

# Process each result
for r in results:
    frame = r.plot()  # Get the frame with bounding boxes drawn
    # Display the frame
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) == ord('q'):  # Exit loop if 'q' is pressed
        break

cv2.destroyAllWindows()