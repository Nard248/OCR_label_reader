import cv2
import matplotlib.pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
plt.rcParams["figure.figsize"] = (15, 15)


def resize_image(path):
    image = cv2.imread(path)
    height = image.shape[0]
    width = image.shape[1]
    size = (1500, int((1500 / width) * height))
    image_resized = cv2.resize(image, dsize=size)
    return image_resized


# image = cv2.imread('media/IMG_3105_rot.JPG')
image = resize_image('media/IMG_3105_rot.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
plt.imshow(image)
plt.show()
plt.imshow(gray)
plt.show()
plt.imshow(blur)
plt.show()
plt.imshow(thresh)
plt.show()
text = pytesseract.image_to_string(gray)
print(text)
# Morph open to remove noise and invert image
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
# invert = 255 - opening
