#!/bin/env python3

infile = open('/etc/passwd', 'r')

for line in infile:
    account = line.split(':')
    if int(account[2]) == 0:
        if 'nologin' not in line:
            print("Privileged User:", account[0]) 
