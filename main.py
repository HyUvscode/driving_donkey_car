import cv2
import numpy as np
from servor import servo_Class




# Load the YOLOv4 Tiny model and class labels
net = cv2.dnn.readNet("best2.weights", "best2.cfg")
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get the output layer names of the YOLOv4 model
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)


class CarController:
    def __init__(self):
        self.servo = servo_Class(Channel=0, ZeroOffset=0)
        # self.speed = 290
        self.steering_angle = 0
        self.is_moving = False

    def move_forward(self):
        self.steering_angle = 30
        self.servo.SetPos(375 + self.steering_angle)

    def slow(self):   
        self.steering_angle = 25
        self.servo.SetPos(375 + self.steering_angle)

    def stop(self):
        # Stop the car
        self.steering_angle = 0  # Assuming 0.5 corresponds to the neutral position
        self.servo.SetPos(375 + self.steering_angle)

        # self.is_moving = False

car = CarController() 

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # car = CarController()
    frame = cv2.flip(frame, -1)  # Flip the frame
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)
    detected_green_light = False
    detected_red_light = False

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                if classes[class_id] == "green":
                    detected_green_light = True
                elif classes[class_id] == "red":
                    detected_red_light = True
                elif classes[class_id] =="yellow":
                    detected_yellow_light = True

    # Determine car action based on traffic light detection
    if detected_green_light:
        # Move forward when green light is detected
        # Add code here to control the car to move forward
        car.move_forward()
        print("Green Light Detected - Moving Forward")
    elif detected_red_light:
        # Stop when red light is detected
        # Add code here to control the car to stop
        car.stop()
        print("Red Light Detected - Stopping")
    elif detected_yellow_light:
        #slow mode
        car.slow()
        print("Yellow Light Detected - Slow")
    else:
        # No traffic light detected, do something (optional)
        print("No Traffic Light Detected")

    cv2.imshow("Traffic Light Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
