# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:50:10 2020

@author: Abdullah
"""

import socket as S
import threading as T
import tqdm
import os

Clients = []
Client = {}

def handler(client_socket,client_address):
    print("Connected by",client_address)
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        else:
             if data.decode("utf-8") == 'file':
                 recievefile(client_socket)
             else:
                 data =  " " + str(Client[client_address[1]]) + " --> " + data.decode("utf-8")
                 SendMsg(client_socket , data)
def recievefile(ClientSocket):
    #print('hello1')
    BUFFER_SIZE = 4096
    received = ClientSocket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split()
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    print('hello')
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = ClientSocket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    '''        
    sendfile(ClientSocket, filename)

def sendfile(clientS, filename):
    for client in Clients:
        if client != clientS:
            msg = 'file'
            client.send(msg.encode("utf-8"))
            BUFFER_SIZE = 4096   
            filesize = os.path.getsize(filename)
     
            client.send(f"{filename} {filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                for _ in progress:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    client.sendall(bytes_read)
                    progress.update(len(bytes_read))
           '''         
def SendMsg(clientS,msg):
    for client in Clients:
        if client != clientS:
            client.send(msg.encode("utf-8"))
            
host = 'localhost'
port = 12345
Server = S.socket(S.AF_INET,S.SOCK_STREAM)
Server.bind((host,port))
Server.listen(3)

print("Server is Online:")
while True:
    client_S,client_A = Server.accept()
    data = client_S.recv(1024)
    data = data.decode("utf-8")
    Client.update({client_A[1] : data})    
    Clients.append(client_S)
    
    print(Client[client_A[1]])
    
    new_thread = T.Thread(target=handler,args=(client_S,client_A))
    new_thread.start()
    
    
    
    
    
'''
BUFFER_SIZE = 4096
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
'''