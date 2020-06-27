# messaging server
# importing libraries
import socket
import sys
import threading
import json
import random
import time
import tqdm
import os

class Server:
    MaxClient = 10   # total clients to be handled at a time
    # OnlineClients = {}  # available clients
    Groups = {}     # Groups members with there IDs
    # Groups = {GroupID:[Group Members List]}
    GroupNames = {}     # saves the name and Group id
    # GroupNames = {'groupID':'group Name'}
    Admins = {}     # Each Group's Admin ID and Group's ID
    # Admins = {GroupID:Group_Admin_ID}
    ClientsSockets = {}    # Each Clients ID and Socket(if available)
    # Clients = {Clients_ID:Client_Socket}
    CurrentClientStatus = {}    # Each Client's ID with its Sign In status
    # CurrentClientStatus = {ClientID:'online/ofline'}
    ClientPass = {}     # Each Client's ID with its Password
    # ClientPass = {Client_ID:Password}
    Buffer = {}     # to store un sended messages with id
    # Buffer = {ID:[Messages]}
    Requests = {}   # store Group joining requests of Each client with there responce
    # Requests = { 'Client_ID':{ 'Group_ID': 'Responce'}
    #               }
    # Responce types:
    #           yes : agree to join group
    #           not : not agree to join group
    #           pen : pending responce
    # by default server will use 'pen' or pending responce
    PendingRequests = {}    # it will store un-sended requests
    # PendingRequests = { 'Client_ID':{ 'Group_ID': 'Responce'}
    #                       }

    def GetID(self, sock):
        #   What it will do?
        #       it will return th id of the given socket
        #   How it will do?
        #       > itrate over the self.ClietsSockets
        #       > mach socket if matched return ID
        #       > if not matched continue
        #   Other
        #
        print("finding id ...")
        for id, s in self.ClientsSockets.items():
            if s == sock:
                print("id found ...")
                return id

    def SignIn(self, id, password, sock):
        #   What it will do?
        #       it will do Sign in work
        #   How it will do?
        #       > Check id is regestered
        #       > match ID and password
        #       > send response = 'res<in<True' if success
        #       > IF response == 'True'
        #           change Client's status to online
        #           Add Client's Socket to available Sockets
        #       > send response = 'res<in<False' if not success
        #   Other
        #
        print("Sign in request form ", id)
        if str(id) in str(self.ClientPass.keys()):
            print("ID found ...")
            if str(self.ClientPass[id]) == str(password):
                print("Password matched ...")
                rep = 'res<in<True'
                sock.sendall(rep.encode('UTF-8'))
                print(self.ClientPass)
                print("Adding Client's Socket to Available Clients Lists ...")
                self.ClientsSockets[str(id)] = sock
                print("added successfully ...")
                print("available clients are ")
                print(self.ClientsSockets)
                print("updating Client's status ...")
                self.CurrentClientStatus[str(id)] = 'online'
                print("updated successfully ...")
                print(self.CurrentClientStatus)
            else:
                print("Password not matched ...")
                rep = 'res<in<False'
                sock.sendall(rep.encode('UTF-8'))
        else:
            print("ID not present ...")
            rep = 'res<in<False'
            sock.sendall(rep.encode('UTF-8'))

    def SignUp(self, password, sock):
        #   What it will do?
        #       it will do Sign Up Work
        #   How it will do?
        #       > genreate a random key
        #       > IF key exist already
        #               genreate an other key
        #       > ELSE
        #               Add key and password to self.ClientPass
        #       > send key to Client
        #   Other
        #
        # print("New Sign Up request ...")
        print("Generating Random key ...")
        tID = random.randint(0, self.MaxClient)     # a temp ID
        tID = str(tID)
        if tID not in self.ClientPass.keys():
            print("Adding to Client's list ...")
            self.ClientPass[tID] = str(password)
            print(self.ClientPass)
            print("Added Successfully ...")
            print("Sending response to Client ...")
            temp = "res<up<" + tID
            sock.sendall(temp.encode('UTF-8'))
            print("Sended Successfully ...")
            print("updating Client's status ...")
            self.CurrentClientStatus[tID] = 'offline'
            print("updated successfully ...")
            print(self.CurrentClientStatus)
        else:
            print("Key is present already ...")
            self.SignUp(password, sock)

    def CheckBuffer(self, stime):
        #   What it will do?
        #       it will send un sended messages
        #   How it will do?
        #       > IF Buffeer is not empty
        #               if Client is Online
        #                   Send messages to client
        #               else
        #                   Check for other client /do nothing
        #       > sleep for some time and repeate again
        #   Other
        #
        while True:
            time.sleep(stime)
            print("checking bufffer ...")
            pass


    def SendMessage(self, msg, id, sock):
        #   What it will do?
        #       it will send message to a client
        #   How it will do?
        #       > IF id is a group's ID
        #            (send message to all group members)
        #            > if Client is online
        #                send message
        #            else
        #                add Cleint's ID and message to Buffer
        #            (repeate above process for all group members)
        #       > ELSE
        #         (send message to Client)
        #         > IF Client is online
        #             send message
        #         > ELSE
        #             add Cleint's ID and message to Buffer
        #   Other
        #
        # first checking id
        if  msg == '':    
          '''  BUFFER_SIZE = 4096
            received = ClientSocket.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split()
            filename = os.path.basename(filename)
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for _ in progress:
                    bytes_read = ClientSocket.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
            
            ClientSocket.close()
            # close the server socket'''
        else:
            print("message sending request ...")
            if id[0] == 'g':    # its a grou;s id
                print("a group id ...")
                MyId = self.GetID(sock)
                for EachMember in self.Groups[id]:
                    print("sending message to client :", EachMember)
                    if EachMember in self.ClientsSockets.keys():
                        print("client is online ...")
                        print("sending message ...")
                        temp = "m<" + str(id) + "<" + str(MyId) + "<" + msg
                        self.ClientsSockets[EachMember].sendall(temp.encode('UTF-8'))
                        print("message sent ...")
    
                    else:
                        print("client is not online ...")
                        print("adding message to buffer for sending latter ...")
                        self.Buffer[str(EachMember)] = []
                        self.Buffer[str(EachMember)].append(msg)
                        print("added to buffer ...")
                        print(self.Buffer)
            else:
                MyId = self.GetID(sock)
                print("a client's id ...")
                if id in self.ClientsSockets.keys():
                    print("client is online ...")
                    print("sending message ...")
                    temp = MyId + "<" + msg
                    temp = "m<" + temp
                    self.ClientsSockets[id].sendall(temp.encode('UTF-8'))
                    print("sent ...")
                else:
                    print("client is not online ...")
                    print("adding to buffer ...")
                    self.Buffer[str(id)] = []
                    self.Buffer[id].append(msg)
                    print("added ...")

    def Info(self, msg, sock):
        #   What it will do?
        #       it will gather information of current status and send it to client
        #   How it will do?
        #       > IF a group_ID:
        #            Send for Each Member's Status in required format
        #       > else
        #            decode the given ids and send there status
        #   Other
        #   response format : MemberID:statsus<MemberID:statsus ...
        print(msg)
        print("got an info request ...")
        rep = ''
        print("gathering info ...")
        # if requests is for Group ID than
        # r<info<gID
        # len(msg) == 1 beacuse only one group ID will be passed
        # and only one client ID can also be passed as well
        # so checking weather a group ID of not will be like
        # msg[0][0] == 'g' mean a group ID
        # other wise it will be Clients ID
        if msg[0][0] == 'g': # group members request
            if self.GetID(sock) in self.Groups[msg[0]]:  # a memeber of that group
                for EachId in self.Groups[msg[0]]:  # getting info of group members
                    print("for EachId in msg:", EachId)
                    if EachId in self.CurrentClientStatus.keys():
                        if self.CurrentClientStatus[EachId] == 'online':
                            if self.Admins[msg[0]] == EachId:
                                rep = rep + str(EachId) + ":online (Admin)<"
                            else:
                                rep = rep + str(EachId) + ":online<"

                            print(rep)
                        else:
                            print("else:")
                            if self.Admins[msg[0]] == EachId:
                                rep = rep + str(EachId) + ":offline (Admin)<"
                            else:
                                rep = rep + str(EachId) + ":offline<"
                            print(rep)
                    else:
                        rep = rep + str(EachId) + ":Not found<"
            else:
                rep = "Sorry you are not a member of this gorup"

        else:
            for EachId in msg:
                print("for EachId in msg:", EachId)
                if EachId in self.CurrentClientStatus.keys():
                    if self.CurrentClientStatus[EachId] == 'online':
                        rep = rep + str(EachId) + ":online<"
                        print(rep)
                    else:
                        print("else:")
                        rep = rep + str(EachId) + ":offline<"
                        print(rep)
                else:
                    rep = rep + str(EachId) + ":Not found<"

        print("gathered ...")
        rep = "res<info<" + rep
        print(rep)
        print("sending to client ...")
        sock.sendall(str(rep).encode('UTF-8'))
        print("sent ...")

    def CreateGroup(self, msg, sock):
        #   What it will do?
        #       create a group
        #   How it will do?
        #       > get request from Client (c<cg<Group_Name<id<id ....)
        #       > genrate a random key
        #       > Add 'g' at start / key = g + str(key)
        #       > IF key is not already present
        #           Add Group_Name and Key to self.Groups
        #       > genarte another key and repeate the process
        #       > decode given ids and add them to group members
        #       > add requester's ID to Group Members
        #       > add requester's ID to Admin list with group ID
        #   Other
        #
        print("request for create a new group ...")
        print("Generating Random key ...")
        temp = random.randint(0, self.MaxClient)
        temp = str(temp)
        temp = "g" + temp
        # msg = ['Group Name','group members']
        if temp not in self.Groups.keys():
            print("Adding to Group to list ...")
            self.Groups[temp] = []
            print("updating GroupNames ...")
            self.GroupNames[temp] = str(msg[0])
            print("updated ...")
            print(self.GroupNames)
            # building request
            req = "req<gjr<" + temp + "<" + msg[0]
            print(req)
            #######################################
            # Formate:
            # self.Requests = { 'client ID':{'Group ID':'Responce'},
            #                       }
            # Responce types:
            #           yes : agree to join group
            #           not : not agree to join group
            #           pen : pending responce
            # by default server will use 'pen' or pending responce
            ######################################
            # adding each member to self.Requests with group ID
            print("Updating self.Requests")
            for EachId in str(msg[1]).split(":")[:-2]:
                print("adding members ...")
                if EachId in self.Requests.keys():
                    self.Requests[EachId][temp] = 'pen'
                else:
                    self.Requests[EachId] = {temp: 'pen'}
            print(self.Requests)
            #####################################
            # sending request to Each Member
            print("sending request to group members")
            for EachId in str(msg[1]).split(":")[:-2]:
                if EachId in self.CurrentClientStatus.keys():      # client with EachID exist
                    if self.CurrentClientStatus[EachId] == 'online':  # client is online
                        self.ClientsSockets[EachId].sendall(req.encode('UTF-8'))   # sending request
                        print(f"sening request to {EachId}")
                    else:
                        if EachId in self.PendingRequests.keys():
                            self.PendingRequests[EachId][temp] = 'pen'
                        else:
                            self.PendingRequests[EachId] = {temp: 'pen'}
            #####################################
            # adding admin to group member list
            id = self.GetID(sock)   # finding id of the requester
            print("adding members to groups ...")
            self.Groups[temp] = [str(id)]
            print("Added Successfully ...")
            print(self.Groups)
            #####################################
            # adding admin to group member list
            print("Adding Group Admin ...")
            self.Admins[str(temp)] = str(id)
            print(self.Admins)
            print("updated ...")
            print("Sending key to Client ...")
            # building response
            temp = "res<cg<" + temp + "<" + msg[0]
            sock.sendall(temp.encode('UTF-8'))
            print("Sended Successfully ...")
        else:
            print("Key is present already ...")
            self.CreateGroup(msg, sock)

    def ChangeAdmin(self, msg, sock):
        #   What it will do?
        #       change the admin of the group
        #   How it will do?
        #       > request from Client (c<cg<New_Admin_ID<Group_ID)
        #       > get requester's id
        #       > IF requester is Admin
        #               change admin
        #               send response 'Admin Changes'
        #       > ELSE no change
        #               send response "You are not admin of this group"
        #   Other
        #
        # formate
        # c<ca<Group_ID<New_Admin_ID
        # here msg = ['Group_ID','New_Admin_ID']
        print("request for changing admin ...")
        if sock in self.ClientsSockets.values():
            print("socket found ...")
            print("finding id of requester ...")
            MyId = self.GetID(sock)
            print("Conferming admin ...")
            if self.Admins[msg[1]] == MyId:     # admin id matched
                print("confermed admin ...")
                print("changing admin ...")
                self.Admins[msg[1]] = msg[0]    # setting new Admin
                print("admin changed ...")
                print(self.Admins)
                rep = "res<ca<True<" + msg[0]
                print("sending reply to client ...")
                sock.sendall(rep.encode('UTF-8'))
                print("sent ...")
            else:
                rep = "res<ca<False<You are not the admin of this group"
                print("sending reply to client ...")
                sock.sendall(rep.encode('UTF-8'))
                print("sent ...")

    def RemoveFromGroup(self,  msg, sock):
        #   What it will do?
        #       it will remove a member from group
        #   How it will do?
        #       > if requester is Admin
        #           > if given_ID is in GroupMembers
        #               remove from group
        #               send response 'removed from group'
        #           > else send response 'No member with this id found'
        #       >else send "you are not admin of this group"
        #   Other
        #
        # msg = ['Member's_ID', 'Group_ID']
        print("got a remove from group request ...")
        print(msg)
        MyId = self.GetID(sock)     # requester's ID
        print('checking admin ...')
        if self.Admins[msg[1]] == MyId:   # checking Admin
            print("admin conformed ...")
            if MyId != msg[0]:      # if member is not admin
                if msg[0] in self.Groups[msg[1]]:  # checking Member
                    print("removing from group ...")
                    self.Groups[msg[1]].remove(msg[0])  # removing member
                    print("removed from group ...")
                    print("sending reply to client ...")
                    rep = "res<rfg<True<Removed " + msg[0] + " from group " + msg[1]
                    sock.sendall(rep.encode('UTF-8'))
            else:
                rep = "res<rfg<False<You are the admin plz change admin and Try again"
                sock.sendall(rep.encode('UTF-8'))
        else:
            rep = "res<rfg<False<You are not the admin or Member deos't exist"
            sock.sendall(rep.encode('UTF-8'))

    def AddToGroup(self,  msg, sock):
        #   What it will do?
        #       add a new member to an already created group
        #   How it will do?
        #       > if requester is Admin:
        #           add given id to member list
        #           send response 'added successfully'
        #       > else send response 'you are not admin of this group'
        #   Other
        #
        # msg = [New_Member's_ID, Group_ID]
        print("got an add member request ...")
        if msg[1] in self.Groups.keys():    # if group exist
            print("group exist ...")
            MyId = self.GetID(sock)     # requester's ID
            print("checking admin ...")
            if MyId == self.Admins[msg[1]]:     # if requester is admin
                if msg[0] not in self.Groups[msg[1]]:   # if member not exist before
                    print("adding member to list ...")
                    self.Groups[msg[1]].append(msg[0])
                    rep = "res<atg<True< Member " + msg[0] + " added to the group " + msg[1]
                    sock.sendall(rep.encode('UTF-8'))
                else:
                    rep = "res<atg<False< Member " + msg[0] + " already exist in group " + msg[1]
                    sock.sendall(rep.encode('UTF-8'))
            else:
                rep = "res<atg<False<You are not he admin of the group " + msg[1]
                sock.sendall(rep.encode('UTF-8'))
        else:
            rep = "res<atg<False<Group not exist"
            sock.sendall(rep.encode('UTF-8'))

    def GJRespHandler(self, resp, sock):
        # Group Joining Responce Handler
        print("got a responce on GJR ...")
        MyId = self.GetID(sock)
        if MyId in self.Requests.keys():    # checking weather requester exist
            if resp[0] in self.Requests[MyId].keys():   # checking weather this request exist
                if resp[1] == 'yes':
                    print("ading member to group ...")
                    self.Groups[resp[0]].append(MyId)  # adding member to list
                    print(self.Groups)
                    del self.Requests[MyId][resp[0]]  # deleting that request
                    rep = f"res<gjr<{resp[0]}<{self.GroupNames[resp[0]]}<True"
                    sock.sendall(rep.encode('UTF-8'))
                elif resp[1] == 'no':
                    del self.Requests[MyId][resp[0]]  # deleting that request
                    rep = f"res<gjr<{resp[0]}<{self.GroupNames[resp[0]]}<False"
                    sock.sendall(rep.encode('UTF-8'))

    def Decoder(self, msg, sock):
        #   What it will do?
        #       it decode the request and call a specific function to handel that request
        #   How it will do?
        #       > split by "<" (eg in sign in case ['r', 'in','id','password'])
        #       > sepreat given info according to specified format and call the specific function
        #   Other
        #
        msg = msg.split("<")
        print(msg)
        if msg[0] == 'r':
            if msg[1] == 'in':
                try:
                    self.SignIn(msg[2], msg[3], sock)
                except IndexError as err:
                    print("Error in msg ...")
                    print(err)
                    rep = 'False'
                    sock.sendall(rep.encode('UTF-8'))
                else:
                    pass
            if msg[1] == 'up':
                try:
                    self.SignUp(msg[2], sock)
                except IndexError as err:
                    print("ERROR in message ...")
            if msg[1] == 'info':
                try:
                    self.Info(msg[2:], sock)
                except IndexError as err:
                    print("error in index ", err)
        if msg[0] == 'c':
            if msg[1] == 'cg':   # create group
                self.CreateGroup(msg[2:], sock)
            if msg[1] == 'rfg':  # remove from group
                self.RemoveFromGroup(msg[2:], sock)
            if msg[1] == 'atg':     # add to group
                self.AddToGroup(msg[2:], sock)
            if msg[1] == 'ca': # change admin
                self.ChangeAdmin(msg[2:], sock)
        if msg[0] == 'm':
            if msg[2] == 'file':
                self.recievefile(sock)
            else:
                self.SendMessage(msg[2], msg[1], sock)
        if msg[0] == 'res':
            self.GJRespHandler(msg[2:], sock)

    def recievefile(self,sock):
        print('Recieving file')
        BUFFER_SIZE = 4096
        received = sock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split()
        filename = os.path.basename(filename)
        filesize = int(filesize)
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        print('hello')
        with open(filename, "wb") as f:
            for _ in progress:
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
                
    def Handler(self, sock, adr):
        #   What it will do?
        #       it will handle incoming connection requets and update sockets of clients
        #   How it will do?
        #       > if connection is not required
        #           > if socket was in self.CleintSockets
        #                delete that socket
        #                change status to offline
        #           > close the connection
        #   Other
        #
        while True:
            msg = sock.recv(1024)
            msg = msg.decode('UTF-8')
            if not msg:
                if sock in self.ClientsSockets.values():
                    for id, s in self.ClientsSockets.items():
                        if sock == s:
                            print("deleting Socket from list ...")
                            del self.ClientsSockets[id]
                            print("deleted ...")
                            print(self.ClientsSockets)
                            print("updating client's status ...")
                            self.CurrentClientStatus[id] = 'offline'
                            print("updated ...")
                            print(self.CurrentClientStatus)
                            break
                break
            else:
                self.Decoder(msg, sock)



    def __init__(self):
        #   What it will do?
        #       inilize the server
        #   How it will do?
        #       > create a socket
        #       > bind it to server address
        #       > waite for new connections
        #       > create a new thread when ever a connection request made
        #   Other
        #
        try:
            print("Creating Socket ...")
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")
        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)
        try:
            print("Running Server at address :", ServerAdress)
            self.Socket.bind(ServerAdress)
        except socket.error as err:
            print("Socket Binding error :", err)
            sys.exit(err)
        else:
            print("Server Running Successfully")

        self.Socket.listen(self.MaxClient)
        while True:
            print("Waiting for connections")
            ClientSocket, ClientAdress = self.Socket.accept()
            print("got a connection from ", ClientAdress)
            newClient = threading.Thread(target=self.Handler, args=(ClientSocket, ClientAdress))
            newClient.start()


if __name__ == '__main__':
    MyServer = Server()