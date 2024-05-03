from ultralytics import YOLO
import cv2

# Load the pretrained model
model = YOLO('../best.pt')

# test video
stream_url = './samples/false-positive-convert.mp4'

# get the video size and pfs from the video
video = cv2.VideoCapture(stream_url)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

# Predictions from the model
results = model(stream_url, conf=0.8, device='mps', stream=True, verbose=True)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output/test_output.mp4', fourcc, fps, (width, height))

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