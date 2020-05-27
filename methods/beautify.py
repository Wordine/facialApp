import face_recognition
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time


def func(img): 
    process_this_frame = 1
    img = np.asarray(img)

    if process_this_frame:
        face_landmarks_list = face_recognition.face_landmarks(img)
        pil_image = Image.fromarray(img)
        for face_landmarks in face_landmarks_list:
            d = ImageDraw.Draw(pil_image, 'RGBA')
            # Make the eyebrows into a nightmare
            d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
            d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
            d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
            d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)
            # Gloss the lips
            d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
            d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
            d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
            d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

            # Sparkle the eyes
            d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
            d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

            # Apply some eyeliner
            d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
            d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
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
    func(image)