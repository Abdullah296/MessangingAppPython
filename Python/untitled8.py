from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk

def submit(name, password): 
  
   
      
    print("The name is : " + name) 
    print("The password is : " + password) 
      
    #username.set("") 
    #password.set("") 

def signup():
    global username
    global password
    
    #global variable
    #global Name
    
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
    
    def submit1():
        submit(username.get(), password.get())
    
    loginButton = Button(Gui, text="Login", command=submit1,  bg = "light green", fg = "dark green").grid(row=6, column=2)
    Signup1 = Button(Gui, text="Signup", command=submit1, bg = "light green", fg = "dark green").grid(row=6, column=3)
    Gui.mainloop()
    
signup()