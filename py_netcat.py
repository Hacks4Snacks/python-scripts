#!/bin/env python3
# simple python utility to replace netcat functionality

import sys
import socket
import getopt
import threading
import subprocess

# define GLOBAL variables
listen = False
command = False
upload = False
execute = ''
target = ''
upload_dest = ''
port = ''

def usage():
    
    print("Python Netcat Tool")
    print ()
    print("Usage: py_netcat.py -t TARGET_HOST -p PORT")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print("-c --command                 - initialize a command shell")
    print("-u --upload=destination      - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("py_netcat.py -t 192.168.0.1 -p 1234 -l -c")
    print("py_netcat.py -t 192.168.0.1 -p 1234 -l -u=/home/user/file.log")
    print("py_netcat.py -t 192.168.0.1 -p 1234 -l -e=\"cat /etc/passwd\"")
    print("echo 'abcd' | ./py_netcat.py -t 192.168.0.1 -p 135")
    sys.exit(0)

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to target
        client.connect((target,port))
        print("Connected")

        if len(buffer) > int(0):
            client.send(buffer.encode())

        while True:
            # wait for data
            recv_len = 1
            response = "".encode()

            while recv_len:
                data = client.recv(4096)
                recv_len = int(len(data))
                response += data

                if recv_len < int(4096):
                    break

#            print(response,)

            # wait for additional input
            buffer = input(response.decode())
            buffer += "\r\n"

            # send data
            client.send(buffer.encode())

    except:
        print(f"[*] Exception observed. Now Exiting.")

        # close connection
        client.close()

def server_loop():
    global target
    global port

    # if not target defined, listen on all interfaces
    if target == None:
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    print(f"Listening on {target} port {port}")
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # create thread to handle client
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command):

    # trim newline
    command = command.rstrip()

    # run command and get output back
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # send output back to client
    output += "\r\n".encode()
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_dest):
        # read in all bytes and write to destination
        file_buffer = ""

        # keep reading until EOF
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # attempt to write bytes out
        try:
            file_descriptor = open(upload_dest, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # ack file write
            client_socket.send(f"Successfully saved file to {upload_dest}\r\n".encode())
        except:
            client_socket.send(f"Failed to save file to {upload_dest}\r\n".encode())

    
    # check for command execution
    if len(execute):

        # run command
        output = run_command(execute)

        client_socket.send(output)

    # go into another loop if command shell was requested
    if command:
        while True:
            # show simple prompt
            #prompt = '<PNT:#> '
            client_socket.send('<PNT:#>'.encode())
                
            #receive until linefeed
            cmd_buffer = "".encode()
            
            while "\n".encode() not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back command output
            response = run_command(cmd_buffer)

            # send response
            client_socket.sendall(response)



def main():

    global listen
    global port
    global execute
    global command
    global upload_dest
    global target

    if not len(sys.argv[1:]):
        usage()

    # read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_dest = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "unhandled Option"

    # listen or send data from stdin
    if not listen and len(target) and port > 0:
        print("CTRL-D to send commands: ")
        # read in buffer from commandline
        buffer = sys.stdin.read()

        # send data
        client_sender(buffer)
    
    # listen and potentially upload, execute commands, or drop shell depending on commandline opt
    if listen:
        server_loop()
main()
