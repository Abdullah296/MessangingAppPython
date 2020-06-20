
import socket   # for creating sockets
import sys      # for handling exceptions
import json     # for saving data
import tqdm
import os
from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk

class Client:
    MyName = None     # My user name
    MyId = None   # My unique Id stored in server
    MyPassword = None
    MyGroups = {}   # Groups which I have joined
    # MyGroups = {'Group Id':'Group Name'}
    MyContacts = {}     # List of contacts which i have saved
    # MyContacts = {'ID':'Name'}
    MyStatus = False   # I am online or offline
    Socket = None 
################################################################################################################################## 
    def ConnectToServer(self):
        #       What it will do?
        #           it will connect to server
        #       How it will do?
        #           > create a new socket
        #           > connect to server
        #       Other
        try:
            # self.MyName = input("Enter user name :")
            print("Creating Socket")
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")
        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)
        try:
            print("connecting to server :", ServerAdress)
            self.Socket.connect(ServerAdress)
        except socket.error as err:
            print("error in connecting to server :", err)
            sys.exit("error in connecting to server :")
        else:
            print("connected to the server")
            
            
################################################################################################################################## 
            
    def Decoder(self):
        #       What it will do?
        #           it will ask user for to enter choise or what he/she wants to do
        #       How it will do?
        #           > Take input from user
        #           > call specific function for given input
        #       Other
        #           this function controal the flow of programe
        while True:
            if self.Socket is None:     # not connected to server
                self.ConnectToServer()
            elif self.MyStatus is False:     # I have't Sign in
                self.signin()
################################################################################################################################## 
                
                
    def SignUp(self,name,password,email,answer):  
        
       # print("name is : ",name)
        # will do sign Up
        #       What it will do?
        #           it will create a new user account
        #       How it will do?
        #           > take user_name, password from user
        #           > build request foramte (r<up<password)
        #           > take response from server (unique_ID)
        #       Other
        self.MyName = name
        print(self.MyName)
        temp = password
        print(temp)
        temp = "r<up<"+ temp
        self.Socket.sendall(temp.encode('UTF-8'))
        self.MyId = self.Socket.recv(1024).decode('UTF-8')
        print("Sign Up Successfully")
        print("Your user name :", self.MyName)
        print("Your ID is :", self.MyId)
        self.savesignup()
        
    def signup(self):
        global username1
        global passwordd
        global useremail
        global Squestion
        global Sanswer
    
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
            self.SignUp(username1.get(), passwordd.get(), useremail.get(), Sanswer.get())
    
        loginButton = Button(root1, text="Signup", command=submit1,  bg = "light green", fg = "dark green").grid(row=11, column=0)
    
        root1.mainloop()
################################################################################################################################## 
    def SignIn(self, name,uid,passw):   # will do sign in
        #       What it will do?
        #           it will sign in to an already created account
        #       How it will do?
        #           > take password and unique_ID from user
        #           > build request formate (r<in<ID<password)
        #           > make request to server
        #           > take response from server ('True'/'False')
        #           > if 'False' repeate the process
        #       Other
        if self.MyName is None:
            self.MyName = name
        if self.MyId is None:
            self.MyId = uid
        temp = passw
        print("name1 is : ",self.MyName)
        print("Id is : ",self.MyId)
        print(temp)
        temp = "r<in<"+str(self.MyId)+"<"+str(temp)
        self.Socket.sendall(temp.encode('UTF-8'))
        temp = self.Socket.recv(1024)
        if temp.decode('UTF-8') == 'True':
            print("Sign in successful")
            self.MyStatus = True
            self.validateLogin()
            RThread = threading.Thread(target=self.Receive)
            RThread.start()
        else:
            print("Try again")
            self.tryagain()

    def signin(self):
        global username
        global userid
        global password
        
        global variable
        global Name
        
        
        global Gui
        Gui = Tk()
        
        username = StringVar()
        userid = StringVar()
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
        Label(Gui, text="Id ", width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=2)
        Entry(Gui, textvariable=userid).grid(row=5, column=3)
        Label(Gui,text="Password", width = 20, bg = "light green", font= ("bold", 10)).grid(row=6, column=2)  
        Entry(Gui, textvariable=password, show='*').grid(row=6, column=3)  
        
        def submit():
            self.SignIn(username.get(),userid.get(),password.get())
            
        loginButton = Button(Gui, text="Login", command=submit,  bg = "light green", fg = "dark green").grid(row=7, column=2)
        Signup1 = Button(Gui, text="Signup", command=self.presignup, bg = "light green", fg = "dark green").grid(row=7, column=3)
        Gui.mainloop()
    
##################################################################################################################################     
    def AddToContact(self, name, idd):
        #       What it will do?
        #           it will save a new contact
        #       How it will do?
        #           > take Client's ID, name from user
        #           > add it to self.MyContacts
        #           (it does not make any request to server)
        #       Other
        if self.MyStatus is True:
            tid = idd
            tname = name
            print(tid)
            print(tname)
            if tid not in self.MyContacts.keys():
                self.MyContacts[str(tid)] = tname
                print("Added successfully")
                
            else:
                print("User Already Exist")
        else:
            print("Please Sign in")
        
    def AddContact(self):
        global nammee
        global tid
    
        global root4
        root4 = Tk()
        
        nammee = StringVar()
        tid = StringVar()
        
        root4.geometry('300x300')  
        root4.title('Messaging app')
        
    
        Label(root4, text="Add Contact",   font= ("bold", 12)).grid(row=1, column= 3, columnspan = 3)
        Label(root4, text="",  ).grid(row=2, column= 3)
         
        Label(root4, text="",  bg = "light green").grid(row=4, column= 0)
        Label(root4, text="",  bg = "light green").grid(row=4, column= 1)
        Label(root4, text="User Name", width = 20,  font= ("bold", 10)).grid(row=4, column=2)
        Entry(root4, textvariable=nammee).grid(row=4, column=3)
        Label(root4,text="ID", width = 20,  font= ("bold", 10)).grid(row=5, column=2)  
        Entry(root4, textvariable=tid, ).grid(row=5, column=3)  
        
        def submit4():
            self.AddToContact(nammee.get(),tid.get())
            
        loginButton = Button(root4, text="Save contact", command=submit4,  bg = "light green", fg = "dark green").grid(row=7, column=2)
        root4.mainloop()
    
    
    
            
    def MyProfile(self):    # will print My basics info
        #       What it will do?
        #           it will print User Name & ID
        #       How it will do?
        #
        #       Other
        if self.MyStatus is True:
            print("User Name :", self.MyName)
            print("User ID :", self.MyId)
            Display.configure(state='normal')
            Display.insert('end', '\n'+"Profile info:  ")
            Display.insert('end', '\n'+"User Name :\n"+self.MyName)
            Display.insert('end', '\n'+"User ID :"+self.MyId)
            Display.configure(state='disabled')
##################################################################################################################################             
    
    def login(self):
       global root2
       global Display
       
       root2 = Tk()
       root2.geometry('500x400')  
       root2.title('Successfully login')
   
       TopFrame = Frame(root2).pack(side=TOP)
    ################################################################################################################################## 
       LeftFrame = Frame(TopFrame)
       
       Label(LeftFrame, text = "    Options: ",  height=1, width=15).pack(side=TOP)
       Option = ["MyProfile","Add Contacts","GroupMembers","Signout"]
       variable1 = StringVar(root2)
       variable1.set(Option[0])
       opt1 = OptionMenu(LeftFrame, variable1, *Option)
       opt1.config(width=13, font=('Helvetica', 9))
       opt1.pack(side="top")
       def printvariable(*args):
           
           if variable1.get() == "MyProfile":
               self.MyProfile()
               
           elif variable1.get() == "Add Contacts":
               self.AddContact()
           
           elif variable1.get() == "GroupMembers":
               pass
           
           elif variable1.get() == "Signout":
               self.Socket.close()
               self.Signout()
               
           
           
       variable1.trace("w", printvariable)
          
       OptionList = ["Abdullah","Abdurrehman","Malik","Usama","Wajiha","Ahmad Tariq"] 
       #OptionList = self.MyContacts.keys()
       variable = StringVar(root2)
       variable.set(OptionList[0])
       opt = OptionMenu(LeftFrame, variable, *OptionList)
       opt.config(width=13, font=('Helvetica', 9))
       opt.pack(side="top")
       
       
       Bar = Scrollbar(LeftFrame)
       Bar.pack(side=RIGHT, fill=Y)
       Display = Text(LeftFrame, height=22, width=15)
       Display.pack(side=TOP, fill=Y, padx=(5, 0))
       Bar.config(command=Display.yview)
       Display.config(yscrollcommand=Bar.set, background="#F4F6F7", highlightbackground="grey",state = 'disabled' )
       Display.configure(state='normal')
       Display.insert('end', 'History: ')
       Display.configure(state='disabled')
       
       def Namechange(*args):
           Name.configure(state='normal')
           Name.delete(1.0, END)
           Name.insert('end', variable.get())
           Name.configure(state='disabled')
           
       def updatehistory(*args):
           Display.configure(state='normal')
           Display.insert('end', '\n'+variable.get())
           Display.configure(state='disabled')
           Namechange()
           
       variable.trace("w", updatehistory)
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
       
       Bar2 = Scrollbar(LowerFrame)
       Bar2.pack(side=RIGHT, fill=Y)
       Display2 = Text(LowerFrame, height=18, width=55)
       Display2.pack(side=LEFT, fill=Y, padx=(5, 0))
       Bar2.config(command=Display2.yview)
       Display2.config(yscrollcommand=Bar2.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
       LowerFrame.pack(side=TOP)
       
       displayFrame.pack(side=TOP)
       
       
       
       def sendmsg(*args):
           
           Display2.configure(state='normal')
           Display2.insert('end', '\n You: '+tkmessage.get())
           Display2.configure(state='disabled')
           
       
       BottomFrame = Frame(RightFrame)
       tkmessage = StringVar(root2)
       
       tkkkkk = Entry(BottomFrame, textvariable=tkmessage, width=40,  ).pack(side=LEFT, padx=(5, 13), pady=(5, 10),  )
       btnConnect = Button(BottomFrame, text = "Send", height=1, width=5, command=sendmsg).pack(side=RIGHT)
       BottomFrame.pack(side=TOP)
       root2.mainloop()
       
##################################################################################################################################        
    def Receive(self):
        while True:
            msg = self.Socket.recv(1024).decode('UTF-8')
            msg = msg.split("<")
            
            print(msg) # for debug purpose
            
            if msg[0] == 'res':     # it's a response from a server
                if msg[1] == 'info':    # an info request responce
                    if msg[2][0] == 'S':
                        print(msg[2])
                    else:
                        for EachInfo in msg[2:-1]:
                            EachInfo = EachInfo.split(":")
                            if EachInfo[0] in self.MyContacts.keys():
                                print(f"Name :{self.MyContacts[EachInfo[0]]}", f"ID :{EachInfo[0]}",
                                      f"status :{EachInfo[1]}",
                                      sep='     ')
                            else:
                                print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
                if msg[1] == 'cg':
                    self.MyGroups[msg[2]] = msg[3]
                    print(self.MyGroups)
                if msg[1] == 'ca':

                    if msg[2] == 'True':
                        print("Group Admin has changed")
                        if msg[3] in self.MyContacts.keys():
                            print(f"New Group Admin is {self.MyContacts[msg[3]]}")
                        else:
                            print(f"New Group Admin is {msg[3]}")

                    elif msg[2] == 'False':
                        print("Group Admin can not be changed")
                        print(msg[3])

            elif msg[0] == 'm':     # a message
                if msg[1][0] == 'g':        # a group ID
                    if msg[2] in self.MyContacts.keys():
                        print(f"In Group --> {self.MyGroups[msg[1]]}<->{self.MyContacts[msg[2]]} --> {msg[3]}")
                    else:
                        print(f"In Group --> {self.MyGroups[msg[1]]}<->{msg[2]} --> {msg[3]}")
                else:       # a user ID
                    if msg[1] in self.MyContacts.keys():
                        print(f"{self.MyContacts[msg[1]]} --> {msg[2]}")
                    else:
                        print(f"From {msg[1]} --> {msg[2]}")   
       
##################################################################################################################################        
       
    def savesignup(self):
        root1.destroy()
        self.signin()
       
    def tryagain(self):
        Gui.destroy()
        self.signin()

    def presignup(self):
        Gui.destroy()
        self.signup()
    
    def validateLogin(self):
        Gui.destroy()
        self.login()
        
    def Signout(self):
        root2.destroy()
        self.signin()
   
    def __init__(self):
        #       What it will do?
        #           it will call the self.Decoder funtion when ever an object will be created
        #       How it will do?
        #
        #       Other
        try:
            self.Decoder()
        except KeyboardInterrupt:
            print("saving data ")
            #self.SaveData()
            print("Saved data")


if __name__ == '__main__':
    MyClient = Client()

