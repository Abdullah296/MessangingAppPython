import socket   # for creating sockets
import sys      # for handling exceptions
import json     # for saving data
import threading
import os
from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image, ImageTk

class Client:
    MyName = None     # My user name
    MyId = None   # My unique Id stored in server
    MyGroups = {}   # Groups which I have joined
    # MyGroups = {'Group Id':'Group Name'}
    MyContacts = {}     # List of contacts which i have saved
    # MyContacts = {'ID':'Name'}
    MyStatus = False   # I am online or offline
    Socket = None     # socket
    Notifications = {'Requests': {}, 'Messages': []}
    # formate:
    # Notification = {
    #                   'Requests' : { 'request' : 'Response'}
    #                   'Messages' : []
    #                   }

    ###############################################################################
    ###############################################################################
    # Format to communicate with Serevr
    # there are three types of communication here
    # 1. Request type (starts with: r<)
    # 2. Command type (starts with: c<)
    # 3. message type (starts with: m<)
    # 4. request from server (starts with: req<)
    # In Request type
    #       SignUp Request
    #           request format: r<up<password
    #           response format: res<up<unique_Id
    #       SignIn Request
    #           request format: r<in<ID<password
    #           response format: res<in<'True'/'False'
    #       Information Request (for current status online/offline)
    #           request format: r<info<ClientID<ClientID ... or r<info<GroupID
    #           response format: res<info<ID:Status<ID:Status ...
    # In Command Type
    #       Create Group
    #           request format:c<cg<GroupName<ID:ID:ID
    #           response format:res<cg<GroupID<GroupName (g+ID mean starts with g always)
    #       Remove from Group
    #           request format:c<rfg<Member's_ID<Group_ID
    #           response format:res<rfg<'True'/'False'<message from server
    #       Add to Group
    #           request format:c<atg<Member's_ID<Group_ID
    #           response format:res<atg<'True'/'False'<message from server
    #       Change Admin
    #           request format:c<ca<New_Admin_ID<Group_ID
    #           response format:res<ca<'True'/'False'<New_Admin
    # In Messsage Type
    #       Message to a single Client
    #           request format:m<OtherClient's_ID<message
    #           response format: m<Sender_ID<message (when ever you will recieve a messaage)
    #       Message in a Group
    #           request format:m<Group_ID<message
    #           response format: m<Group_ID<Sender_ID<message
    # request from server type
    #       Group Joining Request:
    #           request from server : req<gjr<Group_ID<Group_Name
    #           responce to server  : res<gjr<GID<Responce
    #
    # Responce types:
    #           yes : agree to join group
    #           not : not agree to join group
    #           pen : pending responce
    # by default server will use 'pen' or pending responce
    ###############################################################################
    ###############################################################################
    def SignUp(self,name,password,email,answer):     # will do sign Up
        #       What it will do?
        #           it will create a new user account
        #       How it will do?
        #           > take user_name, password from user
        #           > build request foramte (r<up<password)
        #           > take response from server (unique_ID)
        #       Other
        self.MyName = name
        temp = password
        temp = "r<up<" + temp
        self.Socket.sendall(temp.encode('UTF-8'))
        msg = self.Socket.recv(1024).decode('UTF-8')
        msg = msg.split("<")
        if msg[1] == 'up':  # response for Sign up request
            self.MyId = msg[2]  # setting ID
            print("\nSign Up Successfully")
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
        temp = "r<in<"+str(self.MyId)+"<"+str(temp)
        self.Socket.sendall(temp.encode('UTF-8'))
        msg = self.Socket.recv(1024).decode('UTF-8')
        msg = msg.split("<")
        if msg[1] == 'in':
            if msg[2] == 'True':
                print("\nSign in successful")
                self.MyStatus = True
                RThread = threading.Thread(target=self.Receive)
                RThread.start()
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
 ##################################################################################################################################        
    '''def MyProfile(self):    # will print My basics info
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
            Display.configure(state='disabled')'''
 ##################################################################################################################################            
    def Contacts(self):
        #       What it will do?
        #           it will print the saved contacts with there name, id & status if i signIn
        #       How it will do?
        #           > build the request formate (r<info<id<id ...)
        #           > create a request to server(with proper format)
        #           > take response from the server (Client_ID:status<Client_ID:status ...)
        #           > decodes it by spliting it with '<' (['Client_ID:status','Client_ID:status'])
        #           > prints the results by spliting it by ':'
        #       Other
        if self.MyStatus is True:
            msg = "r<info"
            # "r<info<id<id" format
            if len(self.MyContacts) == 0:   # empty no saved contacts
                Display.configure(state='normal')
                Display.insert('end', '\n'+"NO Saved Contacts  ")
                Display.configure(state='disabled')
                print("NO Saved Contacts")
            else:   # no empty conatacts are saved
                for id, name in self.MyContacts.items():
                    msg = msg + "<" + str(id)
                self.Socket.sendall(msg.encode('UTF-8'))
                

        else:
            print("Please Sign in")
            
    def AddContact1(self, name, idd):   # will add new contact
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
            print(idd)
            print(name)
            
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
        
        
        
        root4.geometry('400x400')  
        root4.title('Messaging app')
        
    
        Label(root4, text="Add Contact",   font= ("bold", 12)).grid(row=1, column= 3)
        Label(root4, text="",  ).grid(row=2, column= 3)
        
        Label(root4, text="",  ).grid(row=4, column= 0)
        Label(root4, text="",  ).grid(row=4, column= 1)
        Label(root4, text="User Name", width = 20,  font= ("bold", 10)).grid(row=4, column=2)
        Entry(root4, textvariable=nammee).grid(row=4, column=3)
        Label(root4,text="ID", width = 20,  font= ("bold", 10)).grid(row=5, column=2)  
        Entry(root4, textvariable=tid, ).grid(row=5, column=3)  
        def get():
            self.AddContact1(nammee.get(), tid.get())
            root4.destroy()
            self.login()
        loginButton = Button(root4, text="Add Contact", command=get,  ).grid(row=6, column=2)
        root4.mainloop()
################################################################################################################################## 
        
    def login(self):
       global root2
       global Display
       global Display2
       a = 0
       
       root2 = Tk()
       root2.geometry('500x400')  
       root2.title('Successfully login')
   
       TopFrame = Frame(root2).pack(side=TOP)
    ################################################################################################################################## 
       LeftFrame = Frame(TopFrame)
       
       Label(LeftFrame, text = "    Options: ",  height=1, width=15).pack(side=TOP)
       Option = ["MyProfile","Add Contacts","My Contacts","Create Group","Change admin","My group","Signout"]
       variable1 = StringVar(root2)
       variable1.set(Option[0])
       opt1 = OptionMenu(LeftFrame, variable1, *Option)
       opt1.config(width=13, font=('Helvetica', 9))
       opt1.pack(side="top")
       def printvariable(*args):
           
           if variable1.get() == "MyProfile":
               self.MyProfile()
               '''Display.configure(state='normal')
               Display.insert('end', '\n'+"Profile info:  ")
               Display.insert('end', '\n'+"User Name :\n"+self.MyName)
               Display.insert('end', '\n'+"User ID :"+self.MyId)
               Display.configure(state='disabled')'''
               
           elif variable1.get() == "Add Contacts":
               root2.destroy()
               self.AddContact()
               
           elif variable1.get() == "My Contacts":
               self.Contacts()
               
               
           elif variable1.get() == "Create Group":
               root2.destroy()
               self.CreateGroupGui()
               
               
           elif variable1.get() == "My group":
               self.GroupMembers()
               
               
           
           
           elif variable1.get() == "Signout":
               self.Socket.close()
               self.Signout()
               
           
           
       variable1.trace("w", printvariable)
       
       global variableee
       variableee = StringVar(root2)
       OptionList = Entry(LeftFrame, textvariable=variableee, width=15,  ).pack(side="top"  )
       #OptionList = ["Abdullah","Abdurrehman","Malik","Usama","Wajiha","Ahmad Tariq"] 
       #OptionList = self.MyContacts.keys()
       #variable = StringVar(root2)
       #variable.set(OptionList[0])
       #opt = OptionMenu(LeftFrame, variable, *OptionList)
       #opt.config(width=13, font=('Helvetica', 9))
       #opt.pack(side="top")
       
       
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
           Name.insert('end', variableee.get())
           Name.configure(state='disabled')
           
       def updatehistory(*args):
           #Display.configure(state='normal')
           #Display.insert('end', '\n'+variable.get())
           #Display.configure(state='disabled')
           Namechange()
           
       variableee.trace("w", updatehistory)
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
       a = 0
       
       displayFrame.pack(side=TOP)
       
       
       
       def sendmsg(*args):
           a = 0
           Display2.configure(state='normal')
           Display2.insert('end', '\n You: '+tkmessage.get())
           Display2.configure(state='disabled')
           self.Chat(tkmessage.get(), variableee.get())
           
       
       def callback(sv):
               
               s = ' is Typing '
               #Display2.configure(state='normal')
               #Display2.insert('end', '\n'+self.MyName+' is Typing ')
               #Display2.configure(state='disabled')
               self.Chat(s, variableee.get())
               
       '''def Chattt(s, client):
           global a
           if a == 0:
               self.Chat(s, client)
               a= a+1'''
               
       BottomFrame = Frame(RightFrame)
       
       tkmessage = StringVar(root2)
       tkmessage.trace("w", lambda name, index, mode, tkmessage=tkmessage: callback(tkmessage))
       tkkkkk = Entry(BottomFrame, textvariable=tkmessage, width=40,  ).pack(side=LEFT, padx=(5, 13), pady=(5, 10),  )
       btnConnect = Button(BottomFrame, text = "Send", height=1, width=5, command=sendmsg).pack(side=RIGHT)
       BottomFrame.pack(side=TOP)
       root2.mainloop()
            
  ##################################################################################################################################           
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
    
        
    def SaveData(self):
        #       What it will do?
        #           it will save data like contacts and group information to json fills to hardderive
        #           if i have signed in
        #       How it will do?
        #           > craetes a json file
        #           > write data to this file
        #           > save this file
        #       Other
        if self.MyStatus is True:
            with open("MyContacts.json", 'w') as File:  # creating and than opening file
                json.dump(self.MyContacts, File)    # writing data to file
            with open("MyGroups.json", 'w') as File:
                json.dump(self.MyGroups, File)
        else:
            print("Please Sign in")

    def LoadData(self):
        #       What it will do?
        #           it will load the saved data back to variables
        #       How it will do?
        #           > open the required file
        #           > load data to variable
        #           > close the file
        #       Other
        if self.MyStatus is True:
            try:
                File = open("MyContacts.json")
                self.MyContacts = json.load(File)
            except FileNotFoundError as err:
                print("No Saved Data found")
            else:
                print("Data Loaded successfully")
            try:
                File = open("MyGroups.json")
                self.MyGroups = json.load(File)
            except FileNotFoundError as err:
                print("No Saved Data found")
            else:
                print("Data Loaded successfully")

        else:
            print("Please Sign in")

##################################################################################################################################   

    def GroupMembers(self):
        #       What it will do?
        #           prints the group members with there current status
        #       How it will do?
        #           > builds the request formate (r<info<Group_ID)
        #           > make a request to server
        #           > takes response from server (Member's_ID:status<Member's_ID:status ...)
        #           > decodes and print it
        #       Other
        if self.MyStatus is True:
            msg = "r<info<"
            # "r<info<'group ID'" format
            # printing joined groups
            for gID, Name in self.MyGroups.items():
                print(f"Group ID :{gID} Group Name :{Name}")
                Display.configure(state='normal')
                Display.insert('end', '\n\n'+"Group info:  ")
                Display.insert('end', '\n'+"Group ID : "+gID)
                Display.insert('end', '\n'+"Group Name :"+Name)
                Display.configure(state='disabled')
                
################################################################################################################
   
        
   
       
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
        self.Decoder()
        
####################################################################################################################
    def CreateGroupGui(self):
        
        global Gname
        global tid0
        global tid1
        global tid2
        
        
        global root5
        root5 = Tk()
        
        Gname = StringVar()
        tid0 = StringVar()
        tid1 = StringVar()
        tid2 = StringVar()
        
        
        root5.geometry('400x400')  
        root5.title('Messaging app')
        
    
        Label(root5, text="Create Group",   font= ("bold", 12)).grid(row=1, column= 3)
        Label(root5, text="",  ).grid(row=2, column= 3)
        
        
        
        Label(root5, text="Group Name", width = 20,  font= ("bold", 10)).grid(row=3, column=2)
        Entry(root5, textvariable=Gname).grid(row=3, column=3)
        Label(root5, text="",  ).grid(row=4, column= 1)
        Label(root5,text="Patricipants ID", width = 20,  font= ("bold", 10)).grid(row=5, column=2)  
        Entry(root5, textvariable=tid0, ).grid(row=5, column=3)
        Label(root5,text="Patricipants ID", width = 20,  font= ("bold", 10)).grid(row=6, column=2)  
        Entry(root5, textvariable=tid1, ).grid(row=6, column=3) 
        Label(root5,text="Patricipants ID", width = 20,  font= ("bold", 10)).grid(row=7, column=2)  
        Entry(root5, textvariable=tid2, ).grid(row=7, column=3) 
        
        
        def get1():
            self.CreateGroup(Gname.get(), tid0.get(),tid1.get(), tid2.get())
            root5.destroy()
            self.login()
            
        loginButton = Button(root5, text="Create", command=get1,  ).grid(row=8, column=2)
        root5.mainloop()
    
    def CreateGroup(self, name, idd1,idd2, idd3):
        #       What it will do?
        #           it will create a new group and add inital members to it
        #       How it will do?
        #           > take group_name & group members id from user
        #           > build the request formate (c<cg<member's_ID<member's_ID ...)
        #           > take response from the server ('create ' or 'not created')
        #       Other
        tname = name
        print(name)
        print(idd1)
        print(idd2)
        print(idd3)
        rep = "c<cg<"+tname + "<"
        
        a = idd1
        if a != None:
            rep = rep + a + ":"
        
        if idd2 != '':
            print('hello 22')
            rep = rep + idd2 + ":"
        
        if idd3 != '':
            print('hello 32')
            rep = rep + idd3 + ":"
        self.Socket.sendall(rep.encode('UTF-8'))

    def ChangeAdmin(self):
        #       What it will do?
        #           it will change the admin of the group
        #           (it's server responsibility to check wethear requester is admin or not)
        #       How it will do?
        #           > take group ID, New Admin ID from user
        #           > build required formate (c<ca<New_Admin's_ID<GroupID)
        #           > make request to server
        #           > take response from the server ('Admin changed'/'You are not the admin of this group')
        #       Other
        # formate
        # c<ca<Group_ID<New_Admin_ID
        command = "c<ca<"
        print("Your Groups :")
        print(self.MyGroups)
        gid = input("Enter group Id :")
        self.Contacts()
        id = input("Enter New Admins ID :")
        command = command + str(id) + "<" + str(gid)
        self.Socket.sendall(command.encode('UTF-8'))

    def RemoveFromGroup(self):
        #       What it will do?
        #           it will remove a group member from a Group
        #           (it's server responsibility to check wethear requester is admin or not)
        #       How it will do?
        #           > take Member's ID & Group's ID from user
        #           > build request formate (c<rfg<Member's_ID<Group_ID)
        #           > make request to server
        #           > take response from the server ('Admin changed'/'You are not the admin of this group')
        #       Other
        gID = self.GroupMembers()
        cID = input("Select Group Member: ")
        req = "c<rfg<" + cID + "<" + gID
        print(req)
        self.Socket.sendall(req.encode('UTF-8'))

    def AddToGroup(self):
        #       What it will do?
        #           it will add a new memeber to already created Group
        #           (it's server responsibility to check wethear requester is admin or not)
        #       How it will do?
        #           > take new member's ID, Group ID from user
        #           > build request formate (c<atg<New_Member's_ID<Group_ID)
        #           > make request to server
        #           > response from server
        #       Other
        req = "c<atg<"
        print(self.MyGroups)
        gID = input("Enter group ID: ")
        print(self.MyContacts)
        cID = input("Enter new member ID: ")
        req = req + cID + "<" + gID
        self.Socket.sendall(req.encode('UTF-8'))

    def GoOffline(self):    # will disconnect from server
        #       What it will do?
        #           it will disconnect from server
        #       How it will do?
        #           > close the connection or socket
        #       Other
        self.Socket.close()
        self.Socket = None
        self.MyStatus = False

    

    def Chat(self, message, idd):
        #       What it will do?
        #           it will starts chat to a Client or in Group
        #       How it will do?
        #           > ask's for chat to client or in group
        #           > take other Uer or Group's_ID from Uer
        #           > take message to send
        #           > encode it (m<ID<message)
        #           > make request to Server
        #           > receve a message from another client
        #           > repeate this process till '\end' entered
        #       Other
        
        
            
            OtherClient = idd
            msg = message
            msg = "m<" + OtherClient + "<" + msg
            self.Socket.sendall(msg.encode('UTF-8'))
            
            

    

    def close(self):
        #       What it will do?
        #           it will close the socket
        #       How it will do?
        #
        #       Other
        try:
            print("closing socket")
            self.Socket.close()
        except socket.error as err:
            print("socket closing error :",err)
            sys.exit("Socket closing error")

    def ViewMesssages(self):
        if len(self.Notifications['Messages']) == 0:
            print("No Message")
        else:
            for EachMessage in self.Notifications['Messages']:
                print(EachMessage)
            # removing printed messages from self.Notifications['Messages']
            self.Notifications['Messages'] = []

    def ViewRequests(self):
        if len(self.Notifications['Requests']) == 0:
            print("\nNo Request")
        else:
            i = 0
            
            request = []
            for EachRequest, resp in self.Notifications['Requests'].items():
                request.append(EachRequest)
                EachRequest = EachRequest.split("<")
                tstr = f"{i}. Group ID: {EachRequest[2]} Group Name: {EachRequest[3]} Present Response: {resp}"
                print(tstr)
                i = i + 1
            
            print(request)
            print("\n1. Change Response")
            print("2. Exit")
            op = input(">>>")
            if op == '1':
                rno = input("Enter Request No: ")
                print("Enter 'yes' (for joining)")
                print("Enter 'no' (for rejecting)")
                print("Enter 'pending' (for later)")
                resp = input(">>> ")
                if resp != 'pending':
                    ############################
                    # building responce for sending to server
                    gID = input("Enter Group ID: ")
                    resp = "res<gjr<" + gID + "<" + resp
                    lll = request[0]
                    del self.Notifications['Requests'][lll]
                    self.Socket.sendall(resp.encode('UTF-8'))
                    


    def NotificationHandler(self):
        # it will handler Notification recieved by client
        # it will handel request and Messages
        if len(self.Notifications['Requests']) == 0:
            print("\nNo Request")
        else:
            print(f"Got Requests ({len(self.Notifications['Requests'])})")
        if len(self.Notifications['Messages']) == 0:
            print("No Message")
        else:
            print(f"Got Messages ({len(self.Notifications['Messages'])})")

    def Receive(self):
        while True:
            print('hello 11')
            msgS = self.Socket.recv(1024).decode('UTF-8')
            print(msgS)
            msg = msgS.split("<")
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
                                Display.configure(state='normal')
                                Display.insert('end', '\n'+"My Contacts  ")
                                Display.insert('end', '\n'+'Name :'+self.MyContacts[EachInfo[0]])
                                Display.insert('end', '\n'+"ID :"+EachInfo[0])
                                Display.insert('end', '\n'+"status :"+EachInfo[1])
                                Display.configure(state='disabled')
                                
                            else:
                                print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
                                Display.configure(state='normal')
                                Display.insert('end', '\n'+'Name :'+ 'Not Saved')
                                Display.insert('end', '\n'+"ID :"+EachInfo[0])
                                Display.insert('end', '\n'+"status :"+EachInfo[1])
                                Display.configure(state='disabled')
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
                if msg[1] == 'rfg':     # remove from group request, responce
                    if msg[2] == 'True':    # removed
                        print("Removed from group")
                        print(msg[3])
                    elif msg[2] == 'False':     # can not be removed
                        print("Can not be Removed")
                        print(msg[3])
                if msg[1] == 'atg':     # add to group responce
                    if msg[2] == 'True':    # added to group
                        print(msg[3])
                    elif msg[2] == 'False':     # can not be added to group
                        print(msg[3])
                if msg[1] == 'gjr':     # responce on group joining responce
                    if msg[4] == 'True':    # added to the group
                        self.MyGroups[msg[2]] = msg[3]  # setting group_ID and group_Name
                        print("added to the group")
                    elif msg[4] == 'False':
                        print("can not be added to the group")
            elif msg[0] == 'm':     # a message
                if msg[1][0] == 'g':        # a group ID
                    if msg[2] in self.MyContacts.keys():
                        tmsg = f"In Group --> {self.MyGroups[msg[1]]}<->{self.MyContacts[msg[2]]} --> {msg[3]}"
                        Display2.configure(state='normal')
                        Display2.insert('end', '\n'+'In Group --> '+self.MyGroups[msg[1]]+'<->'+self.MyContacts[msg[2]]+'--> '+msg[3])
                        Display2.configure(state='disabled')
                    else:
                        tmsg = f"In Group --> {self.MyGroups[msg[1]]}<->{msg[2]} --> {msg[3]}"
                        Display2.configure(state='normal')
                        Display2.insert('end', '\n'+'In Group --> '+self.MyGroups[msg[1]]+'<->'+msg[2]+'--> '+msg[3])
                        Display2.configure(state='disabled')
                else:       # a user ID
                    if msg[1] in self.MyContacts.keys():
                        tmsg = f"{self.MyContacts[msg[1]]} --> {msg[2]}"
                        if (msg[2] !=  ' is Typing ')  and (msg[2] !=  'Message Read'):
                                Display2.configure(state='normal')
                                Display2.insert('end', '\n'+self.MyContacts[msg[1]]+'--> '+msg[2])
                                Display2.configure(state='disabled')
                        else:
                            Display2.configure(state='normal')
                            Display2.insert('end', '\n'+self.MyContacts[msg[1]]+': '+msg[2])
                            Display2.configure(state='disabled')
                            
                        
                        if msg[2] !=  ' is Typing ':
                            if msg[2] !=  'Message Read':
                                self.Chat('Message Read', msg[1] )
                    else:
                        tmsg = f"From {msg[1]} --> {msg[2]}"
                        if (msg[2] !=  ' is Typing ')  and (msg[2] !=  'Message Read'):
                            
                                Display2.configure(state='normal')
                                Display2.insert('end', '\n'+msg[1]+'--> '+msg[2])
                                Display2.configure(state='disabled')
                        else:
                            Display2.configure(state='normal')
                            Display2.insert('end', '\n'+msg[1]+'::  '+msg[2])
                            Display2.configure(state='disabled')
                                
                        if msg[2] !=  ' is Typing ':
                            if msg[2] !=  'Message Read':
                                self.Chat('Message Read', msg[1] )
                        
                self.NotificationHandler()
            elif msg[0] == 'req':   # request from server
                if msg[1] == 'gjr':     # a group joining request
                    self.Notifications['Requests'][msgS] = 'pen'
                    print(self.Notifications)
                self.NotificationHandler()

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
            '''RThread = threading.Thread(target=self.Receive)
            RThread.start()'''
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