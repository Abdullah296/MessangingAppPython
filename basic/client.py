# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:01:23 2020

@author: Abdullah
"""

import socket as S
import threading as T
import tqdm
import os

def Receive(client):
    while True:
        msg = client.recv(1024)
        print(msg.decode("utf-8"))

def sendfile():
    BUFFER_SIZE = 4096
    filename = input("Enter file path: ")
    filesize = os.path.getsize(filename)
     #s = socket.socket()
        #print(f"[+] Connecting to {host}:{port}")
        #s.connect((host, port))
        #print("[+] Connected.")
    client_socket.send(f"{filename} {filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
            progress.update(len(bytes_read))
        
client_socket = S.socket(S.AF_INET, S.SOCK_STREAM)
host = 'localhost'
port = 12345
client_socket.connect((host,port))
print("Connected\nWelcome to chatRoom:")
thread =T.Thread(target=Receive , args=(client_socket,))
thread.start()

msg = input("Enter name: ")
client_socket.send(msg.encode("utf-8"))


    
while True:
    
    '''a = input("Enter option \n1. send file \n2. send message\n")
    print(a)
    if a is 2:
        print("hello dude")
        msg = 'file'
        client_socket.send(msg.encode("utf-8"))
        sendfile()
    
    else: '''   
    msg = input("You:")
    client_socket.send(msg.encode("utf-8"))          
            
client_socket.close()

