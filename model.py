# remianber to record all the function, arugment.
# all the packages used for the project
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from deephaven import DynamicTableWriter
import deephaven.dtypes as dht
from deephaven.time import now


def make_person_attendance_table():
    columnT={"Timestamp":dht.DateTime, "Name":dht.string}
    return DynamicTableWriter(columnT)

person_attendance_table=make_person_attendance_table()
person_name_table=person_attendance_table.table

# store all the names who attend the party
# and images of them
person_name=[]
images=[]


# loop through the images, and processing
for pic in os.listdir("images"):
    if pic.endswith("png") or pic.endswith("jpg"):
        img=cv2.imread("images/{}".format(pic))
        name=os.path.splitext(pic)[0]
        images.append(img)
        person_name.append(name)
#
# 
#print(person_name)



def encoding(images):
    """encoding the all the images, and find the 128 measurements for the face"""
    images_encoding=[]
    #loop all the images
    for image in images:
        img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        images_encoding.append(encode)
    return images_encoding


# change it later
# 
def markAttendance(name):
    """recording the attendance, and store the record into the file attendance.csv"""
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
##


encodeListKnown = encoding(images)
print('Encoding Complete')



# record the pic got by webcam
cap = cv2.VideoCapture(0)
 
while True:
    """capture the pics from webcam, doing face encoding, face detection and face comparion, return the most matched face name
    draw rectangle around all the faces, and all the information"""
    degree=0.25
    ret, img = cap.read()
    

    # resize the image tp 0.25 of the orginal one ## make it faster
    imgS = cv2.resize(img,(0,0),None,degree,degree)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # find the face location in the resized image
    facesCurFrame = face_recognition.face_locations(imgS)
    # encoding the img
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    format= cv2.FONT_HERSHEY_COMPLEX
    for encode_Face,face_Loc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encode_Face)
        faceDis = face_recognition.face_distance(encodeListKnown,encode_Face)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
 
        if matches[matchIndex]:
            name = person_name[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = face_Loc
            # scale back the location
            #scale_back=1/degree
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            # draw rectangle on the image
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            #cv2.rectangle(img,(x1,y2),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),format,1,(255,255,255),2)
            markAttendance(name)
            Time=now()
            person_attendance_table.write_row(Time,name)
 
    cv2.imshow('Webcam',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()




