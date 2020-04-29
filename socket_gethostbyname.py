#!/bin/env python3
# learning network sockets using gethostbyname to get IP for hostnames

import socket

HOSTS = [ 'google.com', 'sans.edu', 'microsoft.com' ]

for host in HOSTS:
    try:
        print(f"{host} : {socket.gethostbyname(host)}")
    except socket.error as msg:
        print(f"{host} : {msg}")
