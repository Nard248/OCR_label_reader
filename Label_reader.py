import cv2
import easyocr
import numpy as np
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode
from filter import get_grayscale, remove_noise, thresholding, dilate, erode, opening, canny, deskew

IMAGE_PATH = 'Media/IMG_3105.JPG'


def resize_image(path):
    image = cv2.imread(path)
    height = image.shape[0]
    width = image.shape[1]
    size = (1500, int((1500 / width) * height))
    image_resized = cv2.resize(image, dsize=size)
    return image_resized


def reader_ocr(image):
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
        if 'ARM' in text:
            text_alt = text.split()
            for j in text_alt:
                if 'ARM' in j:
                    return_dict['arm_code'] = j
                    image = cv2.rectangle(image, top_left, bot_right, (255, 0, 0), 2)
                    image = cv2.putText(image, j, (int(top_left[0]) + 25, int(top_left[1])), font, 2, (255, 0, 0),
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
    return_dict = {}
    tracking_dict = {}
    for detection in result:
        text = detection[1]
        if 'ARM' in text:
            text_alt = text.split()
            for j in text_alt:
                if 'ARM' in j:
                    return_dict['arm_code'] = j
        if 'AYRE' in text:
            return_dict['address'] = text
    decoded = decode(image)
    for i in range(len(decoded)):
        tracking_dict[i] = str(decoded[i].data.decode('utf-8'))
    return_dict['tracking'] = tracking_dict
    return return_dict


img = resize_image(IMAGE_PATH)
img = get_grayscale(img)
print(reader_ocr(img))
