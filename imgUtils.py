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
        #f = img.split('.')
        count = findone['pnum']+1
        imgput = GridFS(db, collection='user_photo')
        imgput.put(img,user_id = userid,p_num = count,p_aspect = m,p_name = findone['name'])
        
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

def add_user(imglist, username):
    X = []
    X0 = []
 
    b = open(r"X.txt", "r",encoding='UTF-8')
    outx = b.read()
    outx =  json.loads(outx)
    #print(out)
    for m in outx:
        X.append(m)
        m0 = np.array(m)
        X0.append(m0)

    d = open(r"y.txt", "r",encoding='UTF-8')
    outy = d.read()
    y = json.loads(outy)

    #print(out)
    count = 0
    userid = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1, 10)) for i in range(5)])
    
    for img in imglist:
        image = np.array(img.convert('RGB'))
        m0 = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]
        m = m0.tolist()

        count += 1
        imgput = GridFS(db, collection='user_photo')
        imgput.put(img,user_id = userid,p_num = count,p_aspect = m,p_name = username)

        X.append(m)
        X0.append(m0)
        y.append(userid)
    
    user1 = {'name': username, 'user_id': userid, 'pnum': count}
    col = db.user
    one_insert = col.insert_one(user1)
    
        # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X0, y)

    # Save the trained KNN classifier
    with open("trained_knn_model.clf", 'wb') as f:
        pickle.dump(knn_clf, f)

    xx = json.dumps(X)
    yy = json.dumps(y)

    a = open(r"X.txt", "w",encoding='UTF-8')
    a.write(xx)
    a.close()

    c= open(r"y.txt", "w",encoding='UTF-8')
    c.write(yy)
    c.close()

    return success

