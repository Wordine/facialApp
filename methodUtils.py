#methodUtils.py

from methods import *


def getMethodList():
    methodList = []

    method = {name: 'recognition'}

    return methodList


def getMethodInfo(name):

    #s.argInfo[]
    #name     range    type
    return methodInfo
def callMethod(img, method, arg):
    if method == 'recognition':
        image = recog(img, arg)
    else:
        return ''

    return image

