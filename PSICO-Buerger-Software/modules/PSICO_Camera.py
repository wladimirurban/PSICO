# pip install opencv-python

# Needed Moduls
import cv2

def connect_camera():
    camera = cv2.VideoCapture(0)
    return camera

def takepicture(camera):
    return_value, image = camera.read()
    return image

def show_picture(image):
    cv2.imshow('test.png',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def delete_camera(camera):
    del(camera)

cam = connect_camera()
picture = takepicture(cam)
show_picture(picture)

