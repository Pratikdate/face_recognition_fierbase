# face_recognition_fierbase
attendance system

Typically this process can be divided into four stages,

1. Dataset Creation
Images of students are captured using a web cam. Multiple images of single student will be acquired with varied gestures and angles. These images undergo pre-processing. The images  are cropped  to obtain  the  Region of  Interest (ROI) which will be further used in recognition process. Next step is
to resize the cropped images to particular pixel position. Then these  images will be converted  from  RGB to gray scale images. And then these images will be saved as the names of respective student in a folder.


2. Face Detection
Face detection here is performed using face_recognition python library function called face_recognition.face_locations() .
Other function that use for face encoding called face_recognition.face_encoding(). This is use for  feature extraction. 
Here we are using detectMultiScale module from OpenCV. This is required to create a rectangle around  the faces  in an image. 
It has got three  parameters to  consider-  scaleFactor, minNeighbors, minSize. scaleFactor  is used to indicate how much an image must be reduced in each image scale.


3. Face Recognition
Face recognition process can  be divided  into three steps- prepare training  data, train face recognizer, prediction.  Here training data will  be the images 
present in the dataset. They will be assigned with a integer label of the student it belongs to. Database manage in following json format.

4. Attendance Updation
After face recognition process, the recognized faces will be marked  as  present  in  the  Google Firebase cloud storage  . Faculties will be updated with monthly attendance sheet at the end of every month.


5. Result and  Discussion
The users can interact with the system using a GUI. Here  users  will  be  mainly  provided  with three  different  options such  as, student  registration,  faculty registration,  and  mark attendance. The students are supposed to enter all the required details in the student registration form. After
clicking on register button, the web cam starts automatically and window as shown in Fig.3. pops up and starts detecting the faces in the  frame. Then  it automatically  starts clicking photos until 60 samples are collected or CRTL+Q is pressed. These images then will be pre-processed and stored in
training images folder. The faculties are  supposed to register with the  respective
course codes along with their email-id in the faculty registration form provided. This is important because the list of absentees will be ultimately mailed to the respective faculties.
 

