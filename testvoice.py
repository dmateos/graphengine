import cv2
import os
import random
from PIL import Image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.transforms.functional import pil_to_tensor

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # height
cap.set(cv2.CAP_PROP_FPS, 30)  # frame rate

last_label = None

possible_strings = [
    "say Thats a {thing} you dumb cunt",
    "say Obviously thats a {thing}, you fucking bastard",
    "say I think thats a {thing}, you dickhead",
    "say You have a {thing} there, you stupid shithead"
]

while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
        pass

    img = Image.fromarray(frame)
    img = pil_to_tensor(img)

    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.8)
    model.eval()

    preprocess = weights.transforms()
    batch = [preprocess(img)]

    prediction = model(batch)[0]
    labels = [weights.meta["categories"][i] for i in prediction["labels"]]

    if len(labels) == 0:
        continue
    labels = set(labels)
    print(labels)
    label = " and ".join(labels)
    
    if label != last_label:
        string = random.choice(possible_strings)
        os.system(string.format(thing=label))
        last_label = label
