#!/bin/env python3

import socket

target_host = "google.com"
target_port = 80

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect client
client.connect((target_host,target_port))

# message to send
message = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"

# send data
client.send(message.encode('utf-8'))

# receive data
response = client.recv(4096)

print(response)
