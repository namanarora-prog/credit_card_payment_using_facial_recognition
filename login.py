# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:19:41 2020

@author: Naman Arora
"""


import cv2
import os
import mysql.connector
from mysql.connector import Error
from tkinter import*
from tkinter import filedialog
from tkinter import  messagebox
from PIL import ImageTk,Image 
import face_recognition
import numpy as np
from person import*


def verified(sc,name):
    messagebox.showinfo("Dialog","Face Verified \nWelcome "+name)
    os.remove("known_face.png")
    sc.destroy()
    person(t1.get())

def convertToImage(img):
    # Convert digital data to binary format
    with open("known_face.png",'wb') as file:
        file.write(img)
    

def check(sc):
    messagebox.showinfo("Dialog",t1.get())

def getData(sc):
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="select FNAME,LNAME,FACE_DATA from person where PID='{}'".format(t1.get())
        cur.execute(st)
        li=cur.fetchone()
        if li is not None:
            convertToImage(li[2])
            name=li[0]+" "+li[1]            
            openCam(sc,name,)
        else:
            messagebox.showinfo("Dialog","User doesn't exist")
        
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))

def openCam(sc,st):
    video_capture = cv2.VideoCapture(0)   
     
    image_of_person=face_recognition.load_image_file('known_face.png')
    person_face_encoding=face_recognition.face_encodings(image_of_person)[0]
    
    known_face_encodings = [person_face_encoding,]

    known_face_names = [st,]
    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    name=""
        
    while True:
                
        ret, frame = video_capture.read() 
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            
            face_names=[]
            for face_encoding in face_encodings:
                matches=face_recognition.compare_faces(known_face_encodings,face_encoding,tolerance=0.5)
                name="Unknown Person"
                
                face_distances = face_recognition.face_distance(
                                    known_face_encodings, face_encoding)   
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name=known_face_names[best_match_index]                                    
                    
                face_names.append(name)
        process_this_frame=not process_this_frame
        
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                
            cv2.rectangle(frame, (left, bottom-35),
                  (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left+6, bottom-6),
                font, 1.0, (255, 255, 255), 1)
        
        cv2.imshow("Press 'q' to quit",frame)
    
        if name==st :         
            video_capture.release()
            cv2.destroyAllWindows()
            verified(sc,name)
            break 
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_capture.release()
    cv2.destroyAllWindows()
    

def paintlabel(sc):
    Label(sc,text="Welcome",font=("arial",40),bg="light grey").place(x=820,y=50)
    Label(sc,text="Enter Your ID ",font=("arial",30),bg="light grey").place(x=805,y=400)

def paintfields(sc):
    Entry(sc,font=("arial",20),textvariable=t1,justify='center').place(x=780,y=500)
    
def paintimage(sc):
    rimg=Image.open("acc.png")
    rimg=rimg.resize((200,200),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(rimg)    
    canvas=Canvas(sc,bg="light grey",width=200,height=200, highlightthickness=0, relief='ridge')
    canvas.create_image(0,0, anchor=NW, image=img) 
    canvas.place(x=830,y=150)    
    canvas.image=img

def paintbutton(sc):
    Button(sc, text = "Open Webcam ",font=("arial",20), height=1,width=20,command=lambda:getData(sc)).place(x=770,y=600)

def buildUi(sc):
    global t1
    t1=StringVar()
    w,h=sc.winfo_screenwidth(),sc.winfo_screenheight()
    sc.geometry("%dx%d+0+0"%(w,h))
    sc.state('zoomed')
    sc.configure(bg="light grey")
    sc.title("CREDIT CARD PAYMENT SYSTEM USING FACIAL RECOGNITION")
    
    #Labels
    paintlabel(sc)
    
    #Fields
    paintfields(sc)
    
    #Image
    paintimage(sc)
    
    #Buttons
    paintbutton(sc)
    
    sc.mainloop()

def login():
    sc=Tk()
    buildUi(sc)

#login()