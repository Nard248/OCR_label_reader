import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode
import torch

IMAGE_PATH = 'the_photo.jpg'


def resize_image(path):
    image = cv2.imread(path)
    height = image.shape[0]
    width = image.shape[1]
    size = (1500, int((1500 / width) * height))
    image_resized = cv2.resize(image, dsize=size)
    return image_resized


def reader_ocr(image, number):
    # with open('description.txt', 'w') as f:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    font = cv2.FONT_HERSHEY_COMPLEX
    for detection in result:
        text = detection[1]
        top_left = tuple(detection[0][0])
        bot_right = tuple(detection[0][2])
        top_left = (int(top_left[0]), int(top_left[1]))
        bot_right = (int(bot_right[0]), int(bot_right[1]))
        if str(number) in text:
            image = cv2.rectangle(image, top_left, bot_right, (255, 0, 0), 2)
            image = cv2.putText(image, text, (int(top_left[0]) + 25, int(top_left[1])), font, 2, (255, 0, 0), 2,
                                cv2.LINE_AA)
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.imshow(image)
    plt.show()


def search_number_arr(image, number_arr):
    # with open('description.txt', 'w') as f:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    font = cv2.FONT_HERSHEY_COMPLEX
    for detection in result:
        text = detection[1]
        top_left = tuple(detection[0][0])
        bot_right = tuple(detection[0][2])
        top_left = (int(top_left[0]), int(top_left[1]))
        bot_right = (int(bot_right[0]), int(bot_right[1]))
        for number in number_arr:
            if str(number) in text:
                image = cv2.rectangle(image, top_left, bot_right, (255, 0, 0), 2)
                image = cv2.putText(image, text, (int(top_left[0]) + 25, int(top_left[1])), font, 2, (255, 0, 0), 2,
                                    cv2.LINE_AA)
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.imshow(image)
    plt.show()


img = resize_image(IMAGE_PATH)
search_number_arr(img, [1984, '0004', 6969, 4200])
