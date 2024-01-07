# Get webcam image from osx every 10 seconds

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # height
cap.set(cv2.CAP_PROP_FPS, 30)  # frame rate

while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    print("hello")
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
