# coding: utf-8

import socket

def input():
    global PORT, SERVER
    PORT = input("Port: ")
    SERVER = input("Server: ")
    if len(SERVER.split(".")) != 4:
        print("Invalid IPv4 address (note: IPv6 is not allowed)")
        input()

def main():
    input()
    ADDR = (SERVER, PORT)
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDPLITE)
    soc.connect(ADDR)

if __name__ == '__main__':
    main()