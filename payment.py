# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:11:52 2020

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

def verified(sc,name):
    messagebox.showinfo("Dialog","Face Verified \nPayment Successful, Thank you "+name+" for trusting on us")
    os.remove("known_face.png")

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

def convertToImage(img):
    # Convert digital data to binary format
    with open("known_face.png",'wb') as file:
        file.write(img)

def getFaceData(sc,pid):
    name=""
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="select FNAME,LNAME,FACE_DATA from person where PID='{}'".format(pid)
        cur.execute(st)
        lis=cur.fetchone()
        if lis is not None:
            convertToImage(lis[2])
            name=lis[0]+" "+lis[1]
            openCam(sc,name)
            
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))
    

def getData(sc):
    card_no,validity,cvv=li[0].get(),li[1].get(),li[2].get()
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="select PID from card where CARD_NO='{}' and VALIDITY='{}' and CVV='{}'".format(card_no,validity,cvv)        
        cur.execute(st)
        lis=cur.fetchone()
        if lis is not None:
            getFaceData(sc,lis[0])
            print(lis[0])
        else:
            messagebox.showinfo("Dialog","Card doesn't mapped with any face")
        
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))

def paintimage(sc):
    img=PhotoImage(file="ocr-b.jpg")
    canvas=Canvas(sc,bg="light grey",width=img.width(),height=img.height(), highlightthickness=0, relief='ridge')
    canvas.place(x=751,y=150)
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image=img
    #print(img.height())

def paintlabel(sc):
    Label(sc,text="Welcome",font=("arial",40),bg="light grey").place(x=820,y=50)
    Label(sc,text="Pay to:\nNGO",font=("arial",30),bg="light grey").place(x=50,y=500)
    Label(sc,text="Enter Your Card Details ",font=("arial",30),bg="light grey").place(x=750,y=450)
    
    Label(sc,text="Card No",font=("arial",20),bg="light grey").place(x=650,y=550)
    Label(sc,text="Validity",font=("arial",20),bg="light grey").place(x=650,y=600)
    Label(sc,text="CVV",font=("arial",20),bg="light grey").place(x=650,y=650)

def paintfields(sc):
    Entry(sc,font=("arial",20),textvariable=li[0]).place(x=950,y=550)
    Entry(sc,font=("arial",20),textvariable=li[1]).place(x=950,y=600)
    Entry(sc,font=("arial",20),textvariable=li[2]).place(x=950,y=650)
    
def paintbutton(sc):
    Button(sc, text = "Confirm Payment",font=("arial",20), height=1,width=20,command=lambda:getData(sc)).place(x=800,y=730)

def buildUi(sc):
    global li
    li=[StringVar(),StringVar(),StringVar()]
    w,h=sc.winfo_screenwidth(),sc.winfo_screenheight()
    sc.geometry("%dx%d+0+0"%(w,h))
    sc.state('zoomed')
    sc.configure(bg="light grey")
    sc.title("CREDIT CARD PAYMENT SYSTEM USING FACIAL RECOGNITION")
    
    paintimage(sc)

    paintlabel(sc)
    
    paintfields(sc)
    
    paintbutton(sc)
    
    sc.mainloop()

def payment():
    sc=Tk()
    buildUi(sc)
    
#payment()