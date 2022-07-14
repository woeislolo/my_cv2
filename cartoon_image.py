import os.path
import ctypes
import cv2


def image_to_cartoon(image_filename):
    path_to_pic = os.path.join(os.path.dirname(__file__), 'images', image_filename)
    image = cv2.imread(path_to_pic)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    image_height, image_width = image.shape[:2]
    user = ctypes.windll.user32
    screensize_width, screensize_height = user.GetSystemMetrics(0), user.GetSystemMetrics(1)
    if image_height > screensize_height or image_width > screensize_width:
        k = image_height / image_width
        if k > 1:
            image_height = int(screensize_height * 0.9)
            image_width = int(image_height / k)
        else:
            image_width = int(screensize_width * 0.9)
            image_height = int(image_width * k)

        image = cv2.resize(image, (image_width, image_height), cv2.INTER_AREA)
        edges = cv2.resize(edges, (image_width, image_height), cv2.INTER_AREA)
        cartoon = cv2.resize(cartoon, (image_width, image_height), cv2.INTER_AREA)

    cv2.imshow('Image', image)
    cv2.imshow('Edges', edges)
    cv2.imshow('Cartoon', cartoon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_to_cartoon(input('Введите название файла из папки image: '))
