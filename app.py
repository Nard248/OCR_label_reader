import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

IMAGE_PATH = 'download.png'

reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH)
font = cv2.FONT_HERSHEY_COMPLEX

img = cv2.imread(IMAGE_PATH)
spacer = 25
with open('description.txt', 'w') as f:
    for detection in result:
        top_left = tuple(detection[0][0])
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = tuple(detection[0][2])
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        text = detection[1]
        f.write(text+"\n")
        img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
        img = cv2.putText(img, text, (int(top_left[0])+25, int(top_left[1])), font, 0.5, (255, 255, 0), 1, cv2.LINE_4)
        spacer += 25


plt.imshow(img)
plt.show()