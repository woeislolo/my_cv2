import os.path
import cv2


def detect_and_capture_faces(video_filename):
    face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__),
                                                      'haarcascade_frontalface_default.xml'))
    if video_filename == '0':
        capture_io = cv2.VideoCapture(0)
    else:
        capture_io = cv2.VideoCapture(os.path.join(os.path.dirname(__file__), 'video', video_filename))

    while True:
        b, image = capture_io.read()
        if b:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (153, 204, 255), 3)
                cv2.imshow('image', image)
            
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    
    capture_io.release()
    cv2.destroyAllWindows()


detect_and_capture_faces(input('Введите название видео из папки video либо 0 для захвата видео с веб-камеры: '))
