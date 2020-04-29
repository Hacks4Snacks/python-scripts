#!/bin/env python3
# simple multithreaded TCP "echo" server script

import socket
import threading

# opting to combine server objects, but leaving lines for reference
#bind_ip = "0.0.0.0"
#bind_port = 6969

# create tcp/ip socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define server and port
# empty address = 0.0.0.0
server_address = ('0.0.0.0', 6969)

# opting to combine server objects, but leaving lines for reference
#server.bind((bind_ip, bind_port))

server.bind(server_address)

server.listen(5)

print(f"[*] Listening on {server_address[0]} port {server_address[1]}")

# client handling thread
def handle_client(client_socket):
    # print what client sends
    request = client_socket.recv(1024)
    print(f"[*] Received: {request}")

    # send a packet to client
    #message = "Message Received"
    #client_socket.send(message.encode('utf-8'))
    
    # echo recieved message back to client
    client_socket.sendall(request)
    
    # close connection
    client_socket.close()

while True:
    client,addr = server.accept()

    print(f"[*] Accepted connection from: {addr[0]} {addr[1]}")

    # start client thread to handle incoming connections
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
