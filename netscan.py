from scan import *
from queue import Queue
import threading, socket

print_lock = threading.Lock()
#Implementation of main! call scan functions and GUI
def main():
    
    # router_ip = sr1(IP(dst="www.google.com", ttl=0)/ICMP()/"XXXXXXXXXXX", verbose=False).src

    # host_ip = router_ip+"/24"

    # print("Your router ip is: ", router_ip)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    startTime = time.time()
    q = Queue()

    for x in range(100):
        t = threading.Thread(target= threader, args = (q, ip, print_lock))       
        t.daemon = True
        t.start()

    for worker in range(1, 500):
        q.put(worker)
    q.join()
    print('Time taken: ', time.time() - startTime)
    #result = scan(host_ip)

    #display(result)

if __name__ == "__main__":
    main()
    
