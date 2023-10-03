import cv2
import numpy as np

# Load the YOLOv4 Tiny model and class labels
net = cv2.dnn.readNet("weights/best2.weights", "cfg/best2.cfg")
with open("names/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get the output layer names of the YOLOv4 model
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

light_status = "Unknown"

def process_frame(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)
    detections = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                detections.append((classes[class_id], confidence, (x, y, x+w, y+h)))

    return detections

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, -1)  # Flip the frame
    detections = process_frame(frame)

    # light_status = "Unknown"
    for label, confidence, bbox in detections:
        if 'green' in label:
            light_status = 'Green Light'
        elif 'red' in label:
            light_status = 'Red Light'
        elif 'yellow' in label:
            light_status = 'Yellow Light'

        x, y, x_plus_w, y_plus_h = bbox
        cv2.rectangle(frame, (x, y), (x_plus_w, y_plus_h), (0, 255, 0), 2)
        cv2.putText(frame, light_status, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    print("Traffic Light Status:", light_status)
    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
