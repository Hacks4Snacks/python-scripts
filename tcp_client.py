#!/bin/env python3
# A simple TCP client script that establishes a socket, connected to target_host on target_port, sends message, and gets a response

import socket

# opting to combine server objects, leaving lines for reference
#target_host = "127.0.0.1"
#target_port = 6969

# create socket object, AF_INET = IPv4, SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define server address
server_address = ('127.0.0.1', 6969)
print(f'Connecting to {server_address[0]} on port {server_address[1]}')

# opting to combine server objects, leaving for reference
# connect client
#client.connect((target_host,target_port))

client.connect(server_address)

try:

    # message to send
    #message = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
    message = b'Hello Mate'

    # send data
    #client.send(message.encode('utf-8'))
    print(f'Sending: {message}')
    client.sendall(message)

    # receive data
    response = client.recv(4096)

    print(f'Received from Server: {response}')

finally:
    print('Closing Socket!')
    client.close()
