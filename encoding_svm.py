import cv2 as cv 
import face_recognition
import pickle
import os
import tensorflow as tf
import keras
import matplotlib.pyplot as plt 
import pandas as pd 

import numpy as np
from sklearn.svm  import SVC

foldermodelpath="img"
pathlist=os.listdir(foldermodelpath)
imgpathlist=[]

stdID=[]

for path in pathlist:
    imgpathlist.append(cv.imread(os.path.join(foldermodelpath,path)))
    stdID.append(os.path.splitext(path)[0])



def findencoding(imagelist):
    encode_list=[]
    for img in imagelist:
        imgb=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        face_corframe=face_recognition.face_locations(imgb)
        encode=face_recognition.face_encodings(imgb,face_corframe)
        
        encode_list.append(encode)
        print(encode_list)
    return encode_list



def x_train_y_train(img_path='img'):
    pathlist=os.listdir(img_path)
    pathlist_img=[]
    y_lable=[]
   
    x_feature=[]

    
    for path in pathlist:
        img=cv.imread(os.path.join(img_path,path))
        
        
        imgs=cv.resize(img,(0,0),None,0.25,0.25)
        x_feature.append(imgs)
        


        pathlist_img.append(os.path.join(img_path,path))
        lable=int(os.path.splitext(path)[0])
        print(pathlist_img)
        y_lable.append(lable)
    x_feature=findencoding(x_feature)
    
    return pathlist_img,x_feature,y_lable


def model(x,y):
    
    model=SVC(C=1,kernel="poly")
    model.fit(x,y)
    return model



pathlist_img,x,y=x_train_y_train()

number_of_img,nx,ny=np.array(x).shape
#cv.imshow('img',x[0][0])

#cv.waitKey(0)
X=np.array(x).reshape(number_of_img,nx*ny)

svm_m=model(X,y)
#print(svm_m.fit_status_)

filename = 'nn_encode_model.sav'
pickle.dump((svm_m,pathlist_img,y), open(filename, 'wb'))


def test(img,model):
    
    preo=model.predict(img)

       
    return preo

