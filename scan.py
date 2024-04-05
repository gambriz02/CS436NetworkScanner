from scapy.all import ARP, Ether, srp, sr1, IP, ICMP
import socket
import json

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

#define a function here for port scanning
        
#define a function here for getting the vendor from the MAC address
def vendLookup(dev_list):
    f = open('mac-vendors-export.json')
    data = json.load(f)
    found = False
    for dev in dev_list:
        prefix = dev['mac'][0:8]
        prefix = prefix.upper()
        print(prefix)
        dev['vendor'] = "Unknown"
        for d in data:
            if d['macPrefix'] == prefix:
                vendor = d['vendorName']
                dev['vendor'] = vendor
        
