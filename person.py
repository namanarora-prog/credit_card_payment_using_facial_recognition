# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:30:30 2020

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
from tkinter.ttk import Combobox

def validate(sc,pid):
    c=1
    card_no,validity,cvv=li[0].get(),li[1].get(),li[2].get()
    if len(card_no)==0 or card_no.isalpha():
        messagebox.showinfo("Dialog","Empty / Invalid Card number")
        c=0    
    if len(validity)==0 or validity.isalpha():
        messagebox.showinfo("Dialog","Empty / Invalid Validity")
        c=0
    if len(cvv)==0 or cvv.isalpha():
        messagebox.showinfo("Dialog","Empty / Invalid CVV")
        c=0
    if c==1:
        addCard(sc,pid)
    

def addCard(sc,pid):
    try:
        card_no,validity,cvv=li[0].get(),li[1].get(),li[2].get()
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="""insert into card (CARD_NO,VALIDITY,CVV,PID) values (%s,%s,%s,%s)"""
        insert_tuple=(card_no,validity,cvv,pid)
        cur.execute(st,insert_tuple)
        cn.commit()
        messagebox.showinfo("Dialog","Sucessfully inserted")
        paintcombobox(sc,pid)
        
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured \n"+str(error))

def convertToImage(img):
    # Convert digital data to binary format
    with open("login_face.png",'wb') as file:
        file.write(img)

def getData(sc,pid):
    global name
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="select FNAME,LNAME,PHONENO,ADHAARNO,FACE_DATA from person where PID='{}'".format(pid)
        cur.execute(st)
        li=cur.fetchone()
        convertToImage(li[4])
        name=li[0]+" "+li[1]       
        name=name.title()
        
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))
    

def paintlabel(sc):
    Label(sc,text="Welcome "+name+"",font=("arial",40),bg="light grey").place(x=700,y=50)
    Label(sc,text="Add new card",font=("arial",30),bg="light grey").place(x=150,y=400)
    Label(sc,text="Card No",font=("arial",20),bg="light grey").place(x=50,y=500)
    Label(sc,text="Validity",font=("arial",20),bg="light grey").place(x=50,y=550)
    Label(sc,text="CVV",font=("arial",20),bg="light grey").place(x=50,y=600)
    
    Label(sc,text="Your cards",font=("arial",30),bg="light grey").place(x=1400,y=400)
    
    Label(sc,text="Card Number",font=("arial",20),bg="light grey").place(x=1200,y=500)
    Label(sc,text="Validity",font=("arial",20),bg="light grey").place(x=1500,y=500)
    Label(sc,text="CVV",font=("arial",20),bg="light grey").place(x=1700,y=500)

def paintfields(sc):
    Entry(sc,font=("arial",20),textvariable=li[0]).place(x=200,y=500)
    Entry(sc,font=("arial",20),textvariable=li[1]).place(x=200,y=550)
    Entry(sc,font=("arial",20),textvariable=li[2]).place(x=200,y=600)
    
def paintbutton(sc,pid):
    Button(sc, text = "Add ",font=("arial",15), height=1,width=27,command=lambda:validate(sc,pid)).place(x=200,y=650)
    
def paintuserimage(sc):
    rimg=Image.open("login_face.png")
    rimg=rimg.resize((200,200),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(rimg)    
    canvas=Canvas(sc,bg="light grey",width=200,height=200, highlightthickness=0, relief='ridge')
    canvas.create_image(0,0, anchor=NW, image=img) 
    canvas.place(x=880,y=130)    
    canvas.image=img 
    os.remove("login_face.png")
    
def paintcombobox(sc,pid):
    yaxis=550
    try:
        cn=mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='credit_card')
        cur=cn.cursor()
        st="select CARD_NO,VALIDITY,CVV from card where PID='{}'".format(pid)
        cur.execute(st)
        li=cur.fetchall()
        
        for i in li:
            Label(sc,text=str(i[0])+" ",font=('arial',15)).place(x=1200,y=yaxis)
            Label(sc,text=str(i[1])+" ",font=('arial',15)).place(x=1500,y=yaxis)
            Label(sc,text=str(i[2])+" ",font=('arial',15)).place(x=1700,y=yaxis)
            yaxis+=50
    except mysql.connector.Error as error:
        messagebox.showinfo("Dialog","Some error occured "+str(error))
    

    
    

def buildUi(sc,pid):
    global li
    li=[StringVar(),StringVar(),StringVar(),StringVar()]
    w,h=sc.winfo_screenwidth(),sc.winfo_screenheight()
    sc.geometry("%dx%d+0+0"%(w,h))
    sc.state('zoomed')
    sc.configure(bg="light grey")
    sc.title("CREDIT CARD PAYMENT SYSTEM USING FACIAL RECOGNITION")
    
    paintlabel(sc)
    
    paintfields(sc)
    
    paintbutton(sc,pid)
    
    paintuserimage(sc)
    
    paintcombobox(sc,pid)
    
    
    sc.mainloop()

def person(pid):
    sc=Tk()
    getData(sc,pid)
    buildUi(sc,pid)
    
    
#person(1)
    