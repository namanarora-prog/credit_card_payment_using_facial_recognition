# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:46:39 2020

@author: Naman Arora
"""


from tkinter import*
from PIL import ImageTk,Image 
from register import*
from login import*
from payment import*

def callregister(sc):    
    sc.destroy()
    register()    
    
def calllogin(sc):
    sc.destroy()
    login()

def callpayment(sc):
    sc.destroy()
    payment()
    
sc=Tk()
w,h=sc.winfo_screenwidth(),sc.winfo_screenheight()
sc.geometry("%dx%d+0+0"%(w,h))
sc.state('zoomed')
sc.configure(bg="light grey")
sc.title("CREDIT CARD PAYMENT SYSTEM USING FACIAL RECOGNITION")

#Image with canvas
img=PhotoImage(file="ocr-b.jpg")
canvas=Canvas(sc,bg="light grey",width=img.width(),height=img.height(), highlightthickness=0, relief='ridge')
canvas.place(x=751,y=275)
canvas.create_image(0,0, anchor=NW, image=img)  
#print(img.width())

#Label 1
Label(sc,text="CREDIT CARD PAYMENT SYSYTEM \n USING FACIAL RECOGNITION",font=("arial",40),bg="light grey").place(x=480,y=50)

#Buttons
Button(sc, text = "Register ",font=("arial",20), height=1,width=10,command=lambda:callregister(sc)).place(x=480,y=600)
Button(sc, text = "Payment ",font=("arial",20), height=1,width=10,command=lambda:callpayment(sc)).place(x=875,y=600)
Button(sc, text = "Login ",font=("arial",20), height=1,width=10,command=lambda:calllogin(sc)).place(x=1228,y=600)

#Label 2
Label(sc,text="Powered By",font=("arial",30),bg="light grey").place(x=860,y=750)

#Image with canvas
#resizing
rimg=Image.open("visa-mastercard.png")
rimg=rimg.resize((600,200),Image.ANTIALIAS)
img2=ImageTk.PhotoImage(rimg)
#img2=PhotoImage(file="visa-mastercard.png")
#img2.resize((100,100))
canvas2=Canvas(sc,bg="light grey",width = img2.width(), height = img2.height(), highlightthickness=0, relief='ridge')
canvas2.place(x=665,y=800)
canvas2.create_image(0,0, anchor=NW, image=img2)  


sc.mainloop()

