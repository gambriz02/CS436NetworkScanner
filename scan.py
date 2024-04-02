from scapy.all import ARP, Ether, srp, sr1, IP, ICMP
import socket, time, threading
from queue import Queue
socket.setdefaulttimeout(0.25) #waits for .25 secs before timing out 

#this function discovers hosts by sending out packets using scapy
def scan(ip):
    print("performing scan")

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=False)[0]

    clients = []

    for elem in result:
        client_dict = {"ip": elem[1].psrc, "mac": elem[1].hwsrc}
        clients.append(client_dict)
    
    return clients

def display(result):
    for row in result:
        print(row)

#define a function here for port scanning
def portScan(port, ip, print_lock): #pass in port and ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((ip, port))
        with print_lock:
            print(port, 'is open')
        con.close()
    except:
        pass
def threader(q, ip, print_lock):
    while True:
        worker = q.get()
        portScan(worker, ip, print_lock)
        q.task_done()

#define a function here for getting the vendor from the MAC address


#define a function here for cacheing known devices.


