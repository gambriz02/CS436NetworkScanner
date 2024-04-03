from scapy.all import ARP, Ether, srp, sr1, IP, ICMP

import socket, time, threading
from queue import Queue
socket.setdefaulttimeout(0.25) #waits for .25 secs before timing out 


print_lock = threading.Lock()

#this function discovers hosts by sending out packets using scapy
def scan(ip):
    print("performing scan")

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=False)[0]

    clients = []

    for elem in result:
        try:
            hostname = socket.gethostbyaddr(elem[1].psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        client_dict = {"ip": elem[1].psrc, "mac": elem[1].hwsrc, "hostname": hostname}
        clients.append(client_dict)
    
    return clients

def display(result):
    for row in result:
        print(row)


def scanDevices(device_list):
    for dev in device_list:
        scanDevice(dev.ip)

def scanDevice(ip):
    startTime = time.time() #start the timer
    q = Queue() #quue to store tasks

    for x in range(100): #spawn a 100 threads
        t = threading.Thread(target= threader, args = (q, ip, print_lock)) #each thread has a queue, ip, and print_lock
        t.daemon = True
        t.start()

    for worker in range(1, 500):
        q.put(worker)
    q.join() #wait for threads to finish their tasks
    print('Time taken: ', time.time() - startTime)

#define a function here for port scanning
def portScan(port, ip, print_lock): #pass in port, ip and print_lock
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines a socket object
    try:
        con = s.connect((ip, port)) #establish a connection
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

