import os
import face_recognition as fr
import matplotlib.pyplot as plt
import numpy as np
import cv2
import face_recognition
import face_recognition as fr
import pickle
#import threads
from plyer import notification
import time





class Person:
    def __init__(self, name = None, image = None):
        self.name = name
        self.image = image
        try:
            self.image_fr = fr.load_image_file(image)
        except:
            print("Image not found")
            return
        self.encoding = fr.face_encodings(self.image_fr)[0]

    
def recognize(person_list):
    try:
        f = open("history.his", "rb+")
        history = pickle.load(f)
        f.close()
    except:
        f = open("history.his", "wb+")
        pickle.dump([], f)
        f.close()
        history = []
    video_capture = cv2.VideoCapture(0)

    known_face_encodings = []

    known_face_names = []

    for obj in person_list:
        known_face_encodings.append(obj.encoding)
        known_face_names.append(obj.name)
        
    face_locations = []
    face_encodings = []
    face_name = []
    process_this_frame = True
    fr = 0
    while True:
        p = None
        
        ret, frame = video_capture.read()
        small_frame = frame#cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)
        rbg_small_frame = small_frame[:,:,::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rbg_small_frame)
            face_encodings = face_recognition.face_encodings(rbg_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                
                best_match_index = np.argmin(face_distances)
                #face_distances[best_match_index]
                if face_distances[best_match_index] < 0.50:
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                else:
                    name = "Unknown"

                face_names.append(name)
                
        #process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 1
            right *= 1
            bottom *= 1
            left *= 1
            t = time.localtime()
            if fr % 10 == 0:
                history.append("{} - Date - {}-{}-{} Time - {}:{}:{}".format(name, t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec))
            if name != "Unknown":
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 1)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0,0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "%s - %.2f"%(name,face_distances[best_match_index]) , (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 1)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
##                if fr %50 == 0:
##                    mes = "Date {}-{}-{} Time {}:{}:{}".format(t.tm_mday, t.tm_mon, t.tm_year,t.tm_hour, t.tm_min, t.tm_sec)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "WARNING" , (40, 60), font, 2, (0, 0, 255), 2)
                cv2.putText(frame, "%s"%name , (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("Video", frame)
        fr += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    fi = open("history.his", "wb+")
    pickle.dump(history, fi)
    fi.close()
    cv2.destroyAllWindows()
    video_capture.release()
    

try:
    fil = open("data.dat", "rb+")
    person_list = pickle.load(fil)
    fil.close()
except:
    fil = open("data.dat", "wb+")
    fil.close()
    person_list = []
smsAlert = False
soundAlter = False

while(True):
    print("Enter 1 to start surveilance")
    print("Enter 2 to add person")
    print("Enter 3 print list of all the person")
    print("Enter 4 to remove person")
    print("Enter 5 to print history")
    print("Enter 6 to change other setting")
    try:
        n = int(input("Enter your option:"))
    except:
        continue
    if n == 1:
        if person_list != []:
            recognize(person_list)
    elif n == 2:
        nm = input("Enter name of the person :")
        i = int(input("Enter 1 to capture photo or 2 to load saved photo :"))
        if i == 1:
            vdc = cv2.VideoCapture(0)
            while True:
                ret, frame = vdc.read()
                sm_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)[:,:,::-1]
                face_locations = face_recognition.face_locations(sm_frame)
                if face_locations != []:
                    if cv2.waitKey(1) & 0xFF == ord("c"):
                        cv2.imwrite(nm+".png", frame)
                        vdc.release()
                        cv2.destroyAllWindows()
                        break
                    top, right, bottom, left = face_locations[0]
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0,255, 0))
                cv2.imshow("Video", frame)
            person_object = Person(nm, nm+".png")
            person_list.append(person_object)
        elif i == 2:
            fn = input("Enter file name :")
            person_object = Person(nm, fn)
            person_list.append(person_object)
        fil = open("data.dat", "wb+")
        pickle.dump(person_list, fil)
        fil.close()
    elif n == 3:
        for i in person_list:
            print(i.name)
    elif n == 4:
        nm = input("Enter the person to delete")
        f = False
        for im in person_list:
            if im.name == nm:
                person_list.remove(im)
                f = True
                break
        if not f:
            print("Person not found")
        fil = open("data.dat", "wb+")
        pickle.dump(person_list, fil)
        fil.close()
    elif n == 5:
        fil = open("history.his", "rb+")
        history = pickle.load(fil)
        for h in history:
            print(h)
        fil.close()

