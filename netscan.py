from scan import *

#Implementation of main! call scan functions and GUI
def main():
    
    router_ip = sr1(IP(dst="www.google.com", ttl=0)/ICMP()/"XXXXXXXXXXX", verbose=False).src

    host_ip = router_ip+"/24"

    print("Your router ip is: ", router_ip)
    
    result = scan(host_ip)
    display(result)

def get_host_ip():
    try:
        router_ip = sr1(IP(dst="www.google.com", ttl=0)/ICMP()/"XXXXXXXXXXX", verbose=False).src
        return router_ip + "/24"
    except Exception as e:
        print("Error getting host IP:", e)
        return None
    
if __name__ == "__main__":
    main()