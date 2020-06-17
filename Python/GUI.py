# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:42:02 2020

@author: Abdullah
"""

from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk


def signin():
    global username
    global password
    
    global variable
    global Name
    
    global Gui
    Gui = Tk()
    
    username = StringVar()
    password = StringVar()
    
    
    
    Gui.geometry('500x400')  
    Gui.title('Messaging app')
    Gui.configure(background = "light green")

    Label(Gui, text="WELCOME TO MESSAGING APP",  bg = "light green", font= ("bold", 12)).grid(row=1, column= 3, columnspan = 3)
    Label(Gui, text="",  bg = "light green").grid(row=2, column= 3)
    Label(Gui, text="ENTER USERNAME AND PASSWORD TO CONTINUE",bg = "light green", font= ("bold", 8)).grid(row= 3, column = 0, columnspan = 4) 
    Label(Gui, text="",  bg = "light green").grid(row=4, column= 0)
    Label(Gui, text="",  bg = "light green").grid(row=4, column= 1)
    Label(Gui, text="User Name", width = 20, bg = "light green", font= ("bold", 10)).grid(row=4, column=2)
    Entry(Gui, textvariable=username).grid(row=4, column=3)
    Label(Gui,text="Password", width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=2)  
    Entry(Gui, textvariable=password, show='*').grid(row=5, column=3)  

    loginButton = Button(Gui, text="Login", command=validateLogin,  bg = "light green", fg = "dark green").grid(row=6, column=2)
    Signup1 = Button(Gui, text="Signup", command=presignup, bg = "light green", fg = "dark green").grid(row=6, column=3)
    Gui.mainloop()

    
def signup():
   global root1
   global useremail
   global password1
   global Squestion
   global Sanswer
   global username1
   global passwordd
   
   username = StringVar()
   passwordd = StringVar()
   useremail = StringVar()
   password1 = StringVar()
   Squestion = StringVar()
   Sanswer = StringVar()
   
   root1 = Tk()
   root1.geometry('500x400')  
   root1.title('Messaging app')
   root1.configure(background = "light green")

   Label(root1, text="ENTER YOUR DATA, HERE", bg = "light green").grid(row= 2, column = 0, columnspan = 2)  

   Label(root1, text="User Name *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=4, column=0)
   Entry(root1, textvariable=username1 ).grid(row=4, column=1) 
   Label(root1, text="Email *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=0)
   Entry(root1, textvariable=useremail).grid(row=5, column=1)
   Label(root1,text="Password *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=6, column=0)  
   Entry(root1,  show='*', textvariable=passwordd).grid(row=6, column=1)  
   Label(root1,text="Password *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=7, column=0)  
   Entry(root1, textvariable=password1, show='*').grid(row=7, column=1) 
   Label(root1,text="Security Question",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=8, column=0)  
   OptionMenu(root1, Squestion, "Which month you born? " ).grid(row=8, column=1) 
   Entry(root1, textvariable=Sanswer ).grid(row=9, column=1) 
   
   #Button(root1,text="username *",  width = 20, bg = "light green", font= ("bold", 10), command=getname).grid(row=15, column=0)  
   #Label(root1, textvariable=username).grid(row=15, column=1)
   
   loginButton = Button(root1, text="Signup", command=savesignup, bg = "light green").grid(row=11, column=0)
   root1.mainloop()

def getname():
    eee = username.get()
    username.set(eee)
    
def login():
   root2 = Tk()
   root2.geometry('500x400')  
   root2.title('Successfully login')
   
   TopFrame = Frame(root2).pack(side=TOP)
     
   LeftFrame = Frame(TopFrame)
   
   Label(LeftFrame, text = "Send Message",  height=1, width=15).pack(side=TOP)
   
   OptionList = ["Abdullah","Abdurrehman","Malik","Usama","Wajiha","Ahmad Tariq"] 
   variable = StringVar(root2)
   variable.set(OptionList[0])
   opt = OptionMenu(LeftFrame, variable, *OptionList)
   opt.config(width=13, font=('Helvetica', 9))
   opt.pack(side="top")
   
   scrollBar = Scrollbar(LeftFrame)
   scrollBar.pack(side=RIGHT, fill=Y)
   Display = Text(LeftFrame, height=22, width=15)
   Display.pack(side=TOP, fill=Y, padx=(5, 0))
   scrollBar.config(command=Display.yview)
   Display.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey",state = 'disabled' )
   def Namechange(*args):
       Name.configure(state='normal')
       Name.insert('end', variable.get())
       Name.configure(state='disabled')
       
   def callback(*args):
       Display.configure(state='normal')
       Display.insert('end', '\n'+variable.get())
       Display.configure(state='disabled')
       Namechange()
       
   variable.trace("w", callback)
   LeftFrame.pack(side=LEFT)
    
   
   RightFrame = Frame(TopFrame).pack(side=RIGHT)
      
   displayFrame = Frame(RightFrame)
   
   UpperFrame = Frame(displayFrame,  height=2, width=15)
   Name = Text(LeftFrame, height=2, width=10)
   Name.pack(side=LEFT, fill=Y)
   Name.config(state = 'disabled' )      
   
   #Label(UpperFrame, text = "Option", height=2, width=7).pack(side=RIGHT)
   UpperFrame.pack(side=TOP)
   
   LowerFrame = Frame(displayFrame)
   #lblLine = Label(displayFrame, text="*********************************************************************").pack()
   scrollBar = Scrollbar(LowerFrame)
   scrollBar.pack(side=RIGHT, fill=Y)
   tkDisplay = Text(LowerFrame, height=18, width=55)
   tkDisplay.pack(side=LEFT, fill=Y, padx=(5, 0))
   tkDisplay.tag_config("tag_your_message", foreground="blue")
   scrollBar.config(command=tkDisplay.yview)
   tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
   LowerFrame.pack(side=TOP)
   
   displayFrame.pack(side=TOP)
   
   icon = PhotoImage(file='C:\\Users\Abdullah\Documents\Python\gh.png')
   #icon = icon.subsample(2,2)
   
   BottomFrame = Frame(RightFrame)
   tkMessage = Text(BottomFrame, height=2, width=35).pack(side=LEFT, padx=(5, 13), pady=(5, 10))
   btnConnect = Button(BottomFrame, text = "Send", height=1, width=5).pack(side=RIGHT)
   #btnConnect.config(image =icon)
   BottomFrame.pack(side=TOP)
   
   root2.mainloop()
    

   #############################################################################
   
   
def savesignup():
    print(username1.get())
    print(passwordd.get())
    root1.destroy()
    signin()

def presignup():
    Gui.destroy()
    signup()

def validateLogin():
    Gui.destroy()
    login()

signin()

