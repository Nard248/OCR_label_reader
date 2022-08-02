import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode
import torch

IMAGE_PATH = 'Media/IMG_3088.JPG'


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def resize_image(path):
    image = cv2.imread(path)
    height = image.shape[0]
    width = image.shape[1]
    size = (1500, int((1500 / width) * height))
    image_resized = cv2.resize(image, dsize=size)
    return image_resized


def reader_ocr(image):
    with open('description.txt', 'w') as f:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image)
        font = cv2.FONT_HERSHEY_COMPLEX
        return_dict = {}
        tracking_dict = {}
        for detection in result:
            text = detection[1]
            top_left = tuple(detection[0][0])
            bot_right = tuple(detection[0][2])
            top_left = (int(top_left[0]), int(top_left[1]))
            bot_right = (int(bot_right[0]), int(bot_right[1]))
            f.write(text + '\n')
            if 'ARM' in text:
                text = text.split()
                for l in text:
                    if 'ARM' in l:
                        return_dict['arm_code'] = l
                        image = cv2.rectangle(image, top_left, bot_right, (255, 0, 0), 2)
                        image = cv2.putText(image, l, (int(top_left[0]) + 25, int(top_left[1])), font, 2, (255, 0, 0),
                                            2, cv2.LINE_AA)
            if 'AYRE' in text:
                return_dict['address'] = text
                image = cv2.rectangle(image, top_left, bot_right, (0, 255, 0), 2)
                image = cv2.putText(image, text, (int(top_left[0]) + 25, int(top_left[1])), font, 2, (0, 255, 0), 2,
                                    cv2.LINE_AA)
        decoded = decode(image)
        for i in range(len(decoded)):
            tracking_dict[i] = str(decoded[i].data.decode('utf-8'))
        return_dict['tracking'] = tracking_dict
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.imshow(image)
    plt.show()
    return return_dict


def simple_reader(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    font = cv2.FONT_HERSHEY_COMPLEX
    return_dict = {}
    tracking_dict = {}
    for detection in result:
        text = detection[1]
        if 'ARM' in text:
            text = text.split()
            for l in text:
                if 'ARM' in l:
                    return_dict['arm_code'] = l
        if 'AYRE' in text:
            return_dict['address'] = text
    decoded = decode(image)
    for i in range(len(decoded)):
        tracking_dict[i] = str(decoded[i].data.decode('utf-8'))
    return_dict['tracking'] = tracking_dict
    return return_dict


img = resize_image(IMAGE_PATH)
img = get_grayscale(img)
print(simple_reader(img))
