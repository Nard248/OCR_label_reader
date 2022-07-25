# Importing library
import cv2
from pyzbar.pyzbar import decode


# Make one method to decode the barcode
IMAGE_PATH = 'IMG_3087.JPG'
image = cv2.imread(IMAGE_PATH)
width = image.shape[1]
height = image.shape[0]
print(width, height)
# image = image.resize(800, int((800/width) * height))
img = cv2.resize(image, dsize=(1000, int((1000/width) * height)))

result = decode(img)
for decoded in result:
    print(str(decoded.data.decode('utf-8')))