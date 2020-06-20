import socket   # for creating sockets
import sys      # for handling exceptions
import json     # for saving data
import threading

class Client:
    MyName = None     # My user name
    MyId = None   # My unique Id stored in server
    MyGroups = {}   # Groups which I have joined
    # MyGroups = {'Group Id':'Group Name'}
    MyContacts = {}     # List of contacts which i have saved
    # MyContacts = {'ID':'Name'}
    MyStatus = False   # I am online or offline
    Socket = None     # socket

    ###############################################################################
    ###############################################################################
    # Format to communicate with Serevr
    # there are three types of communication here
    # 1. Request type (starts with: r<)
    # 2. Command type (starts with: c<)
    # 3. message type (starts with: m<)
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
    #           response format:res<rfg<'True'/'False'
    #       Add to Group
    #           request format:c<atg<Member's_ID<Group_ID
    #           response format:res<atg<'True'/'False'
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
    ###############################################################################
    ###############################################################################

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
                print("NO Saved Contacts")
            else:   # no empty conatacts are saved
                for id, name in self.MyContacts.items():
                    msg = msg + "<" + str(id)
                self.Socket.sendall(msg.encode('UTF-8'))
                '''info = self.Socket.recv(1024).decode('UTF-8')
                info = info.split("<")
                for EachInfo in info[:-1]:
                    EachInfo = EachInfo.split(":")
                    if EachInfo[0] in self.MyContacts.keys():
                        print(f"Name :{self.MyContacts[EachInfo[0]]}", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}",
                              sep='     ')
                    else:
                        print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')'''

        else:
            print("Please Sign in")

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
            gID = input("Enter Group ID :")
            msg = msg + gID
            self.Socket.sendall(msg.encode('UTF-8'))
            '''info = self.Socket.recv(1024).decode('UTF-8')
            info = info.split("<")
            if info[0][0] == 'S':
                print(info)
            else:
                for EachInfo in info[:-1]:
                    EachInfo = EachInfo.split(":")
                    if EachInfo[0] in self.MyContacts.keys():
                        print(f"Name :{self.MyContacts[EachInfo[0]]}", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}",
                              sep='     ')
                    elif EachInfo[0] == self.MyId:
                        print(f"You ", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
                    else:
                        print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')'''
        else:
            print("Please Sign in")

    def SignUp(self):   # will do sign Up
        #       What it will do?
        #           it will create a new user account
        #       How it will do?
        #           > take user_name, password from user
        #           > build request foramte (r<up<password)
        #           > take response from server (unique_ID)
        #       Other
        self.MyName = input("Enter your User Name :")
        temp = input("Enter Your Password :")
        temp = "r<up<" + temp
        self.Socket.sendall(temp.encode('UTF-8'))
        msg = self.Socket.recv(1024).decode('UTF-8')
        msg = msg.split("<")
        if msg[1] == 'up':  # response for Sign up request
            self.MyId = msg[2]  # setting ID
            print("\nSign Up Successfully")
            print("Your user name :", self.MyName)
            print("Your ID is :", self.MyId)

    def SignIn(self):   # will do sign in
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
            self.MyName = input("Enter User Name :")
        if self.MyId is None:
            self.MyId = input("Enter Your ID :")
        temp = input("Enter Your Password :")
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
            else:
                print("\nTry again")

    def CreateGroup(self):
        #       What it will do?
        #           it will create a new group and add inital members to it
        #       How it will do?
        #           > take group_name & group members id from user
        #           > build the request formate (c<cg<member's_ID<member's_ID ...)
        #           > take response from the server ('create ' or 'not created')
        #       Other
        tname = input("Enter Group Name :")
        rep = "c<cg<"+tname + "<"
        a = None
        print("Enter 'end' to exit")
        while a != 'end':
            a = input("Enter User Id to Add in this Group:")
            rep = rep + a + ":"
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
        pass

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
        pass

    def GoOffline(self):    # will disconnect from server
        #       What it will do?
        #           it will disconnect from server
        #       How it will do?
        #           > close the connection or socket
        #       Other
        self.Socket.close()
        self.Socket = None
        self.MyStatus = False

    def AddContact(self):   # will add new contact
        #       What it will do?
        #           it will save a new contact
        #       How it will do?
        #           > take Client's ID, name from user
        #           > add it to self.MyContacts
        #           (it does not make any request to server)
        #       Other
        if self.MyStatus is True:
            tid = input("Enter ID :")
            tname = input("Enter Name :")
            if tid not in self.MyContacts.keys():
                self.MyContacts[str(tid)] = tname
                print("Added successfully")
            else:
                print("User Already Exist")
        else:
            print("Please Sign in")

    def MyProfile(self):    # will print My basics info
        #       What it will do?
        #           it will print User Name & ID
        #       How it will do?
        #
        #       Other
        if self.MyStatus is True:
            print("User Name :", self.MyName)
            print("User ID :", self.MyId)

    def Chat(self):
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
        print("1. In group")
        print("2. with client")
        print("3. Exit")
        t = input(">>>")
        if t == '1':
            print(self.MyGroups)
            OtherClient = input("Enter Group ID :")
            msg = input(">>>")
            while msg!='\end':
                msg = "m<" + OtherClient + "<" + msg
                self.Socket.sendall(msg.encode('UTF-8'))
                msg = input(">>>")
                
        if t == '2':
            print(self.MyContacts)
            OtherClient = input("Enter Client's ID :")
            msg = input(">>>")
            while msg != '\end':
                msg = "m<" + OtherClient + "<" + msg
                self.Socket.sendall(msg.encode('UTF-8'))
                msg = input(">>>")

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
                print("1. Go Online")
                print("2. Exit")
                temp = input(">>>")
                if temp is '1':
                    self.ConnectToServer()
                elif temp is '2':
                    break
            elif self.MyStatus is False:     # I have't Sign in
                print("1. Sign UP")
                print("2. Sign In")
                temp = input(">>>")
                if temp is '1':
                    self.SignUp()
                elif temp is '2':
                    self.SignIn()
                    #print("loading data")
                    #self.LoadData()
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

