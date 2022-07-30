import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode

IMAGE_PATH = 'Media/IMG_3087.JPG'
image = cv2.imread(IMAGE_PATH)
width = image.shape[1]
height = image.shape[0]
print(width, height)
# image = image.resize(800, int((800/width) * height))
img = cv2.resize(image, dsize=(1000, int((1000/width) * height)))

reader = easyocr.Reader(['en'])
result = reader.readtext(img)
font = cv2.FONT_HERSHEY_COMPLEX

spacer = 25
with open('description.txt', 'w') as f:
    results = {}
    has_arm = False
    has_address = False
    has_tracking = False
    for detection in result:
        top_left = tuple(detection[0][0])
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = tuple(detection[0][2])
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        text = detection[1]
        if 'ARM' in text and len(text)==9:
            has_arm = True
            print(text)
            results['ARM_Code'] = text
        if 'AYRE' in text:
            has_address = True
            print(text)
            results['address'] = text
        # if len(text.strip()) == 13 and text.isnumeric():
        #     has_tracking = True
        #     print(text)
        #     results['tracking'] = text
        trackings = decode(img)
        tracking = {}
        for i in range(len(trackings)):
            tracking[i] = str(trackings[i].data.decode('utf-8'))
        results['tracking'] = tracking
        f.write(text+"\n")
        img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
        img = cv2.putText(img, text, (int(top_left[0])+25, int(top_left[1])), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
        spacer += 25

print(has_arm, has_address, has_tracking)
print(results)
plt.rcParams["figure.figsize"] = (15, 15)
plt.imshow(img)
plt.show()