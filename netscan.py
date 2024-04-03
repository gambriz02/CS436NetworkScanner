from scan import *
from queue import Queue
import threading, socket

#Implementation of main! call scan functions and GUI
def main():
    
    router_ip = sr1(IP(dst="www.google.com", ttl=0)/ICMP()/"XXXXXXXXXXX", verbose=False).src

    host_ip = router_ip+"/24"

    print("Your router ip is: ", router_ip)

        #hostname = socket.gethostname() #g  etting the hostname of the machine
        #ip = socket.gethostbyname(hostname) #getting the ip
    
    result = scan(host_ip)
    scanDevices(result)
    display(result)

if __name__ == "__main__":
    main()
    
