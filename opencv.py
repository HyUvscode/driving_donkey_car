import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges for red, yellow, and green
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Threshold the image to detect specific colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Combine masks to get the final mask
    final_mask = mask_red + mask_yellow + mask_green

    # Find contours in the final mask
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours to determine the color
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Adjust the minimum contour area based on your requirement
            x, y, w, h = cv2.boundingRect(contour)
            roi_hsv = hsv[y:y + h, x:x + w]

            # Calculate mean hue value within the contour
            mean_hue = np.mean(roi_hsv[:, :, 0])

            # Determine color based on mean hue value
            if 0 <= mean_hue <= 10 or 160 <= mean_hue <= 180:
                color = "Red"
            elif 20 <= mean_hue <= 40:
                color = "Yellow"
            elif 60 <= mean_hue <= 80:
                color = "Green"
            else:
                color = "Unknown"

            # Draw color label on the traffic light
            cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the output frame with detected traffic lights
    cv2.imshow('Traffic Lights Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all windows
cap.release()
cv2.destroyAllWindows()
