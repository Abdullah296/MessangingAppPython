import socket
import tqdm
from tkinter import *
from tkinter import filedialog, Text
import os

def openL():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    host = "localhost"
    port = 5001
    #filename = "D:\hello.txt"
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    s.send(f"{filename} {filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()
    '''BUFFER_SIZE = 4096
    host = "localhost"
    port = 5001
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    s.send(f"{filename} {filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
           bytes_read = f.read(BUFFER_SIZE)
           if not bytes_read:
                break
           s.sendall(bytes_read)
        progress.update(len(bytes_read))
    s.close()
    '''

root = Tk()
root.geometry('500x400') 
canvas = Canvas(root, height=700, width=700, bg="green").pack
frame = Frame(root, bg='white').place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


openfile= Button(root, text = "Send File", command=openL ).pack(padx=10, pady=5, side= BOTTOM ) 

root.mainloop()