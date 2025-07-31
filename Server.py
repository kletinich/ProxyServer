import socket
import threading

from ProxyConnectionHandler import ProxyConnectionHandler

class Server:
    def __init__(self, host='localhost', port=12345, start_server=True):
        self.host = host
        self.port = port
        
        self.server_socket = None
        self.clients = []
        
        self.running = False
        self.server_thread = None
        
        if start_server:
            self.server_thread = threading.Thread(target=self.bind_and_start, daemon=True).start()
        
    
    def bind_and_start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        
        self.running = True
        self.listen()
    
    def listen(self):
        self.server_socket.listen(5)
        print(f"[Server] Proxy listening on {self.host}:{self.port}")
        
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                print(f"[Server] Accepted connection from {client_address}")
                threading.Thread(target=self.handle_new_client, args=(client_socket,)).start()
                
            except socket.timeout:
                continue
            except OSError:
                break
    
    def shutdown(self):
        self.running = False
        
        print("[Server] Shutting down...")
        
        try:
            self.server_socket.close()    
        except Exception as e:
            print(f"[Server] Error while closing server socket: {e}")
        
        print("[Server] Closing all client connections...")
        
        for client in self.clients:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            
            try:
                client.close()
                print(f"[Server]: Closed connection with {client}")
            except Exception as e:
                print(f"[Server] Error while closing {client}:{e}")
                
            self.clients.clear()
        
        
            
    #for now handle only http (port 80)
    def handle_new_client(self, client_socket):
        proxyConnectionHandler = ProxyConnectionHandler(client_socket)
        proxyConnectionHandler.handleConnection()
        
        self.clients.remove(client_socket)