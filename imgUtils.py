import io
import json

import operator
import shutil

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
    
    if type == 1:
        gridFS1 = GridFS(db, collection='user_photo')
        u_photo = gridFS1.find({'user_id':userid})
        for pic in u_photo:
            p_user = pic.pname
            p_hash = pic.phash
            p_id = pic.pid
            p_date = pic.pdate
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            image = np.array(image)
            dic = {'user':p_user,'hash':p_hash,'id':p_id,'date':pdate,'img':image}
            imglist.append(dic)
    elif type == 2:
        gridFS2 = GridFS(db, collection='user_trans')
        u_photo = gridFS2.find({'user_id':userid})
        for pic in u_photo:
            p_user = pic.username
            p_hash = pic.phash
            p_id = pic.pid
            p_date = pic.pdate
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            image = np.array(image)
            dic = {'user':p_user,'hash':p_hash,'id':p_id,'date':pdate,'img':image}
            imglist.append(dic)
    elif type == 3:
        gridFS1 = GridFS(db, collection='user_photo')
        u_photo = gridFS1.find({'user_id':userid})
        for pic in u_photo:
            p_user = pic.username
            p_hash = pic.phash
            p_id = pic.pid
            p_date = pic.pdate
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            image = np.array(image)
            dic = {'user':p_user,'hash':p_hash,'id':p_id,'date':pdate,'img':image}
            imglist.append(dic)
            
        gridFS2 = GridFS(db, collection='user_trans')
        for pic in u_photo:
            p_user = pic.username
            p_hash = pic.phash
            p_id = pic.pid
            p_date = pic.pdate
            data = pic.read()
            image = Image.open(io.BytesIO(data))
            image = np.array(image)
            dic = {'user':p_user,'hash':p_hash,'id':p_id,'date':pdate,'img':image}
            imglist.append(dic)
    else: return Flase
    return imglist
    

#type only allow for 1, 2
def saveUserFile(userid, type, img):

    col = db.user
    #1 for sucess   2 for failure

    fpath = 'user'
    setDir(fpath)
    
    print ('enter save mtehod')
    if type == 1:
        findone = col.find_one({'user_id': userid})
        #f = img.split('.')
        img = Image.fromarray(np.uint8(img)).convert('RGB')
        img.save(fpath + '\\' + findone['name'] + '.png')
        datatamp=open(fpath + '\\' + findone['name'] + '.png','rb')
        pdate = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        pid = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1, 10)) for i in range(5)])
        phash = hash(pid)
        
        count = findone['pnum']+1
        imgput = GridFS(db, collection='user_photo')
        imgput.put(datatamp, user_id=userid, pname=findone['name'],phash = phash,pdate = pdate,pid = pid)
        col.update_one({'user_id': userid}, {'$inc': {'pnum': +1}})
        datatamp.close()
        print ('saved')
        return 1
    
    
    
    
def idVerify (img):
    col = db.user
    distance_threshold=1
    with open('trained_knn_model.clf', 'rb') as f:
        knn_clf = pickle.load(f)
    # X_face_locations = face_recognition.face_locations(img)
    # faces_encodings = face_recognition.face_encodings(img, known_face_locations=X_face_locations)
    img = img.reshape (1, -1)
    closest_distances = knn_clf.kneighbors(img, n_neighbors=1)
    #print(len(X_face_locations))
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(1)]
    if are_matches:
        userid = knn_clf.predict(img)[0]
        # print(userid)
        # print(type(userid))
        # print(userid[0])
        findone = col.find_one({'user_id': userid})
        username = findone['name']
    else:
        userid = 0
        username = 'Unknown'


    return username, userid

def add_user(img, username):
    X = []
    X0=[]
    y = []

    userid = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1, 10)) for i in range(5)])

    user1 = {'name': username, 'user_id': userid, 'pnum': 0,'uaspact':img.tolist()}
    col = db.user
    one_insert = col.insert_one(user1)

    if os.path.exists('X.txt'):
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
    
    X0.append(img)
    X.append(img.tolist())
    y.append(userid)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X0, y)

    # Save the trained KNN classifier
    with open("trained_knn_model.clf", 'wb') as f:
        pickle.dump(knn_clf, f)
    
    xx = json.dumps(X)
    yy = json.dumps(y)

    a = open(r"X.txt", "w+",encoding='UTF-8')
    a.write(xx)
    a.close()

    c= open(r"y.txt", "w+",encoding='UTF-8')
    c.write(yy)
    c.close()

    return 1

def del_pic(pid,userid):
    gridFS = GridFS(db, collection='user_photo')
    id = gridFS.find({'pid':pid})[0]._id
    gridFS.delete(id)
    col.update_one({'user_id':userid},{'$inc':{'pnum':-1}})
    return 1
def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)