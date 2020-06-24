from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import *


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

 
def AddContact():
    global nammee
    global tid
    
    
    
    global root4
    root4 = Tk()
    
    nammee = StringVar()
    tid = StringVar()
    
    
    
    root4.geometry('500x400')  
    root4.title('Messaging app')
    root4.configure(background = "light green")

    Label(root4, text="Add Contact",   font= ("bold", 12)).grid(row=1, column= 3)
    Label(root4, text="",  ).grid(row=2, column= 3)
    
    #photo = PhotoImage(file = r"C:\Users\Abdullah\Pictures\contactpic.jpg")
    #Label(root4, text="ENTER USERNAME AND PASSWORD TO CONTINUE", image = photo, bg = "light green", font= ("bold", 8)).grid(row= 3, column = 0, columnspan = 4) 
    Label(root4, text="",  ).grid(row=4, column= 0)
    Label(root4, text="",  ).grid(row=4, column= 1)
    Label(root4, text="User Name", width = 20,  font= ("bold", 10)).grid(row=4, column=2)
    Entry(root4, textvariable=nammee).grid(row=4, column=3)
    Label(root4,text="ID", width = 20,  font= ("bold", 10)).grid(row=5, column=2)  
    Entry(root4, textvariable=tid, ).grid(row=5, column=3)  
    def get():
        print(nammee.get())
        print(tid.get())
    loginButton = Button(root4, text="Login", command=get,  ).grid(row=6, column=2)
    root4.mainloop()

    
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
   
   #tkMessage = StringVar()
   
   TopFrame = Frame(root2).pack(side=TOP)
################################################################################################################################## 
   LeftFrame = Frame(TopFrame)
   
   Label(LeftFrame, text = "Send Message",  height=1, width=15).pack(side=TOP)
   Option = ["MyProfile","Contacts","GroupMembers","Signout"]
   variable1 = StringVar(root2)
   variable1.set(Option[0])
   opt1 = OptionMenu(LeftFrame, variable1, *Option)
   opt1.config(width=13, font=('Helvetica', 9))
   opt1.pack(side="top")
   def printvariable(*args):
       print(variable1.get())
   variable1.trace("w", printvariable)
   
   
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
       Name.delete(1.0, END)
       Name.insert('end', variable.get())
       Name.configure(state='disabled')
       
   def callback(*args):
       Display.configure(state='normal')
       Display.insert('end', '\n'+variable.get())
       Display.configure(state='disabled')
       Namechange()
       
   variable.trace("w", callback)
   LeftFrame.pack(side=LEFT)
    
##################################################################################################################################
   RightFrame = Frame(TopFrame).pack(side=RIGHT)
      
   displayFrame = Frame(RightFrame)
   
   UpperFrame = Frame(displayFrame,  height=2, width=15)
   Name = Text(UpperFrame, height=2, width=20)
   Name.pack(side=LEFT, fill=Y)
   Name.config(state = 'disabled' )      
   
   
   UpperFrame.pack(side=TOP)
   
   LowerFrame = Frame(displayFrame)
   
   scrollBar = Scrollbar(LowerFrame)
   scrollBar.pack(side=RIGHT, fill=Y)
   tkDisplay = Text(LowerFrame, height=18, width=55)
   tkDisplay.pack(side=LEFT, fill=Y, padx=(5, 0))
   tkDisplay.tag_config("tag_your_message", foreground="blue")
   scrollBar.config(command=tkDisplay.yview)
   tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
   LowerFrame.pack(side=TOP)
   
   displayFrame.pack(side=TOP)
   
   
   
   
       
       
   
   BottomFrame = Frame(RightFrame)
   tkmessage = StringVar(root2)
   
   hello = Entry(BottomFrame, textvariable=tkmessage, width=40,  ).pack(side=LEFT, padx=(5, 13), pady=(5, 10),  )
   btnConnect = Button(BottomFrame, text = "Send", height=1, width=5, command=sendmsg).pack(side=RIGHT)
   BottomFrame.pack(side=TOP)
   
   def sendmsg(*args):
       
       tkDisplay.configure(state='normal')
       tkDisplay.insert('end', '\n You: '+tkmessage.get())
       if hello:
           hello.delete(first=0,last=100)
       tkDisplay.configure(state='disabled')
       
##################################################################################################################################
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

AddContact()

