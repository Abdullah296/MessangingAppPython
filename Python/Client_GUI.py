
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
            '''   
            else:
                print("1. Create New Group")
                print("2. Change Group Admin")
                print("3. Add to Group")
                print("4. Remove from Group")
                print("5. Chat")
                print("6. Go Offline")
                print("7. My Profile")
                print("8. Add New Contact")
                print("9. Contacts")
                print("a. View Group Members")
                print("b. Exit")
                temp = input(">>>")
                if temp is '1':
                    self.CreateGroup()
                elif temp is '2':
                    self.ChangeAdmin()
                elif temp is '3':
                    self.AddToGroup()
                elif temp is '4':
                    self.RemoveFromGroup()
                elif temp is '5':
                    self.Chat()
                elif temp is '6':
                    self.GoOffline()
                elif temp is '7':
                    self.MyProfile()
                elif temp is '8':
                    self.AddContact()
                elif temp is '9':
                    self.Contacts()
                elif temp is 'a':
                    self.GroupMembers()
                elif temp is 'b':
                    #self.SaveData()
                    self.Socket.close()
                    break
                else:
                    print("Please Enter a Valid Option")
    '''
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
           
    def login(self):
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
