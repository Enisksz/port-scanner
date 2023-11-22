import sys
import socket
import threading
from datetime import datetime

"""
Usage: python3 main.py target_ip start_port end_port
"""


# this func take 2 parameter
# parameter : target,port
def scan(target,port):
    try:
        #create socket
        sockt= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = sockt.connect_ex((target,port))
        # if result is zero, connection is successful.
        if result == 0:
            print(f"[+] Port {port} is open")
        
    except socket.error:
        return socket.error.strerror
    finally:
        sockt.close()


def scan_ports(target,start_port,end_port):
    #create threads for each port
    for port in range(start_port,end_port+1):
        # each thread go to scan func and start a connection
        thread = threading.Thread(target=scan,args=(target,port))
        thread.start()


def main():
    
    #gake a target ip or domain
    target= sys.argv[1]
    
    #get a starting port number
    start_port=int(sys.argv[2])

    # get a ending port number
    end_port = int(sys.argv[3])

    # banner
    print("-"*45)
    print("Scanning Target: ",target)
    print("Scanning started at: "+str(datetime.now()))
    print("-"*45)

    scan_ports(target,start_port,end_port)
    

if __name__ == "__main__":
    main()