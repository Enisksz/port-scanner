import argparse ,sys
import socket # bağlantı için
from colorama import Fore
from threading import Thread, Lock
from queue import Queue

GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX


# iş parçacığı sayısı
N_THREADS = 200
# iş parçacığı kuyruğu
q = Queue()

print_lock = Lock()


def portScan(port):

   
    try:
        s = socket.socket() # socket.AF_INET, socket.SOCK_STREAM default olarak geliyor
        #bu bağlantı noktasını kullanarak ana bilgisayara bağlanmaya çalışır
        s.connect((host,port))
    except:
        # bağlanılamıyor, port kapalı 
        with print_lock:
            print(f"{GRAY}{port:5} is closed  {RESET}", end='\r')
    else:
        # bağlantı kuruldu, port açık!
        with print_lock:
            print(f"{GREEN}{port:5} is open    {RESET}")
    finally:
        s.close()


def scan_thread():
    global q
    while True:
        # queue den port numarasını al
        worker = q.get()
        # portu tara
        portScan(worker)
        # tarama yapıldığını söyler
        q.task_done()

def main(host,ports):
    global q
    for t in range(N_THREADS):
        # her iş parçacığını başlatır
        t = Thread(target=scan_thread)
        # ana thread bitince zorunlu olarak durdurulur.
        t.daemon = True
        #deamon thread başlat
        t.start()

    for worker in ports:
        q.put(worker)

    q.join()


if __name__ == "__main__":
   

    host = sys.argv[1]
    start_port= int(sys.argv[2])
    end_port = int(sys.argv[3])

    ports = [ p for p in range(start_port, end_port)]
    main(host, ports)
