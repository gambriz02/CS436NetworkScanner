from scapy.all import ARP, Ether, srp, sr1, IP, ICMP

import json

import socket, threading
from queue import Queue
socket.setdefaulttimeout(0.25) #waits for .25 secs before timing out 

print_lock = threading.Lock()

#this function discovers hosts by sending out packets using scapy
def scan(ip):
    print(" > discovering hosts on network")

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=True)[0]

    clients = []

    print (" > getting hostnames via reverse DNS lookup")
    for elem in result:
        print ("\t> getting hostname of ", elem[1].psrc)
        try:
            hostname = socket.gethostbyaddr(elem[1].psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        device_list = {"ip": elem[1].psrc, "mac": elem[1].hwsrc, "hostname": hostname}
        clients.append(device_list)
    
    return clients

def display(result):
    for row in result:
        print(row)


def scanDevices(device_list):
    ports = {}  # Initialize the ports dictionary outside the loop
    for dev in device_list:
        dev_ports = scanDevice(dev["ip"], device_list)
        # Merge dev_ports into the main ports dictionary
        for ip, open_ports in dev_ports.items():
            ports[ip] = open_ports
    return ports


def scanDevice(ip, device_list):
    print(' > performing port scan of: ', ip)
    
    q = Queue() #quue to store tasks
    
    ports = {}

    for x in range(50): #spawn a 50 threads
            t = threading.Thread(target= threader, args = (q, ip, print_lock, ports)) #each thread has a queue, ip, and print_lock
            t.daemon = True
            t.start()

    for worker in range(1, 500):
        q.put(worker)
    q.join() #wait for threads to finish their tasks

    for ip, open_ports in ports.items():
        print(f"\t> Open ports for {ip}: {', '.join(map(str, open_ports))}")

    return ports

#define a function here for port scanning
def portScan(port, ip, print_lock, ports): #pass in port, ip and print_lock
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines a socket object
    
    try:
        con = s.connect((ip, port)) #establish a connection
        with print_lock:
            ports.setdefault(ip, []).append(port)
        con.close()
       
    except:
        pass
def threader(q, ip, print_lock, ports):
    while True:
        worker = q.get()
        portScan(worker, ip, print_lock, ports)
        q.task_done()

#define a function here for getting the vendor from the MAC address
def vendLookup(dev_list):
    print (" > performing vendor lookup using MAC address")
    with open('mac-vendors-export.json', 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)

    for dev in dev_list:
        prefix = dev['mac'][0:8]
        prefix = prefix.upper()
        print("\t > getting vendor for prefix: ", prefix)
        dev['vendor'] = "Unknown"
        for d in data:
            if d['macPrefix'] == prefix:
                vendor = d['vendorName']
                dev['vendor'] = vendor
