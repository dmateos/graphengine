import cv2
import os
from PIL import Image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.transforms.functional import pil_to_tensor

model_id = 9
host = "http://dmacstudio.mateos.lan:8081"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # height
cap.set(cv2.CAP_PROP_FPS, 30)  # frame rate

while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
        #time.sleep(1)
        pass

    # convert frame to jpg
    ret, frame = cv2.imencode(".jpg", frame)
    img = Image.open(frame)
    img = pil_to_tensor(img)

    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.8)
    model.eval()

    preprocess = weights.transforms()
    batch = [preprocess(img)]

    prediction = model(batch)[0]
    labels = [weights.meta["categories"][i] for i in prediction["labels"]]

    # say first label
    os.system(f"say {labels[0]}")
