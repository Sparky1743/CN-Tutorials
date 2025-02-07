import socket
import threading
import os
import netifaces as ni
from datetime import datetime

def get_ip_address(interface):
    return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

def process_request(data):
    try:
        choice, payload = data.split('|', 1)
        if choice == '1':
            return payload.swapcase()
        elif choice == '2':
            return str(eval(payload))
        elif choice == '3':
            return payload[::-1]
        return "Invalid choice"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_client(conn, addr, server_type, worker_info=""):
    try:
        with conn:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{current_time}] {server_type} - Connection from {addr}")
            print(f"{worker_info} - Handling client {addr}")
            
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                print(f"\n{worker_info} - Received request: {data}")
                response = process_request(data)
                print(f"{worker_info} - Sending response: {response}")
                conn.sendall(response.encode())
                
    finally:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{current_time}] {worker_info} - Client {addr} disconnected")

# 1. Single-Process Server (Sequential)
def single_process_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"\nSingle-Process Server (PID: {os.getpid()})")
        print(f"Listening on {host}:{port}")
        print("-- Only handles one client at a time --\n")
        
        while True:
            print("[MAIN] Waiting for connections...")
            conn, addr = s.accept()
            print(f"New connection from {addr}")
            handle_client(conn, addr, "Single-Process", "[MAIN PROCESS]")
            print(f"Connection from {addr} closed. Ready for next client.")

# 2. Multi-Process Server
def multi_process_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"\nMulti-Process Server (Main PID: {os.getpid()})")
        print(f"Listening on {host}:{port}")
        print("-- New process for each client --\n")
        
        while True:
            conn, addr = s.accept()
            child_pid = os.fork()
            
            if child_pid == 0:  # Child process
                s.close()
                worker_info = f"[CHILD PID: {os.getpid()}]"
                handle_client(conn, addr, "Multi-Process", worker_info)
                os._exit(0)
            else:  # Parent process
                conn.close()
                print(f"\n[MAIN] Forked child process {child_pid} for {addr}")

# 3. Multi-Threaded Server
def multi_threaded_server(interface='eth0', port=65432):
    host = get_ip_address(interface)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"\nMulti-Threaded Server (Main PID: {os.getpid()})")
        print(f"Listening on {host}:{port}")
        print("-- New thread for each client --\n")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(
                conn, 
                addr, 
                "Multi-Threaded",
                f"[THREAD: {threading.current_thread().name}]"
            ))
            thread.start()
            print(f"\n[MAIN] Started thread {thread.name} for {addr}")

if __name__ == "__main__":
    server_type = input("Enter server type (1: Single-Process, 2: Multi-Process, 3: Multi-Threaded): ")
    if server_type == '1':
        single_process_server()
    elif server_type == '2':
        multi_process_server()
    elif server_type == '3':
        multi_threaded_server()
    else:
        print("Invalid server type")
