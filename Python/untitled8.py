from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk

def submit(name, password, email, question): 
  
   
      
    print("The name is : " + name) 
    print("The password is : " + password) 
    print("The email is : " + email) 
    print("The question is : " + question)
    
    root1.destroy()
    signin()
      
    #username.set("") 
    #password.set("") 

def submitt(name, password):
  
    
      
    print("The name is : " + name) 
    print("The password is : " + password) 
    
def signin():
    global username
    global password
    global resultLabel
    
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
    Label(Gui,text="ID", width = 20, bg = "light green", font= ("bold", 10)).grid(row=6, column=2)  
    resultLabel = Label(Gui, text="").grid(row=6, column=3)
    
    def submit1():
        resultLabel.config(text=username.get())
        submitt(username.get(), password.get())
        
    loginButton = Button(Gui, text="Login", command=submit1,  bg = "light green", fg = "dark green").grid(row=7, column=2)
    Gui.mainloop()

def signup():
    global username1
    global passwordd
    global useremail
    global Squestion
    global Sanswer
    
    #global variable
    #global Name
    
    global root1
    root1 = Tk()
    
    username1 = StringVar()
    passwordd = StringVar()
    useremail = StringVar()
    Squestion = StringVar()
    Sanswer = StringVar()
    
    
    root1.geometry('500x400')  
    root1.title('Messaging app')
    root1.configure(background = "light green")

    Label(root1, text="ENTER YOUR DATA, HERE", bg = "light green").grid(row= 2, column = 0, columnspan = 2)
   
    Label(root1, text="User Name", width = 20, bg = "light green", font= ("bold", 10)).grid(row=4, column=0)
    Entry(root1, textvariable=username1).grid(row=4, column=1)
    Label(root1, text="Email *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=0)
    Entry(root1, textvariable=useremail).grid(row=5, column=1)
    Label(root1,text="Password", width = 20, bg = "light green", font= ("bold", 10)).grid(row=6, column=0)  
    Entry(root1, textvariable=passwordd, show='*').grid(row=6, column=1)  
    Label(root1,text="Security Question",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=8, column=0)  
    OptionMenu(root1, Squestion, "Which month you born? " ).grid(row=8, column=1) 
    Entry(root1, textvariable=Sanswer ).grid(row=9, column=1)
    
    def submit1():
        submit(username1.get(), passwordd.get(), useremail.get(), Sanswer.get())
    
    loginButton = Button(root1, text="Signup", command=submit1,  bg = "light green", fg = "dark green").grid(row=11, column=0)
    
    root1.mainloop()
    
signup()