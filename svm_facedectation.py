import cv2 as cv 
import numpy as np 
import pandas as pd
import face_recognition
from sklearn.svm  import SVC
import os
import pytz
import tensorflow as tf
import pickle
from datetime import date,datetime

cap=cv.VideoCapture(0)
cap.set(3,400)
cap.set(4,600)







import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-76762-default-rtdb.firebaseio.com/"

                            }  )

ref=db.reference('Students/')

ref_att=db.reference(f'Attendance/{date.today()}/')






def prepare_pre(pre):
    if len(str(pre[0]))==1:
        return '00'+str(pre[0])
    elif len(str(pre[0]))==2:
        return '0'+str(pre[0])
    else:
        return str(pre[0])












def test(img,model):
    img=img.reshape(1,-1)
    preo=model.predict(img)

       
    return preo





def bb_valid(y1,x1,y2,x2):
    
    if y2-y1 and x2-x1 >= 160:
        return True
    return False
        






file=open("nn_encode_model.sav","rb")
model,pathlist,y=pickle.load(file)
file.close()
svm_model=model


while True:
    succ,img=cap.read()
    imgnew=img.copy()
    imgs=cv.resize(img,(0,0),None,0.25,0.25)
    imgs=cv.cvtColor(imgs,cv.COLOR_BGR2RGB)
    vis = np.zeros((600, 1200,3), np.uint8)

    
    
    
    imgrect=img.copy()
    

    face_corframe=face_recognition.face_locations(imgs)
    
    
    

    encoding_currframe=face_recognition.face_encodings(imgs,face_corframe)
    
    for encoface, facelocat  in zip(encoding_currframe,face_corframe):
        
        pre=test(encoface,svm_model)

       

        font=cv.FONT_HERSHEY_SIMPLEX
        y1 ,x2 ,y2 , x1 =facelocat
        
        y1 ,x2 ,y2 , x1=y1*4 ,x2*4 ,y2*4 , x1*4
        bbox=  y1 ,x2 ,y2 , x1
        

        print(y)
        for i in range(0,len(y)-1):
            if y[i]== pre and bb_valid(y1,x1,y2,x2) :
                imgrect=cv.rectangle(imgrect,(x1,y1),(x2,y2),(0,255,0),3)
            
                imgrect=cv.putText(imgrect, f"std ID :{y[i]}",(x1,y1-8),font,0.6,(0,255,0),1,cv.LINE_4)
                data=ref.get()
                
                ppre=prepare_pre(pre)
                val=data[ppre]
                try:
                    data_att=ref_att.get()
                


                
              
                    print(data_att)
                    if ppre not in data_att:
                        update_data={
                            str(ppre):{
                                    "name":val['name'],
                                    "major":val['major'],
                                    "Lecture sub":val['Lecture sub'],
                                    "Attendance time":str(datetime.now(tz=pytz.timezone('asia/kolkata'))),
                                    
                            }
                        }
                        vis=cv.putText(vis,f"Name:{val['name']}",(700,260),font,0.6,(0,255,0),1,cv.LINE_4)
                        vis=cv.putText(vis,f"major:{val['major']}",(700,280),font,0.6,(0,255,0),1,cv.LINE_4)
                        vis=cv.putText(vis,f"Lecture sub:{val['Lecture sub']}",(700,300),font,0.6,(0,255,0),1,cv.LINE_4)
                        vis=cv.putText(vis,f"Attendance time:{str(datetime.now(tz=pytz.timezone('asia/kolkata')))[:10]}",(700,320),font,0.6,(0,255,0),1,cv.LINE_4)
                        
                        for key,value in update_data.items():
                            ref_att.child(key).set(value)
                        datetime.sleep(0.2)

                        
                    else:
                        vis=cv.putText(vis,f"{val['name']}  attendance aulready present",(700,260),font,0.6,(0,255,0),1,cv.LINE_4)
                except:
                    update_data={
                            str(ppre):{
                                    "name":val['name'],
                                    "major":val['major'],
                                    "Lecture sub":val['Lecture sub'],
                                    "Attendance time":str(datetime.now(tz=pytz.timezone('asia/kolkata'))),
                                    
                            }
                        }
                    vis=cv.putText(vis,f"Name:{val['name']}",(700,260),font,0.6,(0,255,0),1,cv.LINE_4)
                    vis=cv.putText(vis,f"major:{val['major']}",(700,280),font,0.6,(0,255,0),1,cv.LINE_4)
                    vis=cv.putText(vis,f"Lecture sub:{val['Lecture sub']}",(700,300),font,0.6,(0,255,0),1,cv.LINE_4)
                    vis=cv.putText(vis,f"Attendance time:{str(datetime.now(tz=pytz.timezone('asia/kolkata')))[:10]}",(700,320),font,0.6,(0,255,0),1,cv.LINE_4)
                        
                    for key,value in update_data.items():
                        ref_att.child(key).set(value)
                        
                        

                

    vis[60:540,40:680]=imgrect
   
    cv.imshow("Video",vis)

    if cv.waitKey(1)== ord("q"):
        break