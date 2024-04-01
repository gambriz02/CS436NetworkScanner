from scapy.all import ARP, Ether, srp, sr1, IP, ICMP

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
        
#define a function here for getting the vendor from the MAC address


#define a function here for cacheing known devices.


