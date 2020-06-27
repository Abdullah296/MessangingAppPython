import socket
import tqdm
import os


# device's IP address
SERVER_HOST = "localhost"
SERVER_PORT = 5001


# receive 4096 bytes each time



# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))


# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 


# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

def recievefile(ClientSocket):
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
# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split()

# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
'''
# close the client socket
recievefile(client_socket)
client_socket.close()
# close the server socket
s.close()