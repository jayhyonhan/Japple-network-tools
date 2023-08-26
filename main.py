# coding: utf-8

import scapy

def takeInput():
    global PORT
    try:
        PORT = int(input("Port: "))
    except ValueError:
        print("Please specify an Integer")
        takeInput()
    takeInput2()

def takeInput2():
    global SERVER
    SERVER = input("Server: ")
    if len(SERVER.split(".")) != 4:
        print("Invalid IPv4 address (note: IPv6 is not allowed)")
        takeInput2()

def main():
    pass

if __name__ == '__main__':
    main()