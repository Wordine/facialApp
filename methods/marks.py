import face_recognition
import cv2
import numpy as np
from PIL import Image, ImageDraw



def func(img):
    process_this_frame = 1
    img = np.asarray(img)
    if process_this_frame:
        face_landmarks_list = face_recognition.face_landmarks(img)
        pil_image = Image.fromarray(img)
        for face_landmarks in face_landmarks_list:
            d = ImageDraw.Draw(pil_image, 'RGBA')
            d.line(face_landmarks['left_eyebrow'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['right_eyebrow'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['top_lip'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['bottom_lip'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['chin'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['nose_bridge'], fill=(255, 255, 255), width=5)
            d.line(face_landmarks['nose_tip'], fill=(255, 255, 255), width=5)
            #d.ellipse((0,0, 200, 200), fill = (255, 0, 0)
    img = np.array(pil_image)
    img = img[:, :, ::-1]
    return img


def getExample():
    image = face_recognition.load_image_file("methods\Sun.jpg")
    image = Image.fromarray(image)
    return func(image)
if __name__ == '__main__':
    image = face_recognition.load_image_file("Sun.jpg")
    image = Image.fromarray(image)
    img = func(image)
    img.show()