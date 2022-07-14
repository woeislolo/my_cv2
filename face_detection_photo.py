import os
import os.path
import ctypes
import cv2


def detect_and_save_blur_faces(image_filename):
    face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__),
                                                      'haarcascade_frontalface_default.xml'))
    image_path = os.path.join(os.path.dirname(__file__), 'images', image_filename)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=8,
                                          minSize=(10, 10))

    faces_detected = "Objects detected: " + format(len(faces))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (153, 204, 255), 3)
        face = image[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(face, (91, 91), 0)
        image[y:y+h, x:x+w] = blur

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

    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'blur_images')):
        os.mkdir('blur_images')

    cv2.imshow(faces_detected, image)
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'blur_images', f'blur_{image_filename}'), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


detect_and_save_blur_faces(input('Введите название файла из папки image: '))
