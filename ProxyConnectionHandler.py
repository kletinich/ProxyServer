import socket

# for now handles only http requests
class ProxyConnectionHandler:
    def __init__(self, client_socket, packet_size=8192):
        self.client_socket = client_socket
        self.PACKET_SIZE = packet_size
        
        self.client_ip, self.client_port = self.client_socket.getpeername()
        
    def handleConnection(self):
        print("\n[Proxy]")
        
        # receive request from client
        request = self.client_socket.recv(self.PACKET_SIZE)
        
        # process client request
        path, host, port, method, supported_protocol = self.processRequest(request)
        
        if not supported_protocol:
            self.send501()
        
        # processed HEAD request. not relevant
        if not all([path, host, port, method]):
            self.client_socket.close()
            print("[Proxy]\n")
            return
        
        
        # send request to destination server if supported protocol
        if supported_protocol:
            destination_socket = self.sendRequest(path, host, port, method, request)
        
        # return the request from the destination server back to the client
        self.returnToClient(destination_socket, host, port, supported_protocol)
        
        print("[Proxy]\n")
        
        
    def processRequest(self, request):
        supported_protocol = True
        
        request_line = request.split(b'\r\n')[0].decode()
        method, full_url, protocol = request_line.split()
        
        if method == "CONNECT":
            print("\tIgnoring HEAD request")
            return None, None, None, None, False
        
        if full_url.startswith("http://"):
            full_url = full_url[7:]
        
        else:
            supported_protocol = False
            
        host_port, *path = full_url.split("/", 1)
        path = '/' + path[0] if path else '/'
        
        if ':' in host_port:
            host, port = host_port.split(':')
            port = int(port)
        else:
            host = host_port
            port = 80
            
        return path, host, port, method, supported_protocol
        
    # send the request from the client to the server
    def sendRequest(self, path, host, port, method, request):
        print(f"\tForwarding to [{host}/{port}]")   
        
        try:
            destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            destination_socket.connect((host, port))
            destination_socket.settimeout(2)
            updated_request = request.replace(
                f"{method} http://{host}{path}".encode(),
                f"{method} {path}".encode()
            )
            
        except Exception as e:
            print(f"\tError: {e}")
            return None        
        
        destination_socket.sendall(updated_request)
        print(f"\tForwarded successfully to {host}/{port}") 
            
        return destination_socket
            
    # return the message from the destination server to the client
    def returnToClient(self, destination_socket, server_host, server_port, supported_protocol):
                    
        if destination_socket:
            try:
                while True:
                        data = destination_socket.recv(self.PACKET_SIZE)

                        if not data:
                            break
                        self.client_socket.sendall(data)
                        
                
            except socket.timeout:        
                print(f"\tSent data back to [{self.client_ip}/{self.client_port}]")
            
            except Exception as e:
                print(f"\tError: {e}")
                
            finally:
                destination_socket.close()
                self.client_socket.close()
                print(f"\tConnection closed between [{self.client_ip}/{self.client_port}]:[{server_host}/{server_port}]")
                
    # for not supported connections
    def send501(self):
        response = (
            "HTTP/1.1 501 - Not Implemented\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 25\r\n"
            "Connection: close\r\n"
            "\r\n"
            "501 Protocol Not Supported"
        ).encode()

        try:
            self.client_socket.sendall(response)
        except Exception as e:
            print(f"Failed to send 501 response: {e}")
