import socket
import threading
import os
import time
import netifaces as ni

def get_ip_address(interface):
    return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

def handle_client(conn, addr, server_type, worker_info=""):
    try:
        with conn:
            data = conn.recv(1024).decode()
            time.sleep(3)  # Simulate processing delay
            reversed_str = data[::-1]
            conn.sendall(reversed_str.encode())
    finally:
        print(f"{worker_info} - Completed {addr}")

# Single-Process Server
def single_process_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr, "Single-Process")

# Multi-Process Server
def multi_process_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            pid = os.fork()
            if pid == 0:
                s.close()
                handle_client(conn, addr, "Multi-Process")
                os._exit(0)
            else:
                conn.close()

# Multi-Threaded Server
def multi_threaded_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, "Multi-Threaded"))
            thread.start()

if __name__ == "__main__":
    server_type = input("Enter server type (1/2/3): ")
    if server_type == '1':
        single_process_server()
    elif server_type == '2':
        multi_process_server()
    elif server_type == '3':
        multi_threaded_server()
