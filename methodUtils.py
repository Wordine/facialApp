#methodUtils.py
import methods.beautify
import methods.marks
from PIL import Image
import numpy as np
import cv2
def getMethodList():
    methodList = []
    pic = Image.new("RGB" ,(640, 480),(255,255,255))
    pic = np.array(pic)
    method = {'name': 'blank', 'args':'', 'img': pic}
    methodList.append(method)
    pic = methods.beautify.getExample()
    method = {'name': 'beauty', 'args':'', 'img': pic}
    methodList.append(method)
    pic = methods.marks.getExample()
    method = {'name': 'mark', 'args':'', 'img': pic}
    methodList.append(method)
    return methodList


def getMethodInfo(name):

    #s.argInfo[]
    #name     range    type
    return methodInfo
def callMethod(img, method, arg):
    if method == 'blank':
        image = img
        return image
    elif method == '':
        image = img
        return image
    elif method == 'beauty':
        print('beaty')
        image = methods.beautify.func(img)
        image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        return image
    elif method == 'mark':
        print('mark')
        image = methods.marks.func(img)
        image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        return image
    else:
        return ''


if __name__ == '__main__':
    getMethodList()
