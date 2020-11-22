# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:34:40 2020

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

def validate(sc):
    c=1
    fname,lname,phoneno,adhaarno=li[0].get(),li[1].get(),li[2].get(),li[3].get()
    if len(fname)==0 or fname.isdigit():
        messagebox.showinfo("Dialog","Empty / Invalid first name")
        c=0
    if len(lname)==0 or lname.isdigit():
        messagebox.showinfo("Dialog","Empty / Invalid last name")
        c=0
    if len(phoneno)==0 or phoneno.isalpha():
        messagebox.showinfo("Dialog","Empty / Invalid phone no")
        c=0
    
    if len(adhaarno)==0 or adhaarno.isalpha():
        messagebox.showinfo("Dialog","Empty / Invalid adhaar no")
        c=0
    
    if not os.path.isfile("temp.png"):
        messagebox.showinfo("Dialog","Upload/Capture your face data")
        c=0
    if c==1:
        image=face_recognition.load_image_file("temp.png")
        face_locations=face_recognition.face_locations(image)
        
        if len(face_locations)==0:
            messagebox.showinfo("Dialog","Face not detected")
        elif len(face_locations)>1:
            messagebox.showinfo("Dialog","Multiple face detected\nCapture / Upload single face image")
            #for face_location in face_locations:
             #   top, right, bottom, left = face_location
              #  face_image = image[top:bottom, left:right]
               # pil_image = Image.fromarray(face_image)
                #pil_image.show()
        else:
            messagebox.showinfo("Dialog","Face Detected")
            connects(sc)
            
            
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
    

def connects(sc):
    fname,lname,phoneno,adhaarno=li[0].get(),li[1].get(),li[2].get(),li[3].get()
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')     
        cur=cn.cursor()
        
        st="select count(*) from person"
        cur.execute(st)
        zz=cur.fetchall()        
        #print(zz[0][0])
        no=zz[0][0]
        
        st="""insert into person (PID,FNAME,LNAME,PHONENO,ADHAARNO,FACE_DATA) values (%s,%s,%s,%s,%s,%s)"""
        
        #messagebox.showinfo("Dialog","connection successful")
        empPicture=convertToBinaryData("temp.png")
        insert_tuple=(no+1,fname,lname,phoneno,adhaarno,empPicture)
        
        result=cur.execute(st,insert_tuple)
        cn.commit()
        messagebox.showinfo("Dialog","Thank you "+fname+" "+lname+" for registering with us \nPlease remember your id = "+str(no+1)+"\nYour face will be used as your password")
        os.remove("temp.png")
        sc.destroy()
        register()
        
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))
        
    
    
def goHome(sc):
    sc.destroy()
    mainform
    

def openCam(sc):
#    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)        
    while True:
        ret, frame = video_capture.read()   
        
        if ret:
            cv2.imwrite(os.path.join("", 'temp.png'), frame)                    
    
        cv2.imshow("Press 'q' to capture", frame)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()     
    showimage(sc)
    
def openFile(sc):
    file=filedialog.askopenfilename(initialdir="", filetypes =[('JPG','*.jpg'),('PNG', '*.png'),('JPEG','*.jpeg')])
    img=cv2.imread(file)
    cv2.imwrite(os.path.join("","temp.png"),img)
    showimage(sc)
    
    
def showimage(sc):    
    rimg=Image.open("temp.png")
    rimg=rimg.resize((640,480),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(rimg)    
    canvas=Canvas(sc,bg="light grey",width=640,height=480, highlightthickness=0, relief='ridge')
    canvas.create_image(0,0, anchor=NW, image=img) 
    canvas.place(x=1050,y=430)    
    canvas.image=img
    

def paintlabel(sc):
    Label(sc,text="Register Yourself",font=("arial",40),bg="light grey").place(x=760,y=50)
    
    Label(sc,text="First Name *",bg="light grey",font=("arial", 20)).place(x=100,y=250)
    Label(sc,text="Last Name *",bg="light grey",font=("arial", 20)).place(x=100,y=350)
    Label(sc,text="Phone no *",bg="light grey",font=("arial", 20)).place(x=100,y=450)
    Label(sc,text="Adhaar no *",bg="light grey",font=("arial", 20)).place(x=100,y=550)
    Label(sc,text="Fields marked with (*) are mandatory",fg="red",bg="light grey",font=("arial", 10)).place(x=390,y=600)
    Label(sc,text="Suggestion: For better results upload image",fg="red",bg="light grey",font=("arial", 10)).place(x=1240,y=400)
    
    
def paintfields(sc):
    Entry(sc,font=("arial",20),textvariable=li[0]).place(x=300,y=250)
    Entry(sc,font=("arial",20),textvariable=li[1]).place(x=300,y=350)
    Entry(sc,font=("arial",20),textvariable=li[2]).place(x=300,y=450)
    Entry(sc,font=("arial",20),textvariable=li[3]).place(x=300,y=550)

def paintbuttons(sc):
    Button(sc, text = "Open Webcam ",font=("arial",20), height=1,width=20,command=lambda:openCam(sc)).place(x=1200,y=230)
    Button(sc, text = "Browse ",font=("arial",20), height=1,width=20,command=lambda:openFile(sc)).place(x=1200,y=330)
    Button(sc, text = "Register  ",font=("arial",20), height=1,width=20,command=lambda:validate(sc)).place(x=800,y=950)        

def buildUi(sc):
    global li
    li=[StringVar(),StringVar(),StringVar(),StringVar()]
    t1=StringVar()
    w,h=sc.winfo_screenwidth(),sc.winfo_screenheight()
    sc.geometry("%dx%d+0+0"%(w,h))
    sc.state('zoomed')
    sc.configure(bg="light grey")
    sc.title("CREDIT CARD PAYMENT SYSTEM USING FACIAL RECOGNITION")
    
    #Labels
    paintlabel(sc)
    
    
    #TextFields
    paintfields(sc)
    
    #Buttons
    paintbuttons(sc)
    
    sc.mainloop()

def register():
    sc=Tk()        
    buildUi(sc)
    
#register()