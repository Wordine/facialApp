import io
import json

import operator

import numpy as np
#from PIL import Image
from pymongo import MongoClient
from gridfs import *

import math
import datetime
import random
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

client=MongoClient('localhost',27017)
db = client.face


#imgUtils.py
#1 origin   2 transformed  3 all
def getUserFile(userid, type):
    imglist = []
    
    if type == '1':
        gridFS1 = GridFS(db, collection='user_photo')
        u_photo = gridFS1.find({'user_id':userid})
        for pic in u_photo:
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            imglist.append(image)
    elif type == '2':
        gridFS2 = GridFS(db, collection='user_trans')
        u_photo = gridFS2.find({'user_id':userid})
        for pic in u_photo:
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            imglist.append(image)
    elif type == '3':
        gridFS1 = GridFS(db, collection='user_photo')
        u_photo = gridFS1.find({'user_id':userid})
        for pic in u_photo:
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            imglist.append(image)
            
        gridFS2 = GridFS(db, collection='user_trans')
        u_photo = gridFS2.find({'user_id':userid})
        for pic in u_photo:
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            imglist.append(image)
    else: return false       
    return imglist
    

#type only allow for 1, 2
def saveUserFile(userid, type, img):
    
    #1 for sucess   2 for failure
    
    if type == '1':
        findone = col.find_one({'user_id': userid})
        image = np.array(img.convert('RGB'))
        m = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]
        m= m.tolist()
        f = img.split('.')
        count = findone['pnum']+1
        imgput = GridFS(db, collection='user_photo')
        imgput.put(img,user_id = userid,p_num = count,p_aspect = m,p_type=f[-1],p_name = findone['name'])
        
        return sucess
    
    elif type == '2': 
        return failure
    else return false
    
    

def imgTrans(img, method, arg):
    
    return imgT
    
    
def idVerify (img):
    distance_threshold=0.4
    with open('trained_knn_model.clf', 'rb') as f:
        knn_clf = pickle.load(f)
    faces_encodings = img
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold]
    if are_matches:
        userid = knn_clf.predict(faces_encodings)
        findone = col.find_one({'user_id': userid})
        uername = findone['name']
    else:
        userid = 0
        username = Unknown


    return username, userid


