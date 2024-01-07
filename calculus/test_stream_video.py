# Get webcam image from osx every 10 seconds

import cv2
import base64
import requests
import time

model_id = 9

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # height
cap.set(cv2.CAP_PROP_FPS, 30)  # frame rate

while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
        time.sleep(1)

    # convert frame to jpg 
    ret, frame = cv2.imencode(".jpg", frame)

    files = {"input": frame}

    # Auth with django csrf for requests
    session = requests.Session()
    session.get(f"http://dmacstudio.mateos.lan:8081/calculus/models/{model_id}")
    csrf_token = session.cookies["csrftoken"]

    # send frame to server as post data using requests
    response = session.post(f"http://dmacstudio.mateos.lan:8081/calculus/models/{model_id}", files=files, headers={"X-CSRFToken": csrf_token})
    print(response.text)
